#!/usr/bin/env python3
"""Busca años de lanzamiento para juegos sin anio en el catalogo."""
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

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
GAMES_PATH = DATA / "games.json"
CANDIDATES_PATH = DATA / "year_candidates.json"

STEAM_APP_RE = re.compile(r"store\.steampowered\.com/app/(\d+)")
SLUG_YEAR_RE = re.compile(r"-(19|20)\d{2}$")
YEAR_RE = re.compile(r"\b(?:19|20)\d{2}\b")
TBD_MARKERS = (
    "proximamente",
    "próximamente",
    "por confirmarse",
    "to be announced",
    "coming soon",
    "tbd",
    "announced",
    "announce",
)

META_CONTENT_RE = re.compile(
    r'<meta[^>]+(?:property|name)=["\']([^"\']+)["\'][^>]+content=["\']([^"\']+)["\']',
    re.I,
)
META_CONTENT_ALT_RE = re.compile(
    r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\']([^"\']+)["\']',
    re.I,
)
JSON_LD_RE = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.I | re.S,
)
ITCH_PUBLISHED_RE = re.compile(
    r"Published\s*</[^>]+>\s*<[^>]+>\s*([^<]+)",
    re.I,
)

USER_AGENT = "JugarArgentina-YearBot/1.0 (+https://github.com/mebordone/jugar-argentina)"
REQUEST_DELAY = 0.4


def fetch_text(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "replace")


def fetch_json(url: str, timeout: int = 20) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


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
        data = entry["data"]
        return {
            "release_date": (data.get("release_date") or {}).get("date"),
        }
    return None


def is_tbd(raw: str) -> bool:
    lowered = raw.strip().lower()
    if not lowered:
        return True
    return any(marker in lowered for marker in TBD_MARKERS)


def parse_year(raw: str) -> int | None:
    if not raw or is_tbd(raw):
        return None
    match = YEAR_RE.search(raw)
    if not match:
        return None
    year = int(match.group(0))
    if 1970 <= year <= 2100:
        return year
    return None


def year_status(year: int | None, raw: str) -> str:
    if year is None:
        return "tbd" if raw and is_tbd(raw) else "sin_dato"
    if year > date.today().year:
        return "futuro"
    return "ok"


def steam_app_id(game: dict) -> str | None:
    enlaces = game.get("enlaces") or {}
    steam_url = enlaces.get("steam")
    if isinstance(steam_url, str):
        match = STEAM_APP_RE.search(steam_url)
        if match:
            return match.group(1)
    for value in enlaces.values():
        if isinstance(value, str):
            match = STEAM_APP_RE.search(value)
            if match:
                return match.group(1)
    return None


def extract_meta_dates(body: str) -> list[str]:
    dates: list[str] = []
    for pattern in (META_CONTENT_RE, META_CONTENT_ALT_RE):
        for match in pattern.finditer(body):
            prop, content = match.group(1).lower(), html.unescape(match.group(2))
            if any(
                key in prop
                for key in (
                    "article:published",
                    "og:published",
                    "datepublished",
                    "publication_date",
                    "release_date",
                    "date",
                )
            ):
                dates.append(content)
    for block in JSON_LD_RE.findall(body):
        try:
            payload = json.loads(block)
        except json.JSONDecodeError:
            continue
        items = payload if isinstance(payload, list) else [payload]
        for item in items:
            if not isinstance(item, dict):
                continue
            for key in ("datePublished", "releaseDate", "dateCreated"):
                value = item.get(key)
                if isinstance(value, str):
                    dates.append(value)
    return dates


def year_from_html(body: str, confidence: str) -> tuple[int | None, str, str]:
    for raw in extract_meta_dates(body):
        year = parse_year(raw)
        if year:
            return year, raw, confidence
    match = YEAR_RE.search(body[:8000])
    if match:
        year = int(match.group(0))
        if 1970 <= year <= 2100:
            return year, match.group(0), "baja"
    return None, "", "ninguna"


def year_from_slug(game_id: str) -> tuple[int | None, str, str]:
    match = SLUG_YEAR_RE.search(game_id)
    if not match:
        return None, "", "ninguna"
    year = int(match.group(0).lstrip("-"))
    return year, str(year), "baja"


def year_from_itch(url: str) -> tuple[int | None, str, str, str]:
    try:
        body = fetch_text(url)
    except (urllib.error.URLError, TimeoutError):
        return None, "", "ninguna", "itch"

    itch_match = ITCH_PUBLISHED_RE.search(body)
    if itch_match:
        raw = html.unescape(itch_match.group(1).strip())
        year = parse_year(raw)
        if year:
            return year, raw, "alta", "itch"

    year, raw, confidence = year_from_html(body, "media")
    if year:
        return year, raw, confidence, "itch"
    return None, "", "ninguna", "itch"


