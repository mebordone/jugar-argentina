#!/usr/bin/env python3
"""Aplica anos investigados manualmente al catalogo."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
GAMES_PATH = DATA / "games.json"
RESEARCH_PATH = DATA / "year_manual_research.json"


def apply_manual_years(games: list[dict], entries: list[dict]) -> tuple[int, int]:
    by_id = {game["id"]: game for game in games}
    applied = 0
    skipped = 0

    for entry in entries:
        game = by_id.get(entry["id"])
        if not game:
            skipped += 1
            continue
        if game.get("anio"):
            entry["aplicado"] = False
            entry["omitido"] = "ya_tiene_anio"
            skipped += 1
            continue

        year = entry.get("anio_propuesto")
        if not isinstance(year, int):
            skipped += 1
            continue

        game["anio"] = year
        fuente = entry.get("fuente")
        if fuente:
            game["anio_fuente"] = fuente

        enlaces = game.setdefault("enlaces", {})
        fuentes = enlaces.setdefault("fuentes_investigacion", [])
        url = entry.get("url_fuente")
        if isinstance(url, str) and url and url not in fuentes:
            fuentes.append(url)

        entry["aplicado"] = True
        applied += 1

    return applied, skipped


def main() -> int:
    games = json.loads(GAMES_PATH.read_text(encoding="utf-8"))
    payload = json.loads(RESEARCH_PATH.read_text(encoding="utf-8"))
    entries = payload.get("entradas") or []

    applied, skipped = apply_manual_years(games, entries)

    GAMES_PATH.write_text(
        json.dumps(games, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    payload["generado"] = date.today().isoformat()
    payload["aplicados"] = applied
    payload["omitidos"] = skipped
    RESEARCH_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Anos manuales aplicados: {applied}")
    print(f"Omitidos: {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
