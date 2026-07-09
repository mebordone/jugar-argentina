#!/usr/bin/env python3
"""Reclasifica grado_relevancia_argentina cuando la presencia es referencia_menor."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAMES_PATH = ROOT / "data" / "games.json"


def main() -> int:
    games = json.loads(GAMES_PATH.read_text(encoding="utf-8"))
    updated = 0
    for game in games:
        va = game["vinculo_argentina"]
        presencias = [
            va[key].get("presencia")
            for key in ("escenario", "protagonista", "deporte_argentino")
            if va.get(key, {}).get("activo")
        ]
        if presencias and all(p == "referencia_menor" for p in presencias if p):
            if game.get("grado_relevancia_argentina") == "central":
                game["grado_relevancia_argentina"] = "menor"
                updated += 1
    GAMES_PATH.write_text(
        json.dumps(games, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"OK: {updated} juegos reclasificados a grado menor")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
