# Changelog — Base de videojuegos argentinos

## v1.4 (2026-07-15) — Recorridos Release 2, fecha de alta y listas ordenables

### Cambios principales
- Campo `fecha_alta` en cada ficha (ISO con hora cuando viene del historial git).
- Lista `/listas/juegos-verificados` ordenable por título, fecha de alta y año, con la fecha visible en cada fila.
- Recorridos Release 2: refinamiento de fechas patrias, `politica-satira` permanente, 12 de octubre crítico, nuevo `pueblos-originarios-memorias-vivas`, más `patagonia-jugable`, `provincias-argentinas-en-juego` y `videojuegos-educativos-argentinos`.
- Altas verificadas asociadas a memoria, Patagonia, provincias y educativos (p. ej. Kokena, Sub-Namuncurá, Industria Argentina, Semaforo Climber y batch Release 2).
- Validación `npm run validate:recorridos` integrada en `npm run validate`.
- Documentación en `docs/RECORRIDOS.md`, `docs/LISTAS.md` y avance en `ROADMAP.md`.

### Conteos
| Métrica | v1.3 | v1.4 |
|---------|------|------|
| Verificados | ~164 | **199** |
| Recorridos | ~12 | **19** |

### Ajustes técnicos
- Schema y `generate_db.py` exigen `fecha_alta`.
- Orden de listas en `listaSort.ts` + script Astro (sin island React).
- Candidatos de investigación en `data/candidates/`.

## v1.3 (2026-07-15) — Taxonomía pública y guía de lectura

### Cambios principales
- Nuevo campo `formato` para separar juego base, mod, mapa, campaña, DLC, expansión, contenido licenciado, demo, prototipo y colección.
- Rediseño de tarjetas con chips públicos, línea contextual y sensibilidad visible solo cuando corresponde.
- Nueva guía pública de curaduría en `/curaduria`, orientada a entender criterios de entrada, lectura de tarjetas y capas editoriales.
- Documentación editorial en `docs/CURADURIA.md` para mantener criterios de inclusión, exclusión y taxonomía.
- Nuevas entradas y ajustes recientes: Aconcagua, The Path Into The Abyss, Counter Strike: Malvinas y Cambalache - Buenos Aires.

### Ajustes técnicos
- Validación de datos actualizada para exigir `formato`.
- Filtro nuevo por formato en el catálogo.
- Helpers `cardMetadata` para centralizar etiquetas de formato, tema, lugar, vínculo argentino, acceso y sensibilidad.
- Cobertura de tests para metadatos de tarjeta, filtros por formato, resumen cultural y comportamiento del catálogo.

## v1.2 (2026-07-11) — Release 1: Orden y calidad editorial

### Cambios principales
- Enriquecimiento de **41 descripciones** central/importante con vínculo argentino explícito
- Módulo `culturalSummary` para resúmenes culturales en fichas y catálogo
- Reporte editorial (`npm run data:report` → `data/quality_report.md`)
- Corrección de destacados en recorridos (`pomberito-2024`, swap de referencias menores)
- Links jugables al 100% (itch/web para fichas pendientes)
- Suite Vitest con gate de cobertura al 95% en CI

### Métricas antes / después

| Métrica | Pre-Release 1 | v1.2 |
|---------|---------------|------|
| Juegos verificados | 161 | 161 |
| Backlog editorial (central/importante) | 41 | **0** |
| Descripciones similares | 0 | 0 |
| Sin portada | 0 | 0 |
| Sin link jugable | 4 | **0** |
| Sin capturas | 65 | 65 |
| Sin provincia | 80 | 80 |

### Backlog transferido
- **Release 2:** generador CLI de fichas, validaciones editoriales
- **Release 6:** capturas masivas, cobertura provincial, años TBD legítimos

---

## v1.1 (2026-07-09)

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
| Verificados | 68 | 100 |
| Pendientes | 28 | 0 |
| Descartados | 0 | 4 |
| Candidatos CSV | 116 | 169 |

### Exclusiones notables
- **Roots of Pacha** — solo desarrollo argentino, sin temática AR
- **Dark Rage** — shoot'em up sin vínculo temático argentino
- **FIFA 23 / PES 2021** — selección entre muchas

### Ajustes editoriales
- **Golazo!** reclasificado como `grado_relevancia_argentina: menor`
- Saga **PC Fútbol Argentina** normalizada con `serie` y `relacionado_con`
