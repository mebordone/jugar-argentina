#!/usr/bin/env python3
"""Tests del flujo editorial de fichas (Release 3 + consistencia)."""
from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from ficha_model import (  # noqa: E402
    TEMPLATE_IDS,
    apply_template,
    candidate_to_draft,
    find_candidate,
    is_open_candidate_status,
    load_draft,
    normalize_candidate_status,
    publish_draft_to_games,
    save_draft,
    slugify,
    strip_draft_meta,
)
from tracking import empty_tracking_row, save_tracking_rows  # noqa: E402
from validate import partition_findings, validate_game  # noqa: E402
from validate_consistency import validate_consistency  # noqa: E402
import fichas  # noqa: E402


def _complete_draft(ficha: dict, *, titulo: str = "Juego Test") -> dict:
    ficha["titulo"] = titulo
    ficha["desarrollador"] = "Estudio Test"
    ficha["descripcion"] = (
        "Obra de prueba con vínculo argentino explícito en el escenario "
        "y evidencia mínima para validar el pipeline editorial."
    )
    ficha["plataformas"] = ["PC"]
    ficha["generos"] = ["aventura"]
    ficha["ejes_culturales"] = ["geografia"]
    ficha["contexto_argentino"] = {
        "regiones": ["Patagonia"],
        "provincias": ["Neuquén"],
        "periodo_historico": ["contemporaneo"],
        "temas": ["geografia"],
    }
    ficha["enlaces"] = {
        "itch": "https://example.itch.io/juego-test",
        "fuentes_investigacion": ["https://example.com/fuente"],
    }
    ficha["disponibilidad"] = "gratis"
    ficha["imagenes"] = {
        "portada": "https://example.com/cover.jpg",
        "capturas": ["https://example.com/shot.jpg"],
    }
    return ficha


class FichaModelTests(unittest.TestCase):
    def test_slugify_and_templates(self):
        self.assertEqual(slugify("Paleonto RUN!"), "paleonto-run")
        for template in TEMPLATE_IDS:
            ficha = apply_template(template, "Título de Prueba")
            self.assertEqual(ficha["id"], "titulo-de-prueba")
            active = sum(
                1
                for key in ("escenario", "protagonista", "deporte_argentino")
                if ficha["vinculo_argentina"][key]["activo"]
            )
            self.assertGreaterEqual(active, 1)

    def test_normalize_candidate_status(self):
        self.assertEqual(normalize_candidate_status("pendiente"), "en_revision")
        self.assertEqual(normalize_candidate_status("verificado"), "publicado")
        self.assertEqual(normalize_candidate_status("publicado"), "publicado")
        self.assertTrue(is_open_candidate_status("en_revision"))
        self.assertFalse(is_open_candidate_status("descartado"))


class ValidationTests(unittest.TestCase):
    def test_errors_and_warnings(self):
        incomplete = apply_template("escenario", "Hueco")
        findings = validate_game(strip_draft_meta(incomplete), known_ids=set(), strict_draft=True)
        errors, _warnings = partition_findings(findings)
        self.assertTrue(any("desarrollador" in e.message for e in errors))
        self.assertTrue(any("evidencia" in e.message for e in errors))

        complete = _complete_draft(apply_template("escenario", "Completo"))
        findings = validate_game(strip_draft_meta(complete), known_ids={"otro"}, strict_draft=True)
        errors, _warnings = partition_findings(findings)
        self.assertEqual(errors, [])

    def test_duplicate_id(self):
        ficha = _complete_draft(apply_template("central", "Dup"))
        findings = validate_game(strip_draft_meta(ficha), known_ids={"dup"})
        errors, _ = partition_findings(findings)
        self.assertTrue(any("ya existe" in e.message for e in errors))


