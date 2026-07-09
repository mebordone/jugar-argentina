import efemerides from "../content/efemerides.json";
import { gameById, games, type GameView } from "./games";
import { normalizeText } from "./filters";

export type Recorrido = {
  slug: string;
  fecha: string | null;
  titulo: string;
  descripcion: string;
  temas: string[];
  juegos_destacados: string[];
};

export const recorridos = efemerides as Recorrido[];

const MAX_RECORRIDO_GAMES = 18;

const BROAD_TEMAS = new Set(["historia", "educacion", "educativo", "geografia"]);

const RELEVANCIA_ORDER: Record<string, number> = {
  central: 0,
  importante: 1,
  menor: 2,
};

const MESES = [
  "enero",
  "febrero",
  "marzo",
  "abril",
  "mayo",
  "junio",
  "julio",
  "agosto",
  "septiembre",
  "octubre",
  "noviembre",
  "diciembre",
];

export function formatRecorridoFecha(fecha: string | null) {
  if (!fecha) return null;
  const [mm, dd] = fecha.split("-");
  const mes = MESES[Number(mm) - 1];
  if (!mes) return null;
  return `${Number(dd)} de ${mes}`;
}

export function getTodayRecorrido(date = new Date()) {
  const today = `${String(date.getMonth() + 1).padStart(2, "0")}-${String(
    date.getDate(),
  ).padStart(2, "0")}`;
  return (
    recorridos.find((recorrido) => recorrido.fecha === today) ||
    recorridos.find((recorrido) => recorrido.slug === "independencia") ||
    recorridos[0]
  );
}

export function getRecomendadosRecorrido() {
  return (
    recorridos.find((recorrido) => recorrido.slug === "recomendados") ||
    recorridos[recorridos.length - 1]
  );
}

function qualityScore(game: GameView) {
  let score = RELEVANCIA_ORDER[game.grado_relevancia_argentina] ?? 3;
  if (!game.isPlayableToday) score += 10;
  if (game.disponibilidad === "abandonware") score += 2;
  if (game.tipo_obra === "comercial") score -= 0.5;
  if (game.imagenes.portada) score -= 0.25;
  if (game.calidad_fuente === "oficial") score -= 0.25;
  if (game.ejes_culturales.length > 0) score -= 0.5;
  if (game.generos.includes("deportes")) score += 1;
  return score;
}

export function destacadosForRecorrido(recorrido: Recorrido): GameView[] {
  return recorrido.juegos_destacados
    .map((id) => gameById.get(id))
    .filter((game): game is GameView => Boolean(game));
}

function specificTemas(recorrido: Recorrido) {
  return recorrido.temas
    .filter((tema) => !BROAD_TEMAS.has(tema))
    .map(normalizeText);
}

function gameMatchesRecorrido(game: GameView, recorrido: Recorrido) {
  const temas = specificTemas(recorrido);
  if (!temas.length) {
    return recorrido.temas
      .map(normalizeText)
      .some((tema) => game.searchText.includes(tema));
  }
  return temas.some((tema) => game.searchText.includes(tema));
}

export function relatedForRecorrido(recorrido: Recorrido): GameView[] {
  const destacados = destacadosForRecorrido(recorrido);
  const seen = new Set(destacados.map((game) => game.id));
  const remaining = MAX_RECORRIDO_GAMES - destacados.length;
  if (remaining <= 0) return [];

  if (recorrido.slug === "recomendados") {
    return games
      .filter(
        (game) =>
          !seen.has(game.id) &&
          game.grado_relevancia_argentina !== "menor" &&
          game.isPlayableToday,
      )
      .sort((a, b) => qualityScore(a) - qualityScore(b))
      .slice(0, remaining);
  }

  return games
    .filter((game) => !seen.has(game.id) && gameMatchesRecorrido(game, recorrido))
    .slice(0, remaining);
}

export function gamesForRecorrido(recorrido: Recorrido): GameView[] {
  return [...destacadosForRecorrido(recorrido), ...relatedForRecorrido(recorrido)];
}

export function recorridosForGame(gameId: string): Recorrido[] {
  return recorridos.filter((recorrido) =>
    gamesForRecorrido(recorrido).some((game) => game.id === gameId),
  );
}
