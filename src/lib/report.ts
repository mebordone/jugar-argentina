import { SITE } from "../site.config";
import { absoluteUrl } from "./links";
import type { GameView } from "./games";

export function reportGameUrl(game: Pick<GameView, "id" | "titulo">) {
  const ficha = absoluteUrl(`/juegos/${game.id}`);
  const params = new URLSearchParams({
    template: "sugerir-correccion.yml",
    title: `[Corrección] ${game.titulo}`,
    "juego-id": game.id,
    titulo: game.titulo,
    ficha,
  });
  return `https://github.com/${SITE.githubRepo}/issues/new?${params.toString()}`;
}
