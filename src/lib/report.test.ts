import { describe, expect, it } from "vitest";
import { reportGameUrl } from "./report";

describe("reportGameUrl", () => {
  it("genera URL de issue en GitHub con parámetros del juego", () => {
    const url = reportGameUrl({ id: "atuel", titulo: "Atuel" });
    expect(url).toContain("github.com/");
    expect(url).toContain("issues/new");
    expect(url).toContain("template=sugerir-correccion.yml");
    const params = new URL(url).searchParams;
    expect(params.get("title")).toBe("[Corrección] Atuel");
    expect(url).toContain("juego-id=atuel");
    expect(url).toContain(encodeURIComponent("http://localhost:4321/juegos/atuel"));
  });
});
