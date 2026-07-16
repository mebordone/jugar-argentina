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
    actual.enrichGame(
      baseGame({
        id: "sin-link",
        titulo: "Sin link",
        grado_relevancia_argentina: "central",
        disponibilidad: "perdido",
        ejes_culturales: ["historia"],
        enlaces: {},
      }),
    ),
    actual.enrichGame(
      baseGame({
        id: "referencia-menor",
        titulo: "Referencia menor",
        grado_relevancia_argentina: "menor",
        disponibilidad: "gratis",
        ejes_culturales: ["historia"],
        enlaces: { itch: "https://itch.io/menor" },
      }),
    ),
  ];

  return {
    ...actual,
    games: scored,
    gameById: new Map(scored.map((game) => [game.id, game])),
  };
});

import { getRecomendadosRecorrido, relatedForRecorrido, type Recorrido } from "./recorridos";

describe("qualityScore via recomendados", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("ordena juegos jugables priorizando mejor puntaje compuesto", () => {
    const related = relatedForRecorrido(getRecomendadosRecorrido());
    expect(related.map((game) => game.id)).toEqual(["mejor-puntaje", "peor-puntaje"]);
  });

  it("descarta no jugables y referencias menores cuando el recorrido lo pide", () => {
    const recorrido: Recorrido = {
      slug: "historia-jugable",
      tipo: "permanente",
      fecha: null,
      titulo: "Historia jugable",
      bajada: "Bajada",
      descripcion: "Descripción",
      criterio: "Criterio",
      temas: ["historia"],
      territorios: ["Nacional"],
      destacados_editoriales: [],
      relacionados: {
        temas: ["historia"],
        ejes: ["historia"],
        solo_jugables: true,
        excluir_relevancia_menor: true,
      },
    };

    expect(relatedForRecorrido(recorrido).map((game) => game.id)).toEqual([
      "mejor-puntaje",
    ]);
  });
});
