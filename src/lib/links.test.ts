import { beforeEach, describe, expect, it, vi } from "vitest";
import {
  absoluteUrl,
  collectActions,
  hasPlayableLink,
  labelFromKey,
  primaryAction,
  sitePath,
  splitActions,
} from "./links";

describe("sitePath", () => {
  beforeEach(() => {
    Object.assign(import.meta.env, { BASE_URL: "/" });
  });

  it("une base y path", () => {
    expect(sitePath("/catalogo")).toBe("/catalogo");
    expect(sitePath("catalogo")).toBe("/catalogo");
  });

  it("respeta base con subpath", () => {
    Object.assign(import.meta.env, { BASE_URL: "/jugar-argentina/" });
    expect(sitePath("/catalogo")).toBe("/jugar-argentina/catalogo");
  });

  it("normaliza base sin slash final", () => {
    Object.assign(import.meta.env, { BASE_URL: "/jugar-argentina" });
    expect(sitePath("/catalogo")).toBe("/jugar-argentina/catalogo");
  });
});

describe("absoluteUrl", () => {
  beforeEach(() => {
    Object.assign(import.meta.env, {
      BASE_URL: "/jugar-argentina/",
      SITE: "https://example.com",
      PUBLIC_SITE_URL: "https://example.com",
    });
  });

  it("genera URL absoluta con site", () => {
    expect(absoluteUrl("/catalogo")).toBe("https://example.com/jugar-argentina/catalogo");
    expect(absoluteUrl("catalogo")).toBe("https://example.com/jugar-argentina/catalogo");
  });

  it("devuelve path relativo si no hay site", () => {
    Object.assign(import.meta.env, { SITE: "", PUBLIC_SITE_URL: "" });
    expect(absoluteUrl("/catalogo")).toBe("/jugar-argentina/catalogo");
  });

  it("normaliza path sin slash inicial y base vacía", () => {
    Object.assign(import.meta.env, { BASE_URL: "", SITE: "", PUBLIC_SITE_URL: "" });
    expect(absoluteUrl("catalogo")).toBe("/catalogo");
    expect(sitePath("catalogo")).toBe("/catalogo");
  });

  it("no duplica base si el path ya la incluye", () => {
    expect(absoluteUrl("/jugar-argentina/catalogo")).toBe(
      "https://example.com/jugar-argentina/catalogo",
    );
  });
});

describe("labelFromKey", () => {
  it("traduce claves conocidas", () => {
    expect(labelFromKey("steam")).toBe("Steam");
    expect(labelFromKey("itch")).toBe("itch.io");
  });

  it("humaniza claves desconocidas", () => {
    expect(labelFromKey("web_oficial")).toBe("Sitio oficial");
    expect(labelFromKey("foo_bar")).toBe("foo bar");
  });
});

describe("hasPlayableLink", () => {
  it("detecta enlaces jugables", () => {
    expect(hasPlayableLink({ itch: "https://itch.io/game" })).toBe(true);
    expect(hasPlayableLink({ steam: "https://store.steampowered.com/app/1" })).toBe(true);
    expect(hasPlayableLink({})).toBe(false);
  });

  it("ignora claves vacías o inválidas", () => {
    expect(hasPlayableLink({ itch: "" })).toBe(false);
    expect(hasPlayableLink({ itch: 0 })).toBe(false);
  });
});

