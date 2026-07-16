# Listas del catálogo

Las listas son vistas automáticas del catálogo. No compiten con los recorridos: una lista responde “mostrame todos los juegos que cumplen esta condición”; un recorrido responde “guiame por un tema con una mirada editorial”.

## Listas actuales

| Ruta | Criterio |
|------|----------|
| `/listas/juegos-verificados` | Todas las fichas publicadas |
| `/listas/candidatos` | Candidatos rastreados pendientes de triage |
| `/listas/escenario-argentino` | `vinculo_argentina.escenario.activo` |
| `/listas/protagonistas-argentinos` | `vinculo_argentina.protagonista.activo` |
| `/listas/deporte-argentino` | `vinculo_argentina.deporte_argentino.activo` |
| `/listas/descartados` | Exclusiones documentadas |

La definición vive en `src/lib/listas.ts`.

## Ordenamiento (juegos verificados)

En `/listas/juegos-verificados` se puede ordenar por:

- título A–Z / Z–A;
- fecha de alta (más recientes / más antiguos);
- año del juego (más recientes / más antiguos).

La fecha de alta se muestra como columna propia en cada fila. El valor crudo está en `fecha_alta` (ISO) dentro de `data/games.json`.

La lógica de orden es client-safe y vive en `src/lib/listaSort.ts` (sin dependencias de Node), para no romper el script de la página estática.
