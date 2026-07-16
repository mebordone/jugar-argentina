import { describe, expect, it } from "vitest";
import { formatFechaAlta, sortListaItems } from "./listaSort";

describe("listaSort", () => {
  const items = [
    { titulo: "Beta", fecha_alta: "2026-07-15T18:00:10-03:00", anio: 2010 },
    { titulo: "Alpha", fecha_alta: "2026-07-09T16:00:56-03:00", anio: 2020 },
    { titulo: "Gamma", fecha_alta: "2026-07-15T18:00:20-03:00", anio: null },
  ];

  it("ordena alfabéticamente en ambos sentidos", () => {
    expect(sortListaItems(items, "titulo-asc").map((item) => item.titulo)).toEqual([
      "Alpha",
      "Beta",
      "Gamma",
    ]);
    expect(sortListaItems(items, "titulo-desc").map((item) => item.titulo)).toEqual([
      "Gamma",
      "Beta",
      "Alpha",
    ]);
  });

  it("ordena por fecha_alta con timestamp, no solo alfabético", () => {
    expect(sortListaItems(items, "fecha_alta-desc").map((item) => item.titulo)).toEqual([
      "Gamma",
      "Beta",
      "Alpha",
    ]);
    expect(sortListaItems(items, "fecha_alta-asc").map((item) => item.titulo)).toEqual([
      "Alpha",
      "Beta",
      "Gamma",
    ]);
  });

  it("ordena por año y pone null al final en descendente", () => {
    expect(sortListaItems(items, "anio-desc").map((item) => item.titulo)).toEqual([
      "Alpha",
      "Beta",
      "Gamma",
    ]);
    expect(sortListaItems(items, "anio-asc").map((item) => item.titulo)).toEqual([
      "Gamma",
      "Beta",
      "Alpha",
    ]);
  });

  it("tolera fechas inválidas o ausentes al ordenar", () => {
    const messy = [
      { titulo: "SinFecha", fecha_alta: undefined, anio: 2001 },
      { titulo: "Invalida", fecha_alta: "no-es-fecha", anio: 2002 },
      { titulo: "Valida", fecha_alta: "2026-07-15", anio: 2000 },
    ];
    expect(sortListaItems(messy, "fecha_alta-desc").map((item) => item.titulo)).toEqual([
      "Valida",
      "Invalida",
      "SinFecha",
    ]);
    expect(sortListaItems(messy, "fecha_alta-asc").map((item) => item.titulo)[0]).toBe("Valida");
  });

  it("formatea fecha_alta para mostrar solo el día", () => {
    expect(formatFechaAlta("2026-07-15T18:00:20-03:00")).toBe("2026-07-15");
    expect(formatFechaAlta(undefined)).toBe("");
    expect(formatFechaAlta("texto")).toBe("texto");
  });
});
