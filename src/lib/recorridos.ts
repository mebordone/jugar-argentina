import efemerides from "../content/efemerides.json";
import { gameById, games, type GameView } from "./games";
import { humanize, normalizeText } from "./filters";

export type RecorridoTipo =
  | "fecha_patria"
  | "efemeride"
  | "permanente"
  | "territorial"
  | "recomendado";

export type RecorridoVentana = {
  inicio: string;
  fin: string;
  etiqueta?: string;
};

export type RecorridoDestacado = {
  id: string;
  motivo: string;
};

export type RecorridoRelacionados = {
  temas?: string[];
  ejes?: string[];
  provincias?: string[];
  regiones?: string[];
  formatos?: string[];
  generos?: string[];
  vinculos?: Array<"escenario" | "protagonista" | "deporte">;
  solo_jugables?: boolean;
  excluir_relevancia_menor?: boolean;
  excluir_ids?: string[];
  limite?: number;
};

export type Recorrido = {
  slug: string;
  tipo: RecorridoTipo;
  fecha: string | null;
  ventana?: RecorridoVentana;
  titulo: string;
  bajada: string;
  descripcion: string;
  criterio: string;
  fuente_calendario?: string;
  temas: string[];
  territorios: string[];
  destacados_editoriales: RecorridoDestacado[];
  relacionados?: RecorridoRelacionados;
};

export const recorridos = efemerides as Recorrido[];

const MAX_RECORRIDO_GAMES = 18;

const BROAD_TEMAS = new Set(["historia", "educacion", "educativo", "geografia"]);
const DIAS_POR_MES = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

const RELEVANCIA_ORDER: Record<string, number> = {
  central: 0,
  importante: 1,
  menor: 2,
};

const MESES = [
  "enero",
  "febrero",
  "marzo",
  "abril",
  "mayo",
  "junio",
  "julio",
  "agosto",
  "septiembre",
  "octubre",
  "noviembre",
  "diciembre",
];

export const FECHAS_PATRIAS_PRIORITARIAS = [
  { fecha: "03-24", slug: "memoria-verdad-justicia", titulo: "Memoria por la Verdad y la Justicia" },
  { fecha: "04-02", slug: "malvinas", titulo: "Veteranos y Caídos en Malvinas" },
  { fecha: "05-25", slug: "revolucion-mayo", titulo: "Revolución de Mayo" },
  { fecha: "06-20", slug: "bandera-belgrano", titulo: "Día de la Bandera" },
  { fecha: "07-09", slug: "independencia", titulo: "Día de la Independencia" },
  { fecha: "08-17", slug: "san-martin", titulo: "General José de San Martín" },
  { fecha: "10-12", slug: "diversidad-cultural", titulo: "Respeto a la Diversidad Cultural" },
  { fecha: "11-20", slug: "soberania-nacional", titulo: "Soberanía Nacional" },
];

const TIPO_RECORRIDO_LABELS: Record<RecorridoTipo, string> = {
  fecha_patria: "Fecha patria",
  efemeride: "Efeméride",
  permanente: "Recorrido permanente",
  territorial: "Recorrido territorial",
  recomendado: "Recomendados",
};

function isValidDateCode(fecha: string | null | undefined) {
  if (!fecha) return false;
  const match = /^(\d{2})-(\d{2})$/.exec(fecha);
  if (!match) return false;
  const month = Number(match[1]);
  const day = Number(match[2]);
  return month >= 1 && month <= 12 && day >= 1 && day <= DIAS_POR_MES[month - 1];
}

function dayOfYear(fecha: string) {
  const [month, day] = fecha.split("-").map(Number);
  return DIAS_POR_MES.slice(0, month - 1).reduce((sum, value) => sum + value, 0) + day;
}

function dateCode(date: Date) {
  return `${String(date.getMonth() + 1).padStart(2, "0")}-${String(
    date.getDate(),
  ).padStart(2, "0")}`;
}

export function formatRecorridoFecha(fecha: string | null) {
  if (!fecha || !isValidDateCode(fecha)) return null;
  const [mm, dd] = fecha.split("-");
  const mes = MESES[Number(mm) - 1];
  return `${Number(dd)} de ${mes}`;
}