def year_from_web(url: str) -> tuple[int | None, str, str, str]:
    try:
        body = fetch_text(url)
    except (urllib.error.URLError, TimeoutError):
        return None, "", "ninguna", "web"
    year, raw, confidence = year_from_html(body, "media")
    if year:
        return year, raw, confidence, "web"
    return None, "", "ninguna", "web"


def harvest_year(game: dict) -> dict:
    candidate = {
        "id": game["id"],
        "titulo": game.get("titulo", ""),
        "anio_actual": game.get("anio"),
        "anio_propuesto": None,
        "fecha_raw": "",
        "fuente": "",
        "confianza": "ninguna",
        "status": "sin_dato",
        "aplicado": False,
    }

    app_id = steam_app_id(game)
    if app_id:
        details = fetch_appdetails(app_id)
        time.sleep(REQUEST_DELAY)
        if details:
            raw = details.get("release_date") or ""
            year = parse_year(raw)
            candidate["fecha_raw"] = raw
            candidate["fuente"] = "steam"
            if year:
                candidate["anio_propuesto"] = year
                candidate["confianza"] = "alta"
                candidate["status"] = year_status(year, raw)
                return candidate
            candidate["status"] = year_status(None, raw)
            return candidate

    enlaces = game.get("enlaces") or {}
    itch_url = enlaces.get("itch")
    if isinstance(itch_url, str) and itch_url:
        year, raw, confidence, fuente = year_from_itch(itch_url)
        time.sleep(REQUEST_DELAY)
        if year:
            candidate.update(
                {
                    "anio_propuesto": year,
                    "fecha_raw": raw,
                    "fuente": fuente,
                    "confianza": confidence,
                    "status": year_status(year, raw),
                }
            )
            return candidate
        if raw:
            candidate.update({"fecha_raw": raw, "fuente": fuente, "status": "tbd"})
            return candidate

    for key in ("web_oficial", "archive", "abandonware", "descarga_directa"):
        url = enlaces.get(key)
        if isinstance(url, str) and url:
            year, raw, confidence, fuente = year_from_web(url)
            time.sleep(REQUEST_DELAY)
            if year:
                candidate.update(
                    {
                        "anio_propuesto": year,
                        "fecha_raw": raw,
                        "fuente": fuente,
                        "confianza": confidence,
                        "status": year_status(year, raw),
                    }
                )
                return candidate

    year, raw, confidence = year_from_slug(game["id"])
    if year:
        candidate.update(
            {
                "anio_propuesto": year,
                "fecha_raw": raw,
                "fuente": "slug",
                "confianza": confidence,
                "status": year_status(year, raw),
            }
        )
    return candidate


def should_apply(candidate: dict) -> bool:
    return (
        candidate.get("confianza") == "alta"
        and candidate.get("status") == "ok"
        and isinstance(candidate.get("anio_propuesto"), int)
    )


def apply_candidates(games: list[dict], candidates: list[dict]) -> int:
    by_id = {game["id"]: game for game in games}
    applied = 0
    for candidate in candidates:
        if not should_apply(candidate):
            continue
        game = by_id.get(candidate["id"])
        if not game or game.get("anio"):
            continue
        game["anio"] = candidate["anio_propuesto"]
        candidate["aplicado"] = True
        applied += 1
    return applied


def summarize(candidates: list[dict]) -> dict:
    applied = sum(1 for c in candidates if c.get("aplicado"))
    tbd = sum(1 for c in candidates if c.get("status") == "tbd")
    futuro = sum(1 for c in candidates if c.get("status") == "futuro")
    sin_dato = sum(
        1
        for c in candidates
        if c.get("status") == "sin_dato" and not c.get("anio_propuesto")
    )
    pendientes = sum(
        1
        for c in candidates
        if c.get("anio_propuesto") and not c.get("aplicado") and not should_apply(c)
    )
    return {
        "aplicados": applied,
        "pendientes_revision": pendientes,
        "tbd": tbd,
        "futuro": futuro,
        "sin_dato": sin_dato,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Busca anos faltantes en el catalogo.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Aplica anos de alta confianza en games.json",
    )
    args = parser.parse_args()

    games = json.loads(GAMES_PATH.read_text(encoding="utf-8"))
    missing = [game for game in games if not game.get("anio")]
    print(f"Juegos sin anio: {len(missing)}")

    candidates: list[dict] = []
    for index, game in enumerate(missing, start=1):
        candidate = harvest_year(game)
        candidates.append(candidate)
        label = candidate["anio_propuesto"] or candidate["status"]
        print(f"[{index}/{len(missing)}] {game['id']}: {label} ({candidate['fuente']})")

    summary = summarize(candidates)
    payload = {
        "generado": date.today().isoformat(),
        "total_sin_anio": len(missing),
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
        print(f"Anos aplicados en games.json: {applied}")
    else:
        eligible = sum(1 for c in candidates if should_apply(c))
        print(f"Listos para aplicar (--apply): {eligible}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
