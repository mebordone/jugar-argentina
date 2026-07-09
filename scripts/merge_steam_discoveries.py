#!/usr/bin/env python3
"""Merge steam_discoveries.json a raw_candidates.csv con triage automático."""
from __future__ import annotations

import csv
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DISCOVERIES = ROOT / "data" / "steam_discoveries.json"
CSV_PATH = ROOT / "data" / "raw_candidates.csv"
GAMES_PATH = ROOT / "data" / "games.json"

FIELDNAMES = [
    "titulo", "anio", "estado_juego", "vinculo_preliminar", "fuente", "url", "nota",
    "estado_triage", "eje_sugerido", "ejes_culturales_sugeridos", "notas_triage",
]

SKIP_TITLE_RE = re.compile(
    r"\b(demo|soundtrack|dlc|pack|skin|bundle|upgrade|expansion|flags?\s+pack|"
    r"content creator|workshop|100 cats|hidden cats|jigsaw)\b",
    re.I,
)

# IDs que el plan incorpora directamente — no duplicar como pendiente genérico
PLANNED_APP_IDS = {
    "3462960", "2324940", "4187700", "1528370", "1885040", "1376960", "3819930",
    "3955730", "4119760", "4806100", "3272390", "3297900", "701380", "1404560",
    "4309130", "2434120", "4568220", "4297760", "4560800", "2121510", "383930",
    "2017210", "2141010", "767390", "690790", "1996050", "1462810", "718410",
}


def normalize_title(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def main() -> int:
    if not DISCOVERIES.exists():
        print("Sin steam_discoveries.json")
        return 1

    discoveries = json.loads(DISCOVERIES.read_text(encoding="utf-8"))
    games = json.loads(GAMES_PATH.read_text(encoding="utf-8"))
    catalog_steam: set[str] = set()
    for g in games:
        for v in (g.get("enlaces") or {}).values():
            if isinstance(v, str) and "/app/" in v:
                m = re.search(r"/app/(\d+)", v)
                if m:
                    catalog_steam.add(m.group(1))

    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8"))) if CSV_PATH.exists() else []
    by_title = {normalize_title(r["titulo"]): r for r in rows if r.get("titulo")}

    added_pendiente = 0
    added_descartado = 0

    for app_id, app in discoveries.get("apps", {}).items():
        if app_id in catalog_steam or app.get("en_catalogo"):
            continue
        if app_id in PLANNED_APP_IDS:
            continue

        title = app.get("titulo", "").strip()
        if not title or normalize_title(title) in by_title:
            continue

        if SKIP_TITLE_RE.search(title):
            estado = "descartado"
            notas = f"steam auto-descartado; terminos: {','.join(app.get('terminos_busqueda', [])[:3])}"
            added_descartado += 1
        else:
            # Solo agregar candidatos con señal argentina fuerte en términos de búsqueda
            strong_terms = {
                "argentina", "malvinas", "falklands", "gaucho", "mate", "yerba mate",
                "tango", "pombero", "independencia", "libertador", "dakar", "ruta 40",
                "peron", "evita", "conurbano", "patagonia", "pampa",
            }
            terms = set(app.get("terminos_busqueda", []))
            if not (terms & strong_terms) and not app.get("jurisdicciones"):
                continue
            estado = "pendiente"
            juris = ";".join(app.get("jurisdicciones", [])[:2])
            notas = f"steam search {','.join(sorted(terms)[:4])}"
            if juris:
                notas += f"; jurisdiccion:{juris}"
            added_pendiente += 1

        row = {
            "titulo": title,
            "anio": "",
            "estado_juego": "publicado",
            "vinculo_preliminar": "escenario",
            "fuente": app.get("url_steam", ""),
            "url": app.get("url_steam", ""),
            "nota": f"Candidato Steam app {app_id}.",
            "estado_triage": estado,
            "eje_sugerido": "escenario",
            "ejes_culturales_sugeridos": "",
            "notas_triage": notas,
        }
        rows.append(row)
        by_title[normalize_title(title)] = row

    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in FIELDNAMES})

    print(f"CSV: +{added_pendiente} pendiente, +{added_descartado} descartado auto")
    print(f"Total filas: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
