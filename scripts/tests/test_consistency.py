#!/usr/bin/env python3
"""Tests de consistencia del registro de seguimiento."""
from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from reconcile_catalog_tracking import build_reconciled  # noqa: E402
from tracking import TRACKING_FIELDS, load_tracking_rows, save_tracking_rows  # noqa: E402
from validate_consistency import validate_consistency  # noqa: E402
from publish_games_public import publish_public_copy  # noqa: E402


class ConsistencyTests(unittest.TestCase):
    def test_reconcile_makes_published_sets_equal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            games = [
                {
                    "id": "juego-a",
                    "titulo": "Juego A",
                    "estado": "publicado",
                    "anio": 2020,
                    "fecha_alta": "2020-01-01",
                },
                {
                    "id": "juego-b",
                    "titulo": "Juego B",
                    "estado": "publicado",
                    "anio": 2021,
                    "fecha_alta": "2021-01-01",
                },
            ]
            games_path = root / "games.json"
            games_path.write_text(json.dumps(games), encoding="utf-8")
            csv_path = root / "raw.csv"
            with csv_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=["titulo", "estado_triage", "url", "nota"],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "titulo": "Juego A alias",
                        "estado_triage": "verificado",
                        "url": "https://example.com/a",
                        "nota": "alias",
                    }
                )
                writer.writerow(
                    {
                        "titulo": "Pendiente X",
                        "estado_triage": "pendiente",
                        "url": "https://example.com/x",
                        "nota": "open",
                    }
                )
            aliases = root / "aliases.json"
            aliases.write_text(
                json.dumps({"title_to_ficha_id": {"Juego A alias": "juego-a"}, "notes": {}}),
                encoding="utf-8",
            )
            descartados = root / "descartados.json"
            descartados.write_text("[]", encoding="utf-8")
            candidates = root / "candidates"
            candidates.mkdir()
            (candidates / "m.json").write_text("[]", encoding="utf-8")

            rows, stats = build_reconciled(
                csv_path=csv_path,
                games_path=games_path,
                descartados_path=descartados,
                candidates_dir=candidates,
                aliases_path=aliases,
            )
            save_tracking_rows(rows, csv_path)
            from tracking import write_descartados

            write_descartados(descartados, stats.get("projected_discards") or [])
            self.assertEqual(stats["published_rows"], 2)
            self.assertEqual(stats["missing_games"], [])
            errors = validate_consistency(
                csv_path=csv_path,
                games_path=games_path,
                public_path=None,
                descartados_path=descartados,
                candidates_dir=candidates,
            )
            self.assertEqual(errors, [])

    def test_discard_parity_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            games_path = root / "games.json"
            games_path.write_text(json.dumps([{"id": "a", "titulo": "A"}]), encoding="utf-8")
            csv_path = root / "raw.csv"
            rows = [{field: "" for field in TRACKING_FIELDS}]
            rows[0].update(
                {
                    "id": "t1",
                    "titulo": "A",
                    "estado_triage": "publicado",
                    "ficha_id": "a",
                }
            )
            rows.append({field: "" for field in TRACKING_FIELDS})
            rows[1].update(
                {
                    "id": "solo-csv",
                    "titulo": "Solo CSV",
                    "estado_triage": "descartado",
                    "motivo_decision": "ruido",
                    "fecha_estado": "2026-01-01",
                }
            )
            save_tracking_rows(rows, csv_path)
            descartados = root / "d.json"
            descartados.write_text("[]", encoding="utf-8")
            candidates = root / "c"
            candidates.mkdir()
            errors = validate_consistency(
                csv_path=csv_path,
                games_path=games_path,
                public_path=None,
                descartados_path=descartados,
                candidates_dir=candidates,
            )
            self.assertTrue(any("ausentes en descartados.json" in error for error in errors))

            from tracking import sync_discards, write_descartados

            synced_rows, projected, _stats = sync_discards(load_tracking_rows(csv_path), [])
            save_tracking_rows(synced_rows, csv_path)
            write_descartados(descartados, projected)
            errors = validate_consistency(
                csv_path=csv_path,
                games_path=games_path,
                public_path=None,
                descartados_path=descartados,
                candidates_dir=candidates,
            )
            self.assertEqual(errors, [])

    def test_duplicate_published_ficha_id_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            games_path = root / "games.json"
            games_path.write_text(
                json.dumps([{"id": "a", "titulo": "A"}, {"id": "b", "titulo": "B"}]),
                encoding="utf-8",
            )
            csv_path = root / "raw.csv"
            rows = [
                {field: "" for field in TRACKING_FIELDS},
                {field: "" for field in TRACKING_FIELDS},
            ]
            rows[0].update({"id": "t1", "titulo": "A", "estado_triage": "publicado", "ficha_id": "a"})
            rows[1].update({"id": "t2", "titulo": "A2", "estado_triage": "publicado", "ficha_id": "a"})
            save_tracking_rows(rows, csv_path)
            descartados = root / "d.json"
            descartados.write_text("[]", encoding="utf-8")
            candidates = root / "c"
            candidates.mkdir()
            errors = validate_consistency(
                csv_path=csv_path,
                games_path=games_path,
                public_path=None,
                descartados_path=descartados,
                candidates_dir=candidates,
            )
            self.assertTrue(any("duplicados" in error for error in errors))

    def test_public_copy_matches(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            games_path = root / "games.json"
            public_path = root / "public" / "data" / "games.json"
            payload = [{"id": "a", "titulo": "A"}]
            games_path.write_text(json.dumps(payload), encoding="utf-8")
            publish_public_copy(games_path=games_path, public_path=public_path)
            self.assertEqual(json.loads(public_path.read_text(encoding="utf-8")), payload)


if __name__ == "__main__":
    unittest.main()
