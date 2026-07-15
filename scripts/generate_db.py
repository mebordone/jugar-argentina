#!/usr/bin/env python3
"""Genera la base de datos de videojuegos vinculados a Argentina."""
import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TODAY = str(date.today())

VINCULO_NULL = {"activo": False, "presencia": None}


def v(esc=None, pro=None, dep=None, subtipo=None):
    out = {
        "escenario": {"activo": bool(esc), "presencia": esc},
        "protagonista": {"activo": bool(pro), "presencia": pro},
        "deporte_argentino": {"activo": bool(dep), "presencia": dep},
    }
    if dep and subtipo:
        out["deporte_argentino"]["subtipo"] = subtipo
    return out


def game(
    id_,
    titulo,
    anio,
    estado,
    vinculo,
    desarrollador,
    pais_desarrollo,
    plataformas,
    generos,
    descripcion,
    contexto,
    enlaces,
    verificado=True,
    titulo_original=None,
    personajes=None,
    deporte=None,
    imagenes=None,
    metadatos=None,
    ejes_culturales=None,
    tipo_obra="comercial",
    formato="juego_base",
    grado_relevancia_argentina="central",
    calidad_fuente="prensa",
    sensibilidad="baja",
    serie=None,
    edicion=None,
    relacionado_con=None,
    disponibilidad="desconocido",
):
    return {
        "id": id_,
        "titulo": titulo,
        "titulo_original": titulo_original or titulo,
        "anio": anio,
        "estado": estado,
        "vinculo_argentina": vinculo,
        "personajes_argentinos": personajes or [],
        "deporte_argentino": deporte,
        "desarrollador": desarrollador,
        "pais_desarrollo": pais_desarrollo,
        "plataformas": plataformas,
        "generos": generos,
        "descripcion": descripcion,
        "contexto_argentino": contexto,
        "enlaces": enlaces,
        "imagenes": imagenes or {"portada": None, "capturas": []},
        "metadatos": metadatos
        or {
            "idiomas": ["es"],
            "multijugador": False,
            "precio": None,
            "rating": {},
            "tipo": "juego",
        },
        "ejes_culturales": ejes_culturales or [],
        "tipo_obra": tipo_obra,
        "formato": formato,
        "grado_relevancia_argentina": grado_relevancia_argentina,
        "calidad_fuente": calidad_fuente,
        "sensibilidad": sensibilidad,
        "serie": serie,
        "edicion": edicion,
        "relacionado_con": relacionado_con or [],
        "disponibilidad": disponibilidad,
        "verificado": verificado,
        "fecha_actualizacion": TODAY,
    }


