# Changelog — Base de videojuegos argentinos

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
