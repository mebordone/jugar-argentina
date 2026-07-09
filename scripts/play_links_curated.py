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
        "web_oficial": "https://lutris.net/games/aconcagua/",
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
