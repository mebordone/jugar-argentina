#!/usr/bin/env python3
"""Barrido multi-término en Steam Store Search API."""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TERMS_PATH = ROOT / "data" / "steam_search_terms.json"
DISCOVERIES_PATH = ROOT / "data" / "steam_discoveries.json"
GAMES_PATH = ROOT / "data" / "games.json"
USER_AGENT = "JugarArgentina-SteamSearch/1.0 (+https://github.com/mebordone/jugar-argentina)"
PAGE_DELAY = 0.6
STEAM_APP_RE = re.compile(r"store\.steampowered\.com/app/(\d+)")


def fetch_search_page(term: str, start: int = 0, count: int = 50, retries: int = 4) -> dict:
    params = urllib.parse.urlencode(
        {
            "query": "",
            "start": start,
            "count": count,
            "dynamic_data": "",
            "sort_by": "_ASC",
            "term": term,
            "supportedlang": "english,spanish",
            "infinite": "1",
        }
    )
    url = f"https://store.steampowered.com/search/results/?{params}"
    last_exc: Exception | None = None
    for attempt in range(retries):
        req = urllib.request.Request(
            url,
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as exc:
            last_exc = exc
            if exc.code == 429 and attempt < retries - 1:
                wait = 8 * (attempt + 1)
                print(f"  429 {term}, esperando {wait}s...")
                time.sleep(wait)
                continue
            raise
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_exc = exc
            if attempt < retries - 1:
                time.sleep(4)
                continue
            raise
    if last_exc:
        raise last_exc
    raise RuntimeError("fetch_search_page failed")


def parse_results(html_body: str) -> list[tuple[str, str]]:
    ids = re.findall(r'data-ds-appid="(\d+)"', html_body)
    titles = re.findall(r'<span class="title">([^<]+)</span>', html_body)
    return list(zip(ids, [html.unescape(t.strip()) for t in titles]))


def search_term(term: str, max_pages: int = 3) -> list[dict]:
    results: list[dict] = []
    seen: set[str] = set()
    start = 0
    total = None

    for _ in range(max_pages):
        try:
            payload = fetch_search_page(term, start=start)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            print(f"  ERR {term} @ {start}: {exc}")
            break

        if total is None:
            total = payload.get("total_count", 0)

        page = parse_results(payload.get("results_html", ""))
        if not page:
            break

        for app_id, title in page:
            if app_id in seen:
                continue
            seen.add(app_id)
            results.append(
                {
                    "app_id": app_id,
                    "titulo": title,
                    "url_steam": f"https://store.steampowered.com/app/{app_id}/",
                }
            )

        start += 50
        if start >= (total or 0):
            break
        time.sleep(PAGE_DELAY)

    return results


def catalog_steam_ids() -> set[str]:
    ids: set[str] = set()
    if not GAMES_PATH.exists():
        return ids
    games = json.loads(GAMES_PATH.read_text(encoding="utf-8"))
    for game in games:
        for value in (game.get("enlaces") or {}).values():
            if isinstance(value, str):
                match = STEAM_APP_RE.search(value)
                if match:
                    ids.add(match.group(1))
        for url in game.get("enlaces", {}).get("fuentes_investigacion") or []:
            if isinstance(url, str):
                match = STEAM_APP_RE.search(url)
                if match:
                    ids.add(match.group(1))
    return ids


def load_terms_config() -> list[dict]:
    config = json.loads(TERMS_PATH.read_text(encoding="utf-8"))
    entries: list[dict] = []
    for group_id, group in config.get("groups", {}).items():
        for item in group.get("terms", []):
            entries.append(
                {
                    "group": group_id,
                    "term": item["term"],
                    "jurisdiccion": item.get("jurisdiccion"),
                    "reuse_from": item.get("reuse_from"),
                }
            )
    return entries


def load_discoveries() -> dict:
    if DISCOVERIES_PATH.exists():
        return json.loads(DISCOVERIES_PATH.read_text(encoding="utf-8"))
    return {"terms": {}, "apps": {}}


def save_discoveries(data: dict) -> None:
    DISCOVERIES_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Barrido Steam multi-término")
    parser.add_argument("--group", help="Solo un grupo (A, B, C, D, E)")
    parser.add_argument("--resume", action="store_true", help="Saltear términos ya cacheados")
    parser.add_argument("--max-pages", type=int, default=3)
    args = parser.parse_args()

    if not TERMS_PATH.exists():
        print(f"Falta {TERMS_PATH}")
        return 1

    entries = load_terms_config()
    if args.group:
        entries = [e for e in entries if e["group"].upper() == args.group.upper()]

    discoveries = load_discoveries()
    discoveries.setdefault("terms", {})
    discoveries.setdefault("apps", {})

    catalog_ids = catalog_steam_ids()
    term_results_cache: dict[str, list[dict]] = {}

    for entry in entries:
        term = entry["term"]
        group = entry["group"]

        if entry.get("reuse_from"):
            source = entry["reuse_from"]
            if source in discoveries["terms"]:
                cached_apps = discoveries["terms"][source].get("app_ids", [])
                discoveries["terms"][term] = {
                    "group": group,
                    "jurisdiccion": entry.get("jurisdiccion"),
                    "reused_from": source,
                    "app_ids": cached_apps,
                    "count": len(cached_apps),
                }
                print(f"REUSE {term} <- {source} ({len(cached_apps)} apps)")
                continue

        if args.resume and term in discoveries["terms"] and discoveries["terms"][term].get("count", 0) > 0:
            print(f"SKIP {term} (cached)")
            continue

        print(f"SEARCH [{group}] {term}...")
        results = search_term(term, max_pages=args.max_pages)
        term_results_cache[term] = results
        app_ids = [r["app_id"] for r in results]

        discoveries["terms"][term] = {
            "group": group,
            "jurisdiccion": entry.get("jurisdiccion"),
            "app_ids": app_ids,
            "count": len(app_ids),
        }

        for result in results:
            app_id = result["app_id"]
            existing = discoveries["apps"].get(app_id, {})
            terms_found = set(existing.get("terminos_busqueda", []))
            terms_found.add(term)
            jurisdictions = set(existing.get("jurisdicciones", []))
            if entry.get("jurisdiccion"):
                jurisdictions.add(entry["jurisdiccion"])

            discoveries["apps"][app_id] = {
                "app_id": app_id,
                "titulo": result["titulo"],
                "url_steam": result["url_steam"],
                "terminos_busqueda": sorted(terms_found),
                "grupos": sorted(set(existing.get("grupos", [])) | {group}),
                "jurisdicciones": sorted(j for j in jurisdictions if j),
                "en_catalogo": app_id in catalog_ids,
            }

        print(f"  -> {len(results)} resultados")
        save_discoveries(discoveries)
        time.sleep(PAGE_DELAY)

    save_discoveries(discoveries)

    apps = discoveries["apps"]
    new_apps = [a for a in apps.values() if not a.get("en_catalogo")]
    in_catalog = [a for a in apps.values() if a.get("en_catalogo")]

    print(f"\n=== Resumen ===")
    print(f"Términos procesados: {len(discoveries['terms'])}")
    print(f"Apps únicas: {len(apps)}")
    print(f"Ya en catálogo: {len(in_catalog)}")
    print(f"Nuevas: {len(new_apps)}")
    print(f"Guardado en {DISCOVERIES_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
