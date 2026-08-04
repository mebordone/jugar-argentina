#!/usr/bin/env python3
"""Núcleo compartido de fichas, plantillas y adaptadores de candidatos."""
from __future__ import annotations

import csv
import json
import re
import unicodedata
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DRAFTS_DIR = DATA / "drafts"
GAMES_PATH = DATA / "games.json"
CANDIDATES_DIR = DATA / "candidates"
CSV_PATH = DATA / "raw_candidates.csv"

EJES_CULTURALES = {
    "politica",
    "satira",
    "folclore",
    "juegos_tradicionales",
    "historia",
    "memoria",
    "cultura_urbana",
    "historieta",
    "literatura",
    "educativo",
    "deporte",
    "geografia",
    "migracion",
    "musica",
}
TIPO_OBRA = {
    "comercial",
    "indie",
    "educativo",
    "jam",
    "mod",
    "fan_game",
    "abandonware",
    "prototipo",
    "promocional",
}
FORMATO = {
    "juego_base",
    "mod",
    "mapa",
    "campania",
    "dlc",
    "expansion",
    "contenido_licenciado",
    "demo",
    "prototipo",
    "coleccion",
}
GRADO = {"central", "importante", "menor"}
CALIDAD = {"oficial", "tienda", "prensa", "wiki", "foro", "archive"}
SENSIBILIDAD = {"baja", "media", "alta"}
DISPONIBILIDAD = {"a_la_venta", "gratis", "abandonware", "perdido", "desconocido"}
ESTADO = {
    "publicado",
    "early_access",
    "en_desarrollo",
    "cancelado",
    "abandonware",
    "prototipo",
}
PRESENCIA = {"principal", "secundaria", "referencia_menor"}

CANONICAL_CANDIDATE_STATES = {"candidato", "en_revision", "publicado", "descartado"}
OPEN_CANDIDATE_STATES = {"candidato", "en_revision"}

DRAFT_META_KEY = "_ficha_draft"

TEMPLATE_IDS = (
    "central",
    "escenario",
    "protagonista",
    "deporte",
    "referencia_menor",
    "educativo",
    "mod",
    "mapa_campania",
    "dlc_contenido",
    "abandonware",
)


def today_iso() -> str:
    return str(date.today())


