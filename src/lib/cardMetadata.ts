import type { GameView } from "./games";
import { humanize } from "./filters";

const FORMAT_LABELS: Record<string, string> = {
  juego_base: "Juego",
  mod: "Mod",
  mapa: "Mapa",
  campania: "Campaña",
  dlc: "DLC",
  expansion: "Expansión",
  contenido_licenciado: "Contenido licenciado",
  demo: "Demo",
  prototipo: "Prototipo",
  coleccion: "Colección",
};

const TYPE_LABELS_FOR_BASE_GAME: Record<string, string> = {
  comercial: "Juego comercial",
  indie: "Indie",
  educativo: "Educativo",
  jam: "Game jam",
  fan_game: "Fan game",
  promocional: "Promocional",
  institucional: "Institucional",
};

const THEME_ALIASES: Record<string, string> = {
  malvinas: "guerra_de_malvinas",
  historia: "historia",
};

const GENERIC_THEME_SLUGS = new Set(["educacion"]);

export function formatLabel(game: Pick<GameView, "formato" | "tipo_obra">) {
  if (game.formato && game.formato !== "juego_base") {
    return FORMAT_LABELS[game.formato] || humanize(game.formato);
  }
  return TYPE_LABELS_FOR_BASE_GAME[game.tipo_obra] || FORMAT_LABELS.juego_base;
}

export function primaryThemeLabels(
  game: Pick<GameView, "ejes_culturales" | "contexto_argentino">,
  limit = 2,
) {
  const seen = new Set<string>();
  const labels: string[] = [];
  const candidates = [
    ...game.ejes_culturales,
    ...game.contexto_argentino.temas,
  ];

  for (const raw of candidates) {
    const slug = THEME_ALIASES[raw] || raw;
    if (!slug || seen.has(slug) || GENERIC_THEME_SLUGS.has(slug)) continue;
    seen.add(slug);
    labels.push(humanize(slug));
    if (labels.length >= limit) break;
  }

  return labels;
}

export function placeLabel(game: Pick<GameView, "contexto_argentino">) {
  const { provincias, regiones } = game.contexto_argentino;
  if (provincias.includes("Ciudad Autónoma de Buenos Aires") && provincias.includes("Buenos Aires")) {
    return "Buenos Aires";
  }
  if (provincias[0]) return provincias[0];
  const region = regiones.find((item) => item && item !== "Nacional");
  if (region) return region;
  return regiones.includes("Nacional") ? "Argentina" : "";
}

export function argentineLinkLabel(game: Pick<GameView, "vinculo_argentina">) {
  const { escenario, protagonista, deporte_argentino } = game.vinculo_argentina;
  if (deporte_argentino.activo) {
    return deporte_argentino.subtipo === "liga_futbol"
      ? "Fútbol argentino"
      : "Deporte argentino";
  }
  if (protagonista.activo) return "Protagonista argentino";
  if (escenario.activo && escenario.presencia === "referencia_menor") {
    return "Referencia argentina";
  }
  if (escenario.activo) return "Ambientado en Argentina";
  return "";
}

export function accessLabel(
  game: Pick<GameView, "enlaces" | "disponibilidad" | "estado" | "isPlayableToday">,
) {
  if (game.enlaces.steam_workshop) return "Steam Workshop";
  if (game.enlaces.uptodown) return "Descarga";
  if (game.disponibilidad === "gratis") return "Gratis";
  if (game.disponibilidad === "a_la_venta") {
    return game.estado === "en_desarrollo" ? "Wishlist / próxima salida" : "A la venta";
  }
  if (game.disponibilidad === "abandonware") return "Preservación";
  if (!game.isPlayableToday || game.disponibilidad === "perdido") return "Sin link actual";
  return humanize(game.disponibilidad);
}

export function sensitivityCardLabel(game: Pick<GameView, "sensibilidad">) {
  if (game.sensibilidad === "alta") return "Contenido sensible";
  if (game.sensibilidad === "media") return "Contenido sensible";
  return "";
}

export function cardChipLabels(game: GameView) {
  return [
    formatLabel(game),
    ...primaryThemeLabels(game, 2),
  ].filter(Boolean).slice(0, 3);
}

export function cardMetaParts(game: GameView) {
  return [
    placeLabel(game),
    argentineLinkLabel(game),
    accessLabel(game),
  ].filter(Boolean);
}
