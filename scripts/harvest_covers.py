#!/usr/bin/env python3
"""Busca URLs de portada desde Steam, itch.io y og:image de enlaces jugables."""
from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "games.json"
STEAM_APP_RE = re.compile(r"store\.steampowered\.com/app/(\d+)")
WORKSHOP_RE = re.compile(r"steamcommunity\.com/sharedfiles/filedetails/\?id=(\d+)")
OG_IMAGE_RE = re.compile(
    r'<meta[^>]+property=["\']og:image(?::url)?["\'][^>]+content=["\']([^"\']+)["\']',
    re.I,
)
OG_IMAGE_RE_ALT = re.compile(
    r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image(?::url)?["\']',
    re.I,
)
PLAY_KEYS = ("steam", "itch", "web_oficial", "kongregate", "archive", "steam_workshop")
USER_AGENT = "JugarArgentina-CoverBot/1.0 (+https://github.com/mebordone/jugar-argentina)"


def fetch_text(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "replace")


def fetch_json(url: str, timeout: int = 20) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def image_ok(url: str) -> bool:
    if not url.startswith(("http://", "https://")):
        return False
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            ctype = resp.headers.get("Content-Type", "")
            return resp.status == 200 and ctype.startswith("image")
    except (urllib.error.HTTPError, urllib.error.URLError, ValueError):
        return False


def absolutize_url(base_url: str, url: str) -> str:
    url = clean_url(url)
    if url.startswith("//"):
        return "https:" + url
    if url.startswith("/"):
        return urljoin(base_url, url)
    return url


def clean_url(url: str) -> str:
    return html.unescape(url.strip())


def og_image(page_url: str) -> str | None:
    try:
        body = fetch_text(page_url)
    except (urllib.error.URLError, TimeoutError):
        return None
    for pattern in (OG_IMAGE_RE, OG_IMAGE_RE_ALT):
        match = pattern.search(body)
        if match:
            candidate = absolutize_url(page_url, match.group(1))
            if candidate.startswith(("http://", "https://")) and not candidate.endswith(".svg"):
                return candidate
    return None


def steam_header(app_id: str) -> str | None:
    url = (
        "https://store.steampowered.com/api/appdetails"
        f"?appids={app_id}&l=spanish&cc=ar"
    )
    try:
        payload = fetch_json(url)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None
    entry = payload.get(app_id) or {}
    if not entry.get("success"):
        return None
    data = entry.get("data") or {}
    return data.get("header_image") or data.get("capsule_imagev5")


def cover_for_game(game: dict) -> tuple[str | None, str]:
    enlaces = game.get("enlaces") or {}
    game_id = game["id"]

    steam_url = enlaces.get("steam")
    if isinstance(steam_url, str):
        match = STEAM_APP_RE.search(steam_url)
        if match:
            image = steam_header(match.group(1))
            if image:
                return image, "steam"

    itch_url = enlaces.get("itch")
    if isinstance(itch_url, str):
        image = og_image(itch_url)
        if image:
            return image, "itch"

    workshop_url = enlaces.get("steam_workshop")
    if isinstance(workshop_url, str):
        image = og_image(workshop_url)
        if image:
            return image, "steam_workshop"

    for key in ("web_oficial", "kongregate", "archive"):
        url = enlaces.get(key)
        if isinstance(url, str) and url:
            image = og_image(url)
            if image:
                return image, key

    return None, ""


def main() -> int:
    games = json.loads(DATA.read_text(encoding="utf-8"))
    found = 0
    skipped = 0
    failed: list[str] = []

    for index, game in enumerate(games):
        imagenes = game.setdefault("imagenes", {"portada": None, "capturas": []})
        if imagenes.get("portada"):
            skipped += 1
            continue

        if not any(game.get("enlaces", {}).get(key) for key in PLAY_KEYS):
            failed.append(game["id"])
            continue

        image, source = cover_for_game(game)
        try:
            if image and (source == "steam" or image_ok(image)):
                imagenes["portada"] = image
                found += 1
                print(f"OK  {game['id']} ({source})")
            else:
                failed.append(game["id"])
                print(f"--- {game['id']}")
        except Exception as exc:  # noqa: BLE001
            failed.append(game["id"])
            print(f"ERR {game['id']}: {exc}")

        if index % 5 == 4:
            time.sleep(0.35)

    DATA.write_text(json.dumps(games, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nPortadas encontradas: {found}/{len(games)}")
    print(f"Ya tenían portada: {skipped}")
    print(f"Sin portada: {len(failed)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