GAMES = [
    game(
        "atuel-2022",
        "Atuel",
        2022,
        "publicado",
        v("principal", None, None),
        "Cooperativa Matajuegos / The 12.01 Project",
        "Argentina",
        ["PC", "Android", "iOS"],
        ["documental", "aventura", "experimental"],
        "Documental interactivo surrealista sobre el río Atuel en Mendoza. Recorre el ecosistema desde la montaña hasta el embalse del Valle Grande con testimonios de especialistas y lugareños.",
        {
            "regiones": ["Cuyo"],
            "provincias": ["Mendoza"],
            "periodo_historico": ["contemporaneo"],
            "temas": ["geografia", "medio_ambiente", "cambio_climatico"],
        },
        {
            "steam": "https://store.steampowered.com/app/2794330/Atuel/",
            "itch": "https://matajuegos.itch.io/atuel",
            "fuentes_investigacion": [
                "https://pressover.news/noticias/atuel-el-videojuego-documental-argentino-llega-a-steam-y-google-play/"
            ],
        },
    ),
    game(
        "zupay-sombras-independencia",
        "Zupay: Sombras de la Independencia",
        None,
        "en_desarrollo",
        v("principal", "principal", None),
        "Abstract Tales",
        "Argentina",
        ["PC"],
        ["accion", "hack_and_slash"],
        "Hack and slash con estética pixel art ambientado en la Guerra de la Independencia. El protagonista es un gaucho sobrenatural inspirado en el folclore y las milicias de Güemes.",
        {
            "regiones": ["Noroeste"],
            "provincias": ["Salta", "Jujuy"],
            "periodo_historico": ["independencia"],
            "temas": ["historia", "folclore", "gauchesco"],
        },
        {
            "steam": "https://store.steampowered.com/app/4074370/Zupay_Sombras_de_la_Independencia/",
            "fuentes_investigacion": [
                "https://pressover.news/analisis/primeras-impresiones/jugamos-a-demo-de-zupay-el-gaucho-que-volvio-de-la-muerte/"
            ],
        },
        personajes=[
            {
                "nombre": "Zupay",
                "tipo": "folclore",
                "rol": "protagonista",
                "descripcion": "Gaucho sobrenatural vinculado a la milicia de Güemes",
            }
        ],
    ),
    game(
        "la-furia-de-las-trenzas",
        "La Furia de las Trenzas",
        None,
        "en_desarrollo",
        v("principal", "principal", None),
        "La Romero Estudio",
        "Argentina",
        ["PC"],
        ["roguelike", "accion", "estrategia"],
        "Roguelike de supervivencia sobre la defensa de Buenos Aires durante la segunda invasión inglesa. El jugador encarna a Santiago de Liniers y recluta milicias históricas.",
        {
            "regiones": ["Pampeana"],
            "provincias": ["Ciudad Autónoma de Buenos Aires"],
            "periodo_historico": ["independencia"],
            "temas": ["historia", "invasiones_inglesas"],
        },
        {
            "steam": "https://store.steampowered.com/app/3217730/La_Furia_de_las_Trenzas/",
            "fuentes_investigacion": [
                "https://www.el1digital.com.ar/cultura/a-defender-buenos-aires-llega-a-steam-la-furia-de-las-trenzas/"
            ],
        },
        personajes=[
            {
                "nombre": "Santiago de Liniers",
                "tipo": "historico",
                "rol": "protagonista",
                "descripcion": "Virrey y defensor de Buenos Aires en 1807",
            }
        ],
    ),
    game(
        "los-infernales",
        "Los Infernales",
        None,
        "en_desarrollo",
        v("principal", "principal", None),
        "TMO Games",
        "Argentina",
        ["PC"],
        ["shooter", "accion"],
        "Shooter inspirado en las milicias gauchas de Martín Miguel de Güemes que defendieron el norte argentino durante la Guerra de la Independencia.",
        {
            "regiones": ["Noroeste"],
            "provincias": ["Salta", "Jujuy"],
            "periodo_historico": ["independencia"],
            "temas": ["historia", "gauchesco", "guerra_de_guerrillas"],
        },
        {
            "fuentes_investigacion": [
                "https://agencia.unq.edu.ar/?p=14461"
            ],
        },
        personajes=[
            {
                "nombre": "Milicias de Güemes",
                "tipo": "historico",
                "rol": "protagonista",
                "descripcion": "División Infernal de Gauchos de Línea",
            }
        ],
    ),
    game(
        "malvinas-2032",
        "Malvinas 2032",
        1999,
        "publicado",
        v("principal", "principal", None),
        "Sabarasa Entertainment",
        "Argentina",
        ["PC"],
        ["estrategia", "rts"],
        "RTS argentino donde el jugador comanda fuerzas militares en una incursión ficticia de 2032 para recuperar las Islas Malvinas. Considerado uno de los primeros videojuegos comerciales del país.",
        {
            "regiones": ["Patagonia", "Atlántico Sur"],
            "provincias": ["Tierra del Fuego"],
            "periodo_historico": ["siglo_xx", "contemporaneo"],
            "temas": ["historia", "guerra_de_malvinas"],
        },
        {
            "mobygames": "https://www.mobygames.com/game/50719/malvinas-2032/",
            "wikipedia": "https://en.wikipedia.org/wiki/Malvinas_2032",
            "fuentes_investigacion": [
                "https://devuego.lat/bd/presskit/malvinas-2032"
            ],
        },
        metadatos={"idiomas": ["es", "en"], "multijugador": False, "precio": None, "rating": {}, "tipo": "juego"},
    ),
    game(
        "malvinas-la-ultima-carta",
        "Malvinas: La Última Carta",
        None,
        "en_desarrollo",
        v("principal", "principal", None),
        "El Burro Studio",
        "Argentina",
        ["PC"],
        ["accion", "aventura", "sigilo"],
        "Acción y sigilo en tercera persona sobre un conscripto de 18 años, último sobreviviente de su batallón, que debe proteger las cartas de sus compañeros caídos durante la Guerra de Malvinas.",
        {
            "regiones": ["Patagonia", "Atlántico Sur"],
            "provincias": [],
            "periodo_historico": ["siglo_xx"],
            "temas": ["historia", "guerra_de_malvinas"],
        },
        {
            "steam": "https://store.steampowered.com/app/2584740/Malvinas_La_Ultima_Carta/",
            "fuentes_investigacion": [
                "https://www.perfil.com/noticias/tecnologia/malvinas-la-ultima-carta-primer-videojuego-argentino-guerra-1982.phtml"
            ],
        },
    ),
    game(
        "gauchos-inmortales",
        "Gauchos Inmortales",
        None,
        "en_desarrollo",
        v("principal", "principal", None),
        "RealiTeam S.A.S.",
        "Argentina",
        ["PC"],
        ["accion", "terror", "mmo"],
        "Juego multijugador de acción y terror rural ambientado en la Argentina del siglo XIX, con gauchos y criaturas del folclore sudamericano.",
        {
            "regiones": ["Pampeana", "Centro"],
            "provincias": [],
            "periodo_historico": ["siglo_xix"],
            "temas": ["folclore", "gauchesco", "terror_rural"],
        },
        {
            "web_oficial": "https://gauchosinmortales.com/",
            "fuentes_investigacion": [
                "https://gauchosinmortales.com/"
            ],
        },
        personajes=[
            {
                "nombre": "Gaucho",
                "tipo": "arquetipo",
                "rol": "protagonista",
                "descripcion": "Protagonista gauchesco en la Argentina rural del siglo XIX",
            }
        ],
    ),
    game(
        "pomberito-2024",
        "Pomberito",
        2024,
        "publicado",
        v("principal", "principal", None),
        "Lara the Pitbull",
        "Argentina",
        ["PC"],
        ["terror", "aventura", "supervivencia"],
        "Survival horror en primera persona ambientado en el campo del noreste argentino. El jugador debe sobrevivir cinco noches mientras aparece el Pombero del folclore guaraní.",
        {
            "regiones": ["Noreste"],
            "provincias": [],
            "periodo_historico": ["contemporaneo", "ficcion_sin_epoca"],
            "temas": ["folclore", "terror_rural"],
        },
        {
            "steam": "https://store.steampowered.com/app/2761100/Pomberito/",
            "fuentes_investigacion": [
                "https://devuego.lat/bd/fjuego/pomberito",
                "https://tn.com.ar/tecno/juegos/2024/06/24/aprendio-a-disenar-con-videos-en-internet-y-creo-el-videojuego-del-pomberito-el-mitico-personaje-argentino/",
            ],
        },
        personajes=[
            {
                "nombre": "Pombero",
                "tipo": "folclore",
                "rol": "secundario",
                "descripcion": "Criatura del folclore guaraní del NEA argentino",
            }
        ],
    ),
    game(
        "fabulas-portenas",
        "Fábulas Porteñas",
        None,
        "en_desarrollo",
        v("principal", None, None),
        "Hypnos Team",
        "Argentina",
        ["PC"],
        ["terror", "aventura", "sigilo"],
        "Terror en primera persona inspirado en leyendas urbanas del subte porteño, centrado en la estación fantasma Pirámides de la línea H.",
        {
            "regiones": ["Pampeana"],
            "provincias": ["Ciudad Autónoma de Buenos Aires"],
            "periodo_historico": ["contemporaneo"],
            "temas": ["cultura_urbana", "leyendas_urbanas"],
        },
        {
            "fuentes_investigacion": [
                "https://tn.com.ar/tecno/juegos/2024/09/14/lanzan-fabulas-portenas-el-videojuego-argentino-de-terror-sobre-un-mito-urbano-de-la-linea-h-del-subte/"
            ],
        },
    ),
    game(
        "el-39-2025",
        "El 39",
        2025,
        "publicado",
        v("principal", None, None),
        "Bohemian Productions",
        "Argentina",
        ["PC"],
        ["terror", "aventura"],
        "Terror corto estilo PSX ambientado en Constitución a la madrugada. El jugador intenta tomar el colectivo 39 para llegar a un examen final.",
        {
            "regiones": ["Pampeana"],
            "provincias": ["Ciudad Autónoma de Buenos Aires"],
            "periodo_historico": ["contemporaneo"],
            "temas": ["cultura_urbana", "porteñidad"],
        },
        {
            "steam": "https://store.steampowered.com/app/3900380/El_39/",
            "fuentes_investigacion": ["https://devuego.lat/bd/fjuego/el-39"],
        },
    ),
    game(
        "buenos-aires-mirror-line",
        "Buenos Aires Mirror Line",
        2026,
        "publicado",
        v("principal", None, None),
        "Luka Hizo Algo",
        "Argentina",
        ["PC"],
        ["terror", "puzzle"],
        "Terror psicológico corto inspirado en Exit 8, ambientado en la bruma de Buenos Aires con música basada en cumbia y reggaetón local.",
        {
            "regiones": ["Pampeana"],
            "provincias": ["Ciudad Autónoma de Buenos Aires"],
            "periodo_historico": ["contemporaneo"],
            "temas": ["cultura_urbana"],
        },
        {
            "steam": "https://store.steampowered.com/app/3987420/Buenos_Aires_Mirror_Line/",
            "fuentes_investigacion": ["https://devuego.lat/bd/fjuego/buenos-aires-mirror-line"],
        },
    ),
    game(
        "echoes-of-the-city",
        "Echoes of the City",
        None,
        "en_desarrollo",
        v("principal", None, None),
        "Olyria Studio",
        "Argentina",
        ["PC"],
        ["terror", "aventura"],
        "Terror psicológico low poly ambientado en San Telmo y la Plaza Dorrego, vinculado a la memoria histórica y el folklore porteño.",
        {
            "regiones": ["Pampeana"],
            "provincias": ["Ciudad Autónoma de Buenos Aires"],
            "periodo_historico": ["siglo_xx", "contemporaneo"],
            "temas": ["historia", "memoria", "dictadura"],
        },
        {
            "fuentes_investigacion": [
                "https://elplanteo.com/echoes-of-the-city-videojuego-dictadura-argentina/"
            ],
        },
    ),
    game(
        "runa-legado-chaikuru-2025",
        "Runa y el Legado Chaikurú",
        2025,
        "publicado",
        v("principal", "principal", None),
        "Fanny Pack Studios",
        "Argentina",
        ["PC"],
        ["plataformas", "aventura", "accion"],
        "Plataformero 3D inspirado en los clásicos de los 90 con estética y mecánicas de cultura latinoamericana: mate, boleadoras, paisajes del norte argentino y fauna local.",
        {
            "regiones": ["Noroeste", "NOA"],
            "provincias": [],
            "periodo_historico": ["ficcion_sin_epoca"],
            "temas": ["cultura_popular", "geografia", "folclore"],
        },
        {
            "steam": "https://store.steampowered.com/app/2283470/Runa__The_Chaikuru_Legacy/",
            "fuentes_investigacion": [
                "https://pressover.news/analisis/runa-y-el-legado-chaikuru-plataformas-3d-made-in-argentina/"
            ],
        },
        personajes=[
            {
                "nombre": "Runa",
                "tipo": "arquetipo",
                "rol": "protagonista",
                "descripcion": "Investigadora en un mundo inspirado en culturas originarias y el NOA",
            }
        ],
    ),
    game(
        "don-ceferino-hazana",
        "Don Ceferino Hazaña",
        2004,
        "publicado",
        v(None, "principal", None),
        "Losersjuegos (Hugo Ruscitti, Walter Velázquez)",
        "Argentina",
        ["PC", "Linux", "Web"],
        ["arcade", "puzzle", "accion"],
        "Gaucho argentino debe rescatar su vaca de alienígenas en un juego estilo Super Pang. Ícono del desarrollo libre argentino.",
        {
            "regiones": ["Pampeana"],
            "provincias": [],
            "periodo_historico": ["ficcion_sin_epoca"],
            "temas": ["gauchesco", "humor"],
        },
        {
            "web_oficial": "https://hugoruscitti.github.io/losersjuegos.com.ar/juegos/ceferino.html",
            "fuentes_investigacion": [
                "https://hugoruscitti.github.io/losersjuegos.com.ar/juegos/ceferino.html"
            ],
        },
        personajes=[
            {
                "nombre": "Don Ceferino Hazaña",
                "tipo": "arquetipo",
                "rol": "protagonista",
                "descripcion": "Gaucho argentino protagonista",
            }
        ],
        metadatos={"idiomas": ["es"], "multijugador": False, "precio": "gratuito", "rating": {}, "tipo": "juego"},
    ),
    game(
        "trucotron",
        "Trucotron",
        1991,
        "publicado",
        v("principal", "principal", None),
        "Gustavo Abella, Ricardo Gayoso",
        "Argentina",
        ["Arcade"],
        ["arcade", "cartas", "simulacion"],
        "Primer arcade diseñado íntegramente en Argentina. Permite jugar al truco contra la máquina con hardware y software nacionales.",
        {
            "regiones": ["Pampeana"],
            "provincias": ["Ciudad Autónoma de Buenos Aires"],
            "periodo_historico": ["contemporaneo"],
            "temas": ["cultura_popular", "juegos_tradicionales"],
        },
        {
            "fuentes_investigacion": [
                "https://gameon2019.com/speaker/trucotron/",
                "https://oasisnerd.com/2026/06/16/industria-videojuegos-argentina/",
            ],
        },
        personajes=[
            {
                "nombre": "Jugador de truco",
                "tipo": "arquetipo",
                "rol": "protagonista",
                "descripcion": "Representa la cultura del truco argentino",
            }
        ],
    ),
    game(
        "pc-futbol-argentina-clausura-95",
        "PC Fútbol Argentina Clausura 95",
        1995,
        "publicado",
        v(None, None, "principal", "liga_futbol"),
        "Dinamic Multimedia",
        "España",
        ["PC"],
        ["deportes", "simulacion", "estrategia"],
        "Primera edición de PC Fútbol adaptada a la liga argentina con los 20 equipos del torneo Clausura 1995.",
        {
            "regiones": [],
            "provincias": [],
            "periodo_historico": ["contemporaneo"],
            "temas": ["deporte", "cultura_popular"],
        },
        {
            "fuentes_investigacion": [
                "https://www.kodromagazine.com/pc-futbol-argentina-clausura-95/"
            ],
        },
        deporte={
            "deporte": "futbol",
            "competicion": ["Primera División Argentina - Clausura 1995"],
            "equipos_destacados": [],
            "modo": "gestion_liga",
        },
    ),
    game(
        "pc-futbol-argentina-apertura-95",
        "PC Fútbol Argentina Apertura 95",
        1995,
        "publicado",
        v(None, None, "principal", "liga_futbol"),
        "Dinamic Multimedia",
        "España",
        ["PC"],
        ["deportes", "simulacion", "estrategia"],
        "Segunda edición argentina de PC Fútbol con el torneo Apertura 1995 y base de datos elaborada por periodistas locales.",
        {
            "regiones": [],
            "provincias": [],
            "periodo_historico": ["contemporaneo"],
            "temas": ["deporte"],
        },
        {
            "fuentes_investigacion": [
                "https://www.kodromagazine.com/pc-futbol-argentina-apertura-95/"
            ],
        },
        deporte={
            "deporte": "futbol",
            "competicion": ["Primera División Argentina - Apertura 1995"],
            "equipos_destacados": [],
            "modo": "gestion_liga",
        },
    ),
    game(
        "pc-futbol-argentina-40-apertura-96",
        "PC Fútbol Argentina 4.0 Apertura 96",
        1996,
        "publicado",
        v(None, None, "principal", "liga_futbol"),
        "Dinamic Multimedia",
        "España",
        ["PC"],
        ["deportes", "simulacion", "estrategia"],
        "Adaptación argentina de PC Fútbol 4.0 con modo Pro-Manager y torneo Apertura 1996 de la Primera División.",
        {
            "regiones": [],
            "provincias": [],
            "periodo_historico": ["contemporaneo"],
            "temas": ["deporte"],
        },
        {
            "fuentes_investigacion": [
                "https://www.kodromagazine.com/pc-futbol-argentina-4-0-apertura-96/",
                "https://www.devuego.es/bd/presskit/pc-futbol-argentina-40",
            ],
        },
        deporte={
            "deporte": "futbol",
            "competicion": ["Primera División Argentina - Apertura 1996"],
            "equipos_destacados": [],
            "modo": "gestion_liga",
        },
    ),
    game(
        "pc-futbol-50-apertura-97-argentina",
        "PC Fútbol 5.0 Apertura 97 (Argentina)",
        1997,
        "publicado",
        v(None, None, "principal", "liga_futbol"),
        "Dinamic Multimedia",
        "España",
        ["PC"],
        ["deportes", "simulacion", "estrategia"],
        "Edición argentina de PC Fútbol 5.0 con relato de Marcelo Araujo y torneo Apertura 1997.",
        {
            "regiones": [],
            "provincias": [],
            "periodo_historico": ["contemporaneo"],
            "temas": ["deporte"],
        },
        {
            "fuentes_investigacion": [
                "https://archive.org/details/pc-futbol-5.0-apertura-97"
            ],
        },
        deporte={
            "deporte": "futbol",
            "competicion": ["Primera División Argentina - Apertura 1997"],
            "equipos_destacados": [],
            "modo": "gestion_liga",
        },
    ),
    game(
        "futbol-deluxe-2004",
        "Fútbol Deluxe",
        2004,
        "publicado",
        v(None, None, "principal", "liga_futbol"),
        "Evoluxion / Edusoft",
        "Argentina",
        ["PC"],
        ["deportes", "simulacion", "estrategia"],
        "Manager de fútbol argentino con reglas locales, barras bravas, dopaje y mecánicas pensadas para el fútbol del país.",
        {
            "regiones": [],
            "provincias": [],
            "periodo_historico": ["contemporaneo"],
            "temas": ["deporte"],
        },
        {
            "wikipedia": "https://es.wikipedia.org/wiki/F%C3%BAtbol_Deluxe",
            "fuentes_investigacion": [
                "https://es.wikipedia.org/wiki/F%C3%BAtbol_Deluxe"
            ],
        },
        deporte={
            "deporte": "futbol",
            "competicion": ["Primera División Argentina"],
            "equipos_destacados": [],
            "modo": "gestion_liga",
        },
    ),
    game(
        "f11-football-manager",
        "F11 Football Manager",
        2023,
        "publicado",
        v(None, None, "principal", "liga_futbol"),
        "Gonzalo (desarrollador indie argentino)",
        "Argentina",
        ["Android"],
        ["deportes", "simulacion", "estrategia"],
        "Manager de fútbol móvil argentino considerado sucesor espiritual de PC Fútbol, con ligas y equipos del fútbol local.",
        {
            "regiones": [],
            "provincias": [],
            "periodo_historico": ["contemporaneo"],
            "temas": ["deporte"],
        },
        {
            "fuentes_investigacion": [
                "https://nogamingnews.com/f11-football-manager-el-sucesor-espiritual-y-argentino-del-pc-futbol"
            ],
        },
        deporte={
            "deporte": "futbol",
            "competicion": ["Ligas argentinas"],
            "equipos_destacados": [],
            "modo": "gestion_liga",
        },
        ejes_culturales=["deporte"],
        serie="pc-futbol-argentina",
        relacionado_con=["pc-futbol-70-argentina"],
        disponibilidad="a_la_venta",
    ),
    game(
        "pes-2014-afa",
        "Pro Evolution Soccer 2014 (Licencia AFA)",
        2013,
        "publicado",
        v(None, None, "principal", "liga_futbol"),
        "Konami",
        "Japón",
        ["PlayStation", "Xbox", "PC"],
        ["deportes", "simulacion"],
        "Primera entrega de PES con licencia completa de la Primera División argentina (20 equipos de la AFA).",
        {
            "regiones": [],
            "provincias": [],
            "periodo_historico": ["contemporaneo"],
            "temas": ["deporte"],
        },
        {
            "fuentes_investigacion": [
                "https://www.hobbyconsolas.com/noticias/pes-2014-adquiere-licencia-primera-division-argentina-55248"
            ],
        },
        deporte={
            "deporte": "futbol",
            "competicion": ["Primera División Argentina"],
            "equipos_destacados": ["Boca Juniors", "River Plate"],
            "modo": "simulacion_partido",
        },
    ),
    game(
        "efootball-pes-2020-superliga",
        "eFootball PES 2020 (Superliga Quilmes Clásica)",
        2019,
        "publicado",
        v(None, None, "principal", "liga_futbol"),
        "Konami",
        "Japón",
        ["PlayStation", "Xbox", "PC"],
        ["deportes", "simulacion"],
        "Incluye la Superliga Quilmes Clásica con 24 clubes argentinos como contenido licenciado central en el mercado local.",
        {
            "regiones": [],
            "provincias": [],
            "periodo_historico": ["contemporaneo"],
            "temas": ["deporte"],
        },
        {
            "fuentes_investigacion": [
                "https://www.clarin.com/tecnologia/boca-river-protagonistas-pes-2020-hizo-presentacion-oficial-argentina_0_8n81eXsKH.html"
            ],
        },
        deporte={
            "deporte": "futbol",
            "competicion": ["Superliga Argentina"],
            "equipos_destacados": ["Boca Juniors", "River Plate"],
            "modo": "simulacion_partido",
        },
    ),
    game(
        "argie-el-carpincho",
        "ARGIE - El Carpincho",
        None,
        "publicado",
        v("principal", "principal", None),
        "Jorge Ayala / UNPAZ-CUDI",
        "Argentina",
        ["PC"],
        ["plataformas", "educativo"],
        "Plataformero 2D educativo donde Argie, un carpincho, viaja por Argentina aprendiendo geografía mientras recolecta matecitos.",
        {
            "regiones": ["Nacional"],
            "provincias": [],
            "periodo_historico": ["contemporaneo"],
            "temas": ["geografia", "educacion"],
        },
        {
            "itch": "https://argiegames.itch.io/argie",
            "fuentes_investigacion": ["https://argiegames.itch.io/argie"],
        },
        personajes=[
            {
                "nombre": "Argie",
                "tipo": "arquetipo",
                "rol": "protagonista",
                "descripcion": "Carpincho mascota que recorre el país",
            }
        ],
        metadatos={"idiomas": ["es"], "multijugador": False, "precio": "gratuito", "rating": {}, "tipo": "juego"},
    ),
    game(
        "tincho-aventuras-a-la-carta",
        "Tincho Aventuras a la Carta",
        None,
        "publicado",
        v("principal", "principal", None),
        "Estudio argentino",
        "Argentina",
        ["PC"],
        ["plataformas", "aventura", "educativo"],
        "Plataformero 2.5D donde Tincho el carpincho recorre regiones argentinas explorando la gastronomía local con animales autóctonos.",
        {
            "regiones": ["Nacional"],
            "provincias": [],
            "periodo_historico": ["contemporaneo"],
            "temas": ["geografia", "gastronomia", "fauna"],
        },
        {
            "steam": "https://store.steampowered.com/app/2172050/Tincho_Aventuras_a_la_Carta/",
            "fuentes_investigacion": [
                "https://store.steampowered.com/app/2172050/Tincho_Aventuras_a_la_Carta/"
            ],
        },
        personajes=[
            {
                "nombre": "Tincho",
                "tipo": "arquetipo",
                "rol": "protagonista",
                "descripcion": "Carpincho que explora la cocina argentina",
            }
        ],
        metadatos={"idiomas": ["es"], "multijugador": False, "precio": "gratuito", "rating": {}, "tipo": "juego"},
    ),
    game(
        "carmen-aventuras-en-el-pasado",
        "Carmen: aventuras en el pasado",
        None,
        "publicado",
        v("principal", "principal", None),
        "Videojuego Carmen Funes / Archivo-Museo Carmen Funes",
        "Argentina",
        ["Android", "Web"],
        ["aventura", "educativo"],
        "Aventura gráfica educativa sobre la historia de Plaza Huincul (Neuquén) a través de la fortinera Carmen Funes y el descubrimiento del petróleo.",
        {
            "regiones": ["Patagonia"],
            "provincias": ["Neuquén"],
            "periodo_historico": ["siglo_xix", "siglo_xx"],
            "temas": ["historia", "patrimonio", "petroleo"],
        },
        {
            "itch": "https://video-juego-carmen-funes.itch.io/carmen-aventuras-en-el-pasado-saga-1",
            "fuentes_investigacion": [
                "https://icom.museum/en/news/museums-video-games-two-projects-developed-in-argentina/"
            ],
        },
        personajes=[
            {
                "nombre": "Carmen Funes",
                "tipo": "historico",
                "rol": "protagonista",
                "descripcion": "Fortinera y figura histórica de Plaza Huincul",
            }
        ],
    ),
    game(
        "busqueda-interestelar",
        "Búsqueda Interestelar",
        None,
        "publicado",
        v("principal", "principal", None),
        "Museo Histórico Sarmiento",
        "Argentina",
        ["PC"],
        ["plataformas", "educativo"],
        "Plataformero educativo sobre la creación del Observatorio Astronómico de Córdoba durante la presidencia de Domingo Faustino Sarmiento.",
        {
            "regiones": ["Centro"],
            "provincias": ["Córdoba"],
            "periodo_historico": ["siglo_xix"],
            "temas": ["historia", "ciencia", "educacion"],
        },
        {
            "fuentes_investigacion": [
                "https://icom.museum/en/news/museums-video-games-two-projects-developed-in-argentina/"
            ],
        },
        personajes=[
            {
                "nombre": "Domingo Faustino Sarmiento",
                "tipo": "historico",
                "rol": "secundario",
                "descripcion": "Contexto histórico del observatorio cordobés",
            }
        ],
    ),
    game(
        "bitacoras-patrias-remedios",
        "Bitácoras Patrias: Remedios del Valle",
        None,
        "publicado",
        v(None, "principal", None),
        "Paz Rozen, Amadis, Cecilia Verino",
        "Argentina",
        ["Web"],
        ["educativo", "aventura"],
        "Colección de minijuegos educativos sobre Remedios del Valle, prócer de las invasiones inglesas, la Campaña del Alto Perú y la Batalla de Salta.",
        {
            "regiones": ["Noroeste", "Centro"],
            "provincias": ["Salta", "Buenos Aires"],
            "periodo_historico": ["independencia"],
            "temas": ["historia", "genero", "educacion"],
        },
        {
            "itch": "https://bitacoraspatrias.itch.io/",
            "fuentes_investigacion": ["https://bitacoraspatrias.itch.io/"],
        },
        personajes=[
            {
                "nombre": "Remedios del Valle",
                "tipo": "historico",
                "rol": "protagonista",
                "descripcion": "Prócer de la independencia argentina",
            }
        ],
        metadatos={"idiomas": ["es"], "multijugador": False, "precio": "gratuito", "rating": {}, "tipo": "juego"},
    ),
    game(
        "mapampa",
        "Mapampa",
        None,
        "publicado",
        v("principal", None, None),
        "Desarrollador argentino",
        "Argentina",
        ["Web"],
        ["educativo", "puzzle", "trivia"],
        "Juego web de geografía argentina con modos competitivo y de aprendizaje sobre provincias, capitales y banderas.",
        {
            "regiones": ["Nacional"],
            "provincias": [],
            "periodo_historico": ["contemporaneo"],
            "temas": ["geografia", "educacion"],
        },
        {
            "web_oficial": "https://www.mapampa.com.ar/",
            "fuentes_investigacion": ["https://www.mapampa.com.ar/"],
        },
        metadatos={"idiomas": ["es"], "multijugador": True, "precio": "gratuito", "rating": {}, "tipo": "juego"},
    ),
    game(
        "perfil-de-riesgo-casos-federales",
        "Perfil de Riesgo: Casos Federales",
        2008,
        "publicado",
        v("principal", None, None),
        "Nucleosys / Sabarasa (comisión AFIP)",
        "Argentina",
        ["PC"],
        ["aventura", "educativo"],
        "Aventura point-and-click encargada por la AFIP donde Martina recorre regiones argentinas resolviendo casos vinculados a impuestos y cultura tributaria.",
        {
            "regiones": ["Patagonia", "Noroeste", "Mesopotamia", "Pampeana"],
            "provincias": [],
            "periodo_historico": ["contemporaneo"],
            "temas": ["educacion", "geografia", "cultura_ciudadana"],
        },
        {
            "mobygames": "https://www.mobygames.com/game/50720/perfil-de-riesgo-casos-federales/",
            "fuentes_investigacion": [
                "https://www.mobygames.com/game/50720/perfil-de-riesgo-casos-federales/"
            ],
        },
    ),
    game(
        "tango-the-adventure-game",
        "Tango: The Adventure Game",
        2018,
        "publicado",
        v("principal", "principal", None),
        "Estudio argentino",
        "Argentina",
        ["PC"],
        ["aventura", "point_and_click"],
        "Aventura gráfica humorística sobre tango que comienza en la cárcel de Ushuaia y continúa hacia Buenos Aires, con referencias a Carlos Gardel.",
        {
            "regiones": ["Patagonia", "Pampeana"],
            "provincias": ["Tierra del Fuego", "Ciudad Autónoma de Buenos Aires"],
            "periodo_historico": ["siglo_xx"],
            "temas": ["tango", "cultura_urbana"],
        },
        {
            "mobygames": "https://www.mobygames.com/game/117299/tango-the-adventure-game/",
            "fuentes_investigacion": [
                "https://www.mobygames.com/game/117299/tango-the-adventure-game/"
            ],
        },
        personajes=[
            {
                "nombre": "Carlos",
                "tipo": "arquetipo",
                "rol": "protagonista",
                "descripcion": "Bailarín de tango inspirado en la cultura porteña",
            }
        ],
    ),
    game(
        "sol-705-2020",
        "Sol 705",
        2020,
        "publicado",
        v("principal", None, None),
        "Patricio Land",
        "Argentina",
        ["PC"],
        ["aventura", "point_and_click"],
        "Aventura gráfica ambientada en un pueblo ficticio de la provincia de Buenos Aires en los años 70, con rock nacional y ovnis.",
        {
            "regiones": ["Pampeana"],
            "provincias": ["Buenos Aires"],
            "periodo_historico": ["siglo_xx"],
            "temas": ["cultura_popular", "ovnis"],
        },
        {
            "steam": "https://store.steampowered.com/app/1316770/Sol_705/",
            "fuentes_investigacion": [
                "https://www.extragamers.com.ar/2022/04/juegos-argentinos-ambientados-en-buenos-aires.html"
            ],
        },
    ),
    game(
        "yo-matias-suenos-peligrosos",
        "Yo Matías: Sueños Peligrosos",
        1999,
        "publicado",
        v(None, "principal", None),
        "Caimán Co. / PC3",
        "Argentina",
        ["PC"],
        ["plataformas", "aventura"],
        "Aventura basada en el personaje de la tira cómica argentina Yo Matías creada por Sendra.",
        {
            "regiones": ["Pampeana"],
            "provincias": [],
            "periodo_historico": ["contemporaneo"],
            "temas": ["cultura_popular", "humor"],
        },
        {
            "fuentes_investigacion": [
                "https://www.abandonsocios.org/index.php?topic=15458.0"
            ],
        },
        personajes=[
            {
                "nombre": "Matías",
                "tipo": "literario",
                "rol": "protagonista",
                "descripcion": "Personaje de tira cómica argentina de Sendra",
            }
        ],
        metadatos={"idiomas": ["es"], "multijugador": False, "precio": None, "rating": {}, "tipo": "juego"},
    ),
    game(
        "super-menem-bros",
        "Super Menem Bros",
        1993,
        "publicado",
        v(None, "principal", None),
        "Super Bit (revista)",
        "Argentina",
        ["PC"],
        ["plataformas", "arcade"],
        "Parodia argentina de Super Mario Bros protagonizada por Carlos Menem y enemigos de la política de los 90.",
        {
            "regiones": ["Pampeana"],
            "provincias": [],
            "periodo_historico": ["contemporaneo"],
            "temas": ["politica", "humor", "cultura_popular"],
        },
        {
            "fuentes_investigacion": [
                "https://www.tribunahacker.com.ar/606/"
            ],
        },
        personajes=[
            {
                "nombre": "Carlos Menem",
                "tipo": "politico",
                "rol": "protagonista",
                "descripcion": "Presidente argentino parodiado como héroe de plataformas",
            }
        ],
        ejes_culturales=["politica", "satira"],
        tipo_obra="fan_game",
        grado_relevancia_argentina="importante",
        sensibilidad="media",
        disponibilidad="abandonware",
        metadatos={"idiomas": ["es"], "multijugador": False, "precio": None, "rating": {}, "tipo": "juego"},
    ),
    game(
        "hitman-3-mendoza",
        "Hitman 3 — Mendoza",
        2021,
        "publicado",
        v("referencia_menor", None, None),
        "IO Interactive",
        "Dinamarca",
        ["PC", "PlayStation", "Xbox"],
        ["sigilo", "accion"],
        "Misión 'The Farewell' ambientada en viñedos de Mendoza con cultura argentina: tango, asado, mate y vino.",
        {
            "regiones": ["Cuyo"],
            "provincias": ["Mendoza"],
            "periodo_historico": ["contemporaneo"],
            "temas": ["geografia", "gastronomia"],
        },
        {
            "fuentes_investigacion": [
                "https://www.infobae.com/gaming/2021/01/17/9-videojuegos-con-niveles-ambientados-en-argentina-y-la-eleccion-de-mendoza-para-hitman-3/"
            ],
        },
    ),
    game(
        "prisoner-of-ice-argentina",
        "Prisoner of Ice",
        1995,
        "publicado",
        v("referencia_menor", None, None),
        "Infogrames",
        "Francia",
        ["PC", "PlayStation", "Sega Saturn"],
        ["aventura", "terror"],
        "Aventura lovecraftiana con segmentos en una base en las Islas Malvinas y la Biblioteca de la Universidad de Buenos Aires.",
        {
            "regiones": ["Patagonia", "Pampeana"],
            "provincias": ["Ciudad Autónoma de Buenos Aires"],
            "periodo_historico": ["siglo_xx"],
            "temas": ["historia", "literatura"],
        },
        {
            "fuentes_investigacion": [
                "https://www.infobae.com/gaming/2021/01/17/9-videojuegos-con-niveles-ambientados-en-argentina-y-la-eleccion-de-mendoza-para-hitman-3/"
            ],
        },
    ),
    game(
        "gaucho-runner",
        "Gaucho Runner",
        None,
        "en_desarrollo",
        v("principal", "principal", None),
        "La Ciudadela Studios",
        "Argentina",
        ["PC"],
        ["carreras", "accion", "fps"],
        "Runner en primera persona donde un gaucho atraviesa Bariloche, la pampa y Buenos Aires combatiendo soldados españoles.",
        {
            "regiones": ["Patagonia", "Pampeana"],
            "provincias": ["Río Negro", "Ciudad Autónoma de Buenos Aires"],
            "periodo_historico": ["independencia"],
            "temas": ["gauchesco", "historia"],
        },
        {
            "itch": "https://jerestein-dev.itch.io/gaucho-runner",
            "fuentes_investigacion": ["https://jerestein-dev.itch.io/gaucho-runner"],
        },
        personajes=[
            {
                "nombre": "Gaucho",
                "tipo": "arquetipo",
                "rol": "protagonista",
                "descripcion": "Gaucho libertador en un runner FPS",
            }
        ],
    ),
    game(
        "gaucho-power",
        "GAUCHO POWER",
        None,
        "en_desarrollo",
        v("principal", "principal", None),
        "Equipo Gaucho Power (Salta)",
        "Argentina",
        ["Web"],
        ["sigilo", "aventura"],
        "Juego de sigilo sobre la Guerra Gaucha y las milicias del noroeste argentino durante la independencia.",
        {
            "regiones": ["Noroeste"],
            "provincias": ["Salta"],
            "periodo_historico": ["independencia"],
            "temas": ["historia", "gauchesco"],
        },
        {
            "itch": "https://revirado.itch.io/gaucho-power",
            "fuentes_investigacion": ["https://revirado.itch.io/gaucho-power"],
        },
    ),
    game(
        "el-intruso-82",
        "El Intruso 82",
        2026,
        "publicado",
        v("principal", None, None),
        "Emilio Kolomenski et al.",
        "Argentina",
        ["PC", "Web"],
        ["accion", "aventura"],
        "Juego de la Global Game Jam 2026: un soldado argentino debe sobrevivir en un barco inglés durante la Guerra de Malvinas.",
        {
            "regiones": ["Atlántico Sur"],
            "provincias": [],
            "periodo_historico": ["siglo_xx"],
            "temas": ["guerra_de_malvinas"],
        },
        {
            "itch": "https://emiliokolo.itch.io/el-intruso-82",
            "fuentes_investigacion": ["https://emiliokolo.itch.io/el-intruso-82"],
        },
    ),
    game(
        "operacion-rosario",
        "Operación Rosario",
        None,
        "publicado",
        v("principal", None, None),
        "Equipo indie argentino",
        "Argentina",
        ["PC"],
        ["accion", "shooter"],
        "Shooter sobre la Guerra de Malvinas con perspectiva de soldado o piloto de Super Étendard.",
        {
            "regiones": ["Patagonia", "Atlántico Sur"],
            "provincias": [],
            "periodo_historico": ["siglo_xx"],
            "temas": ["guerra_de_malvinas"],
        },
        {
            "itch": "https://a-m-o-g-u-s-u-s.itch.io/operacion-rosario",
            "fuentes_investigacion": ["https://a-m-o-g-u-s-u-s.itch.io/operacion-rosario"],
        },
    ),
    game(
        "argentina-recicla",
        "Argentina Recicla",
        None,
        "publicado",
        v("principal", None, None),
        "Akademico77 / Ministerio de Desarrollo Social",
        "Argentina",
        ["PC"],
        ["plataformas", "puzzle", "educativo"],
        "Serious game del programa Argentina Recicla sobre buenas prácticas de reciclado y el rol de recuperadoras urbanas.",
        {
            "regiones": ["Nacional"],
            "provincias": [],
            "periodo_historico": ["contemporaneo"],
            "temas": ["medio_ambiente", "educacion"],
        },
        {
            "itch": "https://hiebaum.itch.io/argentina-recicla",
            "fuentes_investigacion": ["https://hiebaum.itch.io/argentina-recicla"],
        },
        metadatos={"idiomas": ["es"], "multijugador": False, "precio": "gratuito", "rating": {}, "tipo": "juego"},
    ),
]

