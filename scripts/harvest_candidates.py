#!/usr/bin/env python3
"""Fase 0-1: limpia duplicados, agrega columnas de triage y nuevos candidatos al CSV."""
import csv
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "raw_candidates.csv"

FIELDNAMES = [
    "titulo",
    "anio",
    "estado_juego",
    "vinculo_preliminar",
    "fuente",
    "url",
    "nota",
    "estado_triage",
    "eje_sugerido",
    "ejes_culturales_sugeridos",
    "notas_triage",
]

# Candidatos nuevos v1.1 — barrido por ejes culturales
NEW_CANDIDATES = [
    # Política y sátira
    ("Cristina vs Gorilas", 2016, "publicado", "protagonista", "https://nicolasbroner.wordpress.com/2016/02/05/cristina-vs-gorilas/", "", "Android. Nac&Pop. Sátira peronista vs gorilas y buitres.", "candidato", "protagonista", "politica;satira", "sensibilidad alta"),
    ("Menem La Hizo", 2023, "publicado", "protagonista", "https://pressover.news/entrevista/menem-la-hizo-el-videojuego-sobre-desmantelar-el-pais/", "https://ventousa.itch.io/menem-la-hizo", "Elige tu aventura satírica. Game jam Acción Dev.", "candidato", "protagonista", "politica;satira", "sensibilidad alta"),
    ("Evita y Perón contra los Gorilas", 2011, "publicado", "protagonista", "https://pressover.news/articulos/evita-y-peron-contra-los-gorilas/", "https://www.kongregate.com/en/games/sanafapech/evita-y-peron-contra-los-gorilas", "CodeAr jam 2011. Shooter pixel art.", "candidato", "protagonista", "politica;satira", ""),
    ("Argentina Pelea", 2015, "publicado", "protagonista", "https://archive.org/search?query=argentina+pelea+flash", "", "Flash: pelea política Macri vs Cristina. Buscar en archive.org.", "candidato", "protagonista", "politica;satira", "sensibilidad alta; verificar URL"),
    ("Debate Mortal", 2019, "publicado", "protagonista", "https://archive.org/search?query=debate+mortal+argentina", "", "Flash/HTML5: Macri vs Cristina vs Alberto.", "candidato", "protagonista", "politica;satira", "sensibilidad alta; verificar URL"),
    ("Kirchner Hero", 2013, "publicado", "protagonista", "https://archive.org/search?query=kirchner+hero", "", "Juego Flash político kirchnerista. archive.org.", "candidato", "protagonista", "politica;satira", "verificar existencia"),
    ("Macri Bros", 2015, "publicado", "protagonista", "https://archive.org/search?query=macri+bros+juego", "", "Parodia política estilo Mario. Flash perdido.", "candidato", "protagonista", "politica;satira", "verificar existencia"),
    # Folclore
    ("Lobizón: La Bestia del Full Moon", None, "en_desarrollo", "protagonista", "https://itch.io/search?q=lobizon", "", "Prototipos indie sobre la leyenda del lobizón.", "candidato", "protagonista", "folclore", "varios prototipos posibles"),
    ("Gauchito Gil: El Santo Gaucho", None, "prototipo", "protagonista", "https://itch.io/search?q=gauchito+gil", "", "Juegos fan sobre el santo popular.", "candidato", "protagonista", "folclore", "verificar cuál incluir"),
    ("Difunta Correa", None, "prototipo", "protagonista", "https://itch.io/search?q=difunta+correa", "", "Leyenda sanjuanina en formato narrativo.", "candidato", "protagonista", "folclore", ""),
    ("Yaci Yateré", None, "prototipo", "protagonista", "https://devuego.lat/", "", "Duende del nordeste en juegos educativos o terror.", "candidato", "protagonista", "folclore", ""),
    ("El Familiar", None, "prototipo", "protagonista", "https://itch.io/search?q=el+familiar+argentina", "", "Leyenda salteña del pacto con el diablo.", "candidato", "protagonista", "folclore", ""),
    ("Huilliche: Guardianes del Sur", None, "en_desarrollo", "escenario+protagonista", "https://devuego.lat/", "", "Mitología mapuche en desarrollo indie.", "candidato", "mixto", "folclore;memoria", ""),
    # Historieta y literatura
    ("Mafalda: El Videojuego", None, "cancelado", "protagonista", "https://www.mobygames.com/search?q=mafalda", "", "Proyectos oficiales y fan. Verificar cuáles existieron.", "candidato", "protagonista", "historieta", ""),
    ("El Eternauta", None, "en_desarrollo", "protagonista", "https://www.mobygames.com/search?q=eternauta", "", "Adaptaciones y fan games del cómic de Oesterheld.", "candidato", "protagonista", "historieta;memoria", "sensibilidad media"),
    ("Patoruzú", 2007, "publicado", "protagonista", "https://www.mobygames.com/search?q=patoruzu", "", "Juegos oficiales del personaje de Dante Quinterno.", "candidato", "protagonista", "historieta", "verificar ediciones"),
    ("Martín Fierro: La Aventura", None, "prototipo", "protagonista", "https://itch.io/search?q=martin+fierro", "", "Adaptaciones del poema de Hernández.", "candidato", "protagonista", "literatura", ""),
    # Memoria e historia
    ("ESMA: Memoria Virtual", None, "prototipo", "escenario", "https://itch.io/search?q=esma+argentina", "", "Juegos sobre memoria de la dictadura.", "candidato", "escenario", "memoria", "sensibilidad alta"),
    ("Nunca Más: El Juego", None, "prototipo", "escenario", "https://mobbyt.com/", "", "Educativos sobre dictadura militar.", "candidato", "escenario", "memoria;educativo", "sensibilidad alta"),
    ("Malvinas: Operación Rosario (expandido)", None, "publicado", "escenario", "https://a-m-o-g-u-s-u-s.itch.io/operacion-rosario", "https://a-m-o-g-u-s-u-s.itch.io/operacion-rosario", "Ya en base; candidato para enriquecer.", "verificado", "escenario", "memoria;historia", ""),
    # Cultura urbana
    ("152: El Colectivo", None, "prototipo", "escenario", "https://itch.io/search?q=colectivo+buenos+aires", "", "Simuladores del bondi porteño.", "candidato", "escenario", "cultura_urbana", ""),
    ("SUBE Simulator", None, "prototipo", "escenario", "https://itch.io/search?q=sube+argentina", "", "Juegos sobre transporte público CABA.", "candidato", "escenario", "cultura_urbana", ""),
    ("Cumbia Villera: El Ritmo", None, "prototipo", "escenario", "https://itch.io/search?q=cumbia+argentina", "", "Ritmo y cultura villera.", "candidato", "escenario", "cultura_urbana;musica", ""),
    ("Kiosco Simulator", 2024, "publicado", "escenario", "https://itch.io/search?q=kiosco+argentina", "", "Simuladores del kiosco de barrio.", "candidato", "escenario", "cultura_urbana", "verificar existencia"),
    # Educativos — colección Mobbyt
    ("Mobbyt — Colección Geografía Argentina", None, "publicado", "escenario", "https://mobbyt.com/videojuego/educativo/", "https://mobbyt.com/videojuego/educativo/", "Colección: trivias de provincias, capitales, banderas, mapas.", "candidato", "escenario", "educativo;geografia", "entrada colección"),
    ("Mobbyt — Historia Argentina", None, "publicado", "escenario", "https://mobbyt.com/videojuego/educativo/", "https://mobbyt.com/videojuego/educativo/", "Trivias históricas escolares en plataforma Mobbyt.", "candidato", "escenario", "educativo;historia", "entrada colección"),
    ("Aprender Jugando — Provincias AR", None, "publicado", "escenario", "https://mobbyt.com/", "", "Minijuegos educativos varios.", "candidato", "escenario", "educativo;geografia", ""),
    # Deporte
    ("Elifoot 98 — Liga Argentina", 1998, "publicado", "deporte", "https://www.pcfutbol.com/", "", "Simulador con modo liga argentina.", "candidato", "deporte", "deporte", "verificar edición"),
    ("Manager de Fútbol Argentino", None, "abandonware", "deporte", "https://www.abandonsocios.org/", "", "Managers abandonados de liga local.", "candidato", "deporte", "deporte", ""),
    ("Estudiantes: Camino a la Libertadores", None, "publicado", "deporte", "https://archive.org/search?query=futbol+argentino+juego", "", "Juegos promocionales de clubes.", "candidato", "deporte", "deporte", "verificar"),
    # Flash/HTML5 perdidos
    ("Barredor de la City", 2012, "publicado", "escenario", "https://archive.org/search?query=barredor+city+flash", "", "Flash sobre barredores de CABA.", "candidato", "escenario", "cultura_urbana", "archive.org"),
    ("Vialidad Argentina", 2010, "publicado", "escenario", "https://archive.org/search?query=vialidad+argentina+juego", "", "Juego educativo Flash de tránsito.", "candidato", "escenario", "educativo", "archive.org"),
    ("Campaña Presidencial 2011", 2011, "publicado", "protagonista", "https://archive.org/search?query=campana+presidencial+2011+juego", "", "Juegos Flash de elecciones 2011.", "candidato", "protagonista", "politica;satira", ""),
    # J2ME / celulares
    ("Regnum Online Mobile AR", 2005, "publicado", "escenario", "https://www.abandonsocios.org/", "", "Versiones móviles de juegos argentinos.", "candidato", "escenario", "historia", "verificar"),
    ("Truco Mobile (varios)", None, "publicado", "escenario+protagonista", "https://archive.org/search?query=truco+java+mobile", "", "Truco para Nokia y similares.", "candidato", "mixto", "juegos_tradicionales", ""),
    ("Fútbol 5 J2ME", None, "publicado", "deporte", "https://archive.org/search?query=futbol+5+java+argentina", "", "Juegos de fulbito para feature phones.", "candidato", "deporte", "deporte;cultura_urbana", ""),
    # Mods
    ("Malvinas Mod ARMA 3", None, "publicado", "escenario", "https://steamcommunity.com/workshop/browse/?appid=107410&searchtext=malvinas", "", "Total conversion / mod Malvinas.", "candidato", "escenario", "memoria;historia", "tipo mod"),
    ("GTA San Andreas — Mapa Buenos Aires", 2019, "publicado", "escenario", "https://fmfuego.com.ar/interes-general/gta-rio-de-la-plata-el-juego-que-tendra-un-mod-argentino.htm", "", "Ya en base como GTA Río de la Plata.", "verificado", "escenario", "cultura_urbana", "mod"),
    ("Patagonia Nazi — BloodRayne mod", None, "publicado", "escenario", "referencia_menor", "", "Nivel en juego internacional.", "candidato", "escenario", "historia", "referencia menor"),
    # Promocionales
    ("Arcor: El Reino de los Chocolates", 2005, "publicado", "escenario", "https://archive.org/search?query=arcor+juego+argentina", "", "Juego promocional de marca argentina.", "candidato", "escenario", "cultura_urbana", "tipo promocional"),
    ("Banco Nación — Simulador Financiero", None, "publicado", "escenario", "https://archive.org/search?query=banco+nacion+juego", "", "Gamificación bancaria estatal.", "candidato", "escenario", "educativo", "promocional"),
    ("YPF Energía Educativa", None, "publicado", "escenario", "https://mobbyt.com/", "", "Juegos educativos de YPF.", "candidato", "escenario", "educativo", "promocional"),
    # Game jams
    ("GGJ 2026 — El Intruso 82", 2026, "publicado", "escenario", "https://emiliokolo.itch.io/el-intruso-82", "https://emiliokolo.itch.io/el-intruso-82", "Ya en base verificada.", "verificado", "escenario", "memoria", ""),
    ("Ludum Dare — Gaucho entries", None, "prototipo", "protagonista", "https://itch.io/jam/ludum-dare/search?q=gaucho", "", "Prototipos jam con temática gaucha.", "candidato", "protagonista", "folclore", ""),
    # Juegos tradicionales
    ("Chinchón Digital", None, "publicado", "escenario+protagonista", "https://blyts.com/", "https://blyts.com/", "Variante del truco familiar.", "candidato", "mixto", "juegos_tradicionales", ""),
    ("Escoba del 15", None, "publicado", "escenario+protagonista", "https://mobbyt.com/", "", "Juego de naipes argentino digital.", "candidato", "mixto", "juegos_tradicionales", ""),
    ("Generala Online", None, "publicado", "escenario", "https://mobbyt.com/", "", "Dados generala en versión web.", "candidato", "escenario", "juegos_tradicionales", ""),
    ("Pool Argentino", None, "publicado", "escenario", "https://archive.org/search?query=pool+argentina+juego", "", "Billar en versión local.", "candidato", "escenario", "juegos_tradicionales", ""),
    # Migración
    ("Patria Chica Simulator", None, "prototipo", "escenario", "https://itch.io/search?q=argentina+espana", "", "Experiencias de argentinos en el exterior.", "candidato", "escenario", "migracion", ""),
    ("Maradona en Nápoles", None, "en_desarrollo", "protagonista", "https://devuego.lat/", "", "Biográficos del Diez en Europa.", "candidato", "protagonista", "deporte;musica", ""),
    # Música
    ("Rock Nacional: La Aventura", None, "prototipo", "protagonista", "https://itch.io/search?q=rock+argentino", "", "Biografías interactivas de rock nacional.", "candidato", "protagonista", "musica", ""),
    ("Tango Fury", 2018, "publicado", "escenario+protagonista", "referencia", "", "Ya existe Tango: The Adventure Game en base.", "verificado", "mixto", "musica", ""),
    # Excluidos explícitos (para triage → descartados)
    ("FIFA 23", 2022, "publicado", "deporte", "exclusion", "", "Argentina solo como selección.", "descartado", "deporte", "deporte", "no cumple criterio"),
    ("eFootball PES 2021", 2020, "publicado", "deporte", "exclusion", "", "Selección entre muchas.", "descartado", "deporte", "deporte", "no cumple criterio"),
    ("Roots of Pacha", 2023, "publicado", "protagonista", "exclusion", "", "Dev argentino sin temática AR.", "descartado", "protagonista", "", "solo dev AR"),
    ("Dark Rage", 1997, "publicado", "protagonista", "exclusion", "", "Shoot'em up sin temática argentina.", "descartado", "protagonista", "", "solo dev AR"),
]


