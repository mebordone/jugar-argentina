#!/usr/bin/env python3
"""Valida invariantes de consistencia entre CSV, catálogo y copia pública."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ficha_model import (  # noqa: E402
    CANDIDATES_DIR,
    CSV_PATH,
    GAMES_PATH,
    load_json_candidates,
    normalize_candidate_status,
    slugify,
)
from tracking import (  # noqa: E402
    CANONICAL_CANDIDATE_STATES,
    DESCARTADOS_PATH,
    OPEN_CANDIDATE_STATES,
    PUBLIC_GAMES_PATH,
    load_tracking_rows,
)


def validate_consistency(
    *,
    csv_path: Path = CSV_PATH,
    games_path: Path = GAMES_PATH,
    public_path: Path | None = PUBLIC_GAMES_PATH,
    descartados_path: Path = DESCARTADOS_PATH,
    candidates_dir: Path = CANDIDATES_DIR,
    require_public: bool = False,
) -> list[str]:
    errors: list[str] = []
    rows = load_tracking_rows(csv_path)
    games = json.loads(games_path.read_text(encoding="utf-8"))
    descartados = json.loads(descartados_path.read_text(encoding="utf-8"))
    game_ids = {game["id"] for game in games}
    desc_ids = {item["id"] for item in descartados}

    ids = [row.get("id") or "" for row in rows]
    if any(not value for value in ids):
        errors.append("Hay filas de seguimiento sin id")
    dup_ids = [key for key, count in Counter(ids).items() if key and count > 1]
    if dup_ids:
        errors.append(f"ids de seguimiento duplicados: {', '.join(sorted(dup_ids)[:20])}")

    published_rows = [
        row for row in rows if normalize_candidate_status(row.get("estado_triage")) == "publicado"
    ]
    published_ficha_ids = [row.get("ficha_id") or "" for row in published_rows]
    if any(not value for value in published_ficha_ids):
        errors.append("Hay filas publicadas sin ficha_id")
    dup_fichas = [key for key, count in Counter(published_ficha_ids).items() if key and count > 1]
    if dup_fichas:
        errors.append(f"ficha_id duplicados en publicados: {', '.join(sorted(dup_fichas)[:20])}")

    published_set = {value for value in published_ficha_ids if value}
    if published_set != game_ids:
        missing = sorted(game_ids - published_set)
        extras = sorted(published_set - game_ids)
        if missing:
            errors.append(f"juegos sin fila publicada ({len(missing)}): {', '.join(missing[:20])}")
        if extras:
            errors.append(f"filas publicadas huérfanas ({len(extras)}): {', '.join(extras[:20])}")

    for row in rows:
        estado = normalize_candidate_status(row.get("estado_triage"))
        if estado not in CANONICAL_CANDIDATE_STATES:
            errors.append(f"{row.get('id')}: estado inválido '{row.get('estado_triage')}'")
        if estado in OPEN_CANDIDATE_STATES:
            ficha_id = row.get("ficha_id") or ""
            if ficha_id and ficha_id in game_ids:
                errors.append(f"{row.get('id')}: candidato abierto apunta a ficha publicada '{ficha_id}'")
            if ficha_id and ficha_id in desc_ids:
                errors.append(f"{row.get('id')}: candidato abierto apunta a descarte '{ficha_id}'")
        if estado == "descartado":
            if row.get("ficha_id"):
                errors.append(f"{row.get('id')}: descartado no debe tener ficha_id")
            if not (row.get("motivo_decision") or "").strip():
                errors.append(f"{row.get('id')}: descartado sin motivo_decision")
            if (row.get("id") in game_ids) and (row.get("titulo") or "").strip().lower() in {
                (game.get("titulo") or "").strip().lower() for game in games if game["id"] == row.get("id")
            }:
                errors.append(f"{row.get('id')}: descartado colisiona con ficha publicada homónima")

    # Manifiestos representados
    tracking_ids = {row.get("id") for row in rows}
    tracking_titles = {(row.get("titulo") or "").strip().lower() for row in rows}
    for item in load_json_candidates(candidates_dir):
        item_id = str(item.get("id") or "")
        titulo = str(item.get("titulo") or "").strip().lower()
        if item_id not in tracking_ids and titulo not in tracking_titles:
            errors.append(f"manifiesto sin fila de seguimiento: {item.get('id') or item.get('titulo')}")

    # descartados.json no debería estar publicado
    for item in descartados:
        if item.get("id") in game_ids:
            errors.append(f"descartado.json publicado: {item.get('id')}")
        if not (item.get("motivo_exclusion") or "").strip():
            errors.append(f"descartado.json sin motivo: {item.get('id')}")

    # Paridad CSV descartado ↔ descartados.json
    csv_discard_ids = {
        row.get("id") or ""
        for row in rows
        if normalize_candidate_status(row.get("estado_triage")) == "descartado" and row.get("id")
    }
    if csv_discard_ids != desc_ids:
        missing_json = sorted(csv_discard_ids - desc_ids)
        missing_csv = sorted(desc_ids - csv_discard_ids)
        if missing_json:
            errors.append(
                f"descartes en CSV ausentes en descartados.json ({len(missing_json)}): "
                f"{', '.join(missing_json[:20])}"
            )
        if missing_csv:
            errors.append(
                f"descartes en JSON ausentes en CSV ({len(missing_csv)}): "
                f"{', '.join(missing_csv[:20])}"
            )

    if require_public or (public_path and public_path.exists()):
        if not public_path or not public_path.exists():
            errors.append(f"falta copia pública {public_path}")
        else:
            public_games = json.loads(public_path.read_text(encoding="utf-8"))
            if public_games != games:
                errors.append("public/data/games.json difiere de data/games.json")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validar consistencia del catálogo")
    parser.add_argument("--require-public", action="store_true")
    parser.add_argument("--csv", type=Path, default=CSV_PATH)
    parser.add_argument("--games", type=Path, default=GAMES_PATH)
    parser.add_argument("--public", type=Path, default=PUBLIC_GAMES_PATH)
    args = parser.parse_args(argv)
    errors = validate_consistency(
        csv_path=args.csv,
        games_path=args.games,
        public_path=args.public,
        require_public=args.require_public,
    )
    if errors:
        print("ERRORES DE CONSISTENCIA:")
        for error in errors:
            print(" -", error)
        return 1
    rows = load_tracking_rows(args.csv)
    games = json.loads(args.games.read_text(encoding="utf-8"))
    published = sum(1 for row in rows if row.get("estado_triage") == "publicado")
    open_rows = sum(1 for row in rows if row.get("estado_triage") in OPEN_CANDIDATE_STATES)
    discarded = sum(1 for row in rows if row.get("estado_triage") == "descartado")
    print(
        f"OK: consistencia válida — {len(games)} juegos, "
        f"{published} publicados, {open_rows} abiertos, {discarded} descartados, {len(rows)} filas"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
