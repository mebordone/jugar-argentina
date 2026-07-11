import { beforeEach, describe, expect, it, vi } from "vitest";

vi.mock("./games", async (importOriginal) => {
  const actual = await importOriginal<typeof import("./games")>();
  const { baseGame } = await vi.importActual<typeof import("../test/fixtures/game")>(
    "../test/fixtures/game",
  );

  const scored = [
    actual.enrichGame(
      baseGame({
        id: "mejor-puntaje",
        titulo: "Mejor puntaje",
        grado_relevancia_argentina: "central",
        disponibilidad: "gratis",
        tipo_obra: "indie",
        calidad_fuente: "oficial",
        ejes_culturales: ["historia"],
        generos: ["aventura"],
        imagenes: { portada: "https://example.com/a.jpg", capturas: [] },
        enlaces: { itch: "https://itch.io/mejor" },
      }),
    ),
    actual.enrichGame(
      baseGame({
        id: "peor-puntaje",
        titulo: "Peor puntaje",
        grado_relevancia_argentina: "importante",
        disponibilidad: "abandonware",
        tipo_obra: "comercial",
        calidad_fuente: "prensa",
        ejes_culturales: [],
        generos: ["deportes"],
        imagenes: { portada: null, capturas: [] },
        enlaces: { itch: "https://itch.io/peor" },
      }),
    ),
  ];

  return {
    ...actual,
    games: scored,
    gameById: new Map(scored.map((game) => [game.id, game])),
  };
});

import { getRecomendadosRecorrido, relatedForRecorrido } from "./recorridos";

describe("qualityScore via recomendados", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("ordena juegos jugables priorizando mejor puntaje compuesto", () => {
    const related = relatedForRecorrido(getRecomendadosRecorrido());
    expect(related.map((game) => game.id)).toEqual(["mejor-puntaje", "peor-puntaje"]);
  });
});
