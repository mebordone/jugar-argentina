# Flujo editorial de fichas

Release 3 + consistencia de seguimiento:

`candidato → borrador → validación → publicación transaccional`.

Las fichas ya publicadas en `data/games.json` no se reescriben masivamente: el pipeline estricto aplica a borradores.

## Contrato de datos

| Capa | Ubicación | Rol |
|------|-----------|-----|
| Seguimiento | `data/raw_candidates.csv` | Registro maestro por investigación (`id`, `ficha_id`, estado) |
| Borradores | `data/drafts/<id>.json` | Staging editorial |
| Publicados | `data/games.json` | Contenido del catálogo |
| Copia web | `public/data/games.json` | Artefacto publicado (idéntico a `games.json`) |
| Descartes | `data/descartados.json` | Motivos de exclusión |
| Manifiestos | `data/candidates/` | Evidencia de investigación |

Invariante central: `CSV[estado=publicado].ficha_id == games.json.id` (conjuntos iguales).

## Comandos

```bash
# Crear borrador (también crea/asegura fila de seguimiento)
npm run ficha -- new --template escenario --titulo "Mi Juego"
npm run ficha -- new --template escenario --candidate paleontorun --non-interactive

# Validar / listar
npm run ficha -- list
npm run ficha -- show paleontorun
npm run ficha -- validate paleontorun

# Publicar (actualiza games.json + CSV + manifiesto; sin --no-sync)
npm run ficha -- publish paleontorun

# Descartar investigación
npm run ficha -- discard <tracking_id> --motivo "Sin vínculo argentino verificable"

# Estado editorial (cola, huecos, invariantes)
npm run ficha -- status
npm run ficha -- status --limit 30

# Consistencia
npm run validate:consistency
npm run data:reconcile   # migración/reconciliación reproducible
npm run data:publish     # copia verificable a public/data/games.json
```

Plantillas: `central`, `escenario`, `protagonista`, `deporte`, `referencia_menor`, `educativo`, `mod`, `mapa_campania`, `dlc_contenido`, `abandonware`.

## Estados de seguimiento

Canónicos en `estado_triage`:

- `candidato`
- `en_revision`
- `publicado` (requiere `ficha_id`)
- `descartado` (requiere `motivo_decision`)

`descartados.json` es proyección 1:1 de las filas CSV `descartado` (mismos ids y motivos).

Mapeo legado: `pendiente→en_revision`, `verificado→publicado`, `alta/requiere_verificacion→en_revision`.

La lista `/listas/candidatos` y el contador de home muestran solo `candidato` y `en_revision`.

`ficha status` resume conteos, invariantes (publicados, descartes, copia pública), huecos (portada/enlaces), borradores y la cola abierta.

## Validación de fichas

- **Errores (bloquean publicación):** campos obligatorios, enums, vínculo argentino, ID duplicado, evidencia enlazada, etc.
- **Advertencias:** descripción corta, sin ejes, sin portada/capturas, disponibilidad desconocida.

`npm run validate:data` valida el catálogo; `npm run validate:consistency` exige igualdad de conjuntos publicados.

## Pruebas

```bash
npm run test:fichas
```
