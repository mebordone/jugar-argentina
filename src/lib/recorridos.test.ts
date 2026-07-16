import { describe, expect, it } from "vitest";
import {
  countsForRecorrido,
  destacadosForRecorrido,
  FECHAS_PATRIAS_PRIORITARIAS,
  formatRecorridoFecha,
  formatRecorridoTipo,
  formatRecorridoVentana,
  gamesForRecorrido,
  getRecomendadosRecorrido,
  getTodayRecorrido,
  isDateInRecorridoWindow,
  motivoForDestacado,
  recorridoFechaLabel,
  recorridos,
  recorridosForGame,
  relatedForRecorrido,
  type Recorrido,
} from "./recorridos";
import { games } from "./games";
import { baseGameView } from "../test/fixtures/game";

function testRecorrido(overrides: Partial<Recorrido> = {}): Recorrido {
  return {
    slug: "test",
    tipo: "permanente",
    fecha: null,
    titulo: "Test",
    bajada: "Bajada",
    descripcion: "Descripción",
    criterio: "Criterio",
    temas: [],
    territorios: ["Nacional"],
    destacados_editoriales: [],
    ...overrides,
  };
}

describe("formatRecorridoFecha", () => {
  it("formatea fechas válidas", () => {
    expect(formatRecorridoFecha("07-09")).toBe("9 de julio");
  });

  it("devuelve null para fechas inválidas o vacías", () => {
    expect(formatRecorridoFecha(null)).toBeNull();
    expect(formatRecorridoFecha("13-40")).toBeNull();
    expect(formatRecorridoFecha("02-31")).toBeNull();
  });
});

