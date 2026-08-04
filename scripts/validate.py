#!/usr/bin/env python3
"""Valida games.json y borradores editoriales con mensajes claros."""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ficha_model import (  # noqa: E402
    CALIDAD,
    DISPONIBILIDAD,
    DRAFT_META_KEY,
    EJES_CULTURALES,
    ESTADO,
    FORMATO,
    GRADO,
    PRESENCIA,
    SENSIBILIDAD,
    TIPO_OBRA,
)

PLAY_KEYS = {
    "steam",
    "itch",
    "gog",
    "epic",
    "archive",
    "abandonware",
    "google_play",
    "apkpure",
    "web_oficial",
    "descarga_directa",
    "steam_workshop",
    "uptodown",
}

REQUIRED_FIELDS = [
    "id",
    "titulo",
    "estado",
    "vinculo_argentina",
    "desarrollador",
    "pais_desarrollo",
    "plataformas",
    "generos",
    "descripcion",
    "contexto_argentino",
    "enlaces",
    "formato",
    "verificado",
    "fecha_alta",
    "fecha_actualizacion",
]

FECHA_ALTA_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(T[0-9:.+-]+)?$")
FECHA_ACTUALIZACION_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URL_RE = re.compile(r"^https?://", re.I)


@dataclass
class Finding:
    level: str  # error | warning
    message: str

    def __str__(self) -> str:
        prefix = "ERROR" if self.level == "error" else "ADVERTENCIA"
        return f"{prefix}: {self.message}"


def _label(game: dict[str, Any]) -> str:
    return game.get("id") or game.get("titulo") or "?"


def _has_evidence(enlaces: dict[str, Any] | None) -> bool:
    if not isinstance(enlaces, dict):
        return False
    for key, value in enlaces.items():
        if key == "fuentes_investigacion":
            if isinstance(value, list) and any(str(item).strip() for item in value):
                return True
            continue
        if value:
            return True
    return False


def _has_playable(enlaces: dict[str, Any] | None) -> bool:
    if not isinstance(enlaces, dict):
        return False
    return any(enlaces.get(key) for key in PLAY_KEYS)