# Regnum excluido: no cumple criterios temáticos de v1 (fantasía sin vínculo argentino jugable)


def build_schema():
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Videojuego vinculado a Argentina",
        "type": "object",
        "required": [
            "id",
            "titulo",
            "estado",
            "vinculo_argentina",
            "desarrollador",
            "pais_desarrollo",
            "plataformas",
            "generos",
            "descripcion",
            "contexto_argentino",
            "enlaces",
            "verificado",
            "fecha_actualizacion",
        ],
        "properties": {
            "id": {"type": "string"},
            "titulo": {"type": "string"},
            "titulo_original": {"type": "string"},
            "anio": {"type": ["integer", "null"]},
            "estado": {
                "enum": [
                    "publicado",
                    "early_access",
                    "en_desarrollo",
                    "cancelado",
                    "abandonware",
                    "prototipo",
                ]
            },
            "vinculo_argentina": {"type": "object"},
            "personajes_argentinos": {"type": "array"},
            "deporte_argentino": {"type": ["object", "null"]},
            "desarrollador": {"type": "string"},
            "pais_desarrollo": {"type": "string"},
            "plataformas": {"type": "array", "items": {"type": "string"}},
            "generos": {"type": "array", "items": {"type": "string"}},
            "descripcion": {"type": "string"},
            "contexto_argentino": {"type": "object"},
            "enlaces": {"type": "object"},
            "imagenes": {"type": "object"},
            "metadatos": {"type": "object"},
            "ejes_culturales": {
                "type": "array",
                "items": {
                    "enum": [
                        "politica",
                        "satira",
                        "folclore",
                        "juegos_tradicionales",
                        "historia",
                        "memoria",
                        "cultura_urbana",
                        "historieta",
                        "literatura",
                        "educativo",
                        "deporte",
                        "geografia",
                        "migracion",
                        "musica",
                    ]
                },
            },
            "tipo_obra": {
                "enum": [
                    "comercial",
                    "indie",
                    "educativo",
                    "jam",
                    "mod",
                    "fan_game",
                    "abandonware",
                    "prototipo",
                    "promocional",
                ]
            },
            "grado_relevancia_argentina": {
                "enum": ["central", "importante", "menor"]
            },
            "calidad_fuente": {
                "enum": ["oficial", "tienda", "prensa", "wiki", "foro", "archive"]
            },
            "sensibilidad": {"enum": ["baja", "media", "alta"]},
            "serie": {"type": ["string", "null"]},
            "edicion": {"type": ["string", "null"]},
            "relacionado_con": {"type": "array", "items": {"type": "string"}},
            "disponibilidad": {
                "enum": [
                    "a_la_venta",
                    "gratis",
                    "abandonware",
                    "perdido",
                    "desconocido",
                ]
            },
            "verificado": {"type": "boolean"},
            "fecha_actualizacion": {"type": "string"},
        },
    }


