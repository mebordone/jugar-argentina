# Tests unitarios

Suite de tests con **Vitest** sobre la lógica TypeScript del frontend (`src/lib` + `src/components/GameFilters.tsx`).

## Comandos

| Comando | Uso |
|---------|-----|
| `npm test` | Ejecuta todos los tests una vez |
| `npm run test:watch` | Modo watch durante desarrollo |
| `npm run test:coverage` | Tests + cobertura v8 con umbral **95%** |
| `npm run test:filters` | Regresión de filtros y recorridos |
| `npm run test:summaries` | Regresión de resúmenes culturales |

## Alcance

**Incluido**

- `src/lib/**/*.ts` — filtros, juegos, enlaces, recorridos, listas, etc.
- `src/components/GameFilters.tsx` — catálogo interactivo (React)

**Excluido**

- Plantillas `.astro` y páginas estáticas
- Scripts Python de `scripts/`
- Validación de `data/games.json` (sigue en `npm run validate`)

## Estructura

```
src/
  lib/
    *.test.ts          # tests por módulo
  components/
    GameFilters.test.tsx
  test/
    setup.ts           # jsdom, matchMedia, mocks de import.meta.env
    fixtures/
      game.ts          # baseGame() / baseGameView() para fixtures
vitest.config.ts       # thresholds de cobertura al 95%
```

## Convenciones

- **Fixtures:** usar `baseGame()` y `baseGameView()` de `src/test/fixtures/game.ts` para lógica aislada; reservar datos reales de `games.json` solo para smoke/regresión.
- **Componentes:** Testing Library + user-event; helpers de scroll/foco viven en `src/lib/catalogUi.ts`.
- **Mocks:** `node:fs` en `games.test.ts` para CSV de candidatos; `vi.mock("./games")` en `listas.test.ts` y `recorridos.scoring.test.ts` cuando hace falta aislar datos.

## CI

- **Pull requests:** `.github/workflows/validate-pr.yml` corre `npm run test:coverage` antes del build.
- **Deploy a main:** `.github/workflows/deploy.yml` valida datos, corre tests con cobertura y publica en GitHub Pages.

## Agregar tests

1. Crear `src/lib/<modulo>.test.ts` junto al módulo (o `.test.tsx` para componentes).
2. Preferir casos tabla-driven para ramas (`describe` + varios `it` con inputs distintos).
3. Verificar localmente: `npm run test:coverage` debe pasar los cuatro umbrales (lines, functions, branches, statements).
