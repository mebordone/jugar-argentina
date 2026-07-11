import { createRef } from "react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import {
  countActiveFilters,
  FILTERS_OPEN_KEY,
  formatFilterValue,
  isSearchInputFocused,
  isSearchOnlyChange,
  joinBase,
  readFiltersOpenPreference,
  scrollToResults,
  scrollToResultsAndFocus,
} from "./catalogUi";
import { EMPTY_CATALOG_FILTERS } from "./filterGames";

describe("catalogUi helpers", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("cuenta filtros activos", () => {
    expect(countActiveFilters(EMPTY_CATALOG_FILTERS)).toBe(0);
    expect(
      countActiveFilters({ ...EMPTY_CATALOG_FILTERS, q: "tango", eje: "folclore" }),
    ).toBe(2);
  });

  it("formatea valores de filtro", () => {
    expect(formatFilterValue("jugable", "si")).toBe("Sí");
    expect(formatFilterValue("eje", "folclore")).toBe("Folclore");
  });

  it("detecta cambios solo de búsqueda", () => {
    expect(
      isSearchOnlyChange(
        { ...EMPTY_CATALOG_FILTERS, q: "ta" },
        { ...EMPTY_CATALOG_FILTERS, q: "tango" },
      ),
    ).toBe(true);
    expect(
      isSearchOnlyChange(
        EMPTY_CATALOG_FILTERS,
        { ...EMPTY_CATALOG_FILTERS, eje: "folclore" },
      ),
    ).toBe(false);
  });

  it("une basePath con rutas", () => {
    expect(joinBase("/", "/catalogo")).toBe("/catalogo");
    expect(joinBase("/jugar-argentina/", "/catalogo")).toBe("/jugar-argentina/catalogo");
    expect(joinBase("/jugar-argentina", "/catalogo")).toBe("/jugar-argentina/catalogo");
  });

  it("lee preferencia explícita true", () => {
    localStorage.setItem(FILTERS_OPEN_KEY, "true");
    expect(readFiltersOpenPreference()).toBe(true);
  });

  it("cae a true cuando no hay window", async () => {
    const originalWindow = globalThis.window;
    // @ts-expect-error simula entorno SSR
    delete globalThis.window;
    const { readFiltersOpenPreference: readPreference } = await import("./catalogUi");
    expect(readPreference()).toBe(true);
    globalThis.window = originalWindow;
  });

  it("lee preferencia de filtros abiertos", () => {
    expect(readFiltersOpenPreference()).toBe(true);
    localStorage.setItem(FILTERS_OPEN_KEY, "false");
    expect(readFiltersOpenPreference()).toBe(false);
  });
});

describe("scroll helpers", () => {
  it("detecta foco en input de búsqueda", () => {
    document.body.innerHTML = `
      <label class="toolbar-search">
        <input aria-label="Buscar juegos en el catálogo" />
      </label>
    `;
    const input = document.querySelector("input") as HTMLInputElement;
    input.focus();
    expect(isSearchInputFocused()).toBe(true);
  });

  it("no hace scroll ni focus si la búsqueda está activa", () => {
    document.body.innerHTML = `
      <div id="catalog-results" tabindex="-1"></div>
      <label class="toolbar-search"><input /></label>
    `;
    const input = document.querySelector("input") as HTMLInputElement;
    input.focus();
    const focusSpy = vi.spyOn(HTMLElement.prototype, "focus");
    const scrollSpy = vi.spyOn(window, "scrollTo").mockImplementation(() => {});
    const ref = createRef<HTMLDivElement>();
    ref.current = document.getElementById("catalog-results") as HTMLDivElement;

    scrollToResultsAndFocus(ref);

    expect(scrollSpy).not.toHaveBeenCalled();
    expect(focusSpy).not.toHaveBeenCalled();
  });

  it("hace scroll cuando no hay foco en búsqueda", () => {
    document.body.innerHTML = `<div id="catalog-results" tabindex="-1"></div>`;
    const scrollSpy = vi.spyOn(window, "scrollTo").mockImplementation(() => {});
    vi.mocked(window.matchMedia).mockReturnValueOnce({
      matches: true,
      media: "",
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    } as MediaQueryList);
    const element = document.getElementById("catalog-results")!;
    vi.spyOn(element, "getBoundingClientRect").mockReturnValue({
      top: 100,
      bottom: 0,
      left: 0,
      right: 0,
      width: 0,
      height: 0,
      x: 0,
      y: 0,
      toJSON: () => ({}),
    });

    scrollToResults();

    expect(scrollSpy).toHaveBeenCalled();
  });

  it("no hace scroll si falta el contenedor de resultados", () => {
    vi.spyOn(document, "getElementById").mockReturnValue(null);
    const scrollSpy = vi.spyOn(window, "scrollTo").mockImplementation(() => {});
    scrollToResults();
    expect(scrollSpy).not.toHaveBeenCalled();
  });

  it("enfoca resultados cuando la búsqueda no está activa", () => {
    document.body.innerHTML = `<div id="catalog-results" tabindex="-1"></div>`;
    vi.spyOn(window, "scrollTo").mockImplementation(() => {});
    const ref = createRef<HTMLDivElement>();
    ref.current = document.getElementById("catalog-results") as HTMLDivElement;
    const focusSpy = vi.spyOn(HTMLElement.prototype, "focus");

    scrollToResultsAndFocus(ref);

    expect(focusSpy).toHaveBeenCalled();
  });

  it("usa scroll suave cuando no hay preferencia de movimiento reducido", () => {
    document.body.innerHTML = `<div id="catalog-results" tabindex="-1"></div>`;
    vi.mocked(window.matchMedia).mockReturnValueOnce({
      matches: false,
      media: "",
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    } as MediaQueryList);
    const element = document.getElementById("catalog-results")!;
    vi.spyOn(element, "getBoundingClientRect").mockReturnValue({
      top: 50,
      bottom: 0,
      left: 0,
      right: 0,
      width: 0,
      height: 0,
      x: 0,
      y: 0,
      toJSON: () => ({}),
    });
    const scrollSpy = vi.spyOn(window, "scrollTo").mockImplementation(() => {});

    scrollToResults();

    expect(scrollSpy).toHaveBeenCalledWith(
      expect.objectContaining({ behavior: "smooth" }),
    );
  });
});
