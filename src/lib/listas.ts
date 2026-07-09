import {
  discarded,
  games,
  getCandidates,
  type Candidate,
  type GameView,
} from "./games";

export type ListaStatKey =
  | "total"
  | "candidatos"
  | "escenario"
  | "protagonista"
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
    game.anio ? String(game.anio) : "Sin fecha",
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
      "Los 100 juegos del catálogo curado con vínculo argentino documentado.",
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
      "Títulos detectados en fuentes abiertas que aún no entraron al catálogo.",
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
      "Juegos donde Argentina aparece como mapa, nivel o ambientación jugable.",
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
      "Juegos con personajes, arquetipos o figuras argentinas como eje central.",
    getItems: () =>
      games
        .filter((game) => game.vinculo_argentina.protagonista.activo)
        .sort((a, b) => a.titulo.localeCompare(b.titulo, "es"))
        .map(gameItem),
  },
  {
    slug: "descartados",
    statKey: "descartados",
    statLabel: "descartes explicados",
    titulo: "Descartes explicados",
    descripcion:
      "Casos evaluados que no entraron al catálogo, con el motivo documentado.",
    getItems: () =>
      discarded.map((item) => ({
        titulo: item.titulo,
        subtitulo: item.motivo_exclusion,
      })),
  },
];

export const listaBySlug = new Map(listas.map((lista) => [lista.slug, lista]));

export const listaHrefByStatKey: Record<ListaStatKey, string> = Object.fromEntries(
  listas.map((lista) => [lista.statKey, `/listas/${lista.slug}`]),
) as Record<ListaStatKey, string>;
