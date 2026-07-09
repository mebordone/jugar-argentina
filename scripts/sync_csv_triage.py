#!/usr/bin/env python3
"""Sincroniza estado_triage del CSV con games.json y descartados.json."""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "raw_candidates.csv"
GAMES_PATH = ROOT / "data" / "games.json"
DESCARTADOS_PATH = ROOT / "data" / "descartados.json"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def main() -> int:
    games = json.loads(GAMES_PATH.read_text(encoding="utf-8"))
    descartados = json.loads(DESCARTADOS_PATH.read_text(encoding="utf-8"))
    titles_in_games = {g["titulo"].lower(): g for g in games}
    ids_in_games = {g["id"] for g in games}
    descartado_titles = {d["titulo"].lower() for d in descartados}
    descartado_ids = {d["id"] for d in descartados}

    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    updated = 0
    seen_keys: set[str] = set()
    deduped_rows = []

    for row in rows:
        key = (row.get("titulo") or "").strip().lower()
        if key in seen_keys:
            updated += 1
            continue
        seen_keys.add(key)
        deduped_rows.append(row)

    for row in deduped_rows:
        titulo = (row.get("titulo") or "").strip()
        titulo_key = titulo.lower()
        game = titles_in_games.get(titulo_key)
        new_status = row.get("estado_triage") or "candidato"

        if titulo_key in descartado_titles or slugify(titulo) in descartado_ids:
            new_status = "descartado"
        elif game and game["id"] in ids_in_games:
            new_status = "verificado"

        if row.get("estado_triage") != new_status:
            row["estado_triage"] = new_status
            updated += 1

    fieldnames = rows[0].keys() if rows else []
    with CSV_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(deduped_rows)

    print(f"OK: CSV triage sincronizado ({updated} cambios, {len(rows) - len(deduped_rows)} duplicados removidos)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
