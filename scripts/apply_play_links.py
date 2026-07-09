#!/usr/bin/env python3
"""Aplica parches de enlaces jugables a data/games.json."""
import json
from pathlib import Path

from play_links_curated import PLAY_LINK_PATCHES, TIPO_OBRA_PATCHES, WORKSHOP_PATCHES

ROOT = Path(__file__).resolve().parent.parent
GAMES_PATH = ROOT / "data" / "games.json"


def apply_patches() -> int:
    games = json.loads(GAMES_PATH.read_text(encoding="utf-8"))
    patched = 0

    for game in games:
        game_id = game["id"]
        enlaces = game.setdefault("enlaces", {})

        if game_id in PLAY_LINK_PATCHES:
            enlaces.update(PLAY_LINK_PATCHES[game_id])
            patched += 1

        if game_id in TIPO_OBRA_PATCHES:
            game["tipo_obra"] = TIPO_OBRA_PATCHES[game_id]

        if game_id in WORKSHOP_PATCHES:
            enlaces["steam_workshop"] = WORKSHOP_PATCHES[game_id]
            enlaces.pop("steam", None)
            patched += 1

    GAMES_PATH.write_text(
        json.dumps(games, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return patched


if __name__ == "__main__":
    count = apply_patches()
    print(f"OK: {count} juegos actualizados con enlaces jugables")
