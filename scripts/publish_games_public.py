#!/usr/bin/env python3
"""Copia atómica y verificable de data/games.json → public/data/games.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ficha_model import GAMES_PATH, write_json_atomic  # noqa: E402
from tracking import PUBLIC_GAMES_PATH  # noqa: E402


def publish_public_copy(
    *,
    games_path: Path = GAMES_PATH,
    public_path: Path = PUBLIC_GAMES_PATH,
) -> Path:
    games = json.loads(games_path.read_text(encoding="utf-8"))
    public_path.parent.mkdir(parents=True, exist_ok=True)
    write_json_atomic(public_path, games)
    copied = json.loads(public_path.read_text(encoding="utf-8"))
    if copied != games:
        raise RuntimeError("La copia pública no coincide con data/games.json")
    return public_path


def main() -> int:
    path = publish_public_copy()
    games = json.loads(path.read_text(encoding="utf-8"))
    print(f"OK: public/data/games.json sincronizado ({len(games)} juegos)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
