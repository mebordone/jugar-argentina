#!/usr/bin/env python3
"""Aplica candidatos de ano pendientes y notas de lanzamiento TBD al catalogo."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
GAMES_PATH = DATA / "games.json"
CANDIDATES_PATH = DATA / "year_candidates.json"

TBD_NOTES = {
    "proximamente": "Próximamente",
    "próximamente": "Próximamente",
    "por confirmarse": "Por confirmarse",
    "to be announced": "Por confirmarse",
    "coming soon": "Próximamente",
}


def normalize_note(raw: str) -> str | None:
    lowered = raw.strip().lower()
    for key, label in TBD_NOTES.items():
        if key in lowered:
            return label
    return None


def should_apply_pending(candidate: dict) -> bool:
    if candidate.get("aplicado"):
        return False
    if candidate.get("status") not in {"ok", "futuro"}:
        return False
    year = candidate.get("anio_propuesto")
    if not isinstance(year, int):
        return False
    if candidate.get("fuente") == "slug" and candidate.get("status") == "futuro":
        return False
    if candidate.get("confianza") in {"alta", "media", "baja"}:
        return True
    return False


def apply_pending_years(games: list[dict], candidates: list[dict]) -> int:
    by_id = {game["id"]: game for game in games}
    applied = 0
    for candidate in candidates:
        if not should_apply_pending(candidate):
            continue
        game = by_id.get(candidate["id"])
        if not game or game.get("anio"):
            continue
        game["anio"] = candidate["anio_propuesto"]
        candidate["aplicado"] = True
        applied += 1
    return applied


def apply_launch_notes(games: list[dict], candidates: list[dict]) -> int:
    by_id = {game["id"]: game for game in games}
    updated = 0
    for candidate in candidates:
        if candidate.get("status") != "tbd":
            continue
        raw = candidate.get("fecha_raw") or ""
        note = normalize_note(raw)
        if not note:
            continue
        game = by_id.get(candidate["id"])
        if not game:
            continue
        changed = False
        if game.get("anio_nota") != note:
            game["anio_nota"] = note
            changed = True
        if game.get("estado") == "publicado":
            game["estado"] = "en_desarrollo"
            changed = True
        if changed:
            updated += 1
    return updated


def main() -> int:
    games = json.loads(GAMES_PATH.read_text(encoding="utf-8"))
    payload = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))
    candidates = payload.get("candidatos") or []

    applied_years = apply_pending_years(games, candidates)
    updated_notes = apply_launch_notes(games, candidates)

    GAMES_PATH.write_text(
        json.dumps(games, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    payload["aplicados"] = sum(1 for c in candidates if c.get("aplicado"))
    payload["pendientes_revision"] = sum(
        1
        for c in candidates
        if c.get("anio_propuesto") and not c.get("aplicado")
    )
    CANDIDATES_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Anos pendientes aplicados: {applied_years}")
    print(f"Fichas con nota de lanzamiento actualizada: {updated_notes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