def validate_game(
    game: dict[str, Any],
    *,
    known_ids: Iterable[str] | None = None,
    strict_draft: bool = False,
    skip_duplicate_check: bool = False,
) -> list[Finding]:
    """Valida una ficha. Errores bloquean publicación; advertencias son editoriales."""
    findings: list[Finding] = []
    label = _label(game)
    known = set(known_ids or [])

    for field in REQUIRED_FIELDS:
        if field not in game:
            findings.append(Finding("error", f"{label}: falta el campo obligatorio '{field}'"))

    game_id = game.get("id")
    if not game_id:
        findings.append(Finding("error", f"{label}: el id no puede estar vacío"))
    elif not skip_duplicate_check and game_id in known:
        findings.append(
            Finding(
                "error",
                f"{label}: el id '{game_id}' ya existe en el catálogo publicado",
            )
        )

    if not str(game.get("titulo") or "").strip():
        findings.append(Finding("error", f"{label}: el título no puede estar vacío"))

    if not str(game.get("desarrollador") or "").strip():
        findings.append(
            Finding(
                "error",
                f"{label}: falta desarrollador — indicalo aunque sea 'estudio desconocido' con fuente",
            )
        )

    if not str(game.get("descripcion") or "").strip():
        findings.append(
            Finding(
                "error",
                f"{label}: falta descripción — explicá el vínculo argentino en al menos una oración",
            )
        )

    estado = game.get("estado")
    if estado is not None and estado not in ESTADO:
        findings.append(Finding("error", f"{label}: estado inválido '{estado}'"))

    for eje in game.get("ejes_culturales") or []:
        if eje not in EJES_CULTURALES:
            findings.append(Finding("error", f"{label}: eje cultural inválido '{eje}'"))

    if game.get("tipo_obra") and game["tipo_obra"] not in TIPO_OBRA:
        findings.append(Finding("error", f"{label}: tipo_obra inválido '{game['tipo_obra']}'"))

    if "formato" in game and game.get("formato") not in FORMATO:
        findings.append(Finding("error", f"{label}: formato inválido '{game.get('formato')}'"))

    if game.get("grado_relevancia_argentina") not in GRADO:
        findings.append(
            Finding(
                "error",
                f"{label}: grado_relevancia_argentina inválido — usá central, importante o menor",
            )
        )

    if game.get("calidad_fuente") not in CALIDAD:
        findings.append(Finding("error", f"{label}: calidad_fuente inválida"))

    if game.get("sensibilidad") not in SENSIBILIDAD:
        findings.append(Finding("error", f"{label}: sensibilidad inválida"))

    if game.get("disponibilidad") not in DISPONIBILIDAD:
        findings.append(Finding("error", f"{label}: disponibilidad inválida"))

    va = game.get("vinculo_argentina")
    if not isinstance(va, dict):
        findings.append(Finding("error", f"{label}: vinculo_argentina debe ser un objeto"))
        va = {}

    active = 0
    presencias = []
    for key in ("escenario", "protagonista", "deporte_argentino"):
        block = va.get(key) or {}
        if not isinstance(block, dict):
            findings.append(Finding("error", f"{label}: vinculo_argentina.{key} inválido"))
            continue
        if block.get("activo"):
            active += 1
            presencia = block.get("presencia")
            if presencia not in PRESENCIA:
                findings.append(
                    Finding(
                        "error",
                        f"{label}: presencia inválida en {key} — usá principal, secundaria o referencia_menor",
                    )
                )
            else:
                presencias.append(presencia)
    if active == 0:
        findings.append(
            Finding(
                "error",
                f"{label}: sin vínculo argentino activo — activá escenario, protagonista o deporte argentino",
            )
        )

    grado = game.get("grado_relevancia_argentina", "central")
    if grado == "menor" and presencias and all(p == "principal" for p in presencias):
        findings.append(
            Finding(
                "error",
                f"{label}: grado 'menor' incompatible con presencia 'principal' en todos los vínculos activos — bajá la presencia o subí el grado",
            )
        )

    for rel in game.get("relacionado_con") or []:
        if known and rel not in known and rel != game_id:
            findings.append(
                Finding(
                    "error",
                    f"{label}: relacionado_con apunta a ID inexistente '{rel}'",
                )
            )

    fecha_alta = game.get("fecha_alta")
    if fecha_alta is not None and not FECHA_ALTA_RE.match(str(fecha_alta)):
        findings.append(
            Finding(
                "error",
                f"{label}: fecha_alta inválida — usá YYYY-MM-DD o ISO con hora",
            )
        )

    fecha_act = game.get("fecha_actualizacion")
    if fecha_act is not None and not FECHA_ACTUALIZACION_RE.match(str(fecha_act)):
        findings.append(
            Finding(
                "error",
                f"{label}: fecha_actualizacion inválida — usá YYYY-MM-DD",
            )
        )

    enlaces = game.get("enlaces")
    if not isinstance(enlaces, dict):
        findings.append(Finding("error", f"{label}: enlaces debe ser un objeto"))
        enlaces = {}
    else:
        for key, value in enlaces.items():
            if key == "fuentes_investigacion":
                if not isinstance(value, list):
                    findings.append(
                        Finding("error", f"{label}: enlaces.fuentes_investigacion debe ser lista")
                    )
                else:
                    for url in value:
                        if url and not URL_RE.match(str(url)):
                            findings.append(
                                Finding(
                                    "error",
                                    f"{label}: fuente de investigación no parece una URL válida ({url})",
                                )
                            )
            elif value and not URL_RE.match(str(value)):
                findings.append(
                    Finding("error", f"{label}: enlace '{key}' no parece una URL válida")
                )

    if not _has_evidence(enlaces):
        findings.append(
            Finding(
                "error",
                f"{label}: falta evidencia — agregá un enlace jugable o fuentes_investigacion",
            )
        )

    plataformas = game.get("plataformas")
    if not isinstance(plataformas, list) or not plataformas:
        findings.append(Finding("error", f"{label}: plataformas debe tener al menos un valor"))

    generos = game.get("generos")
    if not isinstance(generos, list) or not generos:
        findings.append(Finding("error", f"{label}: generos debe tener al menos un valor"))

    contexto = game.get("contexto_argentino")
    if not isinstance(contexto, dict):
        findings.append(Finding("error", f"{label}: contexto_argentino debe ser un objeto"))
        contexto = {}

    # Advertencias editoriales
    descripcion = str(game.get("descripcion") or "")
    if len(descripcion.strip()) < 80:
        findings.append(
            Finding(
                "warning",
                f"{label}: descripción corta — conviene explicar mejor el vínculo argentino",
            )
        )

    temas = contexto.get("temas") if isinstance(contexto, dict) else None
    if not temas:
        findings.append(
            Finding(
                "warning",
                f"{label}: contexto_argentino.temas vacío — sumá temas editoriales útiles",
            )
        )

    if not game.get("ejes_culturales"):
        findings.append(
            Finding(
                "warning",
                f"{label}: sin ejes_culturales — la ficha queda menos explorables en filtros",
            )
        )

    if game.get("disponibilidad") == "desconocido":
        findings.append(
            Finding(
                "warning",
                f"{label}: disponibilidad desconocida — completá a_la_venta, gratis, abandonware o perdido",
            )
        )

    imagenes = game.get("imagenes") or {}
    if not isinstance(imagenes, dict) or not imagenes.get("portada"):
        findings.append(Finding("warning", f"{label}: sin portada"))
    if not isinstance(imagenes, dict) or not imagenes.get("capturas"):
        findings.append(Finding("warning", f"{label}: sin capturas"))

    if not _has_playable(enlaces):
        findings.append(
            Finding(
                "warning",
                f"{label}: sin link jugable — solo hay fuentes de investigación",
            )
        )

    if strict_draft and DRAFT_META_KEY in game and not get_draft_ready_fields(game):
        # hook reserved; currently covered by required checks above
        pass

    return findings


