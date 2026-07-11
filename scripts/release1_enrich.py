#!/usr/bin/env python3
"""Enriquece descripciones y enlaces para el cierre de Release 1."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAMES_PATH = ROOT / "data" / "games.json"

DESCRIPTION_PATCHES: dict[str, str] = {
    # Lote A — PC Fútbol
    "pc-futbol-70-argentina": (
        "Última gran entrega de la saga PC Fútbol adaptada al fútbol argentino: "
        "Primera División, planteles reales y gestión de clubes con la identidad "
        "de la liga local que popularizó Dinamic en los noventa."
    ),
    "pc-futbol-60-argentina": (
        "Versión argentina de PC Fútbol 6.0 con Primera División, Copa Argentina "
        "y divisiones inferiores: simulador de gestión y partidos pensado para "
        "recrear el calendario y la economía del fútbol profesional local."
    ),
    "pc-futbol-50-apertura-97-argentina": (
        "Edición argentina de PC Fútbol 5.0 con relato de Marcelo Araujo y el "
        "torneo Apertura 1997: combina narración periodística con la simulación "
        "de liga que consolidó la saga como referencia del deporte argentino en PC."
    ),
    "pc-futbol-argentina-clausura-95": (
        "Primera edición de PC Fútbol adaptada a la liga argentina con los 20 "
        "equipos del Clausura 1995: hito del simulador español en el mercado "
        "local y punto de partida de la saga nacional."
    ),
    "pc-futbol-argentina-40-apertura-96": (
        "Adaptación argentina de PC Fútbol 4.0 con modo Pro-Manager y el torneo "
        "Apertura 1996 de Primera División: gestión de club, mercado de pases "
        "y calendario real del fútbol argentino de la época."
    ),
    # Lote B — Reversion
    "reversion-the-meeting": (
        "Segundo capítulo de la trilogía Reversion de 3f Interactive: aventura "
        "point-and-click en las ruinas de Buenos Aires distópica, con puzzles "
        "y continuidad narrativa sobre la ciudad argentina devastada."
    ),
    "reversion-the-return": (
        "Capítulo final de Reversion, desarrollado en Argentina por 3f Interactive: "
        "cierra la trilogía en una Buenos Aires postapocalíptica con acertijos, "
        "decisiones y atmósfera de ciencia ficción porteña."
    ),
    "reversion-the-escape": (
        "Primer capítulo de Reversion: aventura point-and-click en Buenos Aires "
        "devastada en 2035; el protagonista despierta en el Garrahan y debe "
        "reconstruir la memoria de una ciudad argentina en ruinas."
    ),
    # Lote C — PES
    "pes-2014-afa": (
        "Primera entrega de PES con licencia completa de la Primera División "
        "argentina (20 equipos AFA): referencia del fútbol local en consolas "
        "por escudos, planteles y estadios oficiales, aunque desarrollada por Konami."
    ),
    "pes-2017-afa": (
        "PES 2017 con 30 equipos argentinos licenciados y estadios Bombonera y "
        "Monumental: edición ampliada de la liga AFA en el simulador internacional "
        "de Konami, útil para comparar cómo el fútbol argentino entró al mercado global."
    ),
    # Lote D — Indies centrales
    "noir-storm": (
        "Aventura noir en desarrollo por Diskeletton Studios (Argentina), "
        "ambientada en Buenos Aires de 1952: detective privado, conspiraciones "
        "y atmósfera de crimen en una ciudad porteña reconstruida en pixel art."
    ),
    "resistencia-en-obligado": (
        "Estrategia histórica sobre la batalla de Obligado de 1845 en el Paraná: "
        "prototipo argentino que recrea la defensa fluvial contra la escuadra "
        "anglo-francesa con foco en un episodio clave de la historia nacional."
    ),
    "bienvenidos-a-la-matanza": (
        "Open world de acción en desarrollo por Esteban Muñoz que recrea San Justo "
        "y el conurbano bonaerense con misiones, corrupción policial y referencias "
        "locales: el proyecto indie apodado «GTA villero» por la prensa argentina."
    ),
    "delta-kayak-parque-del-delta": (
        "Terror de exploración en el Delta del Paraná con kayak y geografía real: "
        "aventura argentina en desarrollo que usa islas, canales y paisaje bonaerense "
        "como escenario principal de tensión y supervivencia."
    ),
    "gaucho-liberacion": (
        "Juego de vida gauchesca en desarrollo por Bacord Games (Argentina) sobre "
        "costumbres, tradiciones y folklore de la campaña del siglo XIX: busca "
        "transmitir identidad autóctona con carga histórica y narrativa popular."
    ),
    "gran-malvina": (
        "Top-down shooter prototipo argentino sobre un soldado conscripto en la "
        "Guerra de Malvinas de 1982: combate pixel art con tono memorial y "
        "escenario bélico del Atlántico Sur desde perspectiva local."
    ),
    "la-salamanca": (
        "Terror y puzzles basado en la leyenda de La Salamanca de los Llanos "
        "(Santiago del Estero): aventura argentina en Steam que cruza folklore "
        "nordestino, enigmas y atmósfera de pesadilla rural."
    ),
    "conur-life": (
        "GTA-like en pixel art ambientado en San Hugo, ciudad ficticia inspirada "
        "en Florencio Varela (Buenos Aires): desarrollo argentino de Lutte con "
        "mundo abierto, crimen urbano y referencias del conurbano bonaerense."
    ),
    "gaucho-power": (
        "Juego de sigilo sobre la Guerra Gaucha y las milicias del noroeste "
        "argentino durante la independencia: acción histórica con estética "
        "retro y foco en el nordeste como frente de las guerras libertadoras."
    ),
    "gta-rio-de-la-plata": (
        "Mod de GTA San Andreas con mapa de Buenos Aires: Casa Rosada, Obelisco, "
        "La Boca y barrios porteños recreados por la comunidad argentina como "
        "referencia urbana jugable dentro del motor de Rockstar."
    ),
    "envido": (
        "Juego de cartas argentino con almas en pena, pulpería y macumbas: "
        "bluff, estrategia y folklore gauchesco en una experiencia indie que "
        "transforma el envido en mecánica narrativa de terror rural."
    ),
    "zonda": (
        "Thriller narrativo en los cerros de San Juan: el Autódromo El Zonda "
        "guarda un silencio con nombre propio en esta aventura argentina de "
        "misterio, paisaje cuyano y tensión psicológica."
    ),
    "pista-motorsport": (
        "Simulador de carreras con autos de competición argentinos y circuitos "
        "emblemáticos del automovilismo local: desarrollo nacional que celebra "
        "TC, turismo y pistas históricas del deporte a motor en Argentina."
    ),
    "tierras-infernales": (
        "Roguelike arcade de acción ambientado en una distopía de las guerras "
        "de independencia en el norte argentino: combate frenético, memoria "
        "histórica y estética infernal sobre el NOA libertador."
    ),
    "game-of-patios": (
        "Teo vuelve a su barrio cordobés para ayudar a su abuela en el concurso "
        "de patios: regar, decorar y resolver enigmas en esta simulación argentina "
        "sobre la cultura urbana de Córdoba y la vida de barrio."
    ),
    # Lote E — Resto central/importante
    "argentina-y-sus-provincias": (
        "Juego educativo argentino para memorizar la geografía política del país "
        "y sus provincias: mapa interactivo pensado para escuela y consulta "
        "rápida del armado federal desde una perspectiva local."
    ),
    "operacion-rosario": (
        "Shooter sobre la Guerra de Malvinas con perspectiva de soldado o piloto "
        "de Super Étendard: acción bélica argentina que recrea combate aéreo "
        "y desembarco con foco en el conflicto del Atlántico Sur."
    ),
    "aconcagua-1999": (
        "Aventura de supervivencia en una Mendoza ficticia tras un accidente de "
        "avión en el Aconcagua: título comercial con escenario cordillerano "
        "argentino, frío extremo y rescate en los Andes."
    ),
    "el-gaucho-martin-fierro": (
        "Videojuego argentino inspirado en el poema de José Hernández, ambientado "
        "en la pampa del siglo XIX: minijuegos y versos que adaptan la odisea "
        "del gaucho Martín Fierro a formato interactivo."
    ),
    "truco-arbiser-1982": (
        "Primer videojuego comercial latinoamericano: simulación del truco argentino "
        "con frases, música de tango y reglas clásicas; hito de la industria "
        "regional creado por Enrique y Ariel Arbiser en 1982."
    ),
    # Vagas — reforzar señales locales
    "echoes-of-the-city": (
        "Terror psicológico low poly ambientado en San Telmo y la Plaza Dorrego "
        "de Buenos Aires: memoria histórica, folklore porteño y pesadillas urbanas "
        "en un desarrollo argentino de exploración y atmósfera."
    ),
    "fabulas-portenas": (
        "Terror en primera persona inspirado en leyendas urbanas del subte porteño, "
        "centrado en la estación fantasma Pirámides de la línea H en Buenos Aires: "
        "folklore urbano argentino convertido en pesadilla claustrofóbica."
    ),
    "qsvt-que-se-vayan-todos": (
        "Estrategia política satírica argentina donde conducís una fuerza política, "
        "competís en elecciones y tomás decisiones sobre el destino del país: "
        "crítica humorística a la vida institucional local en clave de simulador."
    ),
    "chacal": (
        "Bullet hell argentino que recorre el sur y el centro del país hasta "
        "enfrentar al presidente Francisco en una cruzada arcade: sátira política "
        "y acción frenética con referencias a la vida pública nacional."
    ),
    "el-39-2025": (
        "Terror corto estilo PSX ambientado en Constitución, Buenos Aires, a la "
        "madrugada: el jugador intenta tomar el colectivo 39 para llegar a un "
        "examen final en este relato urbano porteño de suspenso."
    ),
    "funeraria-marquez-paz": (
        "Aventura en las calles de Marquez Paz (Buenos Aires): laburás para la "
        "funeraria, explorás el barrio conurbano y te metés en situaciones "
        "violentas para ganar plata en un relato crudo de la Argentina real."
    ),
    "deep-beyond-2024": (
        "Thriller narrativo de puzzles desarrollado en La Plata (Buenos Aires), "
        "con identidad visual urbana asociada a la escena indie bonaerense: "
        "misterio, ciencia ficción ligera y atmósfera porteña contemporánea."
    ),
    "menem-la-hizo": (
        "Elige tu propia aventura satírica argentina donde el jugador encarna a "
        "Carlos Saúl Menem con el objetivo de desmantelar el país: surgido de "
        "la game jam Acción Dev como crítica política en clave de humor."
    ),
    "cronicas-libertadores": (
        "Estrategia por turnos en desarrollo sobre las campañas independentistas "
        "sudamericanas del siglo XIX, con énfasis en héroes anónimos y figuras "
        "poco difundidas del noroeste y la pampa argentina."
    ),
    "yo-matias-cazador-golosinas": (
        "Minijuego arcade protagonizado por Yo Matías, personaje de historieta "
        "de Sendra: traslada una figura porteña popular al formato interactivo "
        "y suma al catálogo argentino por su vínculo con la cultura infantil local."
    ),
    "evita-peron-contra-gorilas": (
        "Shooter top-down en pixel art creado en la CodeAr jam 2011 (Argentina): "
        "Perón zombie rescata obreros de gorilas literales y los lleva al "
        "colectivo de una manifestación en sátira política porteña."
    ),
}

LINK_PATCHES: dict[str, dict[str, str]] = {
    "bienvenidos-a-la-matanza": {
        "itch": "https://estebanmunoz.itch.io/bam-2025-pc",
    },
    "anahi-juego": {
        "itch": "https://guanacoestudio.itch.io/anahi",
    },
    "gaucho-liberacion": {
        "web_oficial": "https://bacord.ar/",
    },
    "federacion-2073": {
        "web_oficial": "https://www.fabio.com.ar/498-federacion-2073",
    },
}


def main() -> int:
    games = json.loads(GAMES_PATH.read_text(encoding="utf-8"))
    desc_updated = 0
    link_updated = 0

    for game in games:
        game_id = game["id"]
        if game_id in DESCRIPTION_PATCHES:
            game["descripcion"] = DESCRIPTION_PATCHES[game_id]
            desc_updated += 1
        if game_id in LINK_PATCHES:
            game.setdefault("enlaces", {}).update(LINK_PATCHES[game_id])
            link_updated += 1

    GAMES_PATH.write_text(
        json.dumps(games, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"OK: {desc_updated} descripciones, {link_updated} enlaces actualizados")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
