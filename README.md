# Jugar Argentina

Catálogo curado de videojuegos vinculados a la cultura argentina. Sitio estático con Astro + datos en JSON.

**Producción:** `https://mebordone.github.io/jugar-argentina/`

## Desarrollo local

```bash
npm install
npm run dev
```

Abrí [http://localhost:4321](http://localhost:4321).

## Validación de datos

```bash
npm run validate          # schema + links Steam
npm run validate:data     # solo games.json
npm run validate:links    # solo enlaces de tienda
```

## Tests unitarios

```bash
npm test                  # suite completa
npm run test:coverage     # con cobertura (umbral 95%)
```

Detalle de alcance, fixtures y CI en [`docs/TESTING.md`](docs/TESTING.md).

## Build

```bash
npm run build
npm run preview
```

Simular build de GitHub Pages:

```bash
PUBLIC_SITE_URL=https://mebordone.github.io PUBLIC_BASE_PATH=/jugar-argentina/ npm run build
```

## Despliegue en GitHub Pages

1. Creá el repo `jugar-argentina` en GitHub.
2. En **Settings → Pages → Build and deployment**, elegí **GitHub Actions**.
3. En **Settings → Secrets and variables → Actions → Variables**, configurá:

| Variable | Valor |
|---|---|
| `PUBLIC_SITE_URL` | `https://mebordone.github.io` |
| `PUBLIC_BASE_PATH` | `/jugar-argentina/` |

4. Push a `main` dispara el workflow [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) (validación de datos, tests con cobertura, build y publicación).

Atajo (requiere `gh auth login` una vez):

```bash
chmod +x scripts/setup_github.sh
./scripts/setup_github.sh
```

Luego en **Settings → Pages**, elegí **GitHub Actions** como fuente de deploy.

## Sugerir un juego

Usá [Issues con el template “Sugerir juego”](https://github.com/mebordone/jugar-argentina/issues/new?template=sugerir-juego.yml) o la página `/sugerir` del sitio.

## Estructura

| Ruta | Contenido |
|---|---|
| `data/games.json` | Base de 100 juegos verificados |
| `scripts/` | Generación, validación y curaduría |
| `src/` | Sitio Astro |
| `docs/TESTING.md` | Guía de tests unitarios (Vitest) |