def normalize_title(t: str) -> str:
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode("ascii")
    t = re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()
    return t


def row_from_legacy(r: dict) -> dict:
    estado = r.get("estado_juego") or r.get("estado", "")
    return {
        "titulo": r.get("titulo", ""),
        "anio": r.get("anio", ""),
        "estado_juego": estado,
        "vinculo_preliminar": r.get("vinculo_preliminar", ""),
        "fuente": r.get("fuente", ""),
        "url": r.get("url", ""),
        "nota": r.get("nota", ""),
        "estado_triage": r.get("estado_triage", "candidato"),
        "eje_sugerido": r.get("eje_sugerido") or _eje_from_vinculo(r.get("vinculo_preliminar", "")),
        "ejes_culturales_sugeridos": r.get("ejes_culturales_sugeridos", ""),
        "notas_triage": r.get("notas_triage", ""),
    }


def _eje_from_vinculo(v: str) -> str:
    if "+" in v or ("escenario" in v and "protagonista" in v):
        return "mixto"
    if "escenario" in v:
        return "escenario"
    if "protagonista" in v:
        return "protagonista"
    if "deporte" in v:
        return "deporte"
    return ""


def candidate_row(c: tuple) -> dict:
    return {
        "titulo": c[0],
        "anio": c[1] or "",
        "estado_juego": c[2],
        "vinculo_preliminar": c[3],
        "fuente": c[4],
        "url": c[5],
        "nota": c[6],
        "estado_triage": c[7],
        "eje_sugerido": c[8],
        "ejes_culturales_sugeridos": c[9],
        "notas_triage": c[10],
    }


def main():
    existing = []
    if CSV_PATH.exists():
        with open(CSV_PATH, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                existing.append(row_from_legacy(r))

    seen = set()
    merged = []
    for r in existing:
        key = (normalize_title(r["titulo"]), r.get("url", "").strip().lower())
        alt_key = normalize_title(r["titulo"])
        if alt_key in seen and not r.get("url"):
            continue
        if key in seen:
            continue
        seen.add(alt_key)
        seen.add(key)
        if not r.get("estado_triage"):
            r["estado_triage"] = "candidato"
        merged.append(r)

    added = 0
    for c in NEW_CANDIDATES:
        row = candidate_row(c)
        key = normalize_title(row["titulo"])
        if key in seen:
            continue
        seen.add(key)
        merged.append(row)
        added += 1

    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(merged)

    print(f"CSV actualizado: {len(merged)} filas ({added} nuevas, sin duplicados)")


if __name__ == "__main__":
    main()
