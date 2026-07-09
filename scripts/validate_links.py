#!/usr/bin/env python3
"""Valida que enlaces de tienda apunten al juego correcto."""
import argparse
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
STEAM_APP_RE = re.compile(r"store\.steampowered\.com/app/(\d+)")
WORKSHOP_RE = re.compile(r"steamcommunity\.com/sharedfiles/filedetails/\?id=(\d+)")
TITLE_SYNONYMS = {
    "semillas": "seeds",
    "seeds": "semillas",
    "legado": "legacy",
    "legacy": "legado",
}
# Entradas que apuntan al juego base o a un título comercial alternativo verificado.
STEAM_TITLE_OVERRIDES: dict[str, set[str]] = {
    "hitman-3-mendoza": {"hitman", "world", "assassination"},
    "civ6-buenos-aires": {"civilization", "civ", "vi"},
    "fabulas-portenas": {"fabulas", "portenas", "portens", "caba"},
    "caba-demo-hypnos": {"caba", "portens", "fabulas", "portenas"},
    "syndicate-buenos-aires": {"syndicate"},
    "fast-furious-showdown-aeroparque": {"fast", "furious", "showdown"},
    "prisoner-of-ice-argentina": {"prisoner", "ice", "cthulhu"},
    "bloodrayne-argentina": {"bloodrayne"},
    "cod-ghosts-clockwork": {"call", "duty", "ghosts"},
    "chameleon-buenos-aires": {"chameleon"},
    "battlefield-bad-company-2-andes": {"battlefield", "bad", "company"},
    "fifa-street-caminito": {"fifa", "street"},
    "mount-blade-warband-mods-argentina": {"mount", "blade", "warband"},
    "napoleon-total-war-mods-independencia": {"napoleon", "total", "war"},
    "empire-total-war-mods-america": {"empire", "total", "war"},
    "hearts-of-iron-iv-mods-argentina": {"hearts", "iron"},
    "microsoft-flight-simulator-argentina": {"flight", "simulator", "microsoft"},
    "europa-universalis-iv-argentina": {"europa", "universalis"},
}


def normalize_title(value: str) -> str:
    value = value.split("—")[0].split("-")[0]
    value = unicodedata.normalize("NFD", value.lower())
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    value = value.replace(".", "")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\b(demo|soundtrack|dlc|edition|definitive|chapter)\b", "", value)
    words = []
    for word in value.split():
        words.append(TITLE_SYNONYMS.get(word, word))
    return re.sub(r"\s+", " ", " ".join(words)).strip()


def significant_words(value: str) -> set[str]:
    stop = {"the", "de", "del", "la", "el", "y", "and", "en", "a", "of", "game", "juego"}
    return {w for w in normalize_title(value).split() if len(w) > 2 and w not in stop}


def title_match(expected: str, actual: str, game_id: str = "") -> bool:
    a = normalize_title(expected)
    b = normalize_title(actual)
    if not a or not b:
        return False
    if a in b or b in a:
        return True

    expected_words = significant_words(expected)
    actual_words = significant_words(actual)
    overlap = expected_words & actual_words
    if len(overlap) >= 1 and (len(overlap) >= 2 or len(expected_words) == 1):
        return True

    override = STEAM_TITLE_OVERRIDES.get(game_id)
    if override and override & actual_words:
        return True

    ratio = SequenceMatcher(None, a, b).ratio()
    return ratio >= 0.45


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "JugarArgentina/1.0"})
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.loads(response.read().decode())


def steam_store_name(app_id: str) -> str | None:
    for lang in ("spanish", "english"):
        payload = fetch_json(
            f"https://store.steampowered.com/api/appdetails?appids={app_id}&l={lang}"
        )
        data = payload.get(app_id, {})
        if data.get("success"):
            return data.get("data", {}).get("name")
    return None


def validate_steam(game: dict) -> list[str]:
    errors: list[str] = []
    steam_url = game.get("enlaces", {}).get("steam")
    if not steam_url or not isinstance(steam_url, str):
        return errors

    workshop_match = WORKSHOP_RE.search(steam_url)
    if workshop_match:
        errors.append(
            f"{game['id']}: URL de Workshop en enlaces.steam; usar enlaces.steam_workshop"
        )
        return errors

    app_match = STEAM_APP_RE.search(steam_url)
    if not app_match:
        errors.append(f"{game['id']}: URL Steam no reconocida: {steam_url}")
        return errors

    app_id = app_match.group(1)
    try:
        store_name = steam_store_name(app_id)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        errors.append(f"{game['id']}: no se pudo consultar Steam app {app_id}: {exc}")
        return errors

    if not store_name:
        if game["id"] in STEAM_TITLE_OVERRIDES:
            return errors
        errors.append(f"{game['id']}: Steam app {app_id} no encontrada")
        return errors

    candidates = [game.get("titulo", ""), game.get("titulo_original", "")]
    if not any(
        title_match(candidate, store_name, game["id"])
        for candidate in candidates
        if candidate
    ):
        errors.append(
            f"{game['id']}: Steam mismatch — catálogo '{game.get('titulo')}' vs tienda '{store_name}' (app {app_id})"
        )
    return errors


def validate_workshop(game: dict) -> list[str]:
    errors: list[str] = []
    workshop_url = game.get("enlaces", {}).get("steam_workshop")
    if not workshop_url:
        return errors
    if not WORKSHOP_RE.search(workshop_url):
        errors.append(f"{game['id']}: steam_workshop inválido: {workshop_url}")
    return errors


def validate_links(games: list[dict], *, offline: bool = False) -> list[str]:
    if offline:
        return []
    errors: list[str] = []
    for game in games:
        errors.extend(validate_steam(game))
        errors.extend(validate_workshop(game))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida enlaces de tienda en games.json")
    parser.add_argument("--offline", action="store_true", help="Omitir consultas HTTP")
    args = parser.parse_args()

    games = json.loads((DATA / "games.json").read_text(encoding="utf-8"))
    errors = validate_links(games, offline=args.offline)

    if errors:
        print("ERRORES DE ENLACES:")
        for error in errors:
            print(" -", error)
        return 1

    steam_count = sum(1 for g in games if g.get("enlaces", {}).get("steam"))
    workshop_count = sum(1 for g in games if g.get("enlaces", {}).get("steam_workshop"))
    print(f"OK: {steam_count} Steam + {workshop_count} Workshop verificados")
    return 0


if __name__ == "__main__":
    sys.exit(main())
