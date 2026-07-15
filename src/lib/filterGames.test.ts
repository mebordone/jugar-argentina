import { describe, expect, it } from "vitest";
import { games } from "./games";
import {
  catalogQueryForTemas,
  EMPTY_CATALOG_FILTERS,
  filterGames,
  parseCatalogFilters,
} from "./filterGames";
import { baseGameView } from "../test/fixtures/game";

const sampleGames = [
  baseGameView({
    id: "a",
    titulo: "Tango Adventure",
    ejes_culturales: ["cultura_urbana"],
    plataformas: ["PC"],
    disponibilidad: "gratis",
    sensibilidad: "baja",
    tipo_obra: "indie",
    formato: "juego_base",
    vinculo_argentina: {
      escenario: { activo: true, presencia: "principal" },
      protagonista: { activo: false, presencia: null },
      deporte_argentino: { activo: false, presencia: null },
    },
    contexto_argentino: {
      regiones: ["Patagonia"],
      provincias: ["Mendoza"],
      periodo_historico: [],
      temas: ["tango"],
    },
    enlaces: { itch: "https://example.com" },
  }),
  baseGameView({
    id: "b",
    titulo: "Sin Links",
    ejes_culturales: ["historia"],
    plataformas: ["Web"],
    disponibilidad: "perdido",
    sensibilidad: "alta",
    tipo_obra: "comercial",
    formato: "mapa",
    vinculo_argentina: {
      escenario: { activo: false, presencia: null },
      protagonista: { activo: true, presencia: "principal" },
      deporte_argentino: { activo: false, presencia: null },
    },
    contexto_argentino: {
      regiones: ["Pampeana"],
      provincias: ["Buenos Aires"],
      periodo_historico: [],
      temas: ["malvinas"],
    },
    enlaces: {},
  }),
  baseGameView({
    id: "c",
    titulo: "Futbol Deluxe",
    ejes_culturales: ["deporte"],
    plataformas: ["Android"],
    disponibilidad: "a_la_venta",
    sensibilidad: "media",
    tipo_obra: "comercial",
    formato: "contenido_licenciado",
    vinculo_argentina: {
      escenario: { activo: false, presencia: null },
      protagonista: { activo: false, presencia: null },
      deporte_argentino: { activo: true, presencia: "principal", subtipo: "liga_futbol" },
    },
    contexto_argentino: {
      regiones: ["Nacional"],
      provincias: [],
      periodo_historico: [],
      temas: ["deporte"],
    },
    enlaces: { google_play: "https://play.google.com" },
  }),
];

describe("parseCatalogFilters", () => {
  it("lee URLSearchParams", () => {
    const params = new URLSearchParams("jugable=si&eje=folclore");
    expect(parseCatalogFilters(params)).toEqual({
      ...EMPTY_CATALOG_FILTERS,
      jugable: "si",
      eje: "folclore",
    });
  });

  it("lee Record y normaliza valores vacíos", () => {
    expect(parseCatalogFilters({ q: "tango", eje: undefined })).toEqual({
      ...EMPTY_CATALOG_FILTERS,
      q: "tango",
    });
  });
});

describe("filterGames", () => {
  it("filtra por búsqueda de texto", () => {
    const result = filterGames(sampleGames, { ...EMPTY_CATALOG_FILTERS, q: "tango" });
    expect(result.map((g) => g.id)).toEqual(["a"]);
  });

  it("filtra por eje, plataforma, tipo de obra y formato", () => {
    expect(
      filterGames(sampleGames, { ...EMPTY_CATALOG_FILTERS, eje: "deporte" }).length,
    ).toBe(1);
    expect(
      filterGames(sampleGames, { ...EMPTY_CATALOG_FILTERS, plataforma: "Web" }).length,
    ).toBe(1);
    expect(
      filterGames(sampleGames, { ...EMPTY_CATALOG_FILTERS, tipo_obra: "indie" }).length,
    ).toBe(1);
    expect(
      filterGames(sampleGames, { ...EMPTY_CATALOG_FILTERS, formato: "mapa" }).map((g) => g.id),
    ).toEqual(["b"]);
  });

  it("filtra jugable si/no", () => {
    expect(
      filterGames(sampleGames, { ...EMPTY_CATALOG_FILTERS, jugable: "si" }).map((g) => g.id),
    ).toEqual(["a", "c"]);
    expect(
      filterGames(sampleGames, { ...EMPTY_CATALOG_FILTERS, jugable: "no" }).map((g) => g.id),
    ).toEqual(["b"]);
  });

  it("filtra por provincia o región", () => {
    expect(
      filterGames(sampleGames, { ...EMPTY_CATALOG_FILTERS, provincia: "Mendoza" }).length,
    ).toBe(1);
    expect(
      filterGames(sampleGames, { ...EMPTY_CATALOG_FILTERS, provincia: "Pampeana" }).length,
    ).toBe(1);
  });

  it("filtra por vínculo", () => {
    expect(
      filterGames(sampleGames, { ...EMPTY_CATALOG_FILTERS, vinculo: "escenario" }).length,
    ).toBe(1);
    expect(
      filterGames(sampleGames, { ...EMPTY_CATALOG_FILTERS, vinculo: "protagonista" }).length,
    ).toBe(1);
    expect(
      filterGames(sampleGames, { ...EMPTY_CATALOG_FILTERS, vinculo: "deporte" }).length,
    ).toBe(1);
  });

  it("filtra por disponibilidad y sensibilidad", () => {
    expect(
      filterGames(sampleGames, { ...EMPTY_CATALOG_FILTERS, disponibilidad: "gratis" }).length,
    ).toBe(1);
    expect(
      filterGames(sampleGames, { ...EMPTY_CATALOG_FILTERS, sensibilidad: "alta" }).length,
    ).toBe(1);
  });

  it("combina tema con búsqueda", () => {
    const result = filterGames(sampleGames, {
      ...EMPTY_CATALOG_FILTERS,
      tema: "malvinas",
    });
    expect(result.map((g) => g.id)).toEqual(["b"]);
  });
});

describe("catalogQueryForTemas", () => {
  it("genera query para un tema", () => {
    expect(catalogQueryForTemas(["malvinas"])).toBe("/catalogo?tema=malvinas");
  });

  it("genera búsqueda combinada para varios temas", () => {
    expect(catalogQueryForTemas(["guerra_de_malvinas", "historia"])).toBe(
      "/catalogo?q=guerra+de+malvinas+historia",
    );
  });

  it("devuelve catálogo base sin temas", () => {
    expect(catalogQueryForTemas([])).toBe("/catalogo");
  });
});

describe("regresión con catálogo real", () => {
  it("hay al menos 90 juegos jugables", () => {
    const jugables = filterGames(games, { ...EMPTY_CATALOG_FILTERS, jugable: "si" });
    expect(jugables.length).toBeGreaterThanOrEqual(90);
  });

  it("filtro tema malvinas devuelve resultados", () => {
    const malvinas = filterGames(games, { ...EMPTY_CATALOG_FILTERS, tema: "malvinas" });
    expect(malvinas.length).toBeGreaterThan(0);
  });
});
