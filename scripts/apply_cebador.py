#!/usr/bin/env python3
"""Agrega Cebador a data/games.json si aún no existe."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "games.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from games_cebador import CEBADOR_GAME  # noqa: E402


def main() -> int:
    games = json.loads(DATA.read_text(encoding="utf-8"))
    if any(game["id"] == CEBADOR_GAME["id"] for game in games):
        print(f"SKIP {CEBADOR_GAME['id']} (ya existe)")
        return 0
    games.append(CEBADOR_GAME)
    DATA.write_text(json.dumps(games, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK   {CEBADOR_GAME['id']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
