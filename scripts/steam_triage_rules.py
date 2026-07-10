"""Reglas editoriales compartidas para triage de candidatos Steam."""
from __future__ import annotations

import re
import unicodedata

SKIP_TITLE_RE = re.compile(
    r"\b(demo|soundtrack|dlc|pack|skin|bundle|upgrade|expansion|flags?\s+pack|"
    r"content creator|workshop|100 cats|hidden cats|jigsaw|season pass)\b",
    re.I,
)

SPORTS_GENERIC_RE = re.compile(
    r"\b(fifa|pes\b|efootball|motogp|pro basketball manager|wrc\s*\d|football club simulator|"
    r"national rugby manager|head basketball)\b",
    re.I,
)

STRONG_TERMS = {
    "argentina", "malvinas", "falklands", "gaucho", "independencia", "libertador",
    "dakar", "ruta 40", "falkland", "peron", "evita", "conurbano", "patagonia",
    "pampa", "pombero", "yerba mate",
}

NOISE_ONLY_TERMS = {"mate", "tango", "santa fe", "truco"}

AR_KEYWORDS = (
    "argentina", "argentino", "argentinian", "buenos aires", "malvinas", "falkland",
    "gaucho", "patagonia", "pampa", "conurbano", "cordoba", "mendoza", "salta",
    "jujuy", "ushuaia", "iguazu", "perito moreno", "rosario", "tucuman", "neuquen",
    "independencia", "libertador", "provincias unidas", "rio de la plata", "cono sur",
)

AR_DEV_HINTS = (
    "argentina", "argent", "buenos aires", "córdoba", "cordoba", "rosario",
    "mendoza", "saibot", "pernich", "milanesa", "symbio", "devpetrichor",
    "recabarren", "batista", "bennu", "fichiner", "ltp argentina", "sendero",
    "pierucci", "altun", "monte castro", "big mount",
)


def normalize_title(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", normalize_title(text)).strip("-")


def parse_search_terms(notas: str) -> set[str]:
    terms: set[str] = set()
    if not notas:
        return terms
    if "steam search" in notas:
        chunk = notas.split("steam search", 1)[1].split(";")[0]
        terms.update(t.strip() for t in chunk.split(",") if t.strip())
    if "terminos:" in notas:
        chunk = notas.split("terminos:", 1)[1]
        terms.update(t.strip() for t in chunk.split(",") if t.strip())
    return terms


def parse_jurisdicciones(notas: str) -> list[str]:
    if "jurisdiccion:" not in (notas or ""):
        return []
    chunk = notas.split("jurisdiccion:", 1)[1].split(";")[0]
    return [j.strip() for j in chunk.split(";") if j.strip()]


def auto_discard_reason(title: str, app_type: str | None = None) -> str | None:
    if app_type and app_type not in ("game", ""):
        return f"tipo Steam: {app_type}"
    if SKIP_TITLE_RE.search(title):
        return "título indica demo/dlc/pack/skin"
    if SPORTS_GENERIC_RE.search(title):
        return "deporte internacional genérico sin foco AR"
    return None


def score_candidate(
    title: str,
    short_description: str,
    developers: list[str],
    publishers: list[str],
    notas_triage: str = "",
    app_type: str = "game",
) -> tuple[int, str, str]:
    """Retorna (score, bucket, motivo). bucket: incorporar | pendiente | descartado."""
    discard = auto_discard_reason(title, app_type)
    if discard:
        return 0, "descartado", discard

    blob = " ".join([
        title, short_description,
        " ".join(developers), " ".join(publishers),
    ]).lower()

    terms = parse_search_terms(notas_triage)
    juris = parse_jurisdicciones(notas_triage)
    score = 0
    reasons: list[str] = []

    if app_type == "game":
        score += 1
        reasons.append("juego base")
    else:
        return 0, "descartado", f"no es juego ({app_type})"

    if any(h in blob for h in AR_DEV_HINTS):
        score += 3
        reasons.append("dev/publisher AR")
    if any(kw in blob for kw in AR_KEYWORDS):
        score += 2
        reasons.append("descripción AR")

    strong_hits = terms & STRONG_TERMS
    if strong_hits:
        score += 2
        reasons.append(f"términos fuertes: {','.join(sorted(strong_hits)[:3])}")

    if juris:
        score += 1
        reasons.append(f"jurisdicción: {juris[0]}")

    noise_only = terms and terms <= NOISE_ONLY_TERMS and not juris and not any(
        kw in blob for kw in AR_KEYWORDS
    )
    if noise_only:
        score -= 4
        reasons.append("solo ruido mate/tango/santa fe")

    if score >= 5:
        bucket = "incorporar"
    elif score >= 3:
        bucket = "pendiente"
    else:
        bucket = "descartado"
        if not reasons:
            reasons.append("señal argentina insuficiente")

    return score, bucket, "; ".join(reasons)