def normalize_title(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", normalize_title(text)).strip("-")


def vinculo_null() -> dict[str, Any]:
    return {"activo": False, "presencia": None}


def make_vinculo(
    escenario: str | None = None,
    protagonista: str | None = None,
    deporte: str | None = None,
    subtipo: str | None = None,
) -> dict[str, Any]:
    out: dict[str, Any] = {
        "escenario": {"activo": bool(escenario), "presencia": escenario},
        "protagonista": {"activo": bool(protagonista), "presencia": protagonista},
        "deporte_argentino": {"activo": bool(deporte), "presencia": deporte},
    }
    if deporte and subtipo:
        out["deporte_argentino"]["subtipo"] = subtipo
    return out


def empty_contexto() -> dict[str, list[str]]:
    return {"regiones": [], "provincias": [], "periodo_historico": [], "temas": []}


def empty_imagenes() -> dict[str, Any]:
    return {"portada": None, "capturas": []}


def empty_metadatos() -> dict[str, Any]:
    return {
        "idiomas": ["es"],
        "multijugador": False,
        "precio": None,
        "rating": {},
        "tipo": "juego",
    }


def base_ficha(
    *,
    id_: str,
    titulo: str,
    template: str,
    anio: int | None = None,
    estado: str = "publicado",
    desarrollador: str = "",
    pais_desarrollo: str = "Argentina",
    plataformas: list[str] | None = None,
    generos: list[str] | None = None,
    descripcion: str = "",
    contexto: dict[str, Any] | None = None,
    enlaces: dict[str, Any] | None = None,
    vinculo: dict[str, Any] | None = None,
    personajes: list[dict[str, Any]] | None = None,
    deporte: dict[str, Any] | None = None,
    imagenes: dict[str, Any] | None = None,
    metadatos: dict[str, Any] | None = None,
    ejes_culturales: list[str] | None = None,
    tipo_obra: str = "indie",
    formato: str = "juego_base",
    grado_relevancia_argentina: str = "importante",
    calidad_fuente: str = "prensa",
    sensibilidad: str = "baja",
    serie: str | None = None,
    edicion: str | None = None,
    relacionado_con: list[str] | None = None,
    disponibilidad: str = "desconocido",
    verificado: bool = False,
    fecha_alta: str | None = None,
    fecha_actualizacion: str | None = None,
) -> dict[str, Any]:
    day = today_iso()
    return {
        "id": id_,
        "titulo": titulo,
        "titulo_original": titulo,
        "anio": anio,
        "estado": estado,
        "vinculo_argentina": vinculo or make_vinculo(),
        "personajes_argentinos": personajes or [],
        "deporte_argentino": deporte,
        "desarrollador": desarrollador,
        "pais_desarrollo": pais_desarrollo,
        "plataformas": plataformas or ["PC"],
        "generos": generos or [],
        "descripcion": descripcion,
        "contexto_argentino": contexto or empty_contexto(),
        "enlaces": enlaces or {},
        "imagenes": imagenes or empty_imagenes(),
        "metadatos": metadatos or empty_metadatos(),
        "ejes_culturales": ejes_culturales or [],
        "tipo_obra": tipo_obra,
        "formato": formato,
        "grado_relevancia_argentina": grado_relevancia_argentina,
        "calidad_fuente": calidad_fuente,
        "sensibilidad": sensibilidad,
        "serie": serie,
        "edicion": edicion,
        "relacionado_con": relacionado_con or [],
        "disponibilidad": disponibilidad,
        "verificado": verificado,
        "fecha_alta": fecha_alta or day,
        "fecha_actualizacion": fecha_actualizacion or day,
        DRAFT_META_KEY: {"template": template},
    }


TEMPLATE_PRESETS: dict[str, dict[str, Any]] = {
    "central": {
        "formato": "juego_base",
        "tipo_obra": "indie",
        "grado_relevancia_argentina": "central",
        "vinculo": make_vinculo("principal"),
        "disponibilidad": "desconocido",
    },
    "escenario": {
        "formato": "juego_base",
        "tipo_obra": "indie",
        "grado_relevancia_argentina": "importante",
        "vinculo": make_vinculo("principal"),
        "ejes_culturales": ["geografia"],
    },
    "protagonista": {
        "formato": "juego_base",
        "tipo_obra": "indie",
        "grado_relevancia_argentina": "importante",
        "vinculo": make_vinculo(None, "principal"),
    },
    "deporte": {
        "formato": "juego_base",
        "tipo_obra": "comercial",
        "grado_relevancia_argentina": "importante",
        "vinculo": make_vinculo(None, None, "principal", "liga_futbol"),
        "ejes_culturales": ["deporte"],
        "deporte": {
            "deporte": "futbol",
            "competicion": [],
            "equipos_destacados": [],
            "modo": "gestion_liga",
        },
    },
    "referencia_menor": {
        "formato": "juego_base",
        "tipo_obra": "comercial",
        "grado_relevancia_argentina": "menor",
        "vinculo": make_vinculo("referencia_menor"),
        "sensibilidad": "baja",
    },
    "educativo": {
        "formato": "juego_base",
        "tipo_obra": "educativo",
        "grado_relevancia_argentina": "importante",
        "vinculo": make_vinculo("principal"),
        "ejes_culturales": ["educativo"],
        "disponibilidad": "gratis",
    },
    "mod": {
        "formato": "mod",
        "tipo_obra": "mod",
        "grado_relevancia_argentina": "importante",
        "vinculo": make_vinculo("principal"),
        "disponibilidad": "gratis",
    },
    "mapa_campania": {
        "formato": "mapa",
        "tipo_obra": "mod",
        "grado_relevancia_argentina": "importante",
        "vinculo": make_vinculo("principal"),
        "disponibilidad": "gratis",
    },
    "dlc_contenido": {
        "formato": "contenido_licenciado",
        "tipo_obra": "comercial",
        "grado_relevancia_argentina": "importante",
        "vinculo": make_vinculo(None, None, "principal"),
        "ejes_culturales": ["deporte"],
    },
    "abandonware": {
        "formato": "juego_base",
        "tipo_obra": "abandonware",
        "estado": "abandonware",
        "grado_relevancia_argentina": "importante",
        "vinculo": make_vinculo("principal"),
        "disponibilidad": "abandonware",
        "calidad_fuente": "archive",
    },
}


def apply_template(template: str, titulo: str, id_: str | None = None) -> dict[str, Any]:
    if template not in TEMPLATE_PRESETS:
        raise ValueError(f"Plantilla desconocida '{template}'. Opciones: {', '.join(TEMPLATE_IDS)}")
    preset = deepcopy(TEMPLATE_PRESETS[template])
    game_id = id_ or slugify(titulo)
    if not game_id:
        raise ValueError("No se pudo generar un id a partir del título")
    ficha = base_ficha(
        id_=game_id,
        titulo=titulo,
        template=template,
        estado=preset.get("estado", "publicado"),
        vinculo=preset.get("vinculo"),
        deporte=preset.get("deporte"),
        ejes_culturales=list(preset.get("ejes_culturales") or []),
        tipo_obra=preset.get("tipo_obra", "indie"),
        formato=preset.get("formato", "juego_base"),
        grado_relevancia_argentina=preset.get("grado_relevancia_argentina", "importante"),
        calidad_fuente=preset.get("calidad_fuente", "prensa"),
        sensibilidad=preset.get("sensibilidad", "baja"),
        disponibilidad=preset.get("disponibilidad", "desconocido"),
    )
    return ficha


def strip_draft_meta(ficha: dict[str, Any]) -> dict[str, Any]:
    out = deepcopy(ficha)
    out.pop(DRAFT_META_KEY, None)
    return out


def set_draft_meta(ficha: dict[str, Any], **fields: Any) -> dict[str, Any]:
    meta = dict(ficha.get(DRAFT_META_KEY) or {})
    meta.update(fields)
    ficha[DRAFT_META_KEY] = meta
    return ficha


def get_draft_meta(ficha: dict[str, Any]) -> dict[str, Any]:
    return dict(ficha.get(DRAFT_META_KEY) or {})


def normalize_candidate_status(raw: str | None) -> str:
    value = (raw or "").strip().lower()
    mapping = {
        "": "candidato",
        "candidato": "candidato",
        "pendiente": "en_revision",
        "en_revision": "en_revision",
        "requiere_verificacion": "en_revision",
        "alta": "en_revision",
        "verificado": "publicado",
        "publicado": "publicado",
        "descartado": "descartado",
    }
    return mapping.get(value, "candidato" if value not in CANONICAL_CANDIDATE_STATES else value)


def is_open_candidate_status(raw: str | None) -> bool:
    return normalize_candidate_status(raw) in OPEN_CANDIDATE_STATES


def load_games(path: Path | None = None) -> list[dict[str, Any]]:
    target = path or GAMES_PATH
    return json.loads(target.read_text(encoding="utf-8"))


def write_json_atomic(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def draft_path(game_id: str, drafts_dir: Path | None = None) -> Path:
    return (drafts_dir or DRAFTS_DIR) / f"{game_id}.json"


def list_drafts(drafts_dir: Path | None = None) -> list[Path]:
    directory = drafts_dir or DRAFTS_DIR
    if not directory.exists():
        return []
    return sorted(directory.glob("*.json"))


def load_draft(game_id: str, drafts_dir: Path | None = None) -> dict[str, Any]:
    path = draft_path(game_id, drafts_dir)
    if not path.exists():
        raise FileNotFoundError(f"No existe borrador '{game_id}' en {path.parent}")
    return json.loads(path.read_text(encoding="utf-8"))


def save_draft(ficha: dict[str, Any], drafts_dir: Path | None = None) -> Path:
    path = draft_path(ficha["id"], drafts_dir)
    write_json_atomic(path, ficha)
    return path


def load_csv_candidates(path: Path | None = None) -> list[dict[str, str]]:
    target = path or CSV_PATH
    if not target.exists():
        return []
    with target.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_json_candidates(directory: Path | None = None) -> list[dict[str, Any]]:
    target = directory or CANDIDATES_DIR
    if not target.exists():
        return []
    items: list[dict[str, Any]] = []
    for path in sorted(target.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            continue
        for item in payload:
            if not isinstance(item, dict):
                continue
            row = dict(item)
            row["_source_file"] = path.name
            row["_source_kind"] = "json"
            items.append(row)
    return items


def find_candidate(
    candidate_id: str,
    *,
    csv_path: Path | None = None,
    candidates_dir: Path | None = None,
) -> dict[str, Any] | None:
    needle = candidate_id.strip().lower()
    # Preferir registro maestro CSV (tracking).
    try:
        from tracking import load_tracking_rows

        for row in load_tracking_rows(csv_path):
            row_id = (row.get("id") or "").lower()
            titulo = (row.get("titulo") or "").strip()
            if needle in {row_id, titulo.lower(), slugify(titulo)}:
                found = dict(row)
                found["_source_kind"] = "csv"
                found["_source_file"] = "raw_candidates.csv"
                found["tracking_id"] = row.get("id")
                return found
    except Exception:
        pass

    for item in load_json_candidates(candidates_dir):
        item_id = str(item.get("id") or "").lower()
        title_slug = slugify(str(item.get("titulo") or ""))
        if needle in {item_id, title_slug}:
            found = dict(item)
            found["tracking_id"] = str(item.get("id") or title_slug)
            return found

    for row in load_csv_candidates(csv_path):
        titulo = (row.get("titulo") or "").strip()
        row_id = (row.get("id") or slugify(titulo)).lower()
        if needle in {row_id, titulo.lower(), slugify(titulo)}:
            found = dict(row)
            found["id"] = row.get("id") or slugify(titulo)
            found["tracking_id"] = found["id"]
            found["_source_kind"] = "csv"
            found["_source_file"] = "raw_candidates.csv"
            return found
    return None


def guess_link_key(url: str) -> str:
    lower = url.lower()
    if "steampowered.com" in lower or "steamcommunity.com" in lower:
        if "workshop" in lower:
            return "steam_workshop"
        return "steam"
    if "itch.io" in lower:
        return "itch"
    if "gog.com" in lower:
        return "gog"
    if "archive.org" in lower:
        return "archive"
    if "play.google.com" in lower:
        return "google_play"
    if "mobygames.com" in lower:
        return "mobygames"
    if "wikipedia.org" in lower:
        return "wikipedia"
    return "web_oficial"


def candidate_to_draft(
    candidate: dict[str, Any],
    *,
    template: str,
    id_override: str | None = None,
) -> dict[str, Any]:
    titulo = str(candidate.get("titulo") or "").strip()
    if not titulo:
        raise ValueError("El candidato no tiene título")

    game_id = id_override or str(candidate.get("id") or slugify(titulo))
    ficha = apply_template(template, titulo, game_id)

    anio = candidate.get("anio")
    if anio not in (None, ""):
        try:
            ficha["anio"] = int(anio)
        except (TypeError, ValueError):
            pass

    vinculo_texto = str(
        candidate.get("vinculo_argentino")
        or candidate.get("vinculo_preliminar")
        or candidate.get("nota")
        or ""
    ).strip()
    if vinculo_texto and not ficha["descripcion"]:
        ficha["descripcion"] = vinculo_texto

    sensibilidad = str(candidate.get("sensibilidad") or "").strip().lower()
    if sensibilidad in SENSIBILIDAD:
        ficha["sensibilidad"] = sensibilidad

    enlaces: dict[str, Any] = {}
    urls: list[str] = []
    for key in ("url", "fuente"):
        value = candidate.get(key)
        if value:
            urls.append(str(value))
    fuentes = candidate.get("fuentes")
    if isinstance(fuentes, list):
        urls.extend(str(item) for item in fuentes if item)
    for url in urls:
        url = url.strip()
        if not url:
            continue
        key = guess_link_key(url)
        if key == "web_oficial" and "web_oficial" in enlaces:
            enlaces.setdefault("fuentes_investigacion", [])
            if url not in enlaces["fuentes_investigacion"]:
                enlaces["fuentes_investigacion"].append(url)
        elif key not in enlaces:
            enlaces[key] = url
        else:
            enlaces.setdefault("fuentes_investigacion", [])
            if url not in enlaces["fuentes_investigacion"] and url != enlaces.get(key):
                enlaces["fuentes_investigacion"].append(url)
    if enlaces:
        ficha["enlaces"] = enlaces

    estado_raw = (
        candidate.get("estado_analisis")
        or candidate.get("estado_triage")
        or candidate.get("estado")
    )
    set_draft_meta(
        ficha,
        template=template,
        tracking_id=str(candidate.get("tracking_id") or candidate.get("id") or game_id),
        candidate_id=str(candidate.get("id") or game_id),
        candidate_source=candidate.get("_source_kind"),
        candidate_file=candidate.get("_source_file"),
        candidate_status_raw=estado_raw,
        candidate_status=normalize_candidate_status(str(estado_raw) if estado_raw is not None else None),
        ficha_id=game_id,
    )
    return ficha


def mark_json_candidate_published(
    *,
    candidate_id: str,
    source_file: str | None = None,
    candidates_dir: Path | None = None,
) -> bool:
    directory = candidates_dir or CANDIDATES_DIR
    if not directory.exists():
        return False
    paths = [directory / source_file] if source_file else sorted(directory.glob("*.json"))
    changed = False
    for path in paths:
        if not path.exists() or not path.name.endswith(".json"):
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            continue
        file_changed = False
        for item in payload:
            if not isinstance(item, dict):
                continue
            item_id = str(item.get("id") or "")
            if item_id != candidate_id and slugify(str(item.get("titulo") or "")) != candidate_id:
                continue
            if item.get("estado_analisis") != "publicado":
                item["estado_analisis"] = "publicado"
                file_changed = True
            if item.get("decision") != "publicado":
                item["decision"] = "publicado"
                file_changed = True
        if file_changed:
            write_json_atomic(path, payload)
            changed = True
    return changed


def publish_draft_to_games(
    ficha: dict[str, Any],
    *,
    games_path: Path | None = None,
    drafts_dir: Path | None = None,
    csv_path: Path | None = None,
    candidates_dir: Path | None = None,
    public_path: Path | None = None,
    descartados_path: Path | None = None,
) -> dict[str, Any]:
    """Publica de forma transaccional: games + CSV tracking (+ manifiesto) o nada."""
    from tracking import (
        DESCARTADOS_PATH,
        PUBLIC_GAMES_PATH,
        create_open_tracking_row,
        load_tracking_rows,
        mark_tracking_published,
        save_tracking_rows,
    )
    from validate_consistency import validate_consistency

    games_file = games_path or GAMES_PATH
    tracking_file = csv_path or CSV_PATH
    drafts = drafts_dir or DRAFTS_DIR
    public_file = PUBLIC_GAMES_PATH if public_path is None else public_path
    desc_file = DESCARTADOS_PATH if descartados_path is None else descartados_path

    games = load_games(games_file)
    published = strip_draft_meta(ficha)
    published["verificado"] = True
    day = today_iso()
    published["fecha_actualizacion"] = day
    if not published.get("fecha_alta"):
        published["fecha_alta"] = day

    existing_ids = {game["id"] for game in games}
    if published["id"] in existing_ids:
        raise ValueError(f"Ya existe una ficha publicada con id '{published['id']}'")

    meta = get_draft_meta(ficha)
    tracking_id = str(meta.get("tracking_id") or published["id"])
    rows = load_tracking_rows(tracking_file)
    if not any(row.get("id") == tracking_id for row in rows):
        rows.append(
            create_open_tracking_row(
                titulo=published.get("titulo") or published["id"],
                tracking_id=tracking_id,
                origen="cli",
                existing_ids={row.get("id") or "" for row in rows},
            )
        )
    rows = mark_tracking_published(
        rows,
        tracking_id=tracking_id,
        ficha_id=published["id"],
        titulo=published.get("titulo"),
    )

    next_games = list(games) + [published]
    next_games.sort(key=lambda item: item["id"])

    # Escribir temporales y validar antes de reemplazar.
    games_tmp = games_file.with_suffix(games_file.suffix + ".tmp")
    csv_tmp = tracking_file.with_suffix(tracking_file.suffix + ".tmp")
    write_json_atomic(games_tmp, next_games)
    # save_tracking_rows escribe atómico sobre csv_tmp.path parent; usamos path final via tmp rename
    save_tracking_rows(rows, csv_tmp)

    errors = validate_consistency(
        csv_path=csv_tmp,
        games_path=games_tmp,
        public_path=None,
        require_public=False,
        candidates_dir=candidates_dir or CANDIDATES_DIR,
        descartados_path=desc_file,
    )
    if errors:
        games_tmp.unlink(missing_ok=True)
        csv_tmp.unlink(missing_ok=True)
        raise ValueError("Publicación abortada por inconsistencias:\n- " + "\n- ".join(errors))

    games_tmp.replace(games_file)
    csv_tmp.replace(tracking_file)

    candidate_id = str(meta.get("candidate_id") or tracking_id)
    mark_json_candidate_published(
        candidate_id=candidate_id,
        source_file=meta.get("candidate_file"),
        candidates_dir=candidates_dir,
    )

    # Mantener copia pública alineada cuando se indica ruta.
    if public_file is not None:
        public_file.parent.mkdir(parents=True, exist_ok=True)
        write_json_atomic(public_file, next_games)

    path = draft_path(published["id"], drafts)
    if path.exists():
        path.unlink()
    return published


def discard_tracking_candidate(
    tracking_id: str,
    *,
    motivo: str,
    csv_path: Path | None = None,
    descartados_path: Path | None = None,
) -> dict[str, str]:
    from tracking import (
        DESCARTADOS_PATH,
        find_tracking_row,
        load_tracking_rows,
        mark_tracking_discarded,
        save_tracking_rows,
        today_iso,
    )

    if not motivo.strip():
        raise ValueError("El descarte requiere un motivo")
    tracking_file = csv_path or CSV_PATH
    desc_file = descartados_path or DESCARTADOS_PATH
    rows = load_tracking_rows(tracking_file)
    row = find_tracking_row(rows, tracking_id=tracking_id)
    if not row:
        raise FileNotFoundError(f"No existe seguimiento '{tracking_id}'")
    if row.get("estado_triage") == "publicado":
        raise ValueError("No se puede descartar una investigación ya publicada")

    rows = mark_tracking_discarded(
        rows,
        tracking_id=tracking_id,
        motivo=motivo.strip(),
        titulo=row.get("titulo"),
    )
    save_tracking_rows(rows, tracking_file)

    descartados = json.loads(desc_file.read_text(encoding="utf-8")) if desc_file.exists() else []
    if not any(item.get("id") == tracking_id for item in descartados):
        descartados.append(
            {
                "id": tracking_id,
                "titulo": row.get("titulo") or tracking_id,
                "motivo_exclusion": motivo.strip(),
                "fecha_descarte": today_iso(),
            }
        )
        descartados.sort(key=lambda item: item.get("id") or "")
        write_json_atomic(desc_file, descartados)
    return find_tracking_row(rows, tracking_id=tracking_id) or {}
