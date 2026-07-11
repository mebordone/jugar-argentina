import { describe, expect, it } from "vitest";
import {
  destacadosForRecorrido,
  formatRecorridoFecha,
  gamesForRecorrido,
  getRecomendadosRecorrido,
  getTodayRecorrido,
  recorridos,
  recorridosForGame,
  relatedForRecorrido,
  type Recorrido,
} from "./recorridos";
import { games } from "./games";
import { baseGameView } from "../test/fixtures/game";

describe("formatRecorridoFecha", () => {
  it("formatea fechas válidas", () => {
    expect(formatRecorridoFecha("07-09")).toBe("9 de julio");
  });

  it("devuelve null para fechas inválidas o vacías", () => {
    expect(formatRecorridoFecha(null)).toBeNull();
    expect(formatRecorridoFecha("13-40")).toBeNull();
  });
});

describe("getTodayRecorrido", () => {
  it("encuentra recorrido del día", () => {
    const match = recorridos.find((item) => item.fecha);
    expect(match?.fecha).toBeTruthy();
    const [month, day] = match!.fecha!.split("-").map(Number);
    const recorrido = getTodayRecorrido(new Date(2026, month - 1, day));
    expect(recorrido.slug).toBe(match!.slug);
  });

  it("cae a independencia o primer recorrido", () => {
    const recorrido = getTodayRecorrido(new Date(2099, 0, 1));
    expect(recorrido.slug).toBe("independencia");
  });
});

describe("getRecomendadosRecorrido", () => {
  it("devuelve recorrido recomendados", () => {
    expect(getRecomendadosRecorrido().slug).toBe("recomendados");
  });
});

describe("destacadosForRecorrido", () => {
  it("resuelve juegos destacados existentes", () => {
    const recorrido = recorridos.find((item) => item.juegos_destacados.length > 0)!;
    const destacados = destacadosForRecorrido(recorrido);
    expect(destacados.length).toBeGreaterThan(0);
    expect(destacados.every((game) => recorrido.juegos_destacados.includes(game.id))).toBe(
      true,
    );
  });
});

describe("relatedForRecorrido", () => {
  it("limita recomendados a juegos jugables y relevantes", () => {
    const recorrido = getRecomendadosRecorrido();
    const related = relatedForRecorrido(recorrido);
    expect(related.every((game) => game.isPlayableToday)).toBe(true);
    expect(related.every((game) => game.grado_relevancia_argentina !== "menor")).toBe(
      true,
    );
    expect(related.some((game) => game.imagenes.portada)).toBe(true);
    expect(related.some((game) => game.tipo_obra === "comercial")).toBe(true);
  });

  it("relaciona por temas específicos", () => {
    const recorrido = recorridos.find((item) => item.temas.includes("malvinas"));
    expect(recorrido).toBeTruthy();
    const related = relatedForRecorrido(recorrido!);
    expect(related.some((game) => game.searchText.includes("malvinas"))).toBe(true);
  });

  it("usa temas amplios cuando no hay temas específicos", () => {
    const recorrido: Recorrido = {
      slug: "test-educacion",
      fecha: null,
      titulo: "Test",
      descripcion: "Test",
      temas: ["educacion"],
      juegos_destacados: [],
    };
    const related = relatedForRecorrido(recorrido);
    expect(Array.isArray(related)).toBe(true);
  });

  it("no devuelve más juegos si ya hay 18 destacados", () => {
    const recorrido: Recorrido = {
      slug: "lleno",
      fecha: null,
      titulo: "Lleno",
      descripcion: "Lleno",
      temas: ["historia"],
      juegos_destacados: games.slice(0, 18).map((game) => game.id),
    };
    expect(relatedForRecorrido(recorrido)).toEqual([]);
  });
});

describe("gamesForRecorrido", () => {
  it("combina destacados y relacionados hasta 18", () => {
    const recorrido = getRecomendadosRecorrido();
    const result = gamesForRecorrido(recorrido);
    expect(result.length).toBe(18);
  });
});

describe("recorridosForGame", () => {
  it("encuentra recorridos que incluyen un juego", () => {
    const sample = baseGameView({ id: gamesForRecorrido(getRecomendadosRecorrido())[0].id });
    const matches = recorridosForGame(sample.id);
    expect(matches.some((item) => item.slug === "recomendados")).toBe(true);
  });
});

describe("regresión recomendados", () => {
  it("recomendados tiene 18 juegos", () => {
    expect(gamesForRecorrido(getRecomendadosRecorrido()).length).toBe(18);
  });
});
