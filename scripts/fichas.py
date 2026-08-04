#!/usr/bin/env python3
"""CLI de ciclo de vida editorial: borrador → validación → publicación."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ficha_model import (  # noqa: E402
    CSV_PATH,
    DRAFTS_DIR,
    GAMES_PATH,
    TEMPLATE_IDS,
    apply_template,
    candidate_to_draft,
    discard_tracking_candidate,
    draft_path,
    find_candidate,
    get_draft_meta,
    list_drafts,
    load_draft,
    load_games,
    publish_draft_to_games,
    save_draft,
    set_draft_meta,
    strip_draft_meta,
)
from tracking import (  # noqa: E402
    create_open_tracking_row,
    load_tracking_rows,
    save_tracking_rows,
    upsert_tracking_row,
)
from validate import partition_findings, validate_game  # noqa: E402
from validate_consistency import validate_consistency  # noqa: E402


def _prompt(label: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    if value:
        return value
    return default or ""


def _prompt_list(label: str, default: str = "") -> list[str]:
    raw = _prompt(label, default)
    if not raw:
        return []
    return [part.strip() for part in raw.split(",") if part.strip()]


def _print_findings(findings: list[Any]) -> tuple[int, int]:
    errors, warnings = partition_findings(findings)
    for item in errors:
        print(f" - {item}")
    for item in warnings:
        print(f" - {item}")
    if not findings:
        print(" OK: sin hallazgos")
    return len(errors), len(warnings)


def _ensure_tracking_for_draft(
    ficha: dict[str, Any],
    *,
    csv_path: Path,
    tracking_id: str | None = None,
    origen: str = "cli",
    origen_ref: str = "",
) -> str:
    rows = load_tracking_rows(csv_path)
    existing = {row.get("id") or "" for row in rows}
    meta = get_draft_meta(ficha)
    row_id = tracking_id or meta.get("tracking_id") or ficha["id"]
    if row_id not in existing:
        row = create_open_tracking_row(
            titulo=ficha.get("titulo") or ficha["id"],
            tracking_id=str(row_id),
            origen=origen,
            origen_ref=origen_ref,
            existing_ids=existing,
        )
        rows = upsert_tracking_row(rows, row)
        row_id = row["id"]
        save_tracking_rows(rows, csv_path)
    set_draft_meta(ficha, tracking_id=row_id, ficha_id=ficha["id"])
    return str(row_id)


def cmd_new(args: argparse.Namespace) -> int:
    template = args.template
    if template not in TEMPLATE_IDS:
        print(f"Plantilla inválida '{template}'. Opciones: {', '.join(TEMPLATE_IDS)}", file=sys.stderr)
        return 1

    csv_path = Path(args.csv) if getattr(args, "csv", None) else CSV_PATH
    candidate = None
    if args.candidate:
        candidate = find_candidate(args.candidate, csv_path=csv_path)
        if not candidate:
            print(f"No se encontró el candidato '{args.candidate}'", file=sys.stderr)
            return 1
        ficha = candidate_to_draft(candidate, template=template, id_override=args.id)
        print(f"Candidato importado: {candidate.get('titulo')} ({candidate.get('id') or args.candidate})")
    else:
        titulo = args.titulo or (_prompt("Título") if not args.non_interactive else "")
        if not titulo:
            print("Se necesita --titulo o modo interactivo", file=sys.stderr)
            return 1
        ficha = apply_template(template, titulo, args.id)

    if not args.non_interactive and sys.stdin.isatty():
        ficha["titulo"] = _prompt("Título", ficha.get("titulo") or "")
        ficha["titulo_original"] = ficha["titulo"]
        ficha["desarrollador"] = _prompt("Desarrollador", ficha.get("desarrollador") or "")
        ficha["descripcion"] = _prompt("Descripción (vínculo argentino)", ficha.get("descripcion") or "")
        anio_raw = _prompt("Año (vacío si TBD)", str(ficha["anio"]) if ficha.get("anio") else "")
        ficha["anio"] = int(anio_raw) if anio_raw.isdigit() else None
        ficha["plataformas"] = _prompt_list("Plataformas (coma)", ",".join(ficha.get("plataformas") or ["PC"]))
        ficha["generos"] = _prompt_list("Géneros (coma)", ",".join(ficha.get("generos") or []))
        temas = _prompt_list(
            "Temas de contexto (coma)",
            ",".join((ficha.get("contexto_argentino") or {}).get("temas") or []),
        )
        ficha.setdefault("contexto_argentino", {})
        ficha["contexto_argentino"]["temas"] = temas
        fuentes = _prompt_list(
            "Fuentes / URLs (coma)",
            ",".join(
                [
                    *(
                        [ficha["enlaces"][k]]
                        for k in ("steam", "itch", "web_oficial")
                        if ficha.get("enlaces", {}).get(k)
                    ),
                    *((ficha.get("enlaces") or {}).get("fuentes_investigacion") or []),
                ]
            ),
        )
        if fuentes:
            from ficha_model import guess_link_key

            enlaces: dict[str, Any] = dict(ficha.get("enlaces") or {})
            for url in fuentes:
                key = guess_link_key(url)
                if key not in enlaces:
                    enlaces[key] = url
                else:
                    enlaces.setdefault("fuentes_investigacion", [])
                    if url not in enlaces["fuentes_investigacion"] and url != enlaces.get(key):
                        enlaces["fuentes_investigacion"].append(url)
            ficha["enlaces"] = enlaces
        set_draft_meta(ficha, template=template)

    drafts_dir = Path(args.drafts_dir) if args.drafts_dir else DRAFTS_DIR
    path = draft_path(ficha["id"], drafts_dir)
    if path.exists() and not args.force:
        print(f"Ya existe el borrador {path}. Usá --force para sobrescribir.", file=sys.stderr)
        return 1

    games = load_games(Path(args.games) if args.games else GAMES_PATH)
    if any(game["id"] == ficha["id"] for game in games):
        print(f"El id '{ficha['id']}' ya está publicado en el catálogo.", file=sys.stderr)
        return 1

    tracking_id = _ensure_tracking_for_draft(
        ficha,
        csv_path=csv_path,
        tracking_id=str(get_draft_meta(ficha).get("tracking_id") or "") or None,
        origen="cli" if not candidate else str(candidate.get("_source_kind") or "csv"),
        origen_ref=str((candidate or {}).get("_source_file") or ""),
    )
    saved = save_draft(ficha, drafts_dir)
    print(f"Borrador creado: {saved}")
    print(f"Seguimiento: {tracking_id}")
    findings = validate_game(
        strip_draft_meta(ficha),
        known_ids={game["id"] for game in games},
        strict_draft=True,
    )
    print("Validación inicial:")
    _print_findings(findings)
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    drafts_dir = Path(args.drafts_dir) if args.drafts_dir else DRAFTS_DIR
    ficha = load_draft(args.id, drafts_dir)
    games = load_games(Path(args.games) if args.games else GAMES_PATH)
    findings = validate_game(
        strip_draft_meta(ficha),
        known_ids={game["id"] for game in games},
        strict_draft=True,
    )
    errors, warnings = partition_findings(findings)
    print(f"Borrador {args.id}:")
    _print_findings(findings)
    print(f"{len(errors)} error(es), {len(warnings)} advertencia(s)")
    return 1 if errors else 0


def cmd_show(args: argparse.Namespace) -> int:
    drafts_dir = Path(args.drafts_dir) if args.drafts_dir else DRAFTS_DIR
    ficha = load_draft(args.id, drafts_dir)
    print(json.dumps(ficha, ensure_ascii=False, indent=2))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    drafts_dir = Path(args.drafts_dir) if args.drafts_dir else DRAFTS_DIR
    paths = list_drafts(drafts_dir)
    if not paths:
        print("No hay borradores.")
        return 0
    for path in paths:
        ficha = json.loads(path.read_text(encoding="utf-8"))
        meta = get_draft_meta(ficha)
        template = meta.get("template", "-")
        tracking = meta.get("tracking_id", "-")
        print(f"{ficha.get('id')}\t{ficha.get('titulo')}\ttemplate={template}\ttracking={tracking}")
    return 0


def cmd_publish(args: argparse.Namespace) -> int:
    drafts_dir = Path(args.drafts_dir) if args.drafts_dir else DRAFTS_DIR
    games_path = Path(args.games) if args.games else GAMES_PATH
    csv_path = Path(args.csv) if getattr(args, "csv", None) else CSV_PATH
    ficha = load_draft(args.id, drafts_dir)
    games = load_games(games_path)
    findings = validate_game(
        strip_draft_meta(ficha),
        known_ids={game["id"] for game in games},
        strict_draft=True,
    )
    errors, warnings = partition_findings(findings)
    if errors:
        print("No se puede publicar: hay errores.")
        _print_findings(findings)
        return 1
    if warnings:
        print("Advertencias (no bloquean):")
        for item in warnings:
            print(f" - {item}")

    _ensure_tracking_for_draft(ficha, csv_path=csv_path)
    try:
        published = publish_draft_to_games(
            ficha,
            games_path=games_path,
            drafts_dir=drafts_dir,
            csv_path=csv_path,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    consistency_errors = validate_consistency(
        csv_path=csv_path,
        games_path=games_path,
        require_public=False,
    )
    if consistency_errors:
        print("Publicado con advertencia de consistencia residual:", file=sys.stderr)
        for error in consistency_errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    print(f"Publicado: {published['id']} → {games_path}")
    return 0


def cmd_discard(args: argparse.Namespace) -> int:
    csv_path = Path(args.csv) if getattr(args, "csv", None) else CSV_PATH
    try:
        row = discard_tracking_candidate(
            args.id,
            motivo=args.motivo,
            csv_path=csv_path,
        )
    except (ValueError, FileNotFoundError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Descartado: {row.get('id')} — {row.get('motivo_decision')}")
    return 0


def cmd_track(args: argparse.Namespace) -> int:
    """Alta de investigación abierta en el CSV (sin crear borrador)."""
    from ficha_model import normalize_candidate_status, slugify

    csv_path = Path(args.csv) if getattr(args, "csv", None) else CSV_PATH
    titulo = (args.titulo or "").strip()
    if not titulo:
        print("Indicá --titulo", file=sys.stderr)
        return 1

    estado = normalize_candidate_status(args.estado or "en_revision")
    if estado not in {"candidato", "en_revision"}:
        print("estado debe ser candidato o en_revision", file=sys.stderr)
        return 1

    rows = load_tracking_rows(csv_path)
    existing_ids = {row.get("id") or "" for row in rows}
    tracking_id = (args.id or "").strip() or slugify(titulo)
    url = (args.url or "").strip()

    # Evitar duplicar por id o por URL Steam ya rastreada.
    for row in rows:
        if row.get("id") == tracking_id:
            print(f"Ya existe seguimiento '{tracking_id}' ({row.get('estado_triage')})", file=sys.stderr)
            return 1
        if url and url in (row.get("url") or ""):
            print(
                f"Ya existe URL en '{row.get('id')}' ({row.get('estado_triage')}): {row.get('titulo')}",
                file=sys.stderr,
            )
            return 1

    row = create_open_tracking_row(
        titulo=titulo,
        tracking_id=tracking_id,
        origen=args.origen or "cli",
        origen_ref=args.origen_ref or "",
        existing_ids=existing_ids,
    )
    row["estado_triage"] = estado
    row["url"] = url
    row["fuente"] = (args.fuente or "").strip()
    row["nota"] = (args.nota or "").strip()
    row["vinculo_preliminar"] = (args.vinculo or "").strip()
    row["notas_triage"] = (args.notas_triage or "").strip()
    rows = upsert_tracking_row(rows, row)
    save_tracking_rows(rows, csv_path)
    print(f"Seguimiento abierto: {row['id']} [{estado}] — {titulo}")
    if url:
        print(f"URL: {url}")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """Reporte editorial de seguimiento, huecos y cola abierta."""
    from collections import Counter

    from ficha_model import CANDIDATES_DIR, normalize_candidate_status
    from tracking import (
        DESCARTADOS_PATH,
        PUBLIC_GAMES_PATH,
        discarded_tracking_ids,
        open_tracking_rows,
        published_ficha_ids,
    )

    games_path = Path(args.games) if getattr(args, "games", None) else GAMES_PATH
    csv_path = Path(args.csv) if getattr(args, "csv", None) else CSV_PATH
    drafts_dir = Path(args.drafts_dir) if getattr(args, "drafts_dir", None) else DRAFTS_DIR
    public_path = PUBLIC_GAMES_PATH
    descartados_path = DESCARTADOS_PATH
    candidates_dir = Path(args.candidates_dir) if getattr(args, "candidates_dir", None) else CANDIDATES_DIR
    limit = getattr(args, "limit", 15) or 15

    games = load_games(games_path)
    rows = load_tracking_rows(csv_path)
    drafts = list_drafts(drafts_dir)
    descartados = json.loads(descartados_path.read_text(encoding="utf-8")) if descartados_path.exists() else []

    game_ids = {game["id"] for game in games}
    pub_ids = published_ficha_ids(rows)
    open_rows = open_tracking_rows(rows)
    discard_ids = discarded_tracking_ids(rows)
    desc_json_ids = {item.get("id") for item in descartados if item.get("id")}
    by_estado = Counter(normalize_candidate_status(row.get("estado_triage")) for row in rows)

    sin_portada = sum(1 for g in games if not ((g.get("imagenes") or {}).get("portada")))
    sin_enlace = 0
    for game in games:
        enlaces = game.get("enlaces") or {}
        if not any(
            enlaces.get(key)
            for key in ("steam", "itch", "web_oficial", "descarga", "jugable", "otro")
        ) and not (enlaces.get("fuentes_investigacion") or []):
            sin_enlace += 1

    public_ok = public_path.exists() and public_path.read_text(encoding="utf-8") == games_path.read_text(
        encoding="utf-8"
    )

    print("=== Estado editorial ===")
    print(f"Juegos publicados:     {len(game_ids)}")
    print(f"Filas CSV:             {len(rows)}")
    print(f"  publicado:           {by_estado.get('publicado', 0)}")
    print(f"  en_revision:         {by_estado.get('en_revision', 0)}")
    print(f"  candidato:           {by_estado.get('candidato', 0)}")
    print(f"  descartado:          {by_estado.get('descartado', 0)}")
    print(f"Abiertos (cola):       {len(open_rows)}")
    print(f"Borradores:            {len(drafts)}")
    print(f"Descartes JSON:        {len(desc_json_ids)}")
    print()
    print("=== Invariantes ===")
    print(f"Publicados CSV ↔ games.json: {'OK' if pub_ids == game_ids else 'FALLA'}")
    if pub_ids != game_ids:
        print(f"  faltan en CSV: {', '.join(sorted(game_ids - pub_ids)[:10]) or '—'}")
        print(f"  sobran en CSV: {', '.join(sorted(pub_ids - game_ids)[:10]) or '—'}")
    print(f"Descartes CSV ↔ JSON:        {'OK' if discard_ids == desc_json_ids else 'FALLA'}")
    if discard_ids != desc_json_ids:
        print(f"  solo CSV: {len(discard_ids - desc_json_ids)} | solo JSON: {len(desc_json_ids - discard_ids)}")
    print(f"Copia pública idéntica:      {'OK' if public_ok else 'FALLA / ausente'}")
    print()
    print("=== Huecos del catálogo ===")
    print(f"Sin portada:           {sin_portada}/{len(games)}")
    print(f"Sin enlaces/fuentes:   {sin_enlace}/{len(games)}")
    print()
    if drafts:
        print(f"=== Borradores ({len(drafts)}) ===")
        for draft_id in drafts[:limit]:
            print(f" - {draft_id}")
        if len(drafts) > limit:
            print(f" - … +{len(drafts) - limit} más")
        print()
    print(f"=== Cola abierta (top {min(limit, len(open_rows))}) ===")
    for row in sorted(open_rows, key=lambda item: (item.get("titulo") or "").lower())[:limit]:
        url = (row.get("url") or "").strip()
        suffix = f" | {url}" if url else ""
        print(f" - [{row.get('estado_triage')}] {row.get('id')}: {row.get('titulo')}{suffix}")
    if len(open_rows) > limit:
        print(f" - … +{len(open_rows) - limit} más")

    errors = validate_consistency(
        csv_path=csv_path,
        games_path=games_path,
        public_path=public_path if public_path.exists() else None,
        descartados_path=descartados_path,
        candidates_dir=candidates_dir,
        require_public=False,
    )
    if errors:
        print()
        print("=== Errores de consistencia ===")
        for error in errors[:30]:
            print(f" - {error}")
        if len(errors) > 30:
            print(f" - … +{len(errors) - 30} más")
        return 1
    print()
    print("OK: sin roturas de consistencia")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Administración básica de fichas (Release 3)")
    parser.add_argument("--games", help="Ruta alternativa a games.json")
    parser.add_argument("--drafts-dir", help="Directorio de borradores")
    parser.add_argument("--csv", help="Ruta alternativa al CSV de seguimiento")
    parser.add_argument("--candidates-dir", help="Directorio de manifiestos de candidatos")
    sub = parser.add_subparsers(dest="command", required=True)

    new_p = sub.add_parser("new", help="Crear borrador desde plantilla o candidato")
    new_p.add_argument("--template", required=True, choices=TEMPLATE_IDS)
    new_p.add_argument("--titulo", help="Título de la ficha")
    new_p.add_argument("--id", help="ID forzado")
    new_p.add_argument("--candidate", help="ID o slug de candidato (CSV/JSON)")
    new_p.add_argument("--force", action="store_true", help="Sobrescribir borrador existente")
    new_p.add_argument(
        "--non-interactive",
        action="store_true",
        help="No pedir prompts (útil para scripts/tests)",
    )
    new_p.set_defaults(func=cmd_new)

    val_p = sub.add_parser("validate", help="Validar un borrador")
    val_p.add_argument("id")
    val_p.set_defaults(func=cmd_validate)

    show_p = sub.add_parser("show", help="Mostrar un borrador")
    show_p.add_argument("id")
    show_p.set_defaults(func=cmd_show)

    list_p = sub.add_parser("list", help="Listar borradores")
    list_p.set_defaults(func=cmd_list)

    pub_p = sub.add_parser("publish", help="Publicar un borrador válido")
    pub_p.add_argument("id")
    pub_p.set_defaults(func=cmd_publish)

    disc_p = sub.add_parser("discard", help="Descartar un candidato del registro")
    disc_p.add_argument("id", help="tracking id")
    disc_p.add_argument("--motivo", required=True, help="Motivo editorial del descarte")
    disc_p.set_defaults(func=cmd_discard)

    track_p = sub.add_parser("track", help="Abrir investigación en el CSV sin crear borrador")
    track_p.add_argument("--titulo", required=True, help="Título del candidato")
    track_p.add_argument("--id", help="ID de seguimiento (slug)")
    track_p.add_argument("--url", help="URL de evidencia (Steam, web, etc.)")
    track_p.add_argument("--fuente", help="Fuente de detección")
    track_p.add_argument("--nota", help="Nota editorial breve")
    track_p.add_argument("--vinculo", help="Vínculo preliminar (escenario/protagonista/deporte/...)")
    track_p.add_argument("--notas-triage", dest="notas_triage", help="Notas de triage")
    track_p.add_argument(
        "--estado",
        default="en_revision",
        choices=["candidato", "en_revision"],
        help="Estado abierto (default: en_revision)",
    )
    track_p.add_argument("--origen", default="cli", help="Origen del alta")
    track_p.add_argument("--origen-ref", dest="origen_ref", default="", help="Referencia de origen")
    track_p.set_defaults(func=cmd_track)

    status_p = sub.add_parser("status", help="Reporte editorial de cola, huecos e invariantes")
    status_p.add_argument("--limit", type=int, default=15, help="Máximo de abiertos/borradores a listar")
    status_p.set_defaults(func=cmd_status)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
