import type { Game } from "./games";
import { humanize } from "./filters";

const LAUNCH_STATES = new Set(["en_desarrollo", "early_access", "prototipo"]);

export function gameReleasePrimary(game: Game): string {
  if (game.anio) return String(game.anio);
  if (game.anio_nota) return game.anio_nota;
  if (LAUNCH_STATES.has(game.estado)) return humanize(game.estado);
  return "Sin fecha";
}

export function gameReleaseEyebrow(game: Game): string {
  const primary = gameReleasePrimary(game);
  const estadoLabel = humanize(game.estado);

  if (game.anio) return `${primary} · ${estadoLabel}`;
  if (game.anio_nota) return `${primary} · ${estadoLabel}`;
  if (primary !== "Sin fecha" && primary !== estadoLabel) {
    return `${primary} · ${estadoLabel}`;
  }
  if (primary !== "Sin fecha") return primary;
  return estadoLabel || "Sin fecha";
}
