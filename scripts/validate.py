#!/usr/bin/env python3
"""Valida games.json contra schema.json y reglas editoriales v1.1."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

EJES_CULTURALES = {
    "politica", "satira", "folclore", "juegos_tradicionales", "historia", "memoria",
    "cultura_urbana", "historieta", "literatura", "educativo", "deporte", "geografia",
    "migracion", "musica",
}
TIPO_OBRA = {
    "comercial", "indie", "educativo", "jam", "mod", "fan_game",
    "abandonware", "prototipo", "promocional",
}
GRADO = {"central", "importante", "menor"}
CALIDAD = {"oficial", "tienda", "prensa", "wiki", "foro", "archive"}
SENSIBILIDAD = {"baja", "media", "alta"}
DISPONIBILIDAD = {"a_la_venta", "gratis", "abandonware", "perdido", "desconocido"}


def validate():
    games = json.loads((DATA / "games.json").read_text(encoding="utf-8"))
    schema = json.loads((DATA / "schema.json").read_text(encoding="utf-8"))
    required = schema["required"]
    errors = []
    ids = set()
    game_ids = {g["id"] for g in games}

    for i, g in enumerate(games):
        for field in required:
            if field not in g:
                errors.append(f"[{i}] {g.get('titulo', '?')}: falta campo '{field}'")
        if g["id"] in ids:
            errors.append(f"ID duplicado: {g['id']}")
        ids.add(g["id"])

        va = g["vinculo_argentina"]
        active = sum(
            1
            for k in ("escenario", "protagonista", "deporte_argentino")
            if va.get(k, {}).get("activo")
        )
        if active == 0:
            errors.append(f"{g['id']}: sin vínculo argentino activo")

        for eje in g.get("ejes_culturales", []):
            if eje not in EJES_CULTURALES:
                errors.append(f"{g['id']}: eje cultural inválido '{eje}'")
        if g.get("tipo_obra") and g["tipo_obra"] not in TIPO_OBRA:
            errors.append(f"{g['id']}: tipo_obra inválido")
        if g.get("grado_relevancia_argentina") not in GRADO:
            errors.append(f"{g['id']}: grado_relevancia_argentina inválido")
        if g.get("calidad_fuente") not in CALIDAD:
            errors.append(f"{g['id']}: calidad_fuente inválida")
        if g.get("sensibilidad") not in SENSIBILIDAD:
            errors.append(f"{g['id']}: sensibilidad inválida")
        if g.get("disponibilidad") not in DISPONIBILIDAD:
            errors.append(f"{g['id']}: disponibilidad inválida")

        grado = g.get("grado_relevancia_argentina", "central")
        presencias = [
            va[k].get("presencia")
            for k in ("escenario", "protagonista", "deporte_argentino")
            if va.get(k, {}).get("activo")
        ]
        if grado == "menor" and all(p == "principal" for p in presencias if p):
            errors.append(f"{g['id']}: grado menor incompatible con presencia principal en todos los ejes")

        for rel in g.get("relacionado_con", []):
            if rel not in game_ids:
                errors.append(f"{g['id']}: relacionado_con apunta a ID inexistente '{rel}'")

    if errors:
        print("ERRORES:")
        for e in errors:
            print(" -", e)
        return 1

    link_errors = []
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from validate_links import validate_links as validate_store_links
        link_errors = validate_store_links(games)
    except ImportError:
        pass

    if link_errors:
        print("ERRORES DE ENLACES:")
        for e in link_errors:
            print(" -", e)
        return 1

    play_keys = {
        "steam", "itch", "gog", "epic", "archive", "abandonware",
        "google_play", "apkpure", "web_oficial", "descarga_directa",
        "steam_workshop", "uptodown",
    }
    with_cover = sum(1 for g in games if g.get("imagenes", {}).get("portada"))
    with_play = sum(
        1 for g in games
        if any(g.get("enlaces", {}).get(k) for k in play_keys)
    )
    known_disp = sum(1 for g in games if g.get("disponibilidad") != "desconocido")
    with_ejes = sum(1 for g in games if g.get("ejes_culturales"))
    with_anio = sum(1 for g in games if g.get("anio"))
    with_capturas = sum(1 for g in games if g.get("imagenes", {}).get("capturas"))
    n = len(games)

    print(f"OK: {n} juegos válidos, {len(ids)} IDs únicos")
    print("--- Completitud ---")
    print(f"  Link jugable:   {with_play}/{n} ({100 * with_play // n}%)")
    print(f"  Portada:        {with_cover}/{n} ({100 * with_cover // n}%)")
    print(f"  Disponibilidad: {known_disp}/{n} ({100 * known_disp // n}% curado)")
    print(f"  Ejes culturales:{with_ejes}/{n} ({100 * with_ejes // n}%)")
    print(f"  Año:            {with_anio}/{n} ({100 * with_anio // n}%)")
    print(f"  Capturas:       {with_capturas}/{n} ({100 * with_capturas // n}%)")
    return 0


if __name__ == "__main__":
    sys.exit(validate())
