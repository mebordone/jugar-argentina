#!/usr/bin/env python3
"""Enlaces jugables curados para juegos que solo tenían fuentes de prensa."""
from __future__ import annotations

PLAY_LINK_PATCHES: dict[str, dict[str, str]] = {
    # Indies argentinos en Steam (IDs verificados con Steam Store API)
    "deep-beyond-2024": {
        "steam": "https://store.steampowered.com/app/2841720/Deep_Beyond/",
    },
    "desvelado-2024": {
        "steam": "https://store.steampowered.com/app/2878710/Desvelado/",
    },
    "echoes-of-the-city": {
        "steam": "https://store.steampowered.com/app/3616220/Echoes_Of_The_City/",
    },
    "la-salamanca": {
        "steam": "https://store.steampowered.com/app/3025180/La_Salamanca/",
    },
    "luz-mala": {
        "steam": "https://store.steampowered.com/app/2776360/Luz_Mala/",
    },
    "f11-football-manager": {
        "steam": "https://store.steampowered.com/app/3465170/F11_Football_Manager/",
    },
    "noir-storm": {
        "steam": "https://store.steampowered.com/app/1845980/Noir_Storm/",
    },
    "conur-life": {
        "steam": "https://store.steampowered.com/app/1888330/Conur_Life/",
    },
    "farol-del-diablo": {
        "steam": "https://store.steampowered.com/app/3544060/Farol_del_Diablo/",
    },
    "los-infernales": {
        "steam": "https://store.steampowered.com/app/2650400/Los_Infernales/",
    },
    "fabulas-portenas": {
        "steam": "https://store.steampowered.com/app/3279900/Portens/",
    },
    "caba-demo-hypnos": {
        "steam": "https://store.steampowered.com/app/3279900/CABA/",
    },
    "slender-threads": {
        "steam": "https://store.steampowered.com/app/1116480/Slender_Threads/",
    },
    "stellar-mess-princess-conundrum": {
        "steam": "https://store.steampowered.com/app/1507530/Stellar_Mess_The_Princess_Conundrum/",
    },
    "tango-the-adventure-game": {
        "steam": "https://store.steampowered.com/app/888010/Tango_The_Adventure_Game/",
    },
    "portenolandia": {
        "steam": "https://store.steampowered.com/app/3588830/Portenolandia/",
    },
    "simuladron": {
        "steam": "https://store.steampowered.com/app/4094990/SimuLadron/",
    },
    # Referencias internacionales con escenario argentino
    "hitman-3-mendoza": {
        "steam": "https://store.steampowered.com/app/1659040/HITMAN_World_of_Assassination/",
    },
    "ara-history-untold-evita": {
        "steam": "https://store.steampowered.com/app/2021880/Ara_History_Untold/",
        "web_oficial": "https://www.oxidegames.com/",
    },
    "cod-ghosts-clockwork": {
        "steam": "https://store.steampowered.com/app/209160/Call_of_Duty_Ghosts/",
    },
    "bloodrayne-argentina": {
        "steam": "https://store.steampowered.com/app/1373510/BloodRayne_Terminal_Cut/",
    },
    "civ6-buenos-aires": {
        "steam": "https://store.steampowered.com/app/289070/Sid_Meiers_Civilization_VI/",
    },
    "prisoner-of-ice-argentina": {
        "steam": "https://store.steampowered.com/app/359620/Call_of_Cthulhu_Prisoner_of_Ice/",
    },
    "syndicate-buenos-aires": {
        "steam": "https://store.steampowered.com/app/4980/Syndicate/",
    },
    "fast-furious-showdown-aeroparque": {
        "steam": "https://store.steampowered.com/app/243070/Fast_Furious_Showdown/",
    },
    "chameleon-buenos-aires": {
        "web_oficial": "https://www.gog.com/game/chameleon_deluxe_opera",
    },
    "battlefield-bad-company-2-andes": {
        "web_oficial": "https://www.ea.com/games/battlefield/battlefield-bad-company-2",
    },
    # Abandonware y preservación
    "malvinas-2032": {
        "archive": "https://www.myabandonware.com/game/malvinas-2032-e5m",
    },
    "aconcagua-1999": {
        "archive": "https://coolrom.com/roms/psx/a/",
    },
    "futbol-deluxe-2004": {
        "archive": "https://redump.org/disc/99941/",
    },
    "pc-futbol-50-apertura-97-argentina": {
        "archive": "https://www.pcfutbol.com/",
    },
    "pc-futbol-60-argentina": {
        "archive": "https://www.dekazeta.net/foro/files/file/4226-pc-f%C3%BAtbol-60-argentina/",
    },
    "pc-futbol-70-argentina": {
        "archive": "https://www.pcfutbol.com/",
    },
    "pc-futbol-argentina-40-apertura-96": {
        "archive": "https://www.pcfutbol.com/",
    },
    "pc-futbol-argentina-apertura-95": {
        "archive": "https://www.pcfutbol.com/",
    },
    "pc-futbol-argentina-clausura-95": {
        "archive": "https://www.pcfutbol.com/",
    },
    # Web, mods y sitios oficiales
    "busqueda-interestelar": {
        "web_oficial": "https://icom.museum/en/news/museums-video-games-two-projects-developed-in-argentina",
    },
    "gta-rio-de-la-plata": {
        "web_oficial": "https://www.gta5-mods.com/maps/gta-rio-de-la-plata",
    },
    # Lote 2: 25 juegos que aún no tenían link jugable
    "golazo-2": {
        "steam": "https://store.steampowered.com/app/1499700/Golazo_2/",
    },
    "xplorite": {
        "steam": "https://store.steampowered.com/app/2720230/Xplorite/",
    },
    "truco-blyts": {
        "web_oficial": "https://truco.blyts.com/",
    },
    "pes-2017-afa": {
        "web_oficial": "https://www.konami.com/games/eu/en/topics/13834/",
    },
    "pes-2014-afa": {
        "web_oficial": "https://www.konami.com/games/efootball/",
    },
    "efootball-pes-2020-superliga": {
        "web_oficial": "https://www.konami.com/efootball/",
    },
    "fifa-street-caminito": {
        "web_oficial": "https://www.mobygames.com/game/57553/fifa-street-3/",
    },
    "perfil-de-riesgo-casos-federales": {
        "web_oficial": "https://www.mobygames.com/game/50720/perfil-de-riesgo-casos-federales/",
    },
    "yo-matias-suenos-peligrosos": {
        "archive": "https://www.abandonsocios.org/index.php?topic=15458.0",
    },
    "yo-matias-futbol-5": {
        "archive": "https://www.abandonsocios.org/index.php?topic=15458.0",
    },
    "yo-matias-fantasmas-calabazas": {
        "archive": "https://archive.org/details/yomatias2",
    },
    "yo-matias-viajeros-tiempo-1": {
        "archive": "https://www.abandonsocios.org/index.php?topic=15458.0",
    },
    "yo-matias-cazador-golosinas": {
        "archive": "https://www.abandonsocios.org/index.php?topic=15458.0",
    },
    "elifoot-98-liga-argentina": {
        "archive": "https://www.pcfutbol.com/",
    },
    "super-menem-bros": {
        "archive": "https://www.old-games.ru/game/download/9255.html",
    },
    "argentina-8-bit": {
        "web_oficial": "https://argentina8bit.com/",
        "google_play": "https://play.google.com/store/apps/details?id=com.marianolarronde.argentina8bit",
    },
    "argentina-y-sus-provincias": {
        "itch": "https://themaxcraft1.itch.io/argentina-y-sus-provincias",
    },
    "tito-en-el-humedal": {
        "itch": "https://juegotito.itch.io/tito",
    },
    "cristina-vs-gorilas": {
        "apkpure": "https://apkpure.com/cristina-vs-gorilas/com.cfk.cristinavsgorilas",
    },
    "truco-arbiser-1982": {
        "web_oficial": "https://www-2.dc.uba.ar/charlas/lud/truco/",
    },
    "resistencia-en-obligado": {
        "itch": "https://pazrozen.itch.io/resistenciaenobligado",
    },
    "cronicas-libertadores": {
        "steam": "https://store.steampowered.com/app/2603120/Liberators_Chronicles/",
    },
    "el-gaucho-martin-fierro": {
        "steam": "https://store.steampowered.com/app/3610780/El_gaucho_Martn_Fierro/",
    },
    "microsoft-flight-simulator-argentina": {
        "steam": "https://store.steampowered.com/app/1250410/Microsoft_Flight_Simulator/",
    },
    "fortnite-argentina-maps": {
        "web_oficial": "https://www.fortnite.com/",
    },
    "libertad-o-muerte": {
        "steam": "https://store.steampowered.com/app/1174420/Libertad_o_Muerte/",
    },
    "mount-blade-warband-mods-argentina": {
        "steam": "https://store.steampowered.com/app/48700/Mount__Blade_Warband/",
    },
    "napoleon-total-war-mods-independencia": {
        "steam": "https://store.steampowered.com/app/34030/Napoleon_Total_War/",
    },
    "empire-total-war-mods-america": {
        "steam": "https://store.steampowered.com/app/10500/Empire_Total_War/",
    },
    "europa-universalis-iv-argentina": {
        "steam": "https://store.steampowered.com/app/236850/Europa_Universalis_IV/",
    },
    "hearts-of-iron-iv-mods-argentina": {
        "steam": "https://store.steampowered.com/app/394360/Hearts_of_Iron_IV/",
    },
    "heroinas-independencia": {
        "web_oficial": "https://fundacionariadna.org.ar/videojuego",
    },
    "cebador": {
        "web_oficial": "https://cebadoreljuego.com/",
        "google_play": "https://play.google.com/store/apps/details?id=com.cebatoriodejuegos.cebador",
    },
    "malon": {"steam": "https://store.steampowered.com/app/3462960/Malon/"},
    "aesir-online": {"steam": "https://store.steampowered.com/app/2324940/AESIR_Online/"},
    "qsvt-que-se-vayan-todos": {"steam": "https://store.steampowered.com/app/4187700/QSVT_Que_se_vayan_todos/"},
    "chacal": {"steam": "https://store.steampowered.com/app/1528370/CHACAL/"},
    "funeraria-marquez-paz": {"steam": "https://store.steampowered.com/app/1885040/Funerary_Services_Marquez_Paz/"},
    "dead-world": {"steam": "https://store.steampowered.com/app/1376960/Dead_World/"},
    "built-brick-by-brick": {"steam": "https://store.steampowered.com/app/3819930/Built_Brick_by_Brick/"},
    "anothers-memories": {"steam": "https://store.steampowered.com/app/3955730/Anothers_Memories/"},
    "en-busca-de-la-libertad": {"steam": "https://store.steampowered.com/app/4119760/In_Search_of_Freedom/"},
    "drident": {"steam": "https://store.steampowered.com/app/4806100/Drident/"},
    "gaucho-subway-escape": {"steam": "https://store.steampowered.com/app/3272390/Gaucho_Subway_Escape/"},
    "tierras-infernales": {"steam": "https://store.steampowered.com/app/3297900/Infernal_Lands/"},
    "el-tango-de-la-muerte": {"steam": "https://store.steampowered.com/app/701380/El_Tango_de_la_Muerte/"},
    "yerba-mate-tycoon": {"steam": "https://store.steampowered.com/app/1404560/Yerba_Mate_Tycoon/"},
    "defensores-del-barrio": {"steam": "https://store.steampowered.com/app/4309130/DEFENSORES_DEL_BARRIO/"},
    "pista-motorsport": {"steam": "https://store.steampowered.com/app/2434120/PISTA_Motorsport/"},
    "panchofobia": {"steam": "https://store.steampowered.com/app/4568220/Panchofobia/"},
    "take-a-hint": {"steam": "https://store.steampowered.com/app/4297760/Take_a_Hint/"},
    "zonda": {"steam": "https://store.steampowered.com/app/4560800/Zonda/"},
    "tenebris-somnia": {"steam": "https://store.steampowered.com/app/2121510/Tenebris_Somnia/"},
    "doorways-holy-mountains": {"steam": "https://store.steampowered.com/app/383930/Doorways_Holy_Mountains_of_Flesh/"},
    "dcs-south-atlantic": {"steam": "https://store.steampowered.com/app/2017210/DCS_South_Atlantic/"},
    "command-falklands": {"steam": "https://store.steampowered.com/app/2141010/CommandMO__Falklands/"},
    "dakar-18-argentina": {"steam": "https://store.steampowered.com/app/767390/Dakar_18/"},
    "dirt-rally-2-argentina": {"steam": "https://store.steampowered.com/app/690790/DiRT_Rally_20/"},
    "wars-curupayti-1866": {"steam": "https://store.steampowered.com/app/1996050/Wars_Across_The_World__Curupayti_1866/"},
    "wrc-10-argentina": {"steam": "https://store.steampowered.com/app/1462810/WRC_10_FIA_World_Rally_Championship/"},
    "aws-argentina-wingshooting": {"steam": "https://store.steampowered.com/app/718410/AWS_Argentina_Wingshooting_Simulator/"},
    "the-almamula": {"steam": "https://store.steampowered.com/app/3219760/"},
    "avaroth-online": {"steam": "https://store.steampowered.com/app/2784670/"},
    "ethereal": {"steam": "https://store.steampowered.com/app/751220/"},
    "the-path-into-the-abyss": {"steam": "https://store.steampowered.com/app/3000460/"},
    "game-of-patios": {"steam": "https://store.steampowered.com/app/3387790/"},
    "envido": {"steam": "https://store.steampowered.com/app/3872160/"},
    "gaucho-and-the-grassland": {"steam": "https://store.steampowered.com/app/1670830/"},
    "the-baron-got-you-again": {"steam": "https://store.steampowered.com/app/538050/"},
    "help-no-brake": {"steam": "https://store.steampowered.com/app/2531960/"},
    "borealis-descent": {"steam": "https://store.steampowered.com/app/2161980/"},
    "youra-the-game": {"steam": "https://store.steampowered.com/app/2724180/"},
    "rhythm-soccer": {"steam": "https://store.steampowered.com/app/2368200/"},
    "havana-blood": {"steam": "https://store.steampowered.com/app/4361180/"},
    "pampas-selene-maze-of-demons": {"steam": "https://store.steampowered.com/app/1966220/"},
    "piggo": {"steam": "https://store.steampowered.com/app/4597790/"},
    "warpzone-vs-the-dimension": {"steam": "https://store.steampowered.com/app/1088060/"},
    "hive-dive": {"steam": "https://store.steampowered.com/app/2707380/"},
    "curilemu": {"steam": "https://store.steampowered.com/app/2362780/"},
    "arcana-ucsb": {"steam": "https://store.steampowered.com/app/3037740/"},
    "wanted-guns": {"steam": "https://store.steampowered.com/app/2462230/"},
}

TIPO_OBRA_PATCHES: dict[str, str] = {
    "civ6-mod-argentina": "mod",
    "gta-rio-de-la-plata": "mod",
    "mount-blade-warband-mods-argentina": "mod",
    "napoleon-total-war-mods-independencia": "mod",
    "empire-total-war-mods-america": "mod",
    "hearts-of-iron-iv-mods-argentina": "mod",
}

WORKSHOP_PATCHES: dict[str, str] = {
    "civ6-mod-argentina": "https://steamcommunity.com/sharedfiles/filedetails/?id=910530559",
}
