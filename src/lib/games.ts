import fs from "node:fs";
import path from "node:path";
import rawGames from "../../data/games.json";
import descartados from "../../data/descartados.json";
import { humanize, normalizeText } from "./filters";
import {
  collectActions,
  hasPlayableLink,
  primaryAction,
  splitActions,
  type LinkAction,
} from "./links";

export type Vinculo = {
  activo: boolean;
  presencia: "principal" | "referencia_menor" | null;
  subtipo?: string;
};

export type Game = {
  id: string;
  titulo: string;
  titulo_original: string;
  anio: number | null;
  estado: string;
  vinculo_argentina: {
    escenario: Vinculo;
    protagonista: Vinculo;
    deporte_argentino: Vinculo;
  };
  personajes_argentinos: Array<Record<string, string>>;
  deporte_argentino: Record<string, unknown> | null;
  desarrollador: string;
  pais_desarrollo: string;
  plataformas: string[];
  generos: string[];
  descripcion: string;
  contexto_argentino: {
    regiones: string[];
    provincias: string[];
    periodo_historico: string[];
    temas: string[];
  };
  enlaces: Record<string, unknown>;
  ejes_culturales: string[];
  tipo_obra: string;
  grado_relevancia_argentina: string;
  calidad_fuente: string;
  sensibilidad: string;
  serie: string | null;
  edicion: string | null;
  relacionado_con: string[];
  disponibilidad: string;
};

export type GameView = Game & {
  actions: LinkAction[];
  primaryAction?: LinkAction;
  sourceActions: LinkAction[];
  playableActions: LinkAction[];
  isPlayableToday: boolean;
  badges: string[];
  searchText: string;
  culturalSummary: string;
};

export type Candidate = {
  titulo: string;
  anio: string;
  estado_juego: string;
  vinculo_preliminar: string;
  fuente: string;
  url: string;
  nota: string;
  estado_triage: string;
  eje_sugerido: string;
  ejes_culturales_sugeridos: string;
  notas_triage: string;
};

export const games = (rawGames as Game[]).map(enrichGame);
export const discarded = descartados;
export const gameById = new Map(games.map((game) => [game.id, game]));

export function enrichGame(game: Game): GameView {
  const actions = collectActions(game.enlaces, game.disponibilidad);
  const { playable, sources } = splitActions(actions);
  const tipoObraBadge = humanize(game.tipo_obra);
  const badges = [
    tipoObraBadge,
    ...game.ejes_culturales.map(humanize),
    ...activeVinculos(game).map(humanize),
  ].filter(Boolean);

  const searchParts = [
    game.titulo,
    game.descripcion,
    game.desarrollador,
    game.tipo_obra,
    game.plataformas.join(" "),
    game.generos.join(" "),
    game.ejes_culturales.join(" "),
    game.contexto_argentino.provincias.join(" "),
    game.contexto_argentino.regiones.join(" "),
    game.contexto_argentino.periodo_historico.join(" "),
    game.contexto_argentino.temas.join(" "),
    game.personajes_argentinos.map((p) => p.nombre).join(" "),
  ];

  return {
    ...game,
    actions,
    primaryAction: primaryAction(actions),
    sourceActions: sources,
    playableActions: playable,
    isPlayableToday: hasPlayableLink(game.enlaces),
    badges: Array.from(new Set(badges)),
    searchText: normalizeText(searchParts.join(" ")),
    culturalSummary: buildSummary(game),
  };
}

export function activeVinculos(game: Game) {
  const out: string[] = [];
  if (game.vinculo_argentina.escenario.activo) out.push("escenario");
  if (game.vinculo_argentina.protagonista.activo) out.push("protagonista");
  if (game.vinculo_argentina.deporte_argentino.activo) out.push("deporte");
  return out;
}

export function getStats() {
  const vinculos = { escenario: 0, protagonista: 0, deporte: 0 };
  const ejes = new Map<string, number>();
  for (const game of games) {
    if (game.vinculo_argentina.escenario.activo) vinculos.escenario += 1;
    if (game.vinculo_argentina.protagonista.activo) vinculos.protagonista += 1;
    if (game.vinculo_argentina.deporte_argentino.activo) vinculos.deporte += 1;
    for (const eje of game.ejes_culturales) {
      ejes.set(eje, (ejes.get(eje) || 0) + 1);
    }
  }

  const candidates = getCandidates();
  return {
    total: games.length,
    descartados: discarded.length,
    candidatos: candidates.length,
    vinculos,
    ejes: [...ejes.entries()].sort((a, b) => b[1] - a[1]),
  };
}

export function getFilterOptions() {
  const ejes = new Set<string>();
  const plataformas = new Set<string>();
  const provincias = new Set<string>();
  const regiones = new Set<string>();
  const disponibilidades = new Set<string>();
  const sensibilidades = new Set<string>();
  const tiposObra = new Set<string>();

  for (const game of games) {
    game.ejes_culturales.forEach((value) => ejes.add(value));
    game.plataformas.forEach((value) => plataformas.add(value));
    game.contexto_argentino.provincias.forEach((value) => provincias.add(value));
    game.contexto_argentino.regiones.forEach((value) => regiones.add(value));
    disponibilidades.add(game.disponibilidad);
    sensibilidades.add(game.sensibilidad);
    if (game.tipo_obra) tiposObra.add(game.tipo_obra);
  }

  return {
    ejes: [...ejes].sort(),
    plataformas: [...plataformas].sort(),
    provincias: [...provincias].sort(),
    regiones: [...regiones].sort(),
    disponibilidades: [...disponibilidades].sort(),
    sensibilidades: [...sensibilidades].sort(),
    tiposObra: [...tiposObra].sort(),
  };
}

export function getCandidates(): Candidate[] {
  const csvPath = path.join(process.cwd(), "data", "raw_candidates.csv");
  const csv = fs.readFileSync(csvPath, "utf-8");
  return parseCsv(csv) as Candidate[];
}

export function relatedGames(game: GameView) {
  return game.relacionado_con
    .map((id) => gameById.get(id))
    .filter((item): item is GameView => Boolean(item));
}

function buildSummary(game: Game) {
  const temas = [
    ...game.ejes_culturales.map(humanize),
    ...game.contexto_argentino.temas.slice(0, 2).map(humanize),
  ].filter(Boolean);
  const place =
    game.contexto_argentino.provincias[0] || game.contexto_argentino.regiones[0];
  const prefix = temas.length ? `${temas.slice(0, 2).join(" y ")}.` : "";
  return [prefix, place ? `Para jugar una Argentina desde ${place}.` : ""]
    .filter(Boolean)
    .join(" ");
}

function parseCsv(csv: string) {
  const lines = csv.trim().split(/\r?\n/);
  const headers = parseCsvLine(lines[0]);
  return lines.slice(1).map((line) => {
    const values = parseCsvLine(line);
    return Object.fromEntries(headers.map((header, i) => [header, values[i] || ""]));
  });
}

function parseCsvLine(line: string) {
  const values: string[] = [];
  let current = "";
  let inQuotes = false;

  for (let i = 0; i < line.length; i += 1) {
    const char = line[i];
    const next = line[i + 1];
    if (char === "\"" && next === "\"") {
      current += "\"";
      i += 1;
    } else if (char === "\"") {
      inQuotes = !inQuotes;
    } else if (char === "," && !inQuotes) {
      values.push(current);
      current = "";
    } else {
      current += char;
    }
  }
  values.push(current);
  return values;
}
