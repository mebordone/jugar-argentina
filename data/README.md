# Base de datos — Videojuegos vinculados a Argentina

## Criterios de inclusión (v1.3)

Un juego entra si cumple al menos una condición:

1. **Escenario argentino** — mapas, niveles o ambientación jugable en Argentina
2. **Protagonista argentino** — figuras de historia, cultura, folclore o política
3. **Deporte argentino** — ligas/equipos argentinos como eje central (ej. PC Fútbol Ed. Argentina)
4. **Contenido derivado verificable** — mods, mapas, campañas, DLCs, expansiones o contenido licenciado con vínculo argentino claro

**Excluido:** FIFA/PES genéricos donde Argentina es solo una selección; juegos con solo desarrollador argentino sin temática AR.

### Campos editoriales v1.4

- `formato` — juego_base, mod, mapa, campania, dlc, expansion, contenido_licenciado, demo, prototipo, coleccion
- `fecha_alta` — ISO de ingreso al catálogo (con hora cuando viene de git). Distinta de `fecha_actualizacion` (última edición editorial)
- `ejes_culturales` — política, sátira, folclore, memoria, cultura urbana, etc.
- `tipo_obra` — comercial, indie, educativo, jam, fan_game, promocional, institucional…
- `grado_relevancia_argentina` — central, importante, menor
- `sensibilidad` — baja, media, alta (dictadura, Malvinas, política partidaria)
- `serie` / `edicion` / `relacionado_con` — variantes y colecciones
- `disponibilidad` — a_la_venta, gratis, abandonware, perdido

`formato` describe qué se incorpora al catálogo. `tipo_obra` describe la naturaleza editorial o productiva de la obra. Por ejemplo, un mapa comunitario puede ser `formato: "mapa"` y `tipo_obra: "mod"`.

`fecha_alta` se infiere al alta: primera aparición en el historial de `data/games.json` cuando existe; si la ficha aún no está commiteada, se usa `fecha_actualizacion` (y un orden relativo entre altas locales del mismo día).

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

## Estadísticas (v1.4)

| Métrica | Valor |
|---------|-------|
| Juegos verificados | 199 |
| Sin link jugable | 0 |
| Sin portada | 11 |
| Sin capturas | ~95 |
| Sin año | 44 |
| Recorridos editoriales | 19 |

Actualizar con `npm run data:report` → `data/quality_report.md` para el detalle editorial.

## Archivos

- `games.json` — base principal verificada
- `schema.json` — esquema de validación
- `pendientes.json` — entradas sin verificar
- `descartados.json` — exclusiones documentadas
- `raw_candidates.csv` — candidatos con columnas de triage
- `candidates/` — manifiestos de investigación (p. ej. Release 2)
- `CHANGELOG.md` — historial de versiones

Actualizado: 2026-07-15
