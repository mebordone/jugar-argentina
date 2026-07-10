#!/usr/bin/env python3
"""Triage masivo de candidatos Steam en raw_candidates.csv."""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "raw_candidates.csv"
REPORT_PATH = ROOT / "data" / "steam_triage_report.json"
DESCARTADOS_PATH = ROOT / "data" / "descartados.json"
GAMES_PATH = ROOT / "data" / "games.json"
USER_AGENT = "JugarArgentina-Triage/1.0 (+https://github.com/mebordone/jugar-argentina)"
STEAM_APP_RE = re.compile(r"/app/(\d+)")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from steam_triage_rules import (  # noqa: E402
    normalize_title,
    parse_jurisdicciones,
    parse_search_terms,
    score_candidate,
    slugify,
)

FIELDNAMES = [
    "titulo", "anio", "estado_juego", "vinculo_preliminar", "fuente", "url", "nota",
    "estado_triage", "eje_sugerido", "ejes_culturales_sugeridos", "notas_triage",
]


def fetch_appdetails(app_id: str) -> dict | None:
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&l=spanish&cc=ar"
    for attempt in range(4):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                payload = json.load(resp)
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < 3:
                time.sleep(8 * (attempt + 1))
                continue
            return None
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            if attempt < 3:
                time.sleep(3)
                continue
            return None
        entry = payload.get(app_id) or payload.get(str(app_id)) or {}
        if not entry.get("success"):
            return None
        data = entry["data"]
        return {
            "app_id": app_id,
            "name": data.get("name", ""),
            "type": data.get("type", ""),
            "developers": data.get("developers") or [],
            "publishers": data.get("publishers") or [],
            "short_description": data.get("short_description") or "",
            "header_image": data.get("header_image") or data.get("capsule_imagev5"),
            "release_date": (data.get("release_date") or {}).get("date"),
            "is_free": data.get("is_free", False),
        }
    return None


def catalog_steam_ids() -> set[str]:
    ids: set[str] = set()
    if not GAMES_PATH.exists():
        return ids
    for game in json.loads(GAMES_PATH.read_text(encoding="utf-8")):
        for value in (game.get("enlaces") or {}).values():
            if isinstance(value, str):
                m = STEAM_APP_RE.search(value)
                if m:
                    ids.add(m.group(1))
    return ids


def load_report() -> dict:
    if REPORT_PATH.exists():
        return json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    return {"apps": {}, "summary": {}}


def save_report(report: dict) -> None:
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_descartados() -> list[dict]:
    if DESCARTADOS_PATH.exists():
        return json.loads(DESCARTADOS_PATH.read_text(encoding="utf-8"))
    return []


def save_descartados(items: list[dict]) -> None:
    DESCARTADOS_PATH.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def extract_app_id(row: dict) -> str | None:
    for key in ("url", "fuente"):
        value = row.get(key) or ""
        m = STEAM_APP_RE.search(value)
        if m:
            return m.group(1)
    note = row.get("nota") or ""
    m = re.search(r"app (\d+)", note)
    return m.group(1) if m else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    catalog_ids = catalog_steam_ids()
    report = load_report()
    report.setdefault("apps", {})
    descartados = load_descartados()
    descartado_ids = {d["id"] for d in descartados}
    today = str(date.today())

    counts = {"incorporar": 0, "pendiente": 0, "descartado": 0, "skipped": 0}

    for row in rows:
        estado = (row.get("estado_triage") or "").strip()
        if estado not in ("pendiente", "candidato"):
            continue

        app_id = extract_app_id(row)
        if not app_id:
            row["estado_triage"] = "descartado"
            row["notas_triage"] = (row.get("notas_triage") or "") + "; sin app_id Steam"
            counts["descartado"] += 1
            continue

        if app_id in catalog_ids:
            row["estado_triage"] = "verificado"
            counts["skipped"] += 1
            continue

        cache_key = app_id
        if args.resume and cache_key in report["apps"]:
            cached = report["apps"][cache_key]
            bucket = cached["bucket"]
            row["estado_triage"] = "descartado" if bucket == "descartado" else (
                "pendiente" if bucket == "pendiente" else "pendiente"
            )
            if bucket == "incorporar":
                row["estado_triage"] = "pendiente"
                row["notas_triage"] = f"batch7 incorporar; score={cached['score']}; {cached.get('motivo','')}"
            elif bucket == "descartado":
                row["estado_triage"] = "descartado"
                row["notas_triage"] = f"triage: {cached.get('motivo','')}"
            counts[bucket] += 1
            continue

        details = fetch_appdetails(app_id)
        time.sleep(0.4)

        title = row.get("titulo") or (details or {}).get("name", "")
        if details:
            title = details["name"] or title

        if not details:
            score, bucket, motivo = 0, "descartado", "Steam API sin datos"
        else:
            score, bucket, motivo = score_candidate(
                title=title,
                short_description=details["short_description"],
                developers=details["developers"],
                publishers=details["publishers"],
                notas_triage=row.get("notas_triage") or "",
                app_type=details["type"],
            )

        entry = {
            "app_id": app_id,
            "titulo": title,
            "score": score,
            "bucket": bucket,
            "motivo": motivo,
            "header_image": (details or {}).get("header_image"),
            "developers": (details or {}).get("developers", []),
            "short_description": (details or {}).get("short_description", "")[:200],
            "terminos": sorted(parse_search_terms(row.get("notas_triage") or "")),
            "jurisdicciones": parse_jurisdicciones(row.get("notas_triage") or ""),
            "steam_url": f"https://store.steampowered.com/app/{app_id}/",
        }
        report["apps"][app_id] = entry

        if bucket == "incorporar":
            row["estado_triage"] = "pendiente"
            row["notas_triage"] = f"batch7 incorporar; score={score}; {motivo}"
        elif bucket == "pendiente":
            row["estado_triage"] = "pendiente"
            row["notas_triage"] = f"triage pendiente; score={score}; {motivo}"
        else:
            row["estado_triage"] = "descartado"
            row["notas_triage"] = f"triage: {motivo}"
            sid = slugify(title) or f"steam-{app_id}"
            if sid not in descartado_ids:
                descartados.append({
                    "id": sid,
                    "titulo": title,
                    "motivo_exclusion": motivo,
                    "fecha_descarte": today,
                })
                descartado_ids.add(sid)

        counts[bucket] += 1
        if sum(counts.values()) % 20 == 0:
            save_report(report)

    # Build summary buckets
    incorporar = [a for a in report["apps"].values() if a.get("bucket") == "incorporar"]
    report["summary"] = {
        "fecha": today,
        "incorporar": len(incorporar),
        "pendiente": sum(1 for a in report["apps"].values() if a.get("bucket") == "pendiente"),
        "descartado": sum(1 for a in report["apps"].values() if a.get("bucket") == "descartado"),
        "incorporar_list": sorted(incorporar, key=lambda x: -x["score"]),
    }
    save_report(report)
    save_descartados(descartados)

    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in FIELDNAMES})

    print(f"Triage completado: {counts}")
    print(f"Incorporar (batch7): {len(incorporar)}")
    print(f"Reporte: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