def build_raw_candidates():
    """Lee el CSV curado por harvest_candidates.py; no regenera duplicados."""
    csv_path = DATA / "raw_candidates.csv"
    if not csv_path.exists():
        return []
    with open(csv_path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def stats(games):
    from collections import Counter

    plat = Counter(p for g in games for p in g["plataformas"])
    gen = Counter(genre for g in games for genre in g["generos"])
    vinc = Counter()
    for g in games:
        va = g["vinculo_argentina"]
        if va["escenario"]["activo"]:
            vinc["escenario"] += 1
        if va["protagonista"]["activo"]:
            vinc["protagonista"] += 1
        if va["deporte_argentino"]["activo"]:
            vinc["deporte_argentino"] += 1
    return plat, gen, vinc


def load_all_games():
    games = list(GAMES)
    for mod_name in (
        "games_extra",
        "games_batch3",
        "games_politica",
        "games_folclore",
        "games_educativos",
    ):
        try:
            mod = __import__(mod_name)
            for attr in (
                "EXTRA_GAMES",
                "BATCH3",
                "POLITICA_GAMES",
                "FOLCLORE_GAMES",
                "EDUCATIVOS_GAMES",
            ):
                extra = getattr(mod, attr, None)
                if extra:
                    games.extend(extra)
        except ImportError:
            pass
    return games


def apply_v11_defaults(g):
    """Retrocompatibilidad: defaults editoriales v1.1."""
    g.setdefault("ejes_culturales", [])
    g.setdefault("tipo_obra", "comercial")
    g.setdefault("formato", "juego_base")
    g.setdefault("grado_relevancia_argentina", "central")
    g.setdefault("calidad_fuente", "prensa")
    g.setdefault("sensibilidad", "baja")
    g.setdefault("serie", None)
    g.setdefault("edicion", None)
    g.setdefault("relacionado_con", [])
    g.setdefault("disponibilidad", "desconocido")
    return g


PC_FUTBOL_SERIES = {
    "pc-futbol-argentina-clausura-95": "Clausura 95",
    "pc-futbol-argentina-apertura-95": "Apertura 95",
    "pc-futbol-argentina-40-apertura-96": "4.0 Apertura 96",
    "pc-futbol-50-apertura-97-argentina": "5.0 Apertura 97",
    "pc-futbol-60-argentina": "6.0",
    "pc-futbol-70-argentina": "7.0",
}


EJES_BY_ID = {
    "la-salamanca": ["folclore"],
    "luz-mala": ["folclore"],
    "flora-ceibo-seeds": ["folclore", "memoria"],
    "anahi-juego": ["folclore", "memoria"],
    "conur-life": ["cultura_urbana"],
    "bienvenidos-a-la-matanza": ["cultura_urbana"],
    "portenolandia": ["cultura_urbana"],
    "simuladron": ["politica", "satira"],
    "truco-arbiser-1982": ["juegos_tradicionales"],
    "truco-blyts": ["juegos_tradicionales"],
    "trucotron": ["juegos_tradicionales"],
}


def apply_series_patches(g):
    g = apply_v11_defaults(g)
    if g["id"] in EJES_BY_ID:
        g["ejes_culturales"] = EJES_BY_ID[g["id"]]
    if g["id"] in PC_FUTBOL_SERIES:
        g["serie"] = "pc-futbol-argentina"
        g["edicion"] = PC_FUTBOL_SERIES[g["id"]]
        g["relacionado_con"] = [
            x for x in PC_FUTBOL_SERIES if x != g["id"]
        ]
        if "deporte" not in g["ejes_culturales"]:
            g["ejes_culturales"] = [*g["ejes_culturales"], "deporte"]
        g["disponibilidad"] = "abandonware"
    if g["id"] in ("golazo-soccer-league", "golazo-2"):
        g["grado_relevancia_argentina"] = "menor"
        if "deporte" not in g["ejes_culturales"]:
            g["ejes_culturales"] = [*g["ejes_culturales"], "deporte"]
    if g["id"] in ("mobbyt-provincias-capitales", "mobbyt-banderas-provincias"):
        g["relacionado_con"] = [
            x
            for x in (
                "mobbyt-geografia-argentina",
                "mobbyt-provincias-capitales",
                "mobbyt-banderas-provincias",
            )
            if x != g["id"]
        ]
        g["ejes_culturales"] = ["educativo", "geografia"]
        g["tipo_obra"] = "educativo"
        g["disponibilidad"] = "gratis"
    return g


def stats_v11(games):
    from collections import Counter

    ejes = Counter(e for g in games for e in g.get("ejes_culturales", []))
    grados = Counter(g.get("grado_relevancia_argentina", "central") for g in games)
    disp = Counter(g.get("disponibilidad", "desconocido") for g in games)
    return ejes, grados, disp


def main():
    global GAMES
    from descartados_data import DESCARTADOS, DESCARTADOS_IDS

    GAMES = [apply_series_patches(g) for g in load_all_games()]
    DATA.mkdir(parents=True, exist_ok=True)

    all_active = [g for g in GAMES if g["id"] not in DESCARTADOS_IDS]
    pendientes = [g for g in all_active if not g["verificado"]]
    verificados = [g for g in all_active if g["verificado"]]

    with open(DATA / "games.json", "w", encoding="utf-8") as f:
        json.dump(verificados, f, ensure_ascii=False, indent=2)

    with open(DATA / "schema.json", "w", encoding="utf-8") as f:
        json.dump(build_schema(), f, ensure_ascii=False, indent=2)

    with open(DATA / "pendientes.json", "w", encoding="utf-8") as f:
        json.dump(pendientes, f, ensure_ascii=False, indent=2)

    with open(DATA / "descartados.json", "w", encoding="utf-8") as f:
        json.dump(DESCARTADOS, f, ensure_ascii=False, indent=2)

    rows = build_raw_candidates()
    plat, gen, vinc = stats(verificados)
    ejes, grados, disp = stats_v11(verificados)
    csv_triage = Counter(r.get("estado_triage", "candidato") for r in rows) if rows else Counter()

    readme = f"""# Base de datos — Videojuegos vinculados a Argentina

## Criterios de inclusión (v1.1)

Un juego entra si cumple al menos una condición:

1. **Escenario argentino** — mapas, niveles o ambientación jugable en Argentina
2. **Protagonista argentino** — figuras de historia, cultura, folclore o política
3. **Deporte argentino** — ligas/equipos argentinos como eje central (ej. PC Fútbol Ed. Argentina)

**Excluido:** FIFA/PES genéricos donde Argentina es solo una selección; juegos con solo desarrollador argentino sin temática AR.

### Campos editoriales v1.1

- `ejes_culturales` — política, sátira, folclore, memoria, cultura urbana, etc.
- `tipo_obra` — comercial, indie, educativo, jam, mod, promocional…
- `grado_relevancia_argentina` — central, importante, menor
- `sensibilidad` — baja, media, alta (dictadura, Malvinas, política partidaria)
- `serie` / `edicion` / `relacionado_con` — variantes y colecciones
- `disponibilidad` — a_la_venta, gratis, abandonware, perdido

### Política educativos (mixto)

- **Colección:** trivias genéricas Mobbyt → una entrada con sublista en descripción
- **Individual:** Mapampa, Bitácoras Patrias, Carmen, etc.

## Playbook de búsqueda

| Fuente | Uso |
|--------|-----|
| Steam / itch.io | Indies y jams argentinos |
| EVA Play / ADVA / devuego.lat | Catálogo nacional |
| archive.org | Flash/HTML5 perdidos (2005–2015) |
| MobyGames / IGDB | Historieta y abandonware |
| Prensa AR (Press Over, Infobae, El Planteo) | Política, sátira, lanzamientos |
| Mobbyt | Educativos escolares |

Keywords por eje: `peronismo juego`, `gorila game`, `lobizón`, `gauchito gil`, `truco android`, `pc futbol argentina`, `conurbano gta`, `malvinas juego`.

## Estadísticas (v1.1)

| Métrica | Valor |
|---------|-------|
| Juegos verificados | {len(verificados)} |
| Pendientes de verificar | {len(pendientes)} |
| Descartados documentados | {len(DESCARTADOS)} |
| Candidatos en CSV | {len(rows)} |
| CSV en triage candidato | {csv_triage.get('candidato', 0)} |
| Con vínculo escenario | {vinc['escenario']} |
| Con vínculo protagonista | {vinc['protagonista']} |
| Con vínculo deporte | {vinc['deporte_argentino']} |

### Por grado de relevancia

{chr(10).join(f'- {k}: {v}' for k, v in grados.most_common())}

### Por eje cultural (top)

{chr(10).join(f'- {k}: {v}' for k, v in ejes.most_common(12)) or '- (sin etiquetar aún)'}

### Por plataforma (top)

{chr(10).join(f'- {k}: {v}' for k, v in plat.most_common(8))}

### Por género (top)

{chr(10).join(f'- {k}: {v}' for k, v in gen.most_common(10))}

## Archivos

- `games.json` — base principal verificada
- `schema.json` — esquema de validación
- `pendientes.json` — entradas sin verificar
- `descartados.json` — exclusiones documentadas
- `raw_candidates.csv` — candidatos con columnas de triage
- `CHANGELOG.md` — historial de versiones

Actualizado: {TODAY}
"""
    (DATA / "README.md").write_text(readme, encoding="utf-8")

    changelog = f"""# Changelog — Base de videojuegos argentinos

## v1.1 ({TODAY})

### Cambios principales
- Ampliación de candidatos en `raw_candidates.csv` con columnas de triage
- Nuevos campos editoriales: `ejes_culturales`, `tipo_obra`, `grado_relevancia_argentina`, `sensibilidad`, `serie`, `disponibilidad`
- Verificación unificada de 28 pendientes v1
- Nuevas entradas: política/sátira (Cristina vs Gorilas, Menem La Hizo, Evita y Perón contra los Gorilas)
- Colecciones educativas Mobbyt
- Archivo `descartados.json` con exclusiones documentadas

### Conteos
| Métrica | v1 | v1.1 |
|---------|-----|------|
| Verificados | 68 | {len(verificados)} |
| Pendientes | 28 | {len(pendientes)} |
| Descartados | 0 | {len(DESCARTADOS)} |
| Candidatos CSV | 116 | {len(rows)} |

### Exclusiones notables
- **Roots of Pacha** — solo desarrollo argentino, sin temática AR
- **Dark Rage** — shoot'em up sin vínculo temático argentino
- **FIFA 23 / PES 2021** — selección entre muchas

### Ajustes editoriales
- **Golazo!** reclasificado como `grado_relevancia_argentina: menor`
- Saga **PC Fútbol Argentina** normalizada con `serie` y `relacionado_con`
"""
    (DATA / "CHANGELOG.md").write_text(changelog, encoding="utf-8")

    print(
        f"Generados {len(verificados)} verificados, {len(pendientes)} pendientes, "
        f"{len(DESCARTADOS)} descartados, {len(rows)} candidatos CSV"
    )


if __name__ == "__main__":
    main()
