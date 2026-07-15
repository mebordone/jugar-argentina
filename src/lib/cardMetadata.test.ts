import { describe, expect, it } from "vitest";
import {
  accessLabel,
  argentineLinkLabel,
  cardChipLabels,
  cardMetaParts,
  formatLabel,
  placeLabel,
  primaryThemeLabels,
  sensitivityCardLabel,
} from "./cardMetadata";
import { baseGameView } from "../test/fixtures/game";

describe("cardMetadata", () => {
  it("usa formato específico antes que tipo de obra", () => {
    const game = baseGameView({ tipo_obra: "mod", formato: "campania" });
    expect(formatLabel(game)).toBe("Campaña");
  });

  it("usa tipo de obra cuando es juego base", () => {
    const game = baseGameView({ tipo_obra: "indie", formato: "juego_base" });
    expect(formatLabel(game)).toBe("Indie");
  });

  it("usa fallbacks legibles para formatos y tipos desconocidos", () => {
    expect(
      formatLabel(baseGameView({ tipo_obra: "experimental", formato: "micro_juego" })),
    ).toBe("micro juego");
    expect(
      formatLabel(baseGameView({ tipo_obra: "experimental", formato: "juego_base" })),
    ).toBe("Juego");
  });

  it("elige temas sin duplicar y prioriza etiquetas legibles", () => {
    const game = baseGameView({
      ejes_culturales: ["historia"],
      contexto_argentino: {
        regiones: [],
        provincias: [],
        periodo_historico: [],
        temas: ["historia", "guerra_de_malvinas"],
      },
    });
    expect(primaryThemeLabels(game)).toEqual(["Historia", "Guerra de Malvinas"]);
  });

  it("omite temas genéricos y respeta el límite configurado", () => {
    const game = baseGameView({
      ejes_culturales: ["educacion", "folclore", "satira"],
      contexto_argentino: {
        regiones: [],
        provincias: [],
        periodo_historico: [],
        temas: ["politica"],
      },
    });
    expect(primaryThemeLabels(game, 1)).toEqual(["Folclore"]);
  });

  it("resume lugar, vínculo y acceso para una campaña de Workshop", () => {
    const game = baseGameView({
      formato: "campania",
      enlaces: { steam_workshop: "https://steamcommunity.com/item" },
      contexto_argentino: {
        regiones: ["Pampeana"],
        provincias: ["Ciudad Autónoma de Buenos Aires", "Buenos Aires"],
        periodo_historico: [],
        temas: ["cultura_urbana"],
      },
      vinculo_argentina: {
        escenario: { activo: true, presencia: "principal" },
        protagonista: { activo: false, presencia: null },
        deporte_argentino: { activo: false, presencia: null },
      },
    });

    expect(placeLabel(game)).toBe("Buenos Aires");
    expect(argentineLinkLabel(game)).toBe("Ambientado en Argentina");
    expect(accessLabel(game)).toBe("Steam Workshop");
    expect(cardMetaParts(game)).toEqual([
      "Buenos Aires",
      "Ambientado en Argentina",
      "Steam Workshop",
    ]);
  });

  it("resume lugares por provincia, región o escala nacional", () => {
    expect(
      placeLabel(
        baseGameView({
          contexto_argentino: {
            regiones: [],
            provincias: ["Mendoza"],
            periodo_historico: [],
            temas: [],
          },
        }),
      ),
    ).toBe("Mendoza");

    expect(
      placeLabel(
        baseGameView({
          contexto_argentino: {
            regiones: ["Patagonia"],
            provincias: [],
            periodo_historico: [],
            temas: [],
          },
        }),
      ),
    ).toBe("Patagonia");

    expect(
      placeLabel(
        baseGameView({
          contexto_argentino: {
            regiones: ["Nacional"],
            provincias: [],
            periodo_historico: [],
            temas: [],
          },
        }),
      ),
    ).toBe("Argentina");
  });

  it("muestra sensibilidad solo cuando no es baja", () => {
    expect(sensitivityCardLabel(baseGameView({ sensibilidad: "baja" }))).toBe("");
    expect(sensitivityCardLabel(baseGameView({ sensibilidad: "media" }))).toBe(
      "Contenido sensible",
    );
  });

  it("traduce vínculos argentinos a etiquetas públicas", () => {
    expect(
      argentineLinkLabel(
        baseGameView({
          vinculo_argentina: {
            escenario: { activo: false, presencia: null },
            protagonista: { activo: false, presencia: null },
            deporte_argentino: { activo: true, presencia: "principal", subtipo: "liga_futbol" },
          },
        }),
      ),
    ).toBe("Fútbol argentino");

    expect(
      argentineLinkLabel(
        baseGameView({
          vinculo_argentina: {
            escenario: { activo: true, presencia: "referencia_menor" },
            protagonista: { activo: false, presencia: null },
            deporte_argentino: { activo: false, presencia: null },
          },
        }),
      ),
    ).toBe("Referencia argentina");

    expect(
      argentineLinkLabel(
        baseGameView({
          vinculo_argentina: {
            escenario: { activo: false, presencia: null },
            protagonista: { activo: true, presencia: "principal" },
            deporte_argentino: { activo: false, presencia: null },
          },
        }),
      ),
    ).toBe("Protagonista argentino");

    expect(
      argentineLinkLabel(
        baseGameView({
          vinculo_argentina: {
            escenario: { activo: false, presencia: null },
            protagonista: { activo: false, presencia: null },
            deporte_argentino: { activo: true, presencia: "principal" },
          },
        }),
      ),
    ).toBe("Deporte argentino");
  });

  it("prioriza etiquetas de acceso legibles para tarjeta", () => {
    expect(
      accessLabel(
        baseGameView({
          disponibilidad: "gratis",
          enlaces: {},
        }),
      ),
    ).toBe("Gratis");

    expect(
      accessLabel(
        baseGameView({
          estado: "en_desarrollo",
          disponibilidad: "a_la_venta",
          enlaces: { steam: "https://store.steampowered.com/app/test" },
        }),
      ),
    ).toBe("Wishlist / próxima salida");

    expect(
      accessLabel(
        baseGameView({
          estado: "publicado",
          disponibilidad: "a_la_venta",
          enlaces: { steam: "https://store.steampowered.com/app/test" },
        }),
      ),
    ).toBe("A la venta");

    expect(
      accessLabel(
        baseGameView({
          disponibilidad: "abandonware",
          enlaces: { archive: "https://archive.org/item/test" },
        }),
      ),
    ).toBe("Preservación");

    expect(
      accessLabel(
        baseGameView({
          disponibilidad: "perdido",
          enlaces: {},
        }),
      ),
    ).toBe("Sin link actual");

    expect(
      accessLabel(
        baseGameView({
          disponibilidad: "desconocida",
          enlaces: { igdb: "https://igdb.com/test" },
        }),
      ),
    ).toBe("Sin link actual");

    expect(
      accessLabel(
        baseGameView({
          disponibilidad: "beta_privada",
          enlaces: { itch: "https://itch.io/test" },
        }),
      ),
    ).toBe("beta privada");
  });

  it("limita chips a formato y dos temas", () => {
    const game = baseGameView({
      tipo_obra: "comercial",
      formato: "dlc",
      ejes_culturales: ["memoria", "geografia"],
      contexto_argentino: {
        regiones: ["Patagonia"],
        provincias: ["Tierra del Fuego"],
        periodo_historico: [],
        temas: ["guerra_de_malvinas"],
      },
    });
    expect(cardChipLabels(game)).toEqual(["DLC", "Memoria", "Geografía"]);
  });
});