export function formatRecorridoTipo(tipo: RecorridoTipo) {
  return TIPO_RECORRIDO_LABELS[tipo] || humanize(tipo);
}

export function formatRecorridoVentana(ventana?: RecorridoVentana) {
  if (!ventana) return null;
  const inicio = formatRecorridoFecha(ventana.inicio);
  const fin = formatRecorridoFecha(ventana.fin);
  if (!inicio || !fin) return null;
  return ventana.etiqueta ? `${ventana.etiqueta}: ${inicio} al ${fin}` : `${inicio} al ${fin}`;
}

export function recorridoFechaLabel(recorrido: Recorrido) {
  return formatRecorridoVentana(recorrido.ventana) || formatRecorridoFecha(recorrido.fecha);
}

export function isDateInRecorridoWindow(recorrido: Recorrido, fecha: string) {
  if (!recorrido.ventana || !isValidDateCode(fecha)) return false;
  const inicio = recorrido.ventana.inicio;
  const fin = recorrido.ventana.fin;
  if (!isValidDateCode(inicio) || !isValidDateCode(fin)) return false;
  const current = dayOfYear(fecha);
  const start = dayOfYear(inicio);
  const end = dayOfYear(fin);
  return start <= end
    ? current >= start && current <= end
    : current >= start || current <= end;
}

export function getTodayRecorrido(date = new Date()) {
  const today = dateCode(date);
  return (
    recorridos.find((recorrido) => recorrido.fecha === today) ||
    recorridos.find((recorrido) => isDateInRecorridoWindow(recorrido, today)) ||
    getRecomendadosRecorrido() ||
    recorridos[0]
  );
}

export function getRecomendadosRecorrido() {
  return (
    recorridos.find((recorrido) => recorrido.slug === "recomendados") ||
    recorridos[recorridos.length - 1]
  );
}

function qualityScore(game: GameView) {
  let score = RELEVANCIA_ORDER[game.grado_relevancia_argentina] ?? 3;
  if (!game.isPlayableToday) score += 10;
  if (game.disponibilidad === "abandonware") score += 2;
  if (game.tipo_obra === "comercial") score -= 0.5;
  if (game.imagenes.portada) score -= 0.25;
  if (game.calidad_fuente === "oficial") score -= 0.25;
  if (game.ejes_culturales.length > 0) score -= 0.5;
  if (game.generos.includes("deportes")) score += 1;
  return score;
}

export function destacadosForRecorrido(recorrido: Recorrido): GameView[] {
  return recorrido.destacados_editoriales
    .map(({ id }) => gameById.get(id))
    .filter((game): game is GameView => Boolean(game));
}

export function motivoForDestacado(recorrido: Recorrido, gameId: string) {
  return recorrido.destacados_editoriales.find((destacado) => destacado.id === gameId)?.motivo || "";
}

function normalizedValues(values: string[] = []) {
  return values.filter(Boolean).map(normalizeText);
}

function specificTemas(recorrido: Recorrido) {
  const temas = recorrido.relacionados?.temas?.length
    ? recorrido.relacionados.temas
    : recorrido.temas;
  return temas
    .filter((tema) => !BROAD_TEMAS.has(tema))
    .map(normalizeText);
}

function hasNormalizedMatch(values: string[], expected: string[]) {
  if (!expected.length) return false;
  const normalized = normalizedValues(values);
  return expected.some((item) => normalized.includes(item));
}

function hasSearchMatch(game: GameView, values: string[]) {
  return values.some((value) => game.searchText.includes(value));
}

function matchesVinculo(game: GameView, vinculos: RecorridoRelacionados["vinculos"] = []) {
  return vinculos.some((vinculo) => {
    if (vinculo === "deporte") return game.vinculo_argentina.deporte_argentino.activo;
    return game.vinculo_argentina[vinculo].activo;
  });
}

