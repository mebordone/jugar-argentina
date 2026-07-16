export const TIPO_OBRA_LABELS: Record<string, string> = {
  comercial: "Juego comercial",
  indie: "Indie",
  educativo: "Educativo",
  jam: "Game jam",
  mod: "Mod",
  fan_game: "Fan game",
  abandonware: "Abandonware",
  prototipo: "Prototipo",
  promocional: "Promocional",
};

export const FORMATO_LABELS: Record<string, string> = {
  juego_base: "Juego base",
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

export const QUICK_FILTERS = [
  { label: "Jugable hoy", query: "jugable", href: "/catalogo?jugable=si" },
  { label: "Independencia", query: "independencia", href: "/catalogo?tema=independencia" },
  { label: "Malvinas", query: "malvinas", href: "/catalogo?tema=malvinas" },
  { label: "Folclore", query: "folclore", href: "/catalogo?eje=folclore" },
  { label: "Política", query: "politica", href: "/catalogo?eje=politica" },
  { label: "Mods", query: "mod", href: "/catalogo?tipo_obra=mod" },
  { label: "Buenos Aires", query: "buenos aires", href: "/catalogo?provincia=Buenos%20Aires" },
  { label: "Educación", query: "educativo", href: "/catalogo?eje=educativo" },
];

export const LABELS: Record<string, string> = {
  politica: "Política",
  satira: "Sátira",
  folclore: "Folclore",
  terror: "Terror",
  terror_rural: "Terror rural",
  juegos_tradicionales: "Juegos tradicionales",
  historia: "Historia",
  memoria: "Memoria",
  cultura_urbana: "Cultura urbana",
  historieta: "Historieta",
  literatura: "Literatura",
  educativo: "Educativo",
  deporte: "Deporte",
  geografia: "Geografía",
  migracion: "Migración",
  musica: "Música",
  guerra_de_malvinas: "Guerra de Malvinas",
  malvinas: "Guerra de Malvinas",
  cultura_popular: "Cultura popular",
  medio_ambiente: "Medio ambiente",
  gauchesco: "Gauchesco",
  supervivencia: "Supervivencia",
  humor: "Humor",
  independencia: "Independencia",
  proceres: "Próceres",
  san_martin: "San Martín",
  bandera: "Bandera",
  dictadura: "Dictadura",
  derechos_humanos: "Derechos humanos",
  identidad: "Identidad",
  censura: "Censura",
  desaparecidos: "Desaparecidos",
  centros_clandestinos: "Centros clandestinos",
  esma: "ESMA",
  abuelas_de_plaza_de_mayo: "Abuelas de Plaza de Mayo",
  nietos_recuperados: "Nietos recuperados",
  violencia_politica: "Violencia política",
  bombardeo_1955: "Bombardeo de 1955",
  mar_del_plata: "Mar del Plata",
  mujeres_de_la_independencia: "Mujeres de la Independencia",
  invasiones_inglesas: "Invasiones Inglesas",
  revolucion_de_mayo: "Revolución de Mayo",
  semana_de_mayo: "Semana de Mayo",
  juana_azurduy: "Juana Azurduy",
  martina_chapanay: "Martina Chapanay",
  catalina_echeverria: "Catalina Echeverría",
  pueblos_originarios: "Pueblos originarios",
  conquista: "Conquista",
  colonialismo: "Colonialismo",
  resistencias_indigenas: "Resistencias indígenas",
  memorias_vivas: "Memorias vivas",
  territorios_indigenas: "Territorios indígenas",
  patagonia: "Patagonia",
  soberania: "Soberanía",
  frontera: "Frontera",
  tradicion_rural: "Tradición rural",
  buenos_aires: "Buenos Aires",
  argentina_internacional: "Argentina internacional",
  mundial_2022: "Mundial 2022",
  seleccion_argentina: "Selección argentina",
  central: "Central",
  importante: "Importante",
  menor: "Referencia menor",
  a_la_venta: "A la venta",
  gratis: "Gratis",
  abandonware: "Abandonware",
  perdido: "Perdido",
  desconocido: "Sin dato",
  publicado: "Publicado",
  en_desarrollo: "En desarrollo",
  early_access: "Early access",
  prototipo: "Prototipo",
  cancelado: "Cancelado",
  ...FORMATO_LABELS,
  ...TIPO_OBRA_LABELS,
};

export function humanize(value?: string | null) {
  if (!value) return "";
  return LABELS[value] || value.replaceAll("_", " ");
}

export function normalizeText(value: string) {
  return value
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "")
    .toLowerCase();
}

export function tipoObraTone(tipoObra?: string) {
  if (tipoObra === "mod" || tipoObra === "fan_game") return "alert";
  if (tipoObra === "abandonware" || tipoObra === "prototipo") return "warm";
  return "cool";
}

export function placeholderClass(ejes: string[]) {
  const eje = ejes[0] || "historia";
  return `cover-placeholder cover-${eje}`;
}
