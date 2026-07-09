import type { GameView } from "./games";
import { normalizeText } from "./filters";

export type CatalogFilters = {
  q: string;
  eje: string;
  vinculo: string;
  plataforma: string;
  provincia: string;
  disponibilidad: string;
  sensibilidad: string;
  tipo_obra: string;
  jugable: string;
  tema: string;
};

export const EMPTY_CATALOG_FILTERS: CatalogFilters = {
  q: "",
  eje: "",
  vinculo: "",
  plataforma: "",
  provincia: "",
  disponibilidad: "",
  sensibilidad: "",
  tipo_obra: "",
  jugable: "",
  tema: "",
};

export function parseCatalogFilters(
  params: URLSearchParams | Record<string, string | undefined>,
): CatalogFilters {
  const get = (key: keyof CatalogFilters) => {
    const value =
      params instanceof URLSearchParams
        ? params.get(key)
        : params[key];
    return value || "";
  };
  return {
    q: get("q"),
    eje: get("eje"),
    vinculo: get("vinculo"),
    plataforma: get("plataforma"),
    provincia: get("provincia"),
    disponibilidad: get("disponibilidad"),
    sensibilidad: get("sensibilidad"),
    tipo_obra: get("tipo_obra"),
    jugable: get("jugable"),
    tema: get("tema"),
  };
}

export function filterGames(games: GameView[], filters: CatalogFilters) {
  const textQuery = normalizeText([filters.q, filters.tema].filter(Boolean).join(" "));
  return games.filter((game) => {
    if (textQuery && !game.searchText.includes(textQuery)) return false;
    if (filters.eje && !game.ejes_culturales.includes(filters.eje)) return false;
    if (filters.tipo_obra && game.tipo_obra !== filters.tipo_obra) return false;
    if (filters.jugable === "si" && !game.isPlayableToday) return false;
    if (filters.jugable === "no" && game.isPlayableToday) return false;
    if (filters.plataforma && !game.plataformas.includes(filters.plataforma)) return false;
    if (
      filters.provincia &&
      !game.contexto_argentino.provincias.includes(filters.provincia) &&
      !game.contexto_argentino.regiones.includes(filters.provincia)
    ) {
      return false;
    }
    if (filters.disponibilidad && game.disponibilidad !== filters.disponibilidad) {
      return false;
    }
    if (filters.sensibilidad && game.sensibilidad !== filters.sensibilidad) {
      return false;
    }
    if (filters.vinculo) {
      const vinculo = game.vinculo_argentina;
      if (filters.vinculo === "escenario" && !vinculo.escenario.activo) return false;
      if (filters.vinculo === "protagonista" && !vinculo.protagonista.activo) {
        return false;
      }
      if (filters.vinculo === "deporte" && !vinculo.deporte_argentino.activo) {
        return false;
      }
    }
    return true;
  });
}

export function catalogQueryForTemas(temas: string[]) {
  const params = new URLSearchParams();
  if (temas.length === 1) {
    params.set("tema", temas[0]);
  } else if (temas.length > 1) {
    params.set("q", temas.map((tema) => tema.replaceAll("_", " ")).join(" "));
  }
  const query = params.toString();
  return query ? `/catalogo?${query}` : "/catalogo";
}
