#!/usr/bin/env python3
"""Valida recorridos editoriales y cobertura de fechas patrias."""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CONTENT = ROOT / "src" / "content"

VALID_TYPES = {
    "fecha_patria",
    "efemeride",
    "permanente",
    "territorial",
    "recomendado",
}

PRIORITY_DATES = {
    "03-24": "memoria-verdad-justicia",
    "04-02": "malvinas",
    "05-25": "revolucion-mayo",
    "06-20": "bandera-belgrano",
    "07-09": "independencia",
    "08-17": "san-martin",
    "10-12": "diversidad-cultural",
    "11-20": "soberania-nacional",
}


def valid_date(value: str | None) -> bool:
    if not value:
        return False
    try:
        datetime.strptime(f"2024-{value}", "%Y-%m-%d")
    except ValueError:
        return False
    return True


def validate() -> int:
    games = json.loads((DATA / "games.json").read_text(encoding="utf-8"))
    game_ids = {game["id"] for game in games}
    recorridos = json.loads((CONTENT / "efemerides.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    seen_slugs: set[str] = set()

    for index, recorrido in enumerate(recorridos):
        label = recorrido.get("slug") or f"[{index}]"
        slug = recorrido.get("slug")
        if not slug:
            errors.append(f"{label}: falta slug")
        elif slug in seen_slugs:
            errors.append(f"{label}: slug duplicado")
        seen_slugs.add(slug)

        if recorrido.get("tipo") not in VALID_TYPES:
            errors.append(f"{label}: tipo inválido")

        fecha = recorrido.get("fecha")
        if fecha is not None and not valid_date(fecha):
            errors.append(f"{label}: fecha inválida '{fecha}'")

        ventana = recorrido.get("ventana")
        if ventana:
            for key in ("inicio", "fin"):
                if not valid_date(ventana.get(key)):
                    errors.append(f"{label}: ventana.{key} inválida")

        for field in ("titulo", "descripcion", "criterio", "bajada"):
            if not recorrido.get(field):
                errors.append(f"{label}: falta {field}")

        if not isinstance(recorrido.get("temas"), list):
            errors.append(f"{label}: temas debe ser lista")
        if not isinstance(recorrido.get("territorios"), list) or not recorrido.get("territorios"):
            errors.append(f"{label}: territorios debe tener al menos un valor")

        destacados = recorrido.get("destacados_editoriales")
        if not isinstance(destacados, list) or not destacados:
            errors.append(f"{label}: destacados_editoriales debe tener al menos un juego")
            continue

        seen_games: set[str] = set()
        for destacado in destacados:
            game_id = destacado.get("id")
            if not game_id:
                errors.append(f"{label}: destacado sin id")
                continue
            if game_id in seen_games:
                errors.append(f"{label}: destacado duplicado '{game_id}'")
            seen_games.add(game_id)
            if game_id not in game_ids:
                errors.append(f"{label}: destacado inexistente '{game_id}'")
            if not destacado.get("motivo"):
                errors.append(f"{label}: destacado '{game_id}' sin motivo")

    recorrido_by_date = {
        recorrido.get("fecha"): recorrido
        for recorrido in recorridos
        if recorrido.get("tipo") == "fecha_patria"
    }
    for fecha, expected_slug in PRIORITY_DATES.items():
        recorrido = recorrido_by_date.get(fecha)
        if not recorrido:
            errors.append(f"fecha patria {fecha}: sin recorrido publicado")
        elif recorrido.get("slug") != expected_slug:
            errors.append(
                f"fecha patria {fecha}: se esperaba slug '{expected_slug}' y se encontró '{recorrido.get('slug')}'"
            )

    if errors:
        print("ERRORES DE RECORRIDOS:")
        for error in errors:
            print(" -", error)
        return 1

    print(f"OK: {len(recorridos)} recorridos válidos, {len(PRIORITY_DATES)} fechas patrias cubiertas")
    return 0


if __name__ == "__main__":
    sys.exit(validate())
