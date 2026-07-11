# Base de datos — Videojuegos vinculados a Argentina

## Criterios de inclusión (v1.2)

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

## Estadísticas (v1.2)

| Métrica | Valor |
|---------|-------|
| Juegos verificados | 161 |
| Sin link jugable | 0 |
| Sin portada | 0 |
| Backlog editorial (central/importante) | 0 |
| Sin capturas | 65 |
| Sin provincia | 80 |
| Candidatos en CSV | 169 |
| Con vínculo escenario | 132 |
| Con vínculo protagonista | 78 |
| Con vínculo deporte | 16 |

### Por grado de relevancia

- central: 117
- importante: 8
- menor: 36

### Por eje cultural (top)

- deporte: 10
- politica: 5
- satira: 5
- folclore: 4
- educativo: 4
- juegos_tradicionales: 3
- cultura_urbana: 3
- geografia: 3
- memoria: 2
- historia: 2

### Por plataforma (top)

- PC: 81
- Web: 18
- PlayStation: 15
- Xbox: 14
- Android: 7
- iOS: 4
- Nintendo: 3
- Linux: 1

### Por género (top)

- aventura: 43
- accion: 25
- educativo: 20
- simulacion: 19
- estrategia: 16
- deportes: 16
- terror: 12
- plataformas: 10
- puzzle: 8
- shooter: 7

## Archivos

- `games.json` — base principal verificada
- `schema.json` — esquema de validación
- `pendientes.json` — entradas sin verificar
- `descartados.json` — exclusiones documentadas
- `raw_candidates.csv` — candidatos con columnas de triage
- `CHANGELOG.md` — historial de versiones

Actualizado: 2026-07-11
