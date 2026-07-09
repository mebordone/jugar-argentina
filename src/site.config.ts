const githubUser = import.meta.env.PUBLIC_GITHUB_USER || "mebordone";
const githubRepo = import.meta.env.PUBLIC_GITHUB_REPO || "jugar-argentina";
const siteOrigin =
  import.meta.env.PUBLIC_SITE_URL?.replace(/\/$/, "") ||
  import.meta.env.SITE?.replace(/\/$/, "") ||
  "https://mebordone.github.io";
const basePath = import.meta.env.BASE_URL || "/jugar-argentina/";

export const SITE = {
  name: "Jugar Argentina",
  tagline: "Videojuegos para recorrer Argentina jugando",
  description:
    "Un catálogo para descubrir, jugar y compartir videojuegos vinculados a la cultura argentina.",
  siteUrl: `${siteOrigin}${basePath === "/" ? "" : basePath.replace(/\/$/, "")}`,
  githubUser,
  githubRepo: `${githubUser}/${githubRepo}`,
  githubIssuesUrl: `https://github.com/${githubUser}/${githubRepo}/issues/new?template=sugerir-juego.yml`,
};
