#!/usr/bin/env python3
"""Busca URLs de portada desde enlaces jugables y fuentes de investigacion."""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
GAMES_PATH = DATA / "games.json"
CANDIDATES_PATH = DATA / "cover_candidates.json"

STEAM_APP_RE = re.compile(r"store\.steampowered\.com/app/(\d+)")
OG_IMAGE_RE = re.compile(
    r'<meta[^>]+property=["\']og:image(?::url)?["\'][^>]+content=["\']([^"\']+)["\']',
    re.I,
)
OG_IMAGE_RE_ALT = re.compile(
    r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image(?::url)?["\']',
    re.I,
)
TWITTER_IMAGE_RE = re.compile(
    r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']',
    re.I,
)
TWITTER_IMAGE_RE_ALT = re.compile(
    r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']twitter:image["\']',
    re.I,
)
ITCH_IMAGE_RE = re.compile(r"https://img\.itch\.zone/[^\"'\s>]+/original/[^\"'\s>]+", re.I)

PLAY_KEYS = (
    "steam",
    "itch",
    "google_play",
    "web_oficial",
    "kongregate",
    "archive",
    "steam_workshop",
    "mobygames",
    "wikipedia",
)
HARVEST_KEYS = PLAY_KEYS + ("fuentes_investigacion",)

USER_AGENT = "JugarArgentina-CoverBot/1.0 (+https://github.com/mebordone/jugar-argentina)"
REQUEST_DELAY = 0.35


def fetch_text(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "replace")


def fetch_json(url: str, timeout: int = 20) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def clean_url(url: str) -> str:
    return html.unescape(url.strip())


def absolutize_url(base_url: str, url: str) -> str:
    url = clean_url(url)
    if url.startswith("//"):
        return "https:" + url
    if url.startswith("/"):
        return urljoin(base_url, url)
    return url


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


def og_image(page_url: str) -> str | None:
    try:
        body = fetch_text(page_url)
    except (urllib.error.URLError, TimeoutError):
        return None

    for pattern in (OG_IMAGE_RE, OG_IMAGE_RE_ALT, TWITTER_IMAGE_RE, TWITTER_IMAGE_RE_ALT):
        match = pattern.search(body)
        if match:
            candidate = absolutize_url(page_url, match.group(1))
            if candidate.startswith(("http://", "https://")) and not candidate.endswith(".svg"):
                return candidate

    if "itch.io" in page_url:
        match = ITCH_IMAGE_RE.search(body)
        if match:
            return clean_url(match.group(0))

    return None


def fetch_appdetails(app_id: str) -> dict | None:
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&l=spanish&cc=ar"
    for attempt in range(4):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                payload = json.load(resp)
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < 3:
                time.sleep(8 * (attempt + 1))
                continue
            return None
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            if attempt < 3:
                time.sleep(3)
                continue
            return None

        entry = payload.get(app_id) or payload.get(str(app_id)) or {}
        if not entry.get("success"):
            return None
        data = entry.get("data") or {}
        return {
            "header_image": data.get("header_image") or data.get("capsule_imagev5"),
        }
    return None


def steam_header(app_id: str) -> str | None:
    details = fetch_appdetails(app_id)
    if not details:
        return None
    return details.get("header_image")


def iter_source_urls(game: dict) -> list[tuple[str, str]]:
    enlaces = game.get("enlaces") or {}
    ordered: list[tuple[str, str]] = []

    for key in PLAY_KEYS:
        value = enlaces.get(key)
        if isinstance(value, str) and value:
            ordered.append((key, value))

    fuentes = enlaces.get("fuentes_investigacion")
    if isinstance(fuentes, list):
        for url in fuentes:
            if isinstance(url, str) and url:
                ordered.append(("fuentes_investigacion", url))

    return ordered


def cover_for_game(game: dict) -> tuple[str | None, str, str]:
    enlaces = game.get("enlaces") or {}

    steam_url = enlaces.get("steam")
    if isinstance(steam_url, str):
        match = STEAM_APP_RE.search(steam_url)
        if match:
            image = steam_header(match.group(1))
            if image:
                return image, "steam", "alta"

    for source, url in iter_source_urls(game):
        if source == "steam":
            continue
        image = og_image(url)
        if image:
            confianza = "alta" if source in {"itch", "google_play", "steam_workshop"} else "media"
            return image, source, confianza

    return None, "", ""


def has_harvestable_link(game: dict) -> bool:
    enlaces = game.get("enlaces") or {}
    if any(enlaces.get(key) for key in PLAY_KEYS):
        return True
    fuentes = enlaces.get("fuentes_investigacion")
    return bool(fuentes)


def harvest_cover(game: dict) -> dict:
    imagenes = game.get("imagenes") or {}
    portada_actual = imagenes.get("portada")
    image, source, confianza = cover_for_game(game)

    candidate = {
        "id": game["id"],
        "titulo": game.get("titulo"),
        "portada_actual": portada_actual,
        "portada_propuesta": image,
        "fuente": source or None,
        "confianza": confianza if image else None,
        "aplicado": False,
    }

    if not image:
        candidate["pendiente_manual"] = not has_harvestable_link(game)
        return candidate

    if source == "steam" or image_ok(image):
        if source != "steam" and confianza == "media" and not image_ok(image):
            candidate["portada_propuesta"] = None
            candidate["fuente"] = None
            candidate["confianza"] = None
        return candidate

    candidate["portada_propuesta"] = None
    candidate["fuente"] = None
    candidate["confianza"] = None
    return candidate


def should_apply(candidate: dict) -> bool:
    return (
        candidate.get("confianza") == "alta"
        and isinstance(candidate.get("portada_propuesta"), str)
        and candidate["portada_propuesta"].startswith(("http://", "https://"))
    )


def apply_candidates(games: list[dict], candidates: list[dict]) -> int:
    by_id = {game["id"]: game for game in games}
    applied = 0

    for candidate in candidates:
        if not should_apply(candidate):
            continue
        game = by_id.get(candidate["id"])
        if not game:
            continue
        imagenes = game.setdefault("imagenes", {"portada": None, "capturas": []})
        if imagenes.get("portada"):
            continue

        imagenes["portada"] = candidate["portada_propuesta"]
        fuente = candidate.get("fuente")
        if fuente:
            imagenes["portada_fuente"] = fuente
        candidate["aplicado"] = True
        applied += 1

    return applied


def summarize(candidates: list[dict]) -> dict:
    aplicados = sum(1 for candidate in candidates if candidate.get("aplicado"))
    pendientes_manual = sum(
        1
        for candidate in candidates
        if not candidate.get("aplicado")
        and not candidate.get("portada_propuesta")
        and candidate.get("pendiente_manual")
    )
    recuperables = sum(
        1
        for candidate in candidates
        if not candidate.get("aplicado")
        and candidate.get("portada_propuesta")
        and candidate.get("confianza") != "alta"
    )
    sin_propuesta = sum(
        1
        for candidate in candidates
        if not candidate.get("aplicado") and not candidate.get("portada_propuesta")
    )
    return {
        "aplicados": aplicados,
        "pendientes_manual": pendientes_manual,
        "recuperables_revision": recuperables,
        "sin_propuesta": sin_propuesta,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Busca portadas faltantes en el catalogo.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Aplica portadas de alta confianza en games.json",
    )
    args = parser.parse_args()

    games = json.loads(GAMES_PATH.read_text(encoding="utf-8"))
    missing = [game for game in games if not (game.get("imagenes") or {}).get("portada")]
    print(f"Juegos sin portada: {len(missing)}")

    candidates: list[dict] = []
    for index, game in enumerate(missing, start=1):
        candidate = harvest_cover(game)
        candidates.append(candidate)
        label = candidate.get("portada_propuesta") or "sin candidato"
        fuente = candidate.get("fuente") or "-"
        print(f"[{index}/{len(missing)}] {game['id']}: {fuente} -> {label}")

        if index % 4 == 0:
            time.sleep(REQUEST_DELAY)

    summary = summarize(candidates)
    payload = {
        "generado": date.today().isoformat(),
        "total_sin_portada": len(missing),
        **summary,
        "candidatos": candidates,
    }
    CANDIDATES_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\nCandidatos guardados en {CANDIDATES_PATH.relative_to(ROOT)}")

    if args.apply:
        applied = apply_candidates(games, candidates)
        GAMES_PATH.write_text(
            json.dumps(games, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        payload["aplicados"] = applied
        CANDIDATES_PATH.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        eligible = sum(1 for candidate in candidates if should_apply(candidate))
        print(f"Portadas aplicadas: {applied}")
        print(f"Listas para aplicar (--apply): {eligible}")
    else:
        eligible = sum(1 for candidate in candidates if should_apply(candidate))
        print(f"Listas para aplicar (--apply): {eligible}")

    remaining = len([g for g in games if not (g.get("imagenes") or {}).get("portada")])
    print(f"Sin portada tras barrido: {remaining}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
