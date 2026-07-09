#!/usr/bin/env python3
"""Agrega lotes Steam 5 y 6 a data/games.json si aún no existen."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "games.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from games_steam_batch5 import STEAM_BATCH5_GAMES  # noqa: E402
from games_steam_batch6 import STEAM_BATCH6_GAMES  # noqa: E402


def main() -> int:
    games = json.loads(DATA.read_text(encoding="utf-8"))
    by_id = {game["id"] for game in games}
    added = 0

    for entry in [*STEAM_BATCH5_GAMES, *STEAM_BATCH6_GAMES]:
        if entry["id"] in by_id:
            print(f"SKIP {entry['id']} (ya existe)")
            continue
        games.append(entry)
        by_id.add(entry["id"])
        added += 1
        print(f"OK   {entry['id']}")

    DATA.write_text(json.dumps(games, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = len(STEAM_BATCH5_GAMES) + len(STEAM_BATCH6_GAMES)
    print(f"\nAgregados: {added}/{total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
