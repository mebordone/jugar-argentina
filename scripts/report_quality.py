#!/usr/bin/env python3
"""Genera un reporte editorial de calidad para el catalogo."""
from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
GAMES_PATH = DATA / "games.json"
REPORT_PATH = DATA / "quality_report.md"
YEAR_CANDIDATES_PATH = DATA / "year_candidates.json"
COVER_CANDIDATES_PATH = DATA / "cover_candidates.json"

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
}

SHORT_DESCRIPTION_CHARS = 110
VERY_SHORT_DESCRIPTION_CHARS = 80
SIMILARITY_THRESHOLD = 0.82
PENDING_STATES = {"en_desarrollo", "early_access", "prototipo"}


def strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value.lower())
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")


def normalize_text(value: str) -> str:
    value = strip_accents(value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def has_playable_link(game: dict) -> bool:
    enlaces = game.get("enlaces", {})
    return any(enlaces.get(key) for key in PLAY_KEYS)


def game_label(game: dict) -> str:
    year = game.get("anio") or "s/f"
    return f"`{game.get('id')}` - {game.get('titulo')} ({year})"


def md_list(items: list[str], empty: str = "Sin casos.") -> list[str]:
    if not items:
        return [f"- {empty}"]
    return [f"- {item}" for item in items]


def top_counter(counter: Counter, limit: int = 20) -> list[str]:
    return [f"{name}: {count}" for name, count in counter.most_common(limit)]


def collect_distributions(games: list[dict]) -> dict[str, Counter]:
    provincias: Counter = Counter()
    regiones: Counter = Counter()
    ejes: Counter = Counter()
    grados: Counter = Counter()
    tipos: Counter = Counter()

    for game in games:
        contexto = game.get("contexto_argentino", {})
        provincias.update(contexto.get("provincias") or ["Sin provincia"])
        regiones.update(contexto.get("regiones") or ["Sin region"])
        ejes.update(game.get("ejes_culturales") or ["Sin eje"])
        grados.update([game.get("grado_relevancia_argentina") or "Sin grado"])
        tipos.update([game.get("tipo_obra") or "Sin tipo"])

    return {
        "provincias": provincias,
        "regiones": regiones,
        "ejes": ejes,
        "grados": grados,
        "tipos": tipos,
    }


def collect_gaps(games: list[dict]) -> dict[str, list[dict]]:
    return {
        "sin_portada": [g for g in games if not g.get("imagenes", {}).get("portada")],
        "sin_capturas": [g for g in games if not g.get("imagenes", {}).get("capturas")],
        "sin_anio": [g for g in games if not g.get("anio")],
        "sin_link_jugable": [g for g in games if not has_playable_link(g)],
        "sin_provincia": [
            g
            for g in games
            if not g.get("contexto_argentino", {}).get("provincias")
        ],
        "sin_eje": [g for g in games if not g.get("ejes_culturales")],
    }


def collect_short_descriptions(games: list[dict]) -> list[dict]:
    return sorted(
        [
            game
            for game in games
            if len((game.get("descripcion") or "").strip()) < SHORT_DESCRIPTION_CHARS
        ],
        key=lambda g: len((g.get("descripcion") or "").strip()),
    )


def collect_similar_descriptions(games: list[dict]) -> list[tuple[dict, dict, float]]:
    normalized = [
        (game, normalize_text(game.get("descripcion") or ""))
        for game in games
        if len(game.get("descripcion") or "") >= VERY_SHORT_DESCRIPTION_CHARS
    ]
    pairs: list[tuple[dict, dict, float]] = []
    for index, (left, left_desc) in enumerate(normalized):
        for right, right_desc in normalized[index + 1 :]:
            ratio = SequenceMatcher(None, left_desc, right_desc).ratio()
            if ratio >= SIMILARITY_THRESHOLD:
                pairs.append((left, right, ratio))
    return sorted(pairs, key=lambda item: item[2], reverse=True)


def classify_release_status(game: dict) -> str:
    if game.get("anio"):
        return "publicado"
    if game.get("anio_nota") or game.get("estado") in PENDING_STATES:
        return "pendiente"
    return "desconocido"


def collect_release_coverage(games: list[dict]) -> dict[str, list[dict]]:
    buckets: dict[str, list[dict]] = {
        "publicado": [],
        "pendiente": [],
        "desconocido": [],
    }
    for game in games:
        buckets[classify_release_status(game)].append(game)
    return buckets


def pct(value: int, total: int) -> str:
    if not total:
        return "0%"
    return f"{100 * value / total:.1f}%"


def build_date_coverage_section(games: list[dict]) -> list[str]:
    buckets = collect_release_coverage(games)
    total = len(games)
    publicado = len(buckets["publicado"])
    pendiente = len(buckets["pendiente"])
    desconocido = len(buckets["desconocido"])
    categorizado = publicado + pendiente + desconocido

    return [
        "## Cobertura de fechas",
        "",
        f"- Con anio publicado: {publicado} ({pct(publicado, total)})",
        f"- Sin anio, en desarrollo/TBD: {pendiente} ({pct(pendiente, total)})",
        f"- Sin anio, desconocido: {desconocido} ({pct(desconocido, total)})",
        f"- Cobertura categorizada: {pct(categorizado, total)}",
        "",
        "### Sin anio, en desarrollo o por confirmarse",
        "",
        *md_list([game_label(game) for game in buckets["pendiente"][:40]]),
        "",
        "### Sin anio, fecha desconocida",
        "",
        *md_list([game_label(game) for game in buckets["desconocido"][:40]]),
        "",
    ]


def load_year_candidates() -> dict | None:
    if not YEAR_CANDIDATES_PATH.exists():
        return None
    return json.loads(YEAR_CANDIDATES_PATH.read_text(encoding="utf-8"))


def load_cover_candidates() -> dict | None:
    if not COVER_CANDIDATES_PATH.exists():
        return None
    return json.loads(COVER_CANDIDATES_PATH.read_text(encoding="utf-8"))


def cover_candidate_label(candidate: dict) -> str:
    fuente = candidate.get("fuente") or "sin fuente"
    confianza = candidate.get("confianza") or "sin dato"
    return (
        f"`{candidate.get('id')}` - {candidate.get('titulo')} "
        f"({fuente}, {confianza})"
    )


def is_recoverable_cover_candidate(game: dict, candidate: dict | None) -> bool:
    if candidate and candidate.get("portada_propuesta"):
        return True
    return has_playable_link(game)


def build_cover_coverage_section(
    games: list[dict], candidates_payload: dict | None
) -> list[str]:
    total = len(games)
    con_portada = [game for game in games if game.get("imagenes", {}).get("portada")]
    sin_portada = [game for game in games if not game.get("imagenes", {}).get("portada")]

    candidates_by_id: dict[str, dict] = {}
    if candidates_payload:
        for candidate in candidates_payload.get("candidatos") or []:
            if candidate.get("id"):
                candidates_by_id[candidate["id"]] = candidate

    recuperables = [
        game
        for game in sin_portada
        if is_recoverable_cover_candidate(game, candidates_by_id.get(game["id"]))
    ]
    pendientes_manual = [
        game
        for game in sin_portada
        if not is_recoverable_cover_candidate(game, candidates_by_id.get(game["id"]))
    ]

    lines = [
        "## Cobertura de portadas",
        "",
        f"- Con portada: {len(con_portada)} ({pct(len(con_portada), total)})",
        f"- Sin portada, recuperable automatico: {len(recuperables)}",
        f"- Sin portada, pendiente manual: {len(pendientes_manual)}",
        f"- Cobertura: {pct(len(con_portada), total)}",
        "",
    ]

    if sin_portada:
        lines.extend(
            [
                "### Sin portada",
                "",
                *md_list([game_label(game) for game in sin_portada[:40]]),
                "",
            ]
        )

    if candidates_payload:
        pendientes = [
            candidate
            for candidate in candidates_payload.get("candidatos") or []
            if candidate.get("portada_propuesta")
            and not candidate.get("aplicado")
            and candidate.get("confianza") != "alta"
        ]
        if pendientes:
            lines.extend(
                [
                    "### Candidatos pendientes de revision",
                    "",
                    *md_list([cover_candidate_label(candidate) for candidate in pendientes[:40]]),
                    "",
                ]
            )

    return lines


def candidate_label(candidate: dict) -> str:
    year = candidate.get("anio_propuesto") or candidate.get("status") or "s/f"
    fuente = candidate.get("fuente") or "sin fuente"
    return (
        f"`{candidate.get('id')}` - {candidate.get('titulo')} "
        f"({year}, {fuente})"
    )


def build_year_section(candidates_payload: dict | None) -> list[str]:
    if not candidates_payload:
        return []

    candidatos = candidates_payload.get("candidatos") or []
    aplicados = [c for c in candidatos if c.get("aplicado")]
    tbd = [c for c in candidatos if c.get("status") == "tbd"]
    futuro = [c for c in candidatos if c.get("status") == "futuro"]
    pendientes = [
        c
        for c in candidatos
        if c.get("anio_propuesto")
        and not c.get("aplicado")
        and c.get("confianza") != "alta"
    ]
    sin_dato = [
        c
        for c in candidatos
        if not c.get("anio_propuesto") and c.get("status") in {"sin_dato", "tbd"}
    ]

    return [
        "## Anos propuestos / pendientes",
        "",
        f"- Barrido sobre juegos sin anio: {candidates_payload.get('total_sin_anio', 0)}",
        f"- Anos aplicados: {candidates_payload.get('aplicados', 0)}",
        f"- Pendientes de revision: {candidates_payload.get('pendientes_revision', 0)}",
        f"- Por confirmarse (TBD): {len(tbd)}",
        f"- Fechas futuras detectadas: {len(futuro)}",
        f"- Sin dato tras barrido: {candidates_payload.get('sin_dato', 0)}",
        "",
        "### Anos aplicados automaticamente",
        "",
        *md_list([candidate_label(c) for c in aplicados[:40]]),
        "",
        "### Por confirmarse en tienda",
        "",
        *md_list(
            [
                f"{candidate_label(c)} - {c.get('fecha_raw', '')}"
                for c in tbd[:40]
            ]
        ),
        "",
        "### Fechas futuras detectadas",
        "",
        *md_list(
            [
                f"{candidate_label(c)} - {c.get('fecha_raw', '')}"
                for c in futuro[:40]
            ]
        ),
        "",
        "### Propuestos sin aplicar (confianza media/baja)",
        "",
        *md_list([candidate_label(c) for c in pendientes[:40]]),
        "",
        "### Sin dato tras barrido",
        "",
        *md_list([candidate_label(c) for c in sin_dato[:40]]),
        "",
    ]


def collect_minor_visibility(games: list[dict]) -> list[dict]:
    out = []
    for game in games:
        if game.get("grado_relevancia_argentina") != "menor":
            continue
        score = 0
        if game.get("imagenes", {}).get("portada"):
            score += 1
        if game.get("imagenes", {}).get("capturas"):
            score += 1
        if has_playable_link(game):
            score += 1
        if game.get("ejes_culturales"):
            score += 1
        if score >= 3:
            out.append(game)
    return sorted(out, key=lambda g: g.get("titulo", ""))


def build_report(games: list[dict]) -> str:
    gaps = collect_gaps(games)
    distributions = collect_distributions(games)
    short_descriptions = collect_short_descriptions(games)
    similar_descriptions = collect_similar_descriptions(games)
    minor_visibility = collect_minor_visibility(games)
    year_candidates = load_year_candidates()
    cover_candidates = load_cover_candidates()
    total = len(games)

    lines = [
        "# Reporte de calidad editorial",
        "",
        f"Generado: {date.today().isoformat()}",
        "",
        "## Resumen",
        "",
        f"- Juegos analizados: {total}",
        f"- Sin portada: {len(gaps['sin_portada'])}",
        f"- Sin capturas: {len(gaps['sin_capturas'])}",
        f"- Sin anio: {len(gaps['sin_anio'])}",
        f"- Sin link jugable: {len(gaps['sin_link_jugable'])}",
        f"- Sin provincia: {len(gaps['sin_provincia'])}",
        f"- Sin eje cultural: {len(gaps['sin_eje'])}",
        f"- Descripciones cortas: {len(short_descriptions)}",
        f"- Pares de descripciones similares: {len(similar_descriptions)}",
        f"- Referencias menores con alta visibilidad: {len(minor_visibility)}",
        "",
        *build_date_coverage_section(games),
        *build_cover_coverage_section(games, cover_candidates),
        "## Backlog editorial prioritario",
        "",
        "### Descripciones cortas",
        "",
        *md_list(
            [
                f"{game_label(game)} - {len((game.get('descripcion') or '').strip())} caracteres"
                for game in short_descriptions[:25]
            ]
        ),
        "",
        "### Posibles descripciones repetidas",
        "",
        *md_list(
            [
                f"{game_label(left)} / {game_label(right)} - similitud {ratio:.0%}"
                for left, right, ratio in similar_descriptions[:20]
            ]
        ),
        "",
        "### Referencias menores con alta visibilidad",
        "",
        *md_list([game_label(game) for game in minor_visibility[:30]]),
        "",
        "## Huecos de completitud",
        "",
        "### Sin portada",
        "",
        *md_list([game_label(game) for game in gaps["sin_portada"][:40]]),
        "",
        "### Sin capturas",
        "",
        *md_list([game_label(game) for game in gaps["sin_capturas"][:40]]),
        "",
        "### Sin anio",
        "",
        *md_list([game_label(game) for game in gaps["sin_anio"][:40]]),
        "",
        "### Sin link jugable",
        "",
        *md_list([game_label(game) for game in gaps["sin_link_jugable"][:40]]),
        "",
        "### Sin provincia",
        "",
        *md_list([game_label(game) for game in gaps["sin_provincia"][:40]]),
        "",
        "### Sin eje cultural",
        "",
        *md_list([game_label(game) for game in gaps["sin_eje"][:40]]),
        "",
        "## Distribuciones",
        "",
        "### Provincias",
        "",
        *md_list(top_counter(distributions["provincias"])),
        "",
        "### Regiones",
        "",
        *md_list(top_counter(distributions["regiones"])),
        "",
        "### Ejes culturales",
        "",
        *md_list(top_counter(distributions["ejes"])),
        "",
        "### Grados de relevancia",
        "",
        *md_list(top_counter(distributions["grados"])),
        "",
        "### Tipos de obra",
        "",
        *md_list(top_counter(distributions["tipos"])),
        "",
        *build_year_section(year_candidates),
    ]
    return "\n".join(lines)


def main() -> int:
    games = json.loads(GAMES_PATH.read_text(encoding="utf-8"))
    report = build_report(games)
    REPORT_PATH.write_text(report + "\n", encoding="utf-8")
    print(f"OK: reporte generado en {REPORT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
