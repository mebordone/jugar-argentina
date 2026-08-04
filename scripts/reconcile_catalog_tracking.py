#!/usr/bin/env python3
"""Reconciliación reproducible del registro de seguimiento editorial."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ficha_model import (  # noqa: E402
    CANDIDATES_DIR,
    CSV_PATH,
    DATA,
    GAMES_PATH,
    load_json_candidates,
    normalize_candidate_status,
    slugify,
)
from tracking import (  # noqa: E402
    ALIASES_PATH,
    DESCARTADOS_PATH,
    TRACKING_FIELDS,
    empty_tracking_row,
    ensure_unique_tracking_id,
    load_tracking_rows,
    save_tracking_rows,
    sync_discards,
    today_iso,
    write_descartados,
)

REPORT_PATH = DATA / "consistency_report.md"


def load_aliases() -> dict[str, Any]:
    if not ALIASES_PATH.exists():
        return {"title_to_ficha_id": {}, "notes": {}}
    return json.loads(ALIASES_PATH.read_text(encoding="utf-8"))


def legacy_csv_rows(path: Path) -> list[dict[str, str]]:
    """Lee el CSV actual tolerando columnas legacy."""
    import csv

    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return [{k: (v or "") for k, v in row.items()} for row in csv.DictReader(handle)]


def resolve_ficha_id(
    titulo: str,
    *,
    games_by_title: dict[str, str],
    game_ids: set[str],
    aliases: dict[str, str],
) -> str | None:
    if titulo in aliases:
        return aliases[titulo]
    key = titulo.strip().lower()
    if key in games_by_title:
        return games_by_title[key]
    slug = slugify(titulo)
    if slug in game_ids:
        return slug
    return None


def build_reconciled(
    *,
    csv_path: Path,
    games_path: Path,
    descartados_path: Path,
    candidates_dir: Path,
    aliases_path: Path,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    aliases_data = json.loads(aliases_path.read_text(encoding="utf-8")) if aliases_path.exists() else {}
    aliases = dict(aliases_data.get("title_to_ficha_id") or {})
    games = json.loads(games_path.read_text(encoding="utf-8"))
    descartados = json.loads(descartados_path.read_text(encoding="utf-8"))
    game_ids = {game["id"] for game in games}
    games_by_title = {(game.get("titulo") or "").strip().lower(): game["id"] for game in games}
    desc_by_title = {(item.get("titulo") or "").strip().lower(): item for item in descartados}
    desc_by_id = {item["id"]: item for item in descartados}

    raw_rows = legacy_csv_rows(csv_path)
    existing_ids: set[str] = set()
    rows: list[dict[str, str]] = []
    covered_fichas: set[str] = set()
    stats = {
        "raw_rows": len(raw_rows),
        "normalized_states": Counter(),
        "alias_links": 0,
        "alias_duplicates": 0,
        "backfilled_games": 0,
        "imported_manifests": 0,
        "descartes_with_motivo": 0,
        "descartes_without_motivo": 0,
        "descartes_backfilled_from_json": 0,
        "exceptions": [],
    }

    for raw in raw_rows:
        titulo = (raw.get("titulo") or "").strip()
        estado = normalize_candidate_status(raw.get("estado_triage"))
        stats["normalized_states"][estado] += 1
        base_id = (raw.get("id") or "").strip() or slugify(titulo) or "sin-titulo"
        tracking_id = ensure_unique_tracking_id(base_id, existing_ids)

        ficha_id = ""
        motivo = (raw.get("motivo_decision") or "").strip()
        nota = (raw.get("nota") or "").strip()
        notas_triage = (raw.get("notas_triage") or "").strip()
        if estado == "publicado":
            existing_ficha = (raw.get("ficha_id") or "").strip()
            resolved = (
                existing_ficha
                if existing_ficha in game_ids
                else resolve_ficha_id(
                    titulo,
                    games_by_title=games_by_title,
                    game_ids=game_ids,
                    aliases=aliases,
                )
            )
            if resolved:
                if resolved in covered_fichas:
                    # Una sola fila publicada por ficha_id.
                    estado = "en_revision"
                    stats["alias_duplicates"] += 1
                    extra = f"Alias/duplicado de seguimiento hacia ficha publicada `{resolved}`."
                    notas_triage = f"{notas_triage}; {extra}".strip("; ").strip()
                    if titulo in aliases:
                        stats["alias_links"] += 1
                else:
                    ficha_id = resolved
                    covered_fichas.add(resolved)
                    if titulo in aliases:
                        stats["alias_links"] += 1
            else:
                stats["exceptions"].append(f"publicado sin ficha: {titulo}")
                estado = "en_revision"
        elif estado == "descartado":
            desc = desc_by_title.get(titulo.lower()) or desc_by_id.get(slugify(titulo))
            if desc and desc.get("motivo_exclusion"):
                motivo = motivo or str(desc["motivo_exclusion"])
            if not motivo:
                motivo = (
                    notas_triage
                    or nota
                    or (raw.get("fuente") or "").strip()
                )
            if motivo:
                stats["descartes_with_motivo"] += 1
            else:
                stats["descartes_without_motivo"] += 1
                stats["exceptions"].append(f"descartado sin motivo: {titulo}")
                motivo = "Descarte histórico sin motivo documentado en la fuente original."

        rows.append(
            empty_tracking_row(
                id=tracking_id,
                titulo=titulo,
                anio=raw.get("anio") or "",
                estado_juego=raw.get("estado_juego") or "",
                vinculo_preliminar=raw.get("vinculo_preliminar") or "",
                fuente=raw.get("fuente") or "",
                url=raw.get("url") or "",
                nota=nota,
                estado_triage=estado,
                ficha_id=ficha_id if estado == "publicado" else "",
                origen="csv_legacy",
                origen_ref="",
                fecha_estado=today_iso(),
                motivo_decision=motivo if estado == "descartado" else "",
                eje_sugerido=raw.get("eje_sugerido") or "",
                ejes_culturales_sugeridos=raw.get("ejes_culturales_sugeridos") or "",
                notas_triage=notas_triage,
            )
        )

    for game in sorted(games, key=lambda item: item["id"]):
        if game["id"] in covered_fichas:
            continue
        tracking_id = ensure_unique_tracking_id(game["id"], existing_ids)
        rows.append(
            empty_tracking_row(
                id=tracking_id,
                titulo=game.get("titulo") or game["id"],
                anio="" if game.get("anio") is None else str(game.get("anio")),
                estado_juego=game.get("estado") or "",
                estado_triage="publicado",
                ficha_id=game["id"],
                origen="catalog_backfill",
                origen_ref="data/games.json",
                fecha_estado=str(game.get("fecha_alta") or today_iso())[:10],
                nota="Alta histórica reconciliada desde games.json",
            )
        )
        stats["backfilled_games"] += 1
        covered_fichas.add(game["id"])

    # Importar manifiestos JSON no cubiertos por título/id.
    titles = {(row.get("titulo") or "").strip().lower() for row in rows}
    ids = {row.get("id") for row in rows}
    for item in load_json_candidates(candidates_dir):
        titulo = str(item.get("titulo") or "").strip()
        item_id = str(item.get("id") or slugify(titulo) or "")
        if not titulo:
            continue
        if titulo.lower() in titles or item_id in ids or item_id in existing_ids:
            # Vincular origen_ref si ya existe fila abierta/publicada con mismo id/título.
            for row in rows:
                if row.get("id") == item_id or (row.get("titulo") or "").strip().lower() == titulo.lower():
                    if not row.get("origen_ref"):
                        row["origen"] = row.get("origen") or "manifest"
                        row["origen_ref"] = str(item.get("_source_file") or "")
                    break
            continue
        tracking_id = ensure_unique_tracking_id(item_id or slugify(titulo), existing_ids)
        estado_raw = item.get("estado_analisis") or item.get("estado") or "candidato"
        estado = normalize_candidate_status(str(estado_raw))
        if estado == "publicado" and item_id in game_ids:
            ficha_id = item_id
        elif estado == "publicado":
            estado = "en_revision"
            ficha_id = ""
        else:
            ficha_id = ""
        rows.append(
            empty_tracking_row(
                id=tracking_id,
                titulo=titulo,
                url=str(item.get("url") or ""),
                fuente=";".join(item.get("fuentes") or []) if isinstance(item.get("fuentes"), list) else str(item.get("fuente") or ""),
                nota=str(item.get("vinculo_argentino") or item.get("nota") or ""),
                estado_triage=estado if estado != "publicado" else "en_revision",
                ficha_id=ficha_id,
                origen="manifest",
                origen_ref=str(item.get("_source_file") or ""),
                fecha_estado=today_iso(),
            )
        )
        stats["imported_manifests"] += 1
        titles.add(titulo.lower())
        ids.add(tracking_id)

    # Asegurar que cada descarte documentado tenga fila de seguimiento.
    tracking_titles = {(row.get("titulo") or "").strip().lower() for row in rows}
    tracking_ids = {row.get("id") for row in rows}
    for item in descartados:
        titulo = (item.get("titulo") or "").strip()
        item_id = item.get("id") or slugify(titulo)
        if titulo.lower() in tracking_titles or item_id in tracking_ids:
            for row in rows:
                if row.get("id") == item_id or (row.get("titulo") or "").strip().lower() == titulo.lower():
                    if row.get("estado_triage") != "descartado":
                        # No forzar descarte sobre publicados.
                        if row.get("estado_triage") == "publicado":
                            stats["exceptions"].append(
                                f"descartado.json choca con publicado: {titulo} ({item_id})"
                            )
                        else:
                            row["estado_triage"] = "descartado"
                            row["ficha_id"] = ""
                            row["motivo_decision"] = item.get("motivo_exclusion") or row.get("motivo_decision")
                            row["fecha_estado"] = str(item.get("fecha_descarte") or today_iso())
                    elif not row.get("motivo_decision"):
                        row["motivo_decision"] = item.get("motivo_exclusion") or ""
                    break
            continue
        tracking_id = ensure_unique_tracking_id(item_id, existing_ids)
        rows.append(
            empty_tracking_row(
                id=tracking_id,
                titulo=titulo,
                estado_triage="descartado",
                origen="descartados_json",
                origen_ref="data/descartados.json",
                motivo_decision=item.get("motivo_exclusion") or "Descarte documentado",
                fecha_estado=str(item.get("fecha_descarte") or today_iso()),
            )
        )
        stats["descartes_backfilled_from_json"] += 1

    rows, projected_discards, discard_stats = sync_discards(
        rows, descartados, game_ids=game_ids
    )
    stats["discards_imported_to_csv"] = discard_stats["imported_to_csv"]
    stats["discards_materialized_to_json"] = discard_stats["materialized_to_json"]
    stats["discards_projected_total"] = discard_stats["discarded_total"]
    stats["discards_renamed_collisions"] = discard_stats["renamed_collisions"]
    stats["projected_discards"] = projected_discards

    published = {
        row["ficha_id"]
        for row in rows
        if row.get("estado_triage") == "publicado" and row.get("ficha_id")
    }
    stats["published_rows"] = len(published)
    stats["games"] = len(game_ids)
    stats["missing_games"] = sorted(game_ids - published)
    stats["orphan_published_rows"] = sorted(published - game_ids)
    stats["state_counts"] = dict(Counter(row.get("estado_triage") for row in rows))
    stats["published_row_count"] = sum(1 for row in rows if row.get("estado_triage") == "publicado")
    return rows, stats


def render_report(stats: dict[str, Any]) -> str:
    lines = [
        "# Consistency report",
        "",
        f"Generado: {today_iso()}",
        "",
        "## Conteos",
        "",
        f"- Filas CSV crudas: {stats.get('raw_rows')}",
        f"- Juegos en games.json: {stats.get('games')}",
        f"- Filas publicadas con ficha_id: {stats.get('published_rows')}",
        f"- Filas con estado publicado: {stats.get('published_row_count')}",
        f"- Backfill desde catálogo: {stats.get('backfilled_games')}",
        f"- Alias aplicados: {stats.get('alias_links')}",
        f"- Alias/duplicados despromovidos: {stats.get('alias_duplicates')}",
        f"- Manifiestos importados: {stats.get('imported_manifests')}",
        f"- Descartes backfill desde JSON: {stats.get('descartes_backfilled_from_json')}",
        f"- Descartes importados a CSV (sync): {stats.get('discards_imported_to_csv')}",
        f"- Descartes materializados a JSON (sync): {stats.get('discards_materialized_to_json')}",
        f"- Descartes proyectados (paridad): {stats.get('discards_projected_total')}",
        f"- Descartes con motivo: {stats.get('descartes_with_motivo')}",
        f"- Descartes sin motivo (completados con fallback): {stats.get('descartes_without_motivo')}",
        "",
        "## Estados canónicos",
        "",
    ]
    for key, value in sorted((stats.get("state_counts") or {}).items()):
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Excepciones", ""])
    exceptions = stats.get("exceptions") or []
    missing = stats.get("missing_games") or []
    orphans = stats.get("orphan_published_rows") or []
    if not exceptions and not missing and not orphans:
        lines.append("- Ninguna.")
    else:
        for item in exceptions:
            lines.append(f"- {item}")
        if missing:
            lines.append(f"- Fichas sin fila publicada: {', '.join(missing)}")
        if orphans:
            lines.append(f"- Filas publicadas huérfanas: {', '.join(orphans)}")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Reconciliar CSV de seguimiento con el catálogo")
    parser.add_argument("--check", action="store_true", help="Solo reportar, no escribir")
    parser.add_argument("--apply", action="store_true", help="Aplicar migración al CSV")
    parser.add_argument("--csv", type=Path, default=CSV_PATH)
    parser.add_argument("--games", type=Path, default=GAMES_PATH)
    parser.add_argument("--descartados", type=Path, default=DESCARTADOS_PATH)
    parser.add_argument("--candidates-dir", type=Path, default=CANDIDATES_DIR)
    parser.add_argument("--aliases", type=Path, default=ALIASES_PATH)
    parser.add_argument("--report", type=Path, default=REPORT_PATH)
    args = parser.parse_args(argv)

    if not args.check and not args.apply:
        parser.error("Indicá --check o --apply")

    rows, stats = build_reconciled(
        csv_path=args.csv,
        games_path=args.games,
        descartados_path=args.descartados,
        candidates_dir=args.candidates_dir,
        aliases_path=args.aliases,
    )
    report = render_report(stats)
    print(report)
    if args.apply:
        save_tracking_rows(rows, args.csv)
        write_descartados(args.descartados, stats.get("projected_discards") or [])
        args.report.write_text(report, encoding="utf-8")
        print(f"CSV actualizado: {args.csv}")
        print(f"Descartes sincronizados: {args.descartados}")
        print(f"Reporte: {args.report}")
    ok = (
        not stats.get("missing_games")
        and not stats.get("orphan_published_rows")
        and stats.get("published_rows") == stats.get("games")
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
