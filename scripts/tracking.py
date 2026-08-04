#!/usr/bin/env python3
"""Registro maestro de seguimiento editorial (CSV)."""
from __future__ import annotations

import csv
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Any

from ficha_model import (
    CANONICAL_CANDIDATE_STATES,
    CSV_PATH,
    DATA,
    OPEN_CANDIDATE_STATES,
    normalize_candidate_status,
    slugify,
    write_json_atomic,
)

TRACKING_FIELDS = [
    "id",
    "titulo",
    "anio",
    "estado_juego",
    "vinculo_preliminar",
    "fuente",
    "url",
    "nota",
    "estado_triage",
    "ficha_id",
    "origen",
    "origen_ref",
    "fecha_estado",
    "motivo_decision",
    "eje_sugerido",
    "ejes_culturales_sugeridos",
    "notas_triage",
]

ALIASES_PATH = DATA / "tracking_aliases.json"
DESCARTADOS_PATH = DATA / "descartados.json"
PUBLIC_GAMES_PATH = DATA.parent / "public" / "data" / "games.json"


def today_iso() -> str:
    return str(date.today())


def empty_tracking_row(**overrides: Any) -> dict[str, str]:
    row = {field: "" for field in TRACKING_FIELDS}
    row.update({k: "" if v is None else str(v) for k, v in overrides.items()})
    return row


def load_tracking_rows(path: Path | None = None) -> list[dict[str, str]]:
    target = path or CSV_PATH
    if not target.exists():
        return []
    with target.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows: list[dict[str, str]] = []
        for raw in reader:
            row = empty_tracking_row()
            for key, value in (raw or {}).items():
                if key in row:
                    row[key] = "" if value is None else str(value)
            # Compatibilidad: filas legacy sin id/estado canónico.
            if not row.get("id"):
                base = slugify(row.get("titulo") or "") or "sin-titulo"
                row["id"] = base
            row["estado_triage"] = normalize_candidate_status(row.get("estado_triage"))
            rows.append(row)
        return rows


def save_tracking_rows(rows: list[dict[str, str]], path: Path | None = None) -> None:
    target = path or CSV_PATH
    normalized: list[dict[str, str]] = []
    for raw in rows:
        row = empty_tracking_row()
        for key in TRACKING_FIELDS:
            row[key] = str(raw.get(key) or "")
        row["estado_triage"] = normalize_candidate_status(row.get("estado_triage"))
        normalized.append(row)

    def sort_key(item: dict[str, str]) -> tuple[str, str, str]:
        return (
            item.get("estado_triage") or "",
            item.get("titulo", "").lower(),
            item.get("id") or "",
        )

    normalized.sort(key=sort_key)
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=TRACKING_FIELDS)
        writer.writeheader()
        writer.writerows(normalized)
    tmp.replace(target)


def ensure_unique_tracking_id(base: str, existing: set[str]) -> str:
    candidate = base or "tracking"
    if candidate not in existing:
        existing.add(candidate)
        return candidate
    index = 2
    while f"{candidate}-{index}" in existing:
        index += 1
    value = f"{candidate}-{index}"
    existing.add(value)
    return value


def find_tracking_row(
    rows: list[dict[str, str]],
    *,
    tracking_id: str | None = None,
    ficha_id: str | None = None,
    titulo: str | None = None,
) -> dict[str, str] | None:
    if tracking_id:
        for row in rows:
            if row.get("id") == tracking_id:
                return row
    if ficha_id:
        for row in rows:
            if row.get("ficha_id") == ficha_id:
                return row
    if titulo:
        key = titulo.strip().lower()
        for row in rows:
            if (row.get("titulo") or "").strip().lower() == key:
                return row
    return None


def upsert_tracking_row(rows: list[dict[str, str]], new_row: dict[str, str]) -> list[dict[str, str]]:
    out = [deepcopy(row) for row in rows]
    tracking_id = new_row.get("id") or ""
    for index, row in enumerate(out):
        if row.get("id") == tracking_id:
            merged = empty_tracking_row()
            merged.update(row)
            merged.update({k: str(v) for k, v in new_row.items() if v is not None})
            out[index] = merged
            return out
    row = empty_tracking_row()
    row.update({k: str(v) for k, v in new_row.items() if v is not None})
    out.append(row)
    return out


