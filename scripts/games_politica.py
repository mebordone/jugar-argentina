"""Juegos políticos y satíricos — curaduría v1.1."""
from generate_db import game, v

POLITICA_GAMES = [
    game(
        "cristina-vs-gorilas",
        "Cristina vs Gorilas",
        2016,
        "publicado",
        v(None, "principal", None),
        "Nac & Pop",
        "Argentina",
        ["Android"],
        ["accion", "arcade"],
        "Juego móvil de acción donde el jugador apoya el proyecto nacional contra gorilas y buitres. Sátira política kirchnerista de la colectiva Nac & Pop.",
        {
            "regiones": ["Nacional"],
            "provincias": [],
            "periodo_historico": ["contemporaneo"],
            "temas": ["politica", "satira"],
        },
        {
            "fuentes_investigacion": [
                "https://nicolasbroner.wordpress.com/2016/02/05/cristina-vs-gorilas/",
                "https://pressover.news/"
            ],
        },
        personajes=[
            {
                "nombre": "Cristina Fernández de Kirchner",
                "tipo": "politico",
                "rol": "protagonista",
                "descripcion": "Figura central de la sátira política",
            }
        ],
        ejes_culturales=["politica", "satira"],
        tipo_obra="indie",
        grado_relevancia_argentina="central",
        calidad_fuente="prensa",
        sensibilidad="alta",
        disponibilidad="perdido",
    ),
    game(
        "menem-la-hizo",
        "Menem La Hizo",
        2023,
        "publicado",
        v(None, "principal", None),
        "Sol Rodríguez Seoane / Javier Ventosa",
        "Argentina",
        ["Web", "PC"],
        ["aventura", "narrativa"],
        "Elige tu propia aventura satírica donde el jugador encarna a Carlos Saúl Menem con el objetivo de desmantelar el país. Surgido de la game jam Acción Dev.",
        {
            "regiones": ["Nacional"],
            "provincias": [],
            "periodo_historico": ["contemporaneo"],
            "temas": ["politica", "satira", "historia"],
        },
        {
            "itch": "https://ventousa.itch.io/menem-la-hizo",
            "fuentes_investigacion": [
                "https://pressover.news/entrevista/menem-la-hizo-el-videojuego-sobre-desmantelar-el-pais/",
                "https://elplanteo.com/videojuego-menem-la-hizo/",
            ],
        },
        personajes=[
            {
                "nombre": "Carlos Saúl Menem",
                "tipo": "politico",
                "rol": "protagonista",
                "descripcion": "Expresidente argentino en parodia interactiva",
            }
        ],
        ejes_culturales=["politica", "satira", "historia"],
        tipo_obra="jam",
        grado_relevancia_argentina="central",
        calidad_fuente="prensa",
        sensibilidad="alta",
        disponibilidad="gratis",
    ),
    game(
        "evita-peron-contra-gorilas",
        "Evita y Perón contra los Gorilas",
        2011,
        "publicado",
        v(None, "principal", None),
        "Agustín Pérez Fernández (sanafapech)",
        "Argentina",
        ["Web"],
        ["accion", "shooter"],
        "Shooter top-down en pixel art creado en la CodeAr jam 2011. Perón zombie rescata obreros de gorilas literales y los lleva al colectivo de una manifestación.",
        {
            "regiones": ["Pampeana"],
            "provincias": ["Ciudad Autónoma de Buenos Aires"],
            "periodo_historico": ["contemporaneo"],
            "temas": ["politica", "satira", "historia"],
        },
        {
            "web_oficial": "https://www.kongregate.com/en/games/sanafapech/evita-y-peron-contra-los-gorilas",
            "fuentes_investigacion": [
                "https://pressover.news/articulos/evita-y-peron-contra-los-gorilas/"
            ],
        },
        personajes=[
            {"nombre": "Juan Domingo Perón", "tipo": "politico", "rol": "protagonista", "descripcion": "Protagonista del shooter"},
            {"nombre": "Eva Perón", "tipo": "politico", "rol": "secundario", "descripcion": "Power-up salvador"},
        ],
        ejes_culturales=["politica", "satira"],
        tipo_obra="jam",
        grado_relevancia_argentina="importante",
        calidad_fuente="prensa",
        sensibilidad="media",
        disponibilidad="gratis",
    ),
]