class PublishFlowTests(unittest.TestCase):
    def test_draft_to_publish_and_sync(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            drafts = root / "drafts"
            drafts.mkdir()
            games_path = root / "games.json"
            games_path.write_text("[]\n", encoding="utf-8")
            csv_path = root / "raw_candidates.csv"
            save_tracking_rows(
                [
                    empty_tracking_row(
                        id="paleontorun",
                        titulo="PaleontoRUN",
                        estado_triage="en_revision",
                        origen="test",
                    )
                ],
                csv_path,
            )
            candidates_dir = root / "candidates"
            candidates_dir.mkdir()
            (candidates_dir / "recorridos_release2.json").write_text(
                json.dumps(
                    [
                        {
                            "id": "paleontorun",
                            "titulo": "PaleontoRUN",
                            "estado_analisis": "alta",
                            "decision": "publicar",
                        }
                    ]
                ),
                encoding="utf-8",
            )
            descartados = root / "descartados.json"
            descartados.write_text("[]\n", encoding="utf-8")

            ficha = _complete_draft(
                apply_template("escenario", "PaleontoRUN", "paleontorun"),
                titulo="PaleontoRUN",
            )
            ficha["_ficha_draft"] = {
                "template": "escenario",
                "tracking_id": "paleontorun",
                "candidate_id": "paleontorun",
                "candidate_file": "recorridos_release2.json",
                "candidate_source": "json",
            }
            save_draft(ficha, drafts)

            published = publish_draft_to_games(
                load_draft("paleontorun", drafts),
                games_path=games_path,
                drafts_dir=drafts,
                csv_path=csv_path,
                candidates_dir=candidates_dir,
                public_path=root / "public" / "data" / "games.json",
                descartados_path=descartados,
            )
            self.assertTrue(published["verificado"])
            games = json.loads(games_path.read_text(encoding="utf-8"))
            self.assertEqual(len(games), 1)
            self.assertFalse((drafts / "paleontorun.json").exists())

            rows = load_tracking_rows(csv_path) if False else None
            from tracking import load_tracking_rows as load_rows

            rows = load_rows(csv_path)
            published_rows = [row for row in rows if row["estado_triage"] == "publicado"]
            self.assertEqual(len(published_rows), 1)
            self.assertEqual(published_rows[0]["ficha_id"], "paleontorun")

            payload = json.loads(
                (candidates_dir / "recorridos_release2.json").read_text(encoding="utf-8")
            )
            self.assertEqual(payload[0]["estado_analisis"], "publicado")

            errors = validate_consistency(
                csv_path=csv_path,
                games_path=games_path,
                public_path=root / "public" / "data" / "games.json",
                descartados_path=descartados,
                candidates_dir=candidates_dir,
                require_public=True,
            )
            self.assertEqual(errors, [])

    def test_cli_new_creates_tracking_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            drafts = root / "drafts"
            drafts.mkdir()
            games_path = root / "games.json"
            games_path.write_text("[]\n", encoding="utf-8")
            csv_path = root / "raw_candidates.csv"
            save_tracking_rows([], csv_path)
            code = fichas.main(
                [
                    "--games",
                    str(games_path),
                    "--drafts-dir",
                    str(drafts),
                    "--csv",
                    str(csv_path),
                    "new",
                    "--template",
                    "educativo",
                    "--titulo",
                    "Mapa Escolar",
                    "--non-interactive",
                ]
            )
            self.assertEqual(code, 0)
            self.assertTrue((drafts / "mapa-escolar.json").exists())
            from tracking import load_tracking_rows as load_rows

            rows = load_rows(csv_path)
            self.assertTrue(any(row["id"] == "mapa-escolar" for row in rows))

    def test_cli_discard(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            csv_path = root / "raw_candidates.csv"
            save_tracking_rows(
                [
                    empty_tracking_row(
                        id="cand-1",
                        titulo="Candidato Uno",
                        estado_triage="en_revision",
                    )
                ],
                csv_path,
            )
            descartados = root / "descartados.json"
            # monkeypatch path via discard_tracking_candidate arg
            from ficha_model import discard_tracking_candidate

            row = discard_tracking_candidate(
                "cand-1",
                motivo="Sin vínculo argentino verificable",
                csv_path=csv_path,
                descartados_path=descartados,
            )
            self.assertEqual(row["estado_triage"], "descartado")
            payload = json.loads(descartados.read_text(encoding="utf-8"))
            self.assertEqual(payload[0]["id"], "cand-1")

    def test_cli_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            games_path = root / "games.json"
            games_path.write_text(
                json.dumps([{"id": "a", "titulo": "A", "imagenes": {"portada": None}, "enlaces": {}}]),
                encoding="utf-8",
            )
            csv_path = root / "raw.csv"
            save_tracking_rows(
                [
                    empty_tracking_row(
                        id="t-a",
                        titulo="A",
                        estado_triage="publicado",
                        ficha_id="a",
                    ),
                    empty_tracking_row(
                        id="open-1",
                        titulo="Abierto",
                        estado_triage="en_revision",
                        url="https://example.com",
                    ),
                ],
                csv_path,
            )
            drafts = root / "drafts"
            drafts.mkdir()
            candidates = root / "candidates"
            candidates.mkdir()
            import fichas as fichas_mod
            import tracking as tracking_mod

            desc = root / "descartados.json"
            desc.write_text("[]", encoding="utf-8")
            public = root / "public" / "data" / "games.json"
            public.parent.mkdir(parents=True)
            public.write_text(games_path.read_text(encoding="utf-8"), encoding="utf-8")

            old_public = tracking_mod.PUBLIC_GAMES_PATH
            old_desc = tracking_mod.DESCARTADOS_PATH
            tracking_mod.PUBLIC_GAMES_PATH = public
            tracking_mod.DESCARTADOS_PATH = desc
            try:
                code = fichas_mod.main(
                    [
                        "--games",
                        str(games_path),
                        "--csv",
                        str(csv_path),
                        "--drafts-dir",
                        str(drafts),
                        "--candidates-dir",
                        str(candidates),
                        "status",
                        "--limit",
                        "5",
                    ]
                )
            finally:
                tracking_mod.PUBLIC_GAMES_PATH = old_public
                tracking_mod.DESCARTADOS_PATH = old_desc
            self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