function gameMatchesRecorrido(game: GameView, recorrido: Recorrido) {
  const reglas = recorrido.relacionados;
  if (reglas?.solo_jugables && !game.isPlayableToday) return false;
  if (reglas?.excluir_ids?.includes(game.id)) return false;
  if (reglas?.excluir_relevancia_menor && game.grado_relevancia_argentina === "menor") {
    return false;
  }

  const temas = specificTemas(recorrido);
  const fallbackTemas = normalizedValues(recorrido.temas);
  const ruleTemas = temas.length ? temas : fallbackTemas;
  const ruleEjes = normalizedValues(reglas?.ejes);
  const ruleProvincias = normalizedValues(reglas?.provincias);
  const ruleRegiones = normalizedValues(reglas?.regiones);
  const ruleFormatos = normalizedValues(reglas?.formatos);
  const ruleGeneros = normalizedValues(reglas?.generos);

  return (
    hasSearchMatch(game, ruleTemas) ||
    hasNormalizedMatch(game.ejes_culturales, ruleEjes) ||
    hasNormalizedMatch(game.contexto_argentino.temas, ruleTemas) ||
    hasNormalizedMatch(game.contexto_argentino.provincias, ruleProvincias) ||
    hasNormalizedMatch(game.contexto_argentino.regiones, ruleRegiones) ||
    hasNormalizedMatch([game.formato], ruleFormatos) ||
    hasNormalizedMatch(game.generos, ruleGeneros) ||
    matchesVinculo(game, reglas?.vinculos)
  );
}

function affinityScore(game: GameView, recorrido: Recorrido) {
  const reglas = recorrido.relacionados;
  const temas = specificTemas(recorrido);
  const fallbackTemas = normalizedValues(recorrido.temas);
  const ruleTemas = temas.length ? temas : fallbackTemas;
  const ruleEjes = normalizedValues(reglas?.ejes);
  const ruleProvincias = normalizedValues(reglas?.provincias);
  const ruleRegiones = normalizedValues(reglas?.regiones);
  const ruleFormatos = normalizedValues(reglas?.formatos);
  const ruleGeneros = normalizedValues(reglas?.generos);
  let score = qualityScore(game);

  if (hasSearchMatch(game, ruleTemas)) score -= 2;
  if (hasNormalizedMatch(game.contexto_argentino.temas, ruleTemas)) score -= 2;
  if (hasNormalizedMatch(game.ejes_culturales, ruleEjes)) score -= 2;
  if (hasNormalizedMatch(game.contexto_argentino.provincias, ruleProvincias)) score -= 1.5;
  if (hasNormalizedMatch(game.contexto_argentino.regiones, ruleRegiones)) score -= 1;
  if (hasNormalizedMatch([game.formato], ruleFormatos)) score -= 0.75;
  if (hasNormalizedMatch(game.generos, ruleGeneros)) score -= 0.75;
  if (matchesVinculo(game, reglas?.vinculos)) score -= 1;
  return score;
}

export function relatedForRecorrido(recorrido: Recorrido): GameView[] {
  const destacados = destacadosForRecorrido(recorrido);
  const seen = new Set(destacados.map((game) => game.id));
  const maxGames = recorrido.relacionados?.limite || MAX_RECORRIDO_GAMES;
  const remaining = maxGames - destacados.length;
  if (remaining <= 0) return [];

  if (recorrido.slug === "recomendados") {
    return games
      .filter(
        (game) =>
          !seen.has(game.id) &&
          game.grado_relevancia_argentina !== "menor" &&
          game.isPlayableToday,
      )
      .sort((a, b) => qualityScore(a) - qualityScore(b))
      .slice(0, remaining);
  }

  return games
    .filter((game) => !seen.has(game.id) && gameMatchesRecorrido(game, recorrido))
    .sort((a, b) => affinityScore(a, recorrido) - affinityScore(b, recorrido))
    .slice(0, remaining);
}

export function gamesForRecorrido(recorrido: Recorrido): GameView[] {
  return destacadosForRecorrido(recorrido);
}

export function countsForRecorrido(recorrido: Recorrido) {
  const destacados = destacadosForRecorrido(recorrido).length;
  return {
    destacados,
    relacionados: 0,
    total: destacados,
  };
}

export function recorridosForGame(gameId: string): Recorrido[] {
  return recorridos.filter((recorrido) =>
    gamesForRecorrido(recorrido).some((game) => game.id === gameId),
  );
}