def get_draft_ready_fields(game: dict[str, Any]) -> bool:
    return bool(game.get("titulo") and game.get("descripcion") and game.get("desarrollador"))


def partition_findings(findings: list[Finding]) -> tuple[list[Finding], list[Finding]]:
    errors = [item for item in findings if item.level == "error"]
    warnings = [item for item in findings if item.level == "warning"]
    return errors, warnings


CATALOG_SOFT_ERROR_MARKERS = (
    "falta evidencia",
    "no parece una URL válida",
    "plataformas debe tener",
    "generos debe tener",
    "falta desarrollador",
    "falta descripción",
)


def validate_catalog(games: list[dict[str, Any]] | None = None) -> tuple[list[str], list[str]]:
    """Validación del catálogo publicado. Solo errores bloquean; no falla por advertencias."""
    if games is None:
        games = json.loads((DATA / "games.json").read_text(encoding="utf-8"))

    errors: list[str] = []
    warnings: list[str] = []
    ids: set[str] = set()
    game_ids = {game["id"] for game in games}

    for game in games:
        if game.get("id") in ids:
            errors.append(f"ID duplicado: {game.get('id')}")
        if game.get("id"):
            ids.add(game["id"])

        findings = validate_game(
            game,
            known_ids=game_ids - {game.get("id")},
            skip_duplicate_check=True,
        )
        for finding in findings:
            if finding.level == "error":
                # El catálogo histórico no exigía evidencia/URLs estrictas ni textos no vacíos
                # más allá de la presencia del campo; esos casos quedan como advertencia.
                if any(marker in finding.message for marker in CATALOG_SOFT_ERROR_MARKERS):
                    warnings.append(finding.message)
                else:
                    errors.append(finding.message)
            else:
                warnings.append(finding.message)

    return errors, warnings


def validate() -> int:
    games = json.loads((DATA / "games.json").read_text(encoding="utf-8"))
    errors, _warnings = validate_catalog(games)

    # Mantener el comportamiento previo de validate:links embebido
    link_errors: list[str] = []
    try:
        from validate_links import validate_links as validate_store_links

        link_errors = validate_store_links(games)
    except ImportError:
        pass

    if errors or link_errors:
        if errors:
            print("ERRORES:")
            for error in errors:
                print(" -", error)
        if link_errors:
            print("ERRORES DE ENLACES:")
            for error in link_errors:
                print(" -", error)
        return 1

    with_cover = sum(1 for g in games if g.get("imagenes", {}).get("portada"))
    with_play = sum(1 for g in games if any(g.get("enlaces", {}).get(k) for k in PLAY_KEYS))
    known_disp = sum(1 for g in games if g.get("disponibilidad") != "desconocido")
    with_ejes = sum(1 for g in games if g.get("ejes_culturales"))
    with_anio = sum(1 for g in games if g.get("anio"))
    with_capturas = sum(1 for g in games if g.get("imagenes", {}).get("capturas"))
    n = len(games)
    ids = {g["id"] for g in games}

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
