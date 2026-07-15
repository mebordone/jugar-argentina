#!/usr/bin/env python3
"""Infiere disponibilidad desde enlaces y metadatos."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAMES_PATH = ROOT / "data" / "games.json"

PLAY_KEYS = {
    "steam",
    "itch",
    "web_oficial",
    "kongregate",
    "archive",
    "apkpure",
    "google_play",
    "uptodown",
    "steam_workshop",
}


def infer_disponibilidad(game: dict) -> str:
    enlaces = game.get("enlaces", {})
    estado = game.get("estado", "")
    current = game.get("disponibilidad", "desconocido")

    if current in {"perdido", "abandonware", "a_la_venta", "gratis"}:
        return current

    if estado in {"en_desarrollo", "cancelado", "prototipo"}:
        return "perdido"

    if enlaces.get("archive"):
        return "abandonware"

    if enlaces.get("steam") or enlaces.get("nintendo") or enlaces.get("playstation"):
        precio = game.get("metadatos", {}).get("precio")
        if precio == "gratuito":
            return "gratis"
        return "a_la_venta"

    if enlaces.get("itch") or enlaces.get("apkpure") or enlaces.get("google_play") or enlaces.get("uptodown"):
        precio = game.get("metadatos", {}).get("precio")
        if precio == "gratuito" or enlaces.get("itch") or enlaces.get("google_play") or enlaces.get("uptodown"):
            return "gratis"

    has_playable = any(
        isinstance(enlaces.get(key), str) and enlaces.get(key)
        for key in PLAY_KEYS
    )
    if has_playable:
        return "gratis"

    if not has_playable:
        return "perdido"

    return current


def main() -> int:
    games = json.loads(GAMES_PATH.read_text(encoding="utf-8"))
    updated = 0
    for game in games:
        inferred = infer_disponibilidad(game)
        if game.get("disponibilidad") != inferred:
            game["disponibilidad"] = inferred
            updated += 1
    GAMES_PATH.write_text(
        json.dumps(games, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"OK: disponibilidad actualizada en {updated} juegos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