def published_ficha_ids(rows: list[dict[str, str]]) -> set[str]:
    return {
        row["ficha_id"]
        for row in rows
        if normalize_candidate_status(row.get("estado_triage")) == "publicado" and row.get("ficha_id")
    }


def open_tracking_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        row
        for row in rows
        if normalize_candidate_status(row.get("estado_triage")) in OPEN_CANDIDATE_STATES
    ]


def mark_tracking_published(
    rows: list[dict[str, str]],
    *,
    tracking_id: str,
    ficha_id: str,
    titulo: str | None = None,
) -> list[dict[str, str]]:
    found = False
    out: list[dict[str, str]] = []
    for row in rows:
        item = deepcopy(row)
        if item.get("id") == tracking_id:
            item["estado_triage"] = "publicado"
            item["ficha_id"] = ficha_id
            item["fecha_estado"] = today_iso()
            if titulo:
                item["titulo"] = titulo
            found = True
        out.append(item)
    if not found:
        out.append(
            empty_tracking_row(
                id=tracking_id,
                titulo=titulo or ficha_id,
                estado_triage="publicado",
                ficha_id=ficha_id,
                origen="cli",
                fecha_estado=today_iso(),
            )
        )
    return out


def mark_tracking_discarded(
    rows: list[dict[str, str]],
    *,
    tracking_id: str,
    motivo: str,
    titulo: str | None = None,
) -> list[dict[str, str]]:
    found = False
    out: list[dict[str, str]] = []
    for row in rows:
        item = deepcopy(row)
        if item.get("id") == tracking_id:
            item["estado_triage"] = "descartado"
            item["ficha_id"] = ""
            item["motivo_decision"] = motivo
            item["fecha_estado"] = today_iso()
            if titulo:
                item["titulo"] = titulo
            found = True
        out.append(item)
    if not found:
        out.append(
            empty_tracking_row(
                id=tracking_id,
                titulo=titulo or tracking_id,
                estado_triage="descartado",
                origen="cli",
                motivo_decision=motivo,
                fecha_estado=today_iso(),
            )
        )
    return out


def create_open_tracking_row(
    *,
    titulo: str,
    tracking_id: str | None = None,
    origen: str = "cli",
    origen_ref: str = "",
    existing_ids: set[str] | None = None,
) -> dict[str, str]:
    ids = existing_ids if existing_ids is not None else set()
    base = tracking_id or slugify(titulo) or "candidato"
    row_id = ensure_unique_tracking_id(base, ids)
    return empty_tracking_row(
        id=row_id,
        titulo=titulo,
        estado_triage="en_revision",
        origen=origen,
        origen_ref=origen_ref,
        fecha_estado=today_iso(),
    )


def discarded_tracking_ids(rows: list[dict[str, str]]) -> set[str]:
    return {
        row["id"]
        for row in rows
        if normalize_candidate_status(row.get("estado_triage")) == "descartado" and row.get("id")
    }


def discard_entry_from_row(row: dict[str, str]) -> dict[str, str]:
    return {
        "id": row.get("id") or "",
        "titulo": row.get("titulo") or row.get("id") or "",
        "motivo_exclusion": (row.get("motivo_decision") or "").strip() or "Descarte documentado",
        "fecha_descarte": (row.get("fecha_estado") or "").strip() or today_iso(),
    }