describe("collectActions", () => {
  it("prioriza play, buy, mod, archive y download", () => {
    const actions = collectActions({
      itch: "https://itch.io/a",
      steam: "https://store.steampowered.com/a",
      steam_workshop: "https://steamcommunity.com/sharedfiles/a",
      archive: "https://archive.org/a",
      apkpure: "https://apkpure.com/a",
    });
    expect(actions.map((a) => a.type)).toEqual([
      "play",
      "buy",
      "mod",
      "archive",
      "download",
    ]);
  });

  it("prioriza búsqueda de descarga para abandonware con archive", () => {
    const actions = collectActions(
      { archive: "https://archive.org/item" },
      "abandonware",
    );
    expect(actions).toHaveLength(1);
    expect(actions[0]).toMatchObject({
      type: "download",
      label: "Buscar descarga",
      url: "https://archive.org/item",
    });
  });

  it("usa etiquetas de tienda y descarga según plataforma", () => {
    const actions = collectActions({
      nintendo: "https://nintendo.com/game",
      google_play: "https://play.google.com/store/apps/details?id=1",
      uptodown: "https://example.uptodown.com/windows/descargar",
    });
    expect(actions.find((a) => a.type === "buy")?.label).toBe("Ver en tienda");
    expect(actions.find((a) => a.type === "download")?.label).toBe("Descargar");
    expect(actions.find((a) => a.source === "Uptodown")?.type).toBe("download");
  });

  it("clasifica MobyGames y Fandom como fuentes especializadas", () => {
    const actions = collectActions({
      fuentes_investigacion: [
        "https://www.mobygames.com/game/1",
        "https://fallout.fandom.com/wiki/Test",
      ],
    });
    expect(actions.find((a) => a.url.includes("mobygames"))?.source).toBe("MobyGames");
    expect(actions.find((a) => a.url.includes("fandom"))?.source).toBe("Wiki");
  });

  it("ignora archive inválido en abandonware", () => {
    expect(collectActions({ archive: 123 }, "abandonware")).toEqual([]);
  });

  it("conserva ver archivo cuando no es abandonware", () => {
    const actions = collectActions({ archive: "https://archive.org/item" });
    expect(actions[0]).toMatchObject({
      type: "archive",
      label: "Ver archivo",
    });
  });

  it("incluye fuentes de investigación sin duplicar URLs", () => {
    const url = "https://infobae.com/nota";
    const actions = collectActions({
      fuentes_investigacion: [url, url, "https://es.wikipedia.org/wiki/Juego"],
    });
    const sources = actions.filter((a) => a.type === "source");
    expect(sources).toHaveLength(2);
    expect(sources[0].source).toBe("Prensa");
    expect(sources[1].source).toBe("Wikipedia");
  });

  it("deduplica acciones con la misma URL", () => {
    const url = "https://archive.org/item";
    const actions = collectActions({ archive: url, itch: url });
    expect(actions).toHaveLength(1);
  });

  it("clasifica hostname desconocido como fuente genérica", () => {
    const actions = collectActions({
      fuentes_investigacion: ["not-a-url", "https://example.org/review"],
    });
    expect(actions.find((a) => a.url === "not-a-url")?.source).toBe("Fuente");
    expect(actions.find((a) => a.url === "https://example.org/review")?.source).toBe(
      "example.org",
    );
  });
});

describe("splitActions", () => {
  it("separa acciones jugables de fuentes", () => {
    const actions = collectActions({
      itch: "https://itch.io/a",
      fuentes_investigacion: ["https://infobae.com/a"],
    });
    const { playable, sources } = splitActions(actions);
    expect(playable.every((a) => a.type !== "source")).toBe(true);
    expect(sources.every((a) => a.type === "source")).toBe(true);
  });
});

describe("primaryAction", () => {
  it("elige play sobre buy", () => {
    const actions = collectActions({
      itch: "https://itch.io/a",
      steam: "https://store.steampowered.com/a",
    });
    expect(primaryAction(actions)?.type).toBe("play");
  });

  it("usa buy si no hay play", () => {
    const actions = collectActions({ steam: "https://store.steampowered.com/a" });
    expect(primaryAction(actions)?.type).toBe("buy");
  });

  it("cae a source si no hay acciones jugables", () => {
    const actions = collectActions({
      fuentes_investigacion: ["https://infobae.com/a"],
    });
    expect(primaryAction(actions)?.type).toBe("source");
  });

  it("prioriza mod, descarga y archivo según disponibilidad", () => {
    expect(
      primaryAction(
        collectActions({ steam_workshop: "https://steamcommunity.com/sharedfiles/a" }),
      )?.type,
    ).toBe("mod");
    expect(
      primaryAction(collectActions({ apkpure: "https://apkpure.com/a" }))?.type,
    ).toBe("download");
    expect(
      primaryAction(collectActions({ archive: "https://archive.org/a" }))?.type,
    ).toBe("archive");
  });
});
