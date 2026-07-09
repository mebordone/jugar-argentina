#!/usr/bin/env python3
"""Valida enlaces externos no-Steam con HEAD requests."""
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAMES_PATH = ROOT / "data" / "games.json"

CHECK_KEYS = ["itch", "web_oficial", "archive", "apkpure", "google_play", "kongregate"]
SKIP_HOSTS = {"itch.io", "www.itch.io"}


def check_url(url: str) -> tuple[bool, str]:
    try:
        request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "JugarArgentina/1.0"})
        with urllib.request.urlopen(request, timeout=12) as response:
            return 200 <= response.status < 400, str(response.status)
    except urllib.error.HTTPError as error:
        if error.code in {403, 405}:
            return True, f"http-{error.code}-allowed"
        return False, f"http-{error.code}"
    except Exception as error:  # noqa: BLE001
        return False, str(error)


def main() -> int:
    games = json.loads(GAMES_PATH.read_text(encoding="utf-8"))
    errors = []
    checked = 0

    for game in games:
        enlaces = game.get("enlaces", {})
        for key in CHECK_KEYS:
            url = enlaces.get(key)
            if not isinstance(url, str) or not url:
                continue
            host = urllib.parse.urlparse(url).netloc.replace("www.", "")
            if host in SKIP_HOSTS and key == "itch" and "/itch.io/" not in url and url.rstrip("/").endswith("itch.io"):
                errors.append(f"{game['id']}: placeholder itch.io")
                continue
            ok, detail = check_url(url)
            checked += 1
            if not ok:
                errors.append(f"{game['id']} [{key}] {url} -> {detail}")

    if errors:
        print("ERRORES:")
        for error in errors:
            print(" -", error)
        print(f"Fallaron {len(errors)} de {checked} URLs")
        return 1

    print(f"OK: {checked} URLs externas verificadas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
