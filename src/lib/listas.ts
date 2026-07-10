import {
  discarded,
  games,
  getCandidates,
  type Candidate,
  type GameView,
} from "./games";
import { gameReleasePrimary } from "./release";

export type ListaStatKey =
  | "total"
  | "candidatos"
  | "escenario"
  | "protagonista"
  | "deporte"
  | "descartados";

export type ListaItem = {
  titulo: string;
  subtitulo?: string;
  href?: string;
  external?: boolean;
};

export type ListaDef = {
  slug: string;
  statKey: ListaStatKey;
  statLabel: string;
  titulo: string;
  descripcion: string;
  getItems: () => ListaItem[];
};

function gameItem(game: GameView): ListaItem {
  const meta = [
    gameReleasePrimary(game),
    game.plataformas.slice(0, 2).join(", "),
  ]
    .filter(Boolean)
    .join(" · ");
  return {
    titulo: game.titulo,
    subtitulo: meta,
    href: `/juegos/${game.id}`,
  };
}

export const listas: ListaDef[] = [
  {
    slug: "juegos-verificados",
    statKey: "total",
    statLabel: "juegos verificados",
    titulo: "Juegos verificados",
    descripcion:
      "Todas las fichas publicadas del catálogo: obras con vínculo argentino documentado, ordenadas alfabéticamente para consulta rápida.",
    getItems: () =>
      [...games]
        .sort((a, b) => a.titulo.localeCompare(b.titulo, "es"))
        .map(gameItem),
  },
  {
    slug: "candidatos",
    statKey: "candidatos",
    statLabel: "candidatos rastreados",
    titulo: "Candidatos rastreados",
    descripcion:
      "Títulos detectados en fuentes abiertas que todavía necesitan verificación editorial, descarte o pase a ficha publicada.",
    getItems: () =>
      getCandidates()
        .sort((a, b) => a.titulo.localeCompare(b.titulo, "es"))
        .map((item: Candidate) => ({
          titulo: item.titulo,
          subtitulo: [
            item.anio || "Sin año",
            item.estado_triage || item.estado_juego,
            item.eje_sugerido,
          ]
            .filter(Boolean)
            .join(" · "),
          href: item.url || undefined,
          external: Boolean(item.url),
        })),
  },
  {
    slug: "escenario-argentino",
    statKey: "escenario",
    statLabel: "con escenario argentino",
    titulo: "Con escenario argentino",
    descripcion:
      "Juegos donde Argentina aparece como territorio jugable: mapas, niveles, ciudades, regiones, paisajes o escenarios históricos.",
    getItems: () =>
      games
        .filter((game) => game.vinculo_argentina.escenario.activo)
        .sort((a, b) => a.titulo.localeCompare(b.titulo, "es"))
        .map(gameItem),
  },
  {
    slug: "protagonistas-argentinos",
    statKey: "protagonista",
    statLabel: "con protagonistas argentinos",
    titulo: "Con protagonistas argentinos",
    descripcion:
      "Juegos donde personajes, figuras históricas, arquetipos culturales o identidades argentinas sostienen parte central de la experiencia.",
    getItems: () =>
      games
        .filter((game) => game.vinculo_argentina.protagonista.activo)
        .sort((a, b) => a.titulo.localeCompare(b.titulo, "es"))
        .map(gameItem),
  },
  {
    slug: "deporte-argentino",
    statKey: "deporte",
    statLabel: "con deporte argentino",
    titulo: "Con deporte argentino",
    descripcion:
      "Juegos donde ligas, equipos, selecciones, estadios o prácticas deportivas argentinas aparecen como contenido relevante.",
    getItems: () =>
      games
        .filter((game) => game.vinculo_argentina.deporte_argentino.activo)
        .sort((a, b) => a.titulo.localeCompare(b.titulo, "es"))
        .map(gameItem),
  },
  {
    slug: "descartados",
    statKey: "descartados",
    statLabel: "descartes explicados",
    titulo: "Descartes explicados",
    descripcion:
      "Casos ya revisados que quedaron fuera del catálogo, conservados con motivo de exclusión para evitar duplicar investigaciones.",
    getItems: () =>
      discarded.map((item) => ({
        titulo: item.titulo,
        subtitulo: item.motivo_exclusion,
        href: "/curaduria#descartados",
      })),
  },
];

export const listaBySlug = new Map(listas.map((lista) => [lista.slug, lista]));

export const listaHrefByStatKey: Record<ListaStatKey, string> = Object.fromEntries(
  listas.map((lista) => [lista.statKey, `/listas/${lista.slug}`]),
) as Record<ListaStatKey, string>;
