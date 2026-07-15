# Changelog — Base de videojuegos argentinos

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
