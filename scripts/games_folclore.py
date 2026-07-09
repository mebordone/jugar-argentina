"""Folclore y leyendas — curaduría v1.1."""
from generate_db import game, v

FOLCLORE_GAMES = [
    game(
        "elifoot-98-liga-argentina",
        "Elifoot 98 — Liga Argentina",
        1998,
        "publicado",
        v(None, None, "principal", "liga_futbol"),
        "Elifoot / distribuidor local",
        "Portugal",
        ["PC"],
        ["deportes", "simulacion", "estrategia"],
        "Simulador de fútbol con modo de gestión de liga argentina. Edición localizada con equipos del fútbol profesional argentino.",
        {
            "regiones": ["Nacional"],
            "provincias": [],
            "periodo_historico": ["contemporaneo"],
            "temas": ["deporte"],
        },
        {"fuentes_investigacion": ["https://www.pcfutbol.com/"]},
        deporte={
            "deporte": "futbol",
            "competicion": ["Primera División Argentina"],
            "equipos_destacados": [],
            "modo": "gestion_liga",
        },
        ejes_culturales=["deporte"],
        tipo_obra="comercial",
        grado_relevancia_argentina="importante",
        disponibilidad="abandonware",
    ),
]