describe("formatRecorridoTipo y ventana", () => {
  it("formatea tipo y ventana editorial", () => {
    expect(formatRecorridoTipo("fecha_patria")).toBe("Fecha patria");
    expect(formatRecorridoTipo("otro" as never)).toBe("otro");
    expect(
      formatRecorridoVentana({
        inicio: "07-04",
        fin: "07-09",
        etiqueta: "Semana de la Independencia",
      }),
    ).toBe("Semana de la Independencia: 4 de julio al 9 de julio");
    expect(formatRecorridoVentana()).toBeNull();
    expect(formatRecorridoVentana({ inicio: "02-31", fin: "03-01" })).toBeNull();
  });

  it("resume fecha de recorrido priorizando ventana", () => {
    expect(
      recorridoFechaLabel(
        testRecorrido({
          fecha: "07-09",
          ventana: { inicio: "07-04", fin: "07-09" },
        }),
      ),
    ).toBe("4 de julio al 9 de julio");
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

  it("encuentra recorrido por ventana temporal", () => {
    const recorrido = getTodayRecorrido(new Date(2026, 6, 6));
    expect(recorrido.slug).toBe("independencia");
  });

  it("cae a recomendados como fallback editorial", () => {
    const recorrido = getTodayRecorrido(new Date(2099, 0, 1));
    expect(recorrido.slug).toBe("recomendados");
  });
});

describe("calendario de fechas patrias", () => {
  it("cubre todas las fechas patrias prioritarias", () => {
    for (const fecha of FECHAS_PATRIAS_PRIORITARIAS) {
      expect(recorridos.some((recorrido) => recorrido.fecha === fecha.fecha)).toBe(true);
    }
  });

  it("detecta fechas dentro de ventana", () => {
    const recorrido = recorridos.find((item) => item.slug === "malvinas")!;
    expect(isDateInRecorridoWindow(recorrido, "03-30")).toBe(true);
    expect(isDateInRecorridoWindow(recorrido, "04-10")).toBe(false);
  });
});

describe("criterios curatoriales publicados", () => {
  it("mantiene política y sátira como recorrido permanente", () => {
    const recorrido = recorridos.find((item) => item.slug === "politica-satira");

    expect(recorrido?.tipo).toBe("permanente");
    expect(recorrido?.fecha).toBeNull();
    expect(recorrido?.ventana).toBeUndefined();
  });

  it("publica un recorrido permanente para pueblos originarios", () => {
    const recorrido = recorridos.find(
      (item) => item.slug === "pueblos-originarios-memorias-vivas",
    );

    expect(recorrido?.tipo).toBe("permanente");
    expect(recorrido?.fecha).toBeNull();
    expect(recorrido?.temas).toContain("pueblos_originarios");
    expect(recorrido?.destacados_editoriales.map((destacado) => destacado.id)).toEqual([
      "runa-legado-chaikuru-2025",
      "anahi-juego",
      "flora-ceibo-seeds",
      "kokena",
    ]);
  });

  it("reenfoca el 12 de octubre en conquista y resistencias", () => {
    const recorrido = recorridos.find((item) => item.slug === "diversidad-cultural");

    expect(recorrido?.tipo).toBe("fecha_patria");
    expect(recorrido?.fecha).toBe("10-12");
    expect(recorrido?.temas).toEqual(
      expect.arrayContaining(["pueblos_originarios", "conquista", "resistencias_indigenas"]),
    );
    expect(recorrido?.destacados_editoriales.map((destacado) => destacado.id)).toEqual([
      "runa-legado-chaikuru-2025",
      "anahi-juego",
      "flora-ceibo-seeds",
    ]);
  });

  it("publica recorridos para Patagonia, provincias y educación", () => {
    const expectedRoutes = [
      ["patagonia-jugable", "territorial", "antarctic-adventure-untdf"],
      ["provincias-argentinas-en-juego", "territorial", "kokena"],
      ["videojuegos-educativos-argentinos", "permanente", "de-regreso-al-habitat"],
    ] as const;

    for (const [slug, tipo, gameId] of expectedRoutes) {
      const recorrido = recorridos.find((item) => item.slug === slug);
      expect(recorrido?.tipo).toBe(tipo);
      expect(recorrido?.destacados_editoriales.map((destacado) => destacado.id)).toContain(
        gameId,
      );
    }
  });

  it("mantiene los destacados dentro del alcance refinado", () => {
    const bySlug = Object.fromEntries(recorridos.map((recorrido) => [recorrido.slug, recorrido]));
    const expectNotCurated = (slug: string, disallowedIds: string[]) => {
      const curatedIds = bySlug[slug].destacados_editoriales.map((destacado) => destacado.id);

      for (const gameId of disallowedIds) {
        expect(curatedIds).not.toContain(gameId);
      }
    };

    expectNotCurated("independencia", [
      "resistencia-en-obligado",
      "el-gaucho-martin-fierro",
      "tierras-infernales",
    ]);
    expectNotCurated("soberania-nacional", [
      "dakar-18-argentina",
      "dirt-rally-2-argentina",
      "microsoft-flight-simulator-argentina",
    ]);
    expectNotCurated("folclore-terror", [
      "tenebris-somnia",
      "doorways-holy-mountains",
      "anothers-memories",
      "drident",
      "borealis-descent",
    ]);
    expectNotCurated("tradicion-gauchesca", [
      "trucotron",
      "truco-arbiser-1982",
      "envido",
    ]);
  });
});

describe("getRecomendadosRecorrido", () => {
  it("devuelve recorrido recomendados", () => {
    expect(getRecomendadosRecorrido().slug).toBe("recomendados");
  });
});

describe("destacadosForRecorrido", () => {
  it("resuelve juegos destacados existentes", () => {
    const recorrido = recorridos.find((item) => item.destacados_editoriales.length > 0)!;
    const destacados = destacadosForRecorrido(recorrido);
    expect(destacados.length).toBeGreaterThan(0);
    expect(
      destacados.every((game) =>
        recorrido.destacados_editoriales.some((destacado) => destacado.id === game.id),
      ),
    ).toBe(true);
    expect(motivoForDestacado(recorrido, destacados[0].id).length).toBeGreaterThan(0);
    expect(motivoForDestacado(recorrido, "no-existe")).toBe("");
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
    const recorrido = testRecorrido({
      temas: ["educacion"],
    });
    const related = relatedForRecorrido(recorrido);
    expect(Array.isArray(related)).toBe(true);
  });

  it("no devuelve más juegos si ya hay 18 destacados", () => {
    const recorrido = testRecorrido({
      slug: "lleno",
      temas: ["historia"],
      destacados_editoriales: games.slice(0, 18).map((game) => ({
        id: game.id,
        motivo: "Motivo",
      })),
    });
    expect(relatedForRecorrido(recorrido)).toEqual([]);
  });

  it("relaciona por formato, género y vínculo cuando están configurados", () => {
    const recorrido = testRecorrido({
      temas: [],
      relacionados: {
        formatos: ["mapa"],
        generos: ["shooter"],
        vinculos: ["deporte"],
      },
    });
    const related = relatedForRecorrido(recorrido);
    expect(related.length).toBeGreaterThan(0);
    expect(
      related.some(
        (game) =>
          game.formato === "mapa" ||
          game.generos.includes("shooter") ||
          game.vinculo_argentina.deporte_argentino.activo,
      ),
    ).toBe(true);
  });

  it("excluye juegos relacionados configurados explícitamente", () => {
    const recorrido = testRecorrido({
      temas: ["malvinas"],
      relacionados: {
        temas: ["malvinas"],
        excluir_ids: ["malvinas-la-ultima-carta"],
      },
    });
    const related = relatedForRecorrido(recorrido);
    expect(related.some((game) => game.id === "malvinas-la-ultima-carta")).toBe(false);
  });
});

describe("gamesForRecorrido", () => {
  it("devuelve solo destacados curados", () => {
    const recorrido = getRecomendadosRecorrido();
    const result = gamesForRecorrido(recorrido);
    expect(result.length).toBe(recorrido.destacados_editoriales.length);
    expect(
      result.every((game) =>
        recorrido.destacados_editoriales.some((destacado) => destacado.id === game.id),
      ),
    ).toBe(true);
  });

  it("cuenta solo destacados curados como total público", () => {
    const recorrido = getRecomendadosRecorrido();
    const counts = countsForRecorrido(recorrido);
    expect(counts.destacados).toBe(recorrido.destacados_editoriales.length);
    expect(counts.relacionados).toBe(0);
    expect(counts.total).toBe(counts.destacados);
  });

  it("no completa el recorrido público con relacionados automáticos", () => {
    const recorrido = testRecorrido({
      slug: "limite",
      temas: ["historia"],
      destacados_editoriales: games.slice(0, 2).map((game) => ({
        id: game.id,
        motivo: "Motivo",
      })),
      relacionados: {
        temas: ["historia"],
        limite: 4,
      },
    });
    expect(gamesForRecorrido(recorrido).length).toBe(2);
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
  it("recomendados muestra solo los destacados curados", () => {
    const recorrido = getRecomendadosRecorrido();
    expect(gamesForRecorrido(recorrido).length).toBe(recorrido.destacados_editoriales.length);
  });
});
