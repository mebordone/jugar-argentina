import { describe, expect, it } from "vitest";
import { buildComoJugarSteps, sensibilidadNotice } from "./comoJugar";
import { baseGame } from "../test/fixtures/game";

describe("buildComoJugarSteps", () => {
  it("agrega paso para mods", () => {
    const steps = buildComoJugarSteps(baseGame({ tipo_obra: "mod", formato: "mod" }));
    expect(steps[0].title).toBe("Revisá el juego base");
  });

  it("cubre cada disponibilidad", () => {
    expect(
      buildComoJugarSteps(baseGame({ disponibilidad: "a_la_venta" }))[0].title,
    ).toBe("Comprá o agregalo a tu biblioteca");
    expect(
      buildComoJugarSteps(baseGame({ disponibilidad: "gratis" }))[0].title,
    ).toBe("Descargalo o jugalo en la web");
    expect(
      buildComoJugarSteps(baseGame({ disponibilidad: "abandonware" }))[0].title,
    ).toBe("Buscá una copia preservada");
    expect(
      buildComoJugarSteps(baseGame({ disponibilidad: "perdido" }))[0].title,
    ).toBe("Consultá fuentes de preservación");
    expect(
      buildComoJugarSteps(baseGame({ disponibilidad: "desconocido" as "gratis" }))[0].title,
    ).toBe("Revisá los enlaces disponibles");
  });

  it("agrega paso de workshop y estado en desarrollo", () => {
    const steps = buildComoJugarSteps(
      baseGame({
        enlaces: { steam_workshop: "https://steamcommunity.com/mod" },
        estado: "early_access",
      }),
    );
    expect(steps.some((s) => s.title === "Suscribite en Workshop")).toBe(true);
    expect(steps.some((s) => s.title === "Tené en cuenta el estado del proyecto")).toBe(
      true,
    );
  });

  it("agrega aviso de sensibilidad media o alta", () => {
    const steps = buildComoJugarSteps(baseGame({ sensibilidad: "alta" }));
    expect(steps.some((s) => s.title === "Contenido sensible")).toBe(true);
  });
});

describe("sensibilidadNotice", () => {
  it("devuelve avisos según nivel", () => {
    expect(sensibilidadNotice("alta")).toContain("alta sensibilidad");
    expect(sensibilidadNotice("media")).toContain("temas sensibles");
    expect(sensibilidadNotice("baja")).toBeNull();
  });
});