def sync_discards(
    rows: list[dict[str, str]],
    descartados: list[dict[str, Any]],
    *,
    game_ids: set[str] | None = None,
) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, int]]:
    """Alinea CSV descartado ↔ descartados.json (proyección 1:1 por id)."""
    published_ids = game_ids or set()
    out_rows = [deepcopy(row) for row in rows]
    by_id = {row.get("id"): row for row in out_rows if row.get("id")}
    existing_ids = set(by_id)
    json_by_id = {item.get("id"): item for item in descartados if item.get("id")}

    # Evitar que un tracking descartado reuse el id de una ficha publicada.
    renamed = 0
    for row in out_rows:
        if normalize_candidate_status(row.get("estado_triage")) != "descartado":
            continue
        rid = row.get("id") or ""
        if rid and rid in published_ids:
            new_id = ensure_unique_tracking_id(f"{rid}-descartado", existing_ids)
            old_id = rid
            row["id"] = new_id
            if old_id in by_id:
                del by_id[old_id]
            by_id[new_id] = row
            if old_id in json_by_id and new_id not in json_by_id:
                item = dict(json_by_id[old_id])
                item["id"] = new_id
                json_by_id[new_id] = item
                del json_by_id[old_id]
            renamed += 1

    imported_to_csv = 0
    for item_id, item in list(json_by_id.items()):
        # Si el id del JSON choca con una ficha publicada, renombrar al importar.
        target_id = item_id
        if target_id in published_ids:
            target_id = ensure_unique_tracking_id(f"{item_id}-descartado", existing_ids)
            item = dict(item)
            item["id"] = target_id
            json_by_id[target_id] = item
            if item_id in json_by_id and item_id != target_id:
                del json_by_id[item_id]
            renamed += 1

        row = by_id.get(target_id)
        motivo = (item.get("motivo_exclusion") or "").strip() or "Descarte documentado"
        fecha = str(item.get("fecha_descarte") or today_iso())
        titulo = (item.get("titulo") or target_id).strip()
        if row is None:
            # Evitar duplicar por título si ya hay un descartado equivalente.
            existing = next(
                (
                    r
                    for r in out_rows
                    if normalize_candidate_status(r.get("estado_triage")) == "descartado"
                    and (r.get("titulo") or "").strip().lower() == titulo.lower()
                ),
                None,
            )
            if existing:
                if not (existing.get("motivo_decision") or "").strip():
                    existing["motivo_decision"] = motivo
                continue
            tracking_id = ensure_unique_tracking_id(target_id, existing_ids)
            new_row = empty_tracking_row(
                id=tracking_id,
                titulo=titulo,
                estado_triage="descartado",
                origen="descartados_json",
                origen_ref="data/descartados.json",
                motivo_decision=motivo,
                fecha_estado=fecha,
            )
            out_rows.append(new_row)
            by_id[tracking_id] = new_row
            imported_to_csv += 1
            continue
        estado = normalize_candidate_status(row.get("estado_triage"))
        if estado == "publicado":
            continue
        if estado != "descartado":
            row["estado_triage"] = "descartado"
            row["ficha_id"] = ""
            row["motivo_decision"] = motivo or row.get("motivo_decision") or ""
            row["fecha_estado"] = fecha
        elif not (row.get("motivo_decision") or "").strip():
            row["motivo_decision"] = motivo

    projected: list[dict[str, str]] = []
    materialized = 0
    projected_ids: set[str] = set()
    for row in out_rows:
        if normalize_candidate_status(row.get("estado_triage")) != "descartado":
            continue
        rid = row.get("id") or ""
        if not rid or rid in projected_ids:
            continue
        if not (row.get("motivo_decision") or "").strip():
            row["motivo_decision"] = "Descarte documentado"
        entry = discard_entry_from_row(row)
        if rid not in {item.get("id") for item in descartados}:
            materialized += 1
        projected.append(entry)
        projected_ids.add(rid)
    projected.sort(key=lambda item: item.get("id") or "")

    stats = {
        "imported_to_csv": imported_to_csv,
        "materialized_to_json": materialized,
        "discarded_total": len(projected),
        "renamed_collisions": renamed,
    }
    return out_rows, projected, stats


def write_descartados(path: Path, items: list[dict[str, str]]) -> None:
    write_json_atomic(path, items)


__all__ = [
    "ALIASES_PATH",
    "CANONICAL_CANDIDATE_STATES",
    "DESCARTADOS_PATH",
    "OPEN_CANDIDATE_STATES",
    "PUBLIC_GAMES_PATH",
    "TRACKING_FIELDS",
    "create_open_tracking_row",
    "discard_entry_from_row",
    "discarded_tracking_ids",
    "empty_tracking_row",
    "ensure_unique_tracking_id",
    "find_tracking_row",
    "load_tracking_rows",
    "mark_tracking_discarded",
    "mark_tracking_published",
    "open_tracking_rows",
    "published_ficha_ids",
    "save_tracking_rows",
    "sync_discards",
    "today_iso",
    "upsert_tracking_row",
    "write_descartados",
    "write_json_atomic",
]
