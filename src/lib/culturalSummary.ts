import { humanize } from "./filters";
import type { Game } from "./games";

const MACRO_REGIONS = new Set([
  "Pampeana",
  "Patagonia",
  "Noroeste",
  "Noreste",
  "Litoral",
  "Cuyo",
  "Nacional",
]);

const REGION_LABELS: Record<string, string> = {
  Pampeana: "Pampeana",
  Patagonia: "Patagonia",
  Noroeste: "Noroeste",
  Noreste: "Noreste",
  Litoral: "Litoral",
  Cuyo: "Cuyo",
  Nacional: "Nacional",
};

const THEME_ALIASES: Record<string, string> = {
  malvinas: "guerra_de_malvinas",
};

function normalizeThemeSlug(slug: string) {
  return THEME_ALIASES[slug] || slug;
}

function uniqueThemeSlugs(game: Game) {
  const seen = new Set<string>();
  const slugs: string[] = [];

  for (const raw of [
    ...game.ejes_culturales,
    ...game.contexto_argentino.temas.slice(0, 2),
  ]) {
    const slug = normalizeThemeSlug(raw);
    if (!slug || seen.has(slug)) continue;
    seen.add(slug);
    slugs.push(slug);
    if (slugs.length >= 2) break;
  }

  return slugs;
}

function buildVinculoSuffix(game: Game): string {
  const { escenario, protagonista, deporte_argentino } = game.vinculo_argentina;

  if (protagonista.activo) {
    return "Protagonistas y figuras argentinas.";
  }
  if (deporte_argentino.activo) {
    return "Deporte y cultura argentina.";
  }
  if (escenario.activo && escenario.presencia === "principal") {
    return "Escenario argentino.";
  }
  if (escenario.activo) {
    return "Referencia a Argentina.";
  }
  return "";
}

function buildThemeSentence(game: Game, labels: string[]) {
  if (!labels.length) return "";

  if (labels.length >= 2) {
    const prefix = `${labels.slice(0, 2).join(" y ")}.`;
    const suffix = buildVinculoSuffix(game);
    return suffix ? `${prefix} ${suffix}` : prefix;
  }

  const tema = labels[0];

  if (game.tipo_obra === "educativo") {
    return `Experiencia educativa sobre ${tema.charAt(0).toLowerCase()}${tema.slice(1)}.`;
  }

  const suffix = buildVinculoSuffix(game);
  return suffix ? `${tema}. ${suffix}` : `${tema}.`;
}

function buildPlacePhrase(game: Game) {
  const provincia = game.contexto_argentino.provincias[0];
  const region = game.contexto_argentino.regiones[0];

  if (provincia) {
    return `Ambientado en ${provincia}.`;
  }
  if (!region || region === "Nacional") {
    return "";
  }
  if (MACRO_REGIONS.has(region)) {
    const label = REGION_LABELS[region] || region;
    return `Una mirada jugable sobre la región ${label}.`;
  }
  return "";
}

function truncateDescription(text: string, max = 140) {
  const trimmed = text.trim();
  if (trimmed.length <= max) return trimmed;

  const cut = trimmed.slice(0, max);
  const lastPeriod = cut.lastIndexOf(".");
  const lastSpace = cut.lastIndexOf(" ");
  const breakAt = lastPeriod > 80 ? lastPeriod + 1 : lastSpace;

  if (breakAt > 0) {
    return `${cut.slice(0, breakAt).trim()}...`;
  }
  return `${cut.trim()}...`;
}

function hasVinculoEnrichment(themeSentence: string) {
  return (
    themeSentence.includes("Escenario argentino") ||
    themeSentence.includes("Referencia a Argentina") ||
    themeSentence.includes("Protagonistas y figuras argentinas") ||
    themeSentence.includes("Deporte y cultura argentina") ||
    themeSentence.startsWith("Experiencia educativa sobre") ||
    themeSentence.startsWith("Relectura argentina:")
  );
}

function isTooGeneric(summary: string, themeSentence: string, _placePhrase: string) {
  if (!summary.trim()) return true;
  if (hasVinculoEnrichment(themeSentence)) return false;
  if (summary.length < 40) return true;
  return false;
}

export function buildCulturalSummary(game: Game) {
  const slugs = uniqueThemeSlugs(game);
  const labels = slugs.map((slug) => humanize(slug)).filter(Boolean);

  let themeSentence = buildThemeSentence(game, labels);

  if (
    (game.tipo_obra === "mod" || game.tipo_obra === "fan_game") &&
    themeSentence &&
    !themeSentence.startsWith("Relectura argentina:")
  ) {
    themeSentence = `Relectura argentina: ${themeSentence.replace(/\.$/, "")}.`;
  }

  const placePhrase = buildPlacePhrase(game);
  const summary = [themeSentence, placePhrase].filter(Boolean).join(" ");

  if (isTooGeneric(summary, themeSentence, placePhrase) && game.descripcion.trim()) {
    return truncateDescription(game.descripcion);
  }

  if (!summary.trim()) {
    return "Recorrido por imaginarios argentinos.";
  }

  return summary;
}
