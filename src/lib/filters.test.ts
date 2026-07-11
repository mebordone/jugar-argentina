import { describe, expect, it } from "vitest";
import { humanize, normalizeText, placeholderClass, tipoObraTone } from "./filters";

describe("humanize", () => {
  it("devuelve cadena vacía para valores falsy", () => {
    expect(humanize(undefined)).toBe("");
    expect(humanize(null)).toBe("");
  });

  it("traduce slugs conocidos", () => {
    expect(humanize("folclore")).toBe("Folclore");
    expect(humanize("guerra_de_malvinas")).toBe("Guerra de Malvinas");
  });

  it("reemplaza guiones bajos en slugs desconocidos", () => {
    expect(humanize("ciencia_ficcion")).toBe("ciencia ficcion");
  });
});

describe("normalizeText", () => {
  it("quita diacríticos y pasa a minúsculas", () => {
    expect(normalizeText("Mendoza")).toBe("mendoza");
    expect(normalizeText("San Martín")).toBe("san martin");
  });
});

describe("tipoObraTone", () => {
  it("asigna tonos según tipo de obra", () => {
    expect(tipoObraTone("mod")).toBe("alert");
    expect(tipoObraTone("fan_game")).toBe("alert");
    expect(tipoObraTone("abandonware")).toBe("warm");
    expect(tipoObraTone("prototipo")).toBe("warm");
    expect(tipoObraTone("comercial")).toBe("cool");
    expect(tipoObraTone(undefined)).toBe("cool");
  });
});

describe("placeholderClass", () => {
  it("usa el primer eje cultural o historia por defecto", () => {
    expect(placeholderClass(["folclore"])).toBe("cover-placeholder cover-folclore");
    expect(placeholderClass([])).toBe("cover-placeholder cover-historia");
  });
});
