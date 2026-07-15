import fs from "node:fs";
import { beforeEach, describe, expect, it, vi } from "vitest";
import {
  activeVinculos,
  enrichGame,
  gameById,
  games,
  getCandidates,
  getFilterOptions,
  getStats,
  relatedGames,
} from "./games";
import { baseGame, baseGameView } from "../test/fixtures/game";

vi.mock("node:fs", () => ({
  default: {
    readFileSync: vi.fn(),
  },
}));

describe("enrichGame", () => {
  it("genera acciones, badges y searchText", () => {
    const view = enrichGame(
      baseGame({
        titulo: "Atuel",
        enlaces: { itch: "https://itch.io/atuel" },
        ejes_culturales: ["geografia"],
        vinculo_argentina: {
          escenario: { activo: true, presencia: "principal" },
          protagonista: { activo: false, presencia: null },
          deporte_argentino: { activo: false, presencia: null },
        },
      }),
    );
    expect(view.primaryAction?.type).toBe("play");
    expect(view.isPlayableToday).toBe(true);
    expect(view.badges).toContain("Geografía");
    expect(view.searchText).toContain("atuel");
    expect(view.culturalSummary.length).toBeGreaterThan(0);
  });

  it("prioriza Buscar descarga en abandonware con archive", () => {
    const view = enrichGame(
      baseGame({
        disponibilidad: "abandonware",
        enlaces: { archive: "https://archive.org/item" },
      }),
    );
    expect(view.primaryAction?.label).toBe("Buscar descarga");
    expect(view.primaryAction?.type).toBe("download");
  });
});

describe("activeVinculos", () => {
  it("lista vínculos activos", () => {
    expect(
      activeVinculos(
        baseGame({
          vinculo_argentina: {
            escenario: { activo: true, presencia: "principal" },
            protagonista: { activo: true, presencia: "principal" },
            deporte_argentino: { activo: false, presencia: null },
          },
        }),
      ),
    ).toEqual(["escenario", "protagonista"]);
  });
});

describe("relatedGames", () => {
  it("resuelve ids relacionados existentes", () => {
    const anchor = games.find((game) => game.relacionado_con.length > 0);
    expect(anchor).toBeTruthy();
    const related = relatedGames(anchor!);
    expect(related.length).toBeGreaterThan(0);
    expect(related.every((game) => anchor!.relacionado_con.includes(game.id))).toBe(
      true,
    );
  });

  it("ignora ids inexistentes", () => {
    const orphan = baseGameView({ relacionado_con: ["no-existe-123"] });
    expect(relatedGames(orphan)).toEqual([]);
  });
});

describe("getCandidates", () => {
  beforeEach(() => {
    vi.mocked(fs.readFileSync).mockReturnValue(
      [
        "titulo,anio,estado_juego,vinculo_preliminar,fuente,url,nota,estado_triage,eje_sugerido,ejes_culturales_sugeridos,notas_triage",
        'Juego CSV,2020,publicado,escenario,fuente,https://example.com,nota,pendiente,historia,historia,"nota ""quoted"""',
      ].join("\n"),
    );
  });

  it("parsea CSV con comillas escapadas", () => {
    const rows = getCandidates();
    expect(rows).toHaveLength(1);
    expect(rows[0].titulo).toBe("Juego CSV");
    expect(rows[0].notas_triage).toBe('nota "quoted"');
  });
});

describe("getStats", () => {
  it("devuelve totales y conteos por eje", () => {
    const stats = getStats();
    expect(stats.total).toBe(games.length);
    expect(stats.descartados).toBeGreaterThan(0);
    expect(stats.candidatos).toBeGreaterThanOrEqual(0);
    expect(stats.vinculos.escenario).toBeGreaterThan(0);
    expect(stats.ejes.length).toBeGreaterThan(0);
  });
});

describe("getFilterOptions", () => {
  it("expone opciones ordenadas del catálogo", () => {
    const options = getFilterOptions();
    expect(options.ejes.length).toBeGreaterThan(0);
    expect(options.plataformas.length).toBeGreaterThan(0);
    expect(options.provincias.length).toBeGreaterThan(0);
    expect(options.regiones.length).toBeGreaterThan(0);
    expect(options.disponibilidades.length).toBeGreaterThan(0);
    expect(options.sensibilidades.length).toBeGreaterThan(0);
    expect(options.tiposObra.length).toBeGreaterThan(0);
    expect(options.formatos.length).toBeGreaterThan(0);
  });
});

describe("regresión culturalSummary en catálogo real", () => {
  it("slender-threads mantiene resumen esperado", () => {
    const slender = gameById.get("slender-threads");
    expect(slender?.culturalSummary).toBe(
      "Geografía. Escenario argentino. Ambientado en Buenos Aires.",
    );
  });

  it("super-menem-bros mantiene resumen esperado", () => {
    const menem = gameById.get("super-menem-bros");
    expect(menem?.culturalSummary).toBe(
      "Relectura argentina: Política y Sátira. Protagonistas y figuras argentinas. Una mirada jugable sobre la región Pampeana.",
    );
  });

  it("pc-futbol-argentina-apertura-95 mantiene resumen esperado", () => {
    const pcFutbol = gameById.get("pc-futbol-argentina-apertura-95");
    expect(pcFutbol?.culturalSummary).toBe("Deporte. Deporte y cultura argentina.");
  });

  it("mapampa evita frases antiguas de lugar", () => {
    const nacional = gameById.get("mapampa");
    expect(nacional?.culturalSummary).not.toMatch(/desde Nacional/i);
    expect(nacional?.culturalSummary).not.toMatch(/Para jugar una Argentina/i);
  });
});
