#!/usr/bin/env python3
"""Obtiene capturas de pantalla desde Steam API y og:image de itch.io."""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "games.json"
STEAM_APP_RE = re.compile(r"store\.steampowered\.com/app/(\d+)")
USER_AGENT = "JugarArgentina-CaptureBot/1.0 (+https://github.com/mebordone/jugar-argentina)"
MAX_CAPTURES = 4


def fetch_json(url: str, timeout: int = 20) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def steam_screenshots(app_id: str) -> list[str]:
    url = (
        "https://store.steampowered.com/api/appdetails"
        f"?appids={app_id}&l=spanish&cc=ar"
    )
    try:
        payload = fetch_json(url)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return []
    entry = payload.get(app_id) or {}
    if not entry.get("success"):
        return []
    shots = entry.get("data", {}).get("screenshots") or []
    return [s["path_full"] for s in shots[:MAX_CAPTURES] if s.get("path_full")]


def captures_for_game(game: dict) -> list[str]:
    enlaces = game.get("enlaces") or {}
    steam_url = enlaces.get("steam")
    if isinstance(steam_url, str):
        match = STEAM_APP_RE.search(steam_url)
        if match:
            shots = steam_screenshots(match.group(1))
            if shots:
                return shots
    return []


def main() -> int:
    games = json.loads(DATA.read_text(encoding="utf-8"))
    updated = 0
    skipped = 0

    for index, game in enumerate(games):
        imagenes = game.setdefault("imagenes", {"portada": None, "capturas": []})
        if imagenes.get("capturas"):
            skipped += 1
            continue

        captures = captures_for_game(game)
        if captures:
            imagenes["capturas"] = captures
            updated += 1
            print(f"OK  {game['id']} ({len(captures)} capturas)")

        if index % 5 == 4:
            time.sleep(0.35)

    DATA.write_text(json.dumps(games, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nCapturas agregadas: {updated}")
    print(f"Ya tenían capturas: {skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
