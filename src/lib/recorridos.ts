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

export function gamesForRecorrido(recorrido: Recorrido): GameView[] {
  const destacados = recorrido.juegos_destacados
    .map((id) => gameById.get(id))
    .filter((game): game is GameView => Boolean(game));
  const seen = new Set(destacados.map((game) => game.id));
  const temaText = recorrido.temas.map(normalizeText);
  const matches = games.filter((game) => {
    if (seen.has(game.id)) return false;
    return temaText.some((tema) => game.searchText.includes(tema));
  });
  return [...destacados, ...matches].slice(0, 18);
}
