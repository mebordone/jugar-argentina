#!/usr/bin/env python3
"""Agrega el lote 4 de juegos a data/games.json si aún no existen."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "games.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from games_batch4 import BATCH4_GAMES  # noqa: E402


def main() -> int:
    games = json.loads(DATA.read_text(encoding="utf-8"))
    by_id = {game["id"]: index for index, game in enumerate(games)}
    added = 0

    for entry in BATCH4_GAMES:
        if entry["id"] in by_id:
            print(f"SKIP {entry['id']} (ya existe)")
            continue
        games.append(entry)
        added += 1
        print(f"OK   {entry['id']}")

    DATA.write_text(json.dumps(games, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nAgregados: {added}/{len(BATCH4_GAMES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
