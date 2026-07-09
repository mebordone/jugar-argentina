#!/usr/bin/env python3
"""Propaga ejes culturales desde contexto_argentino.temas cuando faltan."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAMES_PATH = ROOT / "data" / "games.json"

ALLOWED = {
    "politica",
    "satira",
    "folclore",
    "juegos_tradicionales",
    "historia",
    "memoria",
    "cultura_urbana",
    "historieta",
    "literatura",
    "educativo",
    "deporte",
    "geografia",
    "migracion",
    "musica",
}

THEME_MAP = {
    "conurbano": "cultura_urbana",
    "cultura_popular": "folclore",
    "educacion": "educativo",
    "gauchesco": "folclore",
    "geografia": "geografia",
    "historia": "historia",
    "independencia": "historia",
    "malvinas": "memoria",
    "politica": "politica",
    "satira": "satira",
    "terror": "folclore",
    "truco": "juegos_tradicionales",
}


def main() -> int:
    games = json.loads(GAMES_PATH.read_text(encoding="utf-8"))
    updated = 0
    for game in games:
        ejes = list(game.get("ejes_culturales") or [])
        before = set(ejes)
        for tema in game.get("contexto_argentino", {}).get("temas", []):
            mapped = THEME_MAP.get(tema, tema if tema in ALLOWED else None)
            if mapped and mapped in ALLOWED and mapped not in ejes:
                ejes.append(mapped)
        if set(ejes) != before:
            game["ejes_culturales"] = ejes
            updated += 1
    GAMES_PATH.write_text(
        json.dumps(games, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"OK: ejes culturales actualizados en {updated} juegos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
