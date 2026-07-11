import { beforeEach, describe, expect, it, vi } from "vitest";
import { getCandidates } from "./games";
import { listaBySlug, listaHrefByStatKey, listas } from "./listas";

vi.mock("./games", async (importOriginal) => {
  const actual = await importOriginal<typeof import("./games")>();
  return {
    ...actual,
    getCandidates: vi.fn(() => [
      {
        titulo: "Candidato Test",
        anio: "2024",
        estado_juego: "publicado",
        vinculo_preliminar: "escenario",
        fuente: "fuente",
        url: "https://example.com",
        nota: "nota",
        estado_triage: "pendiente",
        eje_sugerido: "historia",
        ejes_culturales_sugeridos: "historia",
        notas_triage: "notas",
      },
    ]),
  };
});

describe("listas", () => {
  beforeEach(() => {
    vi.mocked(getCandidates).mockReturnValue([
      {
        titulo: "Candidato Test",
        anio: "2024",
        estado_juego: "publicado",
        vinculo_preliminar: "escenario",
        fuente: "fuente",
        url: "https://example.com",
        nota: "nota",
        estado_triage: "pendiente",
        eje_sugerido: "historia",
        ejes_culturales_sugeridos: "historia",
        notas_triage: "notas",
      },
    ]);
  });

  it("expone listas con items y metadatos", () => {
    expect(listas.length).toBeGreaterThan(0);
    for (const lista of listas) {
      expect(lista.slug).toBeTruthy();
      expect(lista.getItems().length).toBeGreaterThan(0);
      expect(lista.getItems()[0].titulo).toBeTruthy();
    }
  });

  it("resuelve listaBySlug", () => {
    expect(listaBySlug.get("juegos-verificados")?.titulo).toBe("Juegos verificados");
  });

  it("mapea stat keys a href", () => {
    expect(listaHrefByStatKey.total).toBe("/listas/juegos-verificados");
    expect(listaHrefByStatKey.candidatos).toBe("/listas/candidatos");
  });

  it("marca candidatos como externos cuando tienen url", () => {
    const candidatos = listaBySlug.get("candidatos")!.getItems();
    expect(candidatos[0].external).toBe(true);
    expect(candidatos[0].href).toBe("https://example.com");
  });

  it("ordena candidatos y omite url cuando no existe", () => {
    vi.mocked(getCandidates).mockReturnValue([
      {
        titulo: "Zeta",
        anio: "2024",
        estado_juego: "publicado",
        vinculo_preliminar: "escenario",
        fuente: "fuente",
        url: "",
        nota: "nota",
        estado_triage: "pendiente",
        eje_sugerido: "historia",
        ejes_culturales_sugeridos: "historia",
        notas_triage: "notas",
      },
      {
        titulo: "Alpha",
        anio: "",
        estado_juego: "",
        vinculo_preliminar: "escenario",
        fuente: "fuente",
        url: "https://alpha.example",
        nota: "nota",
        estado_triage: "",
        eje_sugerido: "",
        ejes_culturales_sugeridos: "",
        notas_triage: "notas",
      },
    ]);

    const candidatos = listaBySlug.get("candidatos")!.getItems();
    expect(candidatos.map((item) => item.titulo)).toEqual(["Alpha", "Zeta"]);
    expect(candidatos[0].subtitulo).toContain("Sin año");
    expect(candidatos[1].external).toBe(false);
    expect(candidatos[1].href).toBeUndefined();
  });
});
