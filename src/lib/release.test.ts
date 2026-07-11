import { describe, expect, it } from "vitest";
import { gameReleaseEyebrow, gameReleasePrimary } from "./release";
import { baseGame } from "../test/fixtures/game";

describe("gameReleasePrimary", () => {
  it("prioriza año numérico", () => {
    expect(gameReleasePrimary(baseGame({ anio: 1995 }))).toBe("1995");
  });

  it("usa anio_nota si no hay año", () => {
    expect(
      gameReleasePrimary(baseGame({ anio: null, anio_nota: "Próximamente" })),
    ).toBe("Próximamente");
  });

  it("humaniza estados de lanzamiento", () => {
    expect(
      gameReleasePrimary(baseGame({ anio: null, estado: "en_desarrollo" })),
    ).toBe("En desarrollo");
  });

  it("devuelve Sin fecha como fallback", () => {
    expect(
      gameReleasePrimary(baseGame({ anio: null, anio_nota: null, estado: "publicado" })),
    ).toBe("Sin fecha");
  });

  it("humaniza early access y prototipo", () => {
    expect(gameReleasePrimary(baseGame({ anio: null, estado: "early_access" }))).toBe(
      "Early access",
    );
    expect(gameReleasePrimary(baseGame({ anio: null, estado: "prototipo" }))).toBe(
      "Prototipo",
    );
  });
});

describe("gameReleaseEyebrow", () => {
  it("combina año y estado", () => {
    expect(gameReleaseEyebrow(baseGame({ anio: 2020, estado: "publicado" }))).toBe(
      "2020 · Publicado",
    );
  });

  it("usa anio_nota con estado", () => {
    expect(
      gameReleaseEyebrow(
        baseGame({ anio: null, anio_nota: "Por confirmarse", estado: "en_desarrollo" }),
      ),
    ).toBe("Por confirmarse · En desarrollo");
  });

  it("devuelve solo estado cuando no hay fecha", () => {
    expect(
      gameReleaseEyebrow(baseGame({ anio: null, anio_nota: null, estado: "cancelado" })),
    ).toBe("Cancelado");
  });

  it("combina estado de lanzamiento cuando difiere del label humanizado", () => {
    expect(
      gameReleaseEyebrow(
        baseGame({ anio: null, anio_nota: null, estado: "early_access" }),
      ),
    ).toBe("Early access");
  });
});
