import { describe, expect, it } from "vitest";
import { buildCulturalSummary } from "./culturalSummary";
import { baseGame } from "../test/fixtures/game";

describe("buildCulturalSummary", () => {
  it("deduplica geografia en eje y tema", () => {
    expect(
      buildCulturalSummary(
        baseGame({
          ejes_culturales: ["geografia"],
          contexto_argentino: {
            regiones: ["Pampeana"],
            provincias: ["Buenos Aires"],
            periodo_historico: ["contemporaneo"],
            temas: ["geografia"],
          },
          vinculo_argentina: {
            escenario: { activo: true, presencia: "principal" },
            protagonista: { activo: false, presencia: null },
            deporte_argentino: { activo: false, presencia: null },
          },
        }),
      ),
    ).toBe("Geografía. Escenario argentino. Ambientado en Buenos Aires.");
  });

  it("usa frase de región macro", () => {
    expect(
      buildCulturalSummary(
        baseGame({
          contexto_argentino: {
            regiones: ["Patagonia"],
            provincias: [],
            periodo_historico: ["contemporaneo"],
            temas: ["historia"],
          },
          ejes_culturales: ["historia"],
          vinculo_argentina: {
            escenario: { activo: true, presencia: "principal" },
            protagonista: { activo: false, presencia: null },
            deporte_argentino: { activo: false, presencia: null },
          },
        }),
      ),
    ).toBe("Historia. Escenario argentino. Una mirada jugable sobre la región Patagonia.");
  });

  it("omite frase de lugar para Nacional", () => {
    expect(
      buildCulturalSummary(
        baseGame({
          ejes_culturales: ["geografia"],
          tipo_obra: "educativo",
          contexto_argentino: {
            regiones: ["Nacional"],
            provincias: [],
            periodo_historico: ["contemporaneo"],
            temas: [],
          },
          vinculo_argentina: {
            escenario: { activo: true, presencia: "principal" },
            protagonista: { activo: false, presencia: null },
            deporte_argentino: { activo: false, presencia: null },
          },
        }),
      ),
    ).toBe("Experiencia educativa sobre geografía.");
  });

  it("humaniza temas crudos", () => {
    expect(
      buildCulturalSummary(
        baseGame({
          contexto_argentino: {
            regiones: ["Patagonia"],
            provincias: [],
            periodo_historico: ["contemporaneo"],
            temas: ["guerra_de_malvinas"],
          },
          ejes_culturales: ["memoria"],
          vinculo_argentina: {
            escenario: { activo: true, presencia: "principal" },
            protagonista: { activo: false, presencia: null },
            deporte_argentino: { activo: false, presencia: null },
          },
        }),
      ).startsWith("Memoria y Guerra de Malvinas."),
    ).toBe(true);
  });

  it("enriquece resumen deportivo", () => {
    expect(
      buildCulturalSummary(
        baseGame({
          ejes_culturales: ["deporte"],
          contexto_argentino: {
            regiones: [],
            provincias: [],
            periodo_historico: ["contemporaneo"],
            temas: ["deporte"],
          },
          descripcion:
            "Segunda edición argentina de PC Fútbol con el torneo Apertura 1995 y base de datos elaborada por periodistas locales.",
          vinculo_argentina: {
            escenario: { activo: false, presencia: null },
            protagonista: { activo: false, presencia: null },
            deporte_argentino: {
              activo: true,
              presencia: "principal",
              subtipo: "liga_futbol",
            },
          },
        }),
      ),
    ).toBe("Deporte. Deporte y cultura argentina.");
  });

  it("prefija mods y fan games", () => {
    expect(
      buildCulturalSummary(
        baseGame({
          tipo_obra: "mod",
          ejes_culturales: ["politica"],
          vinculo_argentina: {
            escenario: { activo: true, presencia: "principal" },
            protagonista: { activo: false, presencia: null },
            deporte_argentino: { activo: false, presencia: null },
          },
        }),
      ),
    ).toBe("Relectura argentina: Política. Escenario argentino.");
  });

  it("prefija fan games como relectura argentina", () => {
    expect(
      buildCulturalSummary(
        baseGame({
          descripcion: "",
          tipo_obra: "fan_game",
          ejes_culturales: ["folclore"],
          vinculo_argentina: {
            escenario: { activo: false, presencia: null },
            protagonista: { activo: false, presencia: null },
            deporte_argentino: { activo: false, presencia: null },
          },
        }),
      ),
    ).toBe("Relectura argentina: Folclore.");
  });

  it("prefija fan game con dos ejes y escenario", () => {
    expect(
      buildCulturalSummary(
        baseGame({
          descripcion: "",
          tipo_obra: "fan_game",
          ejes_culturales: ["historia", "folclore"],
          vinculo_argentina: {
            escenario: { activo: true, presencia: "principal" },
            protagonista: { activo: false, presencia: null },
            deporte_argentino: { activo: false, presencia: null },
          },
        }),
      ),
    ).toBe("Relectura argentina: Historia y Folclore. Escenario argentino.");
  });

  it("usa protagonista y referencia menor de escenario", () => {
    expect(
      buildCulturalSummary(
        baseGame({
          ejes_culturales: ["historia"],
          vinculo_argentina: {
            escenario: { activo: true, presencia: "referencia_menor" },
            protagonista: { activo: true, presencia: "principal" },
            deporte_argentino: { activo: false, presencia: null },
          },
        }),
      ),
    ).toBe("Historia. Protagonistas y figuras argentinas.");
  });

  it("usa fallback de descripción cuando el resumen es genérico", () => {
    const descripcion =
      "Aventura extensa sobre la historia reciente con múltiples referencias documentadas y contexto local detallado para lectores.";
    expect(
      buildCulturalSummary(
        baseGame({
          ejes_culturales: ["historia"],
          descripcion,
          vinculo_argentina: {
            escenario: { activo: false, presencia: null },
            protagonista: { activo: false, presencia: null },
            deporte_argentino: { activo: false, presencia: null },
          },
        }),
      ),
    ).toBe(descripcion);
  });

  it("trunca descripciones largas en fallback", () => {
    const descripcion = `${"Palabra ".repeat(40).trim()}.`;
    const summary = buildCulturalSummary(
      baseGame({
        ejes_culturales: ["historia"],
        descripcion,
        vinculo_argentina: {
          escenario: { activo: false, presencia: null },
          protagonista: { activo: false, presencia: null },
          deporte_argentino: { activo: false, presencia: null },
        },
      }),
    );
    expect(summary.endsWith("...")).toBe(true);
    expect(summary.length).toBeLessThanOrEqual(143);
  });

  it("devuelve fallback por defecto sin datos", () => {
    expect(
      buildCulturalSummary(
        baseGame({
          descripcion: "",
          ejes_culturales: [],
          contexto_argentino: {
            regiones: [],
            provincias: [],
            periodo_historico: [],
            temas: [],
          },
        }),
      ),
    ).toBe("Recorrido por imaginarios argentinos.");
  });

  it("combina dos ejes en una sola frase", () => {
    expect(
      buildCulturalSummary(
        baseGame({
          descripcion: "",
          ejes_culturales: ["historia", "folclore"],
          vinculo_argentina: {
            escenario: { activo: true, presencia: "principal" },
            protagonista: { activo: false, presencia: null },
            deporte_argentino: { activo: false, presencia: null },
          },
        }),
      ),
    ).toBe("Historia y Folclore. Escenario argentino.");
  });

  it("combina dos ejes con enriquecimiento deportivo", () => {
    expect(
      buildCulturalSummary(
        baseGame({
          descripcion: "",
          ejes_culturales: ["historia", "deporte"],
          vinculo_argentina: {
            escenario: { activo: false, presencia: null },
            protagonista: { activo: false, presencia: null },
            deporte_argentino: { activo: true, presencia: "principal" },
          },
        }),
      ),
    ).toBe("Historia y Deporte. Deporte y cultura argentina.");
  });

  it("combina dos ejes con protagonistas argentinos", () => {
    expect(
      buildCulturalSummary(
        baseGame({
          descripcion: "",
          ejes_culturales: ["historia", "folclore"],
          vinculo_argentina: {
            escenario: { activo: false, presencia: null },
            protagonista: { activo: true, presencia: "principal" },
            deporte_argentino: { activo: false, presencia: null },
          },
        }),
      ),
    ).toBe("Historia y Folclore. Protagonistas y figuras argentinas.");
  });

  it("combina dos ejes con referencia menor de escenario", () => {
    expect(
      buildCulturalSummary(
        baseGame({
          descripcion: "",
          ejes_culturales: ["historia", "folclore"],
          vinculo_argentina: {
            escenario: { activo: true, presencia: "referencia_menor" },
            protagonista: { activo: false, presencia: null },
            deporte_argentino: { activo: false, presencia: null },
          },
        }),
      ),
    ).toBe("Historia y Folclore. Referencia a Argentina.");
  });

  it("combina dos ejes sin enriquecimiento de vínculo", () => {
    expect(
      buildCulturalSummary(
        baseGame({
          descripcion: "",
          ejes_culturales: ["historia", "folclore"],
          vinculo_argentina: {
            escenario: { activo: false, presencia: null },
            protagonista: { activo: false, presencia: null },
            deporte_argentino: { activo: false, presencia: null },
          },
        }),
      ),
    ).toBe("Historia y Folclore.");
  });

  it("usa referencia menor de escenario", () => {
    expect(
      buildCulturalSummary(
        baseGame({
          descripcion: "",
          ejes_culturales: ["historia"],
          vinculo_argentina: {
            escenario: { activo: true, presencia: "referencia_menor" },
            protagonista: { activo: false, presencia: null },
            deporte_argentino: { activo: false, presencia: null },
          },
        }),
      ),
    ).toBe("Historia. Referencia a Argentina.");
  });

  it("usa descripción cuando el resumen temático queda genérico", () => {
    const descripcion =
      "Relato extenso sobre folclore argentino con referencias documentadas y contexto regional para lectores del catálogo.";
    expect(
      buildCulturalSummary(
        baseGame({
          ejes_culturales: ["folclore"],
          descripcion,
          vinculo_argentina: {
            escenario: { activo: false, presencia: null },
            protagonista: { activo: false, presencia: null },
            deporte_argentino: { activo: false, presencia: null },
          },
        }),
      ),
    ).toBe(descripcion);
  });

  it("marca como genérico un eje amplio sin enriquecimiento ni lugar", () => {
    const descripcion =
      "Descripción editorial suficientemente extensa para reemplazar un resumen demasiado genérico sobre historia argentina.";
    expect(
      buildCulturalSummary(
        baseGame({
          ejes_culturales: ["historia"],
          descripcion,
          vinculo_argentina: {
            escenario: { activo: false, presencia: null },
            protagonista: { activo: false, presencia: null },
            deporte_argentino: { activo: false, presencia: null },
          },
        }),
      ),
    ).toBe(descripcion);
  });

  it("trunca texto compacto sin espacios útiles", () => {
    const descripcion = "X".repeat(150);
    const summary = buildCulturalSummary(
      baseGame({
        ejes_culturales: ["historia"],
        descripcion,
        vinculo_argentina: {
          escenario: { activo: false, presencia: null },
          protagonista: { activo: false, presencia: null },
          deporte_argentino: { activo: false, presencia: null },
        },
      }),
    );
    expect(summary.endsWith("...")).toBe(true);
    expect(summary.length).toBeLessThanOrEqual(143);
  });

  it("usa descripción cuando no hay temas ni vínculos", () => {
    expect(
      buildCulturalSummary(
        baseGame({
          ejes_culturales: [],
          contexto_argentino: {
            regiones: [],
            provincias: [],
            periodo_historico: [],
            temas: [],
          },
          descripcion: "Resumen editorial disponible sin estructura temática previa.",
          vinculo_argentina: {
            escenario: { activo: false, presencia: null },
            protagonista: { activo: false, presencia: null },
            deporte_argentino: { activo: false, presencia: null },
          },
        }),
      ),
    ).toBe("Resumen editorial disponible sin estructura temática previa.");
  });
});
