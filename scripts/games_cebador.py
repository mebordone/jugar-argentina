"""Ficha: Cebador (Cebatorio de Juegos)."""
from generate_db import game, v

CEBADOR_GAME = game(
    "cebador",
    "Cebador",
    None,
    "publicado",
    v("principal", "principal", None),
    "Cebatorio de Juegos",
    "Argentina",
    ["Android", "iOS"],
    ["casual", "simulacion"],
    "Juego mobile argentino de desafíos contra reloj donde aprendés a cebar mate amargo, dulce o con yuyos. "
    "Tras morir, debés convencer a Dios en el Cielo del Mate cebarle un buen mate, aunque solo tomes latte macchiato.",
    {
        "regiones": ["Nacional"],
        "provincias": [],
        "periodo_historico": ["contemporaneo"],
        "temas": ["cultura_popular", "gastronomia"],
    },
    {
        "web_oficial": "https://cebadoreljuego.com/",
        "google_play": "https://play.google.com/store/apps/details?id=com.cebatoriodejuegos.cebador",
        "fuentes_investigacion": [
            "https://cebadoreljuego.com/",
            "https://apps.apple.com/ar/app/cebador/id6739545369",
        ],
    },
    ejes_culturales=["folclore", "juegos_tradicionales"],
    tipo_obra="indie",
    calidad_fuente="oficial",
    metadatos={
        "idiomas": ["es"],
        "multijugador": False,
        "precio": "gratuito",
        "rating": {},
        "tipo": "juego",
    },
    imagenes={
        "portada": "https://cebadoreljuego.com/assets/img/iso.png",
        "capturas": [],
    },
    disponibilidad="gratis",
)
