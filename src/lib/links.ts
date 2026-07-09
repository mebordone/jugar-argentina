export type LinkActionType =
  | "play"
  | "download"
  | "buy"
  | "archive"
  | "mod"
  | "source";

export type LinkAction = {
  type: LinkActionType;
  label: string;
  url: string;
  source: string;
};

const PLAY_KEYS = ["itch", "web_oficial", "kongregate"];
const STORE_KEYS = ["steam", "nintendo", "playstation", "xbox"];
const PRESS_HOSTS = new Set([
  "infobae.com",
  "pressover.news",
  "tn.com.ar",
  "elplanteo.com",
  "extragamers.com.ar",
  "devuego.lat",
  "lagaceta.com.ar",
  "fmfuego.com.ar",
  "nogamingnews.com",
  "videojuegosargentinos.com.ar",
  "wired.com",
  "theguardian.com",
  "polygon.com",
  "kotaku.com",
  "ign.com",
  "gamespot.com",
  "gitgud.com.ar",
  "nicolasbroner.wordpress.com",
  "agencia.unq.edu.ar",
  "airedesantafe.com.ar",
  "icom.museum",
]);

export function sitePath(path: string) {
  const base = import.meta.env.BASE_URL || "/";
  const cleanBase = base.endsWith("/") ? base.slice(0, -1) : base;
  const cleanPath = path.startsWith("/") ? path : `/${path}`;
  return `${cleanBase}${cleanPath}` || "/";
}

export function absoluteUrl(path = "/") {
  const site = (import.meta.env.SITE || import.meta.env.PUBLIC_SITE_URL || "")
    .replace(/\/$/, "");
  const base = import.meta.env.BASE_URL || "/";
  const cleanBase = base.endsWith("/") ? base.slice(0, -1) : base;
  const cleanPath = path.startsWith("/") ? path : `/${path}`;
  const alreadyBased =
    cleanBase !== "/" &&
    (cleanPath === cleanBase || cleanPath.startsWith(`${cleanBase}/`));
  const joined = alreadyBased
    ? cleanPath
    : `${cleanBase}${cleanPath}`.replace(/\/{2,}/g, "/");
  if (!site) return joined || "/";
  return `${site}${joined.startsWith("/") ? joined : `/${joined}`}`;
}

export function labelFromKey(key: string) {
  const labels: Record<string, string> = {
    steam: "Steam",
    steam_workshop: "Steam Workshop",
    itch: "itch.io",
    web_oficial: "Sitio oficial",
    fuentes_investigacion: "Fuente",
    wikipedia: "Wikipedia",
    archive: "Preservación",
    kongregate: "Kongregate",
  };
  return labels[key] || key.replaceAll("_", " ");
}

export function hasPlayableLink(enlaces: Record<string, unknown>) {
  const keys = [...PLAY_KEYS, ...STORE_KEYS, "steam_workshop", "archive"];
  return keys.some((key) => {
    const value = enlaces[key];
    return typeof value === "string" && value.length > 0;
  });
}

export function collectActions(
  enlaces: Record<string, unknown>,
  disponibilidad?: string,
) {
  const actions: LinkAction[] = [];

  for (const key of PLAY_KEYS) {
    const url = enlaces[key];
    if (typeof url === "string" && url) {
      actions.push({
        type: "play",
        label: "Jugar ahora",
        url,
        source: labelFromKey(key),
      });
    }
  }

  for (const key of STORE_KEYS) {
    const url = enlaces[key];
    if (typeof url === "string" && url) {
      actions.push({
        type: "buy",
        label: key === "steam" ? "Comprar en Steam" : "Ver en tienda",
        url,
        source: labelFromKey(key),
      });
    }
  }

  const workshopUrl = enlaces.steam_workshop;
  if (typeof workshopUrl === "string" && workshopUrl) {
    actions.push({
      type: "mod",
      label: "Ver mod en Workshop",
      url: workshopUrl,
      source: labelFromKey("steam_workshop"),
    });
  }

  const archiveUrl = enlaces.archive;
  if (typeof archiveUrl === "string" && archiveUrl) {
    actions.push({
      type: "archive",
      label: "Ver archivo",
      url: archiveUrl,
      source: labelFromKey("archive"),
    });
  }

  if (disponibilidad === "abandonware") {
    const archive = enlaces.archive;
    if (typeof archive === "string" && archive) {
      actions.push({
        type: "download",
        label: "Buscar descarga",
        url: archive,
        source: "Preservación",
      });
    }
  }

  const fuentes = enlaces.fuentes_investigacion;
  if (Array.isArray(fuentes)) {
    for (const url of fuentes) {
      if (typeof url === "string" && url && !isDuplicateSource(url, actions)) {
        actions.push({
          type: "source",
          label: "Ver fuente",
          url,
          source: sourceFromUrl(url),
        });
      }
    }
  }

  return dedupeActions(actions);
}

export function splitActions(actions: LinkAction[]) {
  const playable = actions.filter((action) => action.type !== "source");
  const sources = actions.filter((action) => action.type === "source");
  return { playable, sources };
}

export function primaryAction(actions: LinkAction[]) {
  const order: LinkActionType[] = [
    "play",
    "mod",
    "buy",
    "download",
    "archive",
    "source",
  ];
  const playable = actions.filter((action) => action.type !== "source");
  const pool = playable.length ? playable : actions;
  return [...pool].sort(
    (a, b) => order.indexOf(a.type) - order.indexOf(b.type),
  )[0];
}

function isDuplicateSource(url: string, actions: LinkAction[]) {
  return actions.some((action) => action.url === url);
}

function sourceFromUrl(url: string) {
  try {
    const hostname = new URL(url).hostname.replace(/^www\./, "");
    if (PRESS_HOSTS.has(hostname)) return "Prensa";
    if (hostname.includes("wikipedia")) return "Wikipedia";
    if (hostname.includes("mobygames")) return "MobyGames";
    if (hostname.includes("fandom.com")) return "Wiki";
    return hostname;
  } catch {
    return "Fuente";
  }
}

function dedupeActions(actions: LinkAction[]) {
  const seen = new Set<string>();
  return actions.filter((action) => {
    if (seen.has(action.url)) return false;
    seen.add(action.url);
    return true;
  });
}
