import type { Game } from "./games";
import { humanize } from "./filters";

export type ComoJugarStep = {
  title: string;
  detail: string;
};

export function buildComoJugarSteps(game: Game): ComoJugarStep[] {
  const steps: ComoJugarStep[] = [];

  if (game.tipo_obra === "mod") {
    steps.push({
      title: "Revisá el juego base",
      detail:
        "Este registro es un mod o contenido de Workshop. Necesitás tener instalado el juego original antes de sumarlo.",
    });
  }

  if (game.disponibilidad === "a_la_venta") {
    steps.push({
      title: "Comprá o agregalo a tu biblioteca",
      detail: "Usá el enlace de tienda para obtener la versión actual del juego.",
    });
  } else if (game.disponibilidad === "gratis") {
    steps.push({
      title: "Descargalo o jugalo en la web",
      detail: "El juego se puede acceder sin compra desde los enlaces de juego o itch.io.",
    });
  } else if (game.disponibilidad === "abandonware") {
    steps.push({
      title: "Buscá una copia preservada",
      detail:
        "El título ya no se vende oficialmente. Revisá archive.org u otras fuentes de preservación y verificá compatibilidad.",
    });
  } else if (game.disponibilidad === "perdido") {
    steps.push({
      title: "Consultá fuentes de preservación",
      detail: "No hay tienda activa. Las fuentes pueden ayudar a reconstruir cómo se jugaba.",
    });
  } else {
    steps.push({
      title: "Revisá los enlaces disponibles",
      detail: "La disponibilidad exacta puede variar. Empezá por los enlaces de juego o tienda.",
    });
  }

  if (game.enlaces.steam_workshop) {
    steps.push({
      title: "Suscribite en Workshop",
      detail: "Abrí el mod en Steam Workshop y suscribite para que aparezca en el juego base.",
    });
  }

  if (game.estado === "en_desarrollo" || game.estado === "early_access") {
    steps.push({
      title: "Tené en cuenta el estado del proyecto",
      detail: `Hoy figura como ${humanize(game.estado)}. Puede haber demos, capítulos parciales o cambios futuros.`,
    });
  }

  if (game.sensibilidad === "media" || game.sensibilidad === "alta") {
    steps.push({
      title: "Contenido sensible",
      detail:
        "Este juego aborda temas con sensibilidad media o alta. Revisá la ficha antes de compartirlo en contextos educativos.",
    });
  }

  return steps;
}

export function sensibilidadNotice(sensibilidad: string) {
  if (sensibilidad === "alta") {
    return "Contenido con alta sensibilidad histórica o política.";
  }
  if (sensibilidad === "media") {
    return "Puede incluir violencia, dictadura u otros temas sensibles.";
  }
  return null;
}
