import type { RefObject } from "react";
import type { CatalogFilters } from "./filterGames";
import { humanize } from "./filters";

export const FILTERS_OPEN_KEY = "catalog-filters-open";

export const FILTER_LABELS: Partial<Record<keyof CatalogFilters, string>> = {
  q: "Búsqueda",
  eje: "Eje cultural",
  tipo_obra: "Tipo de obra",
  formato: "Formato",
  jugable: "Jugable hoy",
  vinculo: "Vínculo",
  plataforma: "Plataforma",
  provincia: "Provincia/región",
  disponibilidad: "Disponibilidad",
  sensibilidad: "Sensibilidad",
  tema: "Tema",
};

export const FILTER_VALUE_LABELS: Partial<
  Record<keyof CatalogFilters, Record<string, string>>
> = {
  jugable: { si: "Sí", no: "Sin link de juego" },
};

export function readFiltersOpenPreference(): boolean {
  if (typeof window === "undefined") return true;
  const stored = window.localStorage.getItem(FILTERS_OPEN_KEY);
  if (stored === "false") return false;
  if (stored === "true") return true;
  return true;
}

export function scrollToResults() {
  const el = document.getElementById("catalog-results");
  if (!el) return;
  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const top = el.getBoundingClientRect().top + window.scrollY - 16;
  window.scrollTo({ top, behavior: prefersReduced ? "auto" : "smooth" });
}

export function isSearchInputFocused() {
  const active = document.activeElement;
  return (
    active instanceof HTMLInputElement &&
    active.closest(".toolbar-search") !== null
  );
}

export function scrollToResultsAndFocus(resultsRef: RefObject<HTMLDivElement | null>) {
  if (isSearchInputFocused()) {
    return;
  }
  scrollToResults();
  resultsRef.current?.focus({ preventScroll: true });
}

export function countActiveFilters(filters: CatalogFilters): number {
  return Object.values(filters).filter(Boolean).length;
}

export function formatFilterValue(key: keyof CatalogFilters, value: string): string {
  return FILTER_VALUE_LABELS[key]?.[value] || humanize(value);
}

export function isSearchOnlyChange(previous: CatalogFilters, next: CatalogFilters) {
  return (
    previous.q !== next.q &&
    (Object.keys(previous) as Array<keyof CatalogFilters>).every(
      (key) => key === "q" || previous[key] === next[key],
    )
  );
}

export function joinBase(basePath: string, path: string) {
  const cleanBase = basePath.endsWith("/") ? basePath.slice(0, -1) : basePath;
  return `${cleanBase}${path}`;
}
