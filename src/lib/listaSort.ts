export type ListaSortKey =
  | "titulo-asc"
  | "titulo-desc"
  | "fecha_alta-desc"
  | "fecha_alta-asc"
  | "anio-desc"
  | "anio-asc";

export type ListaSortableFields = {
  titulo: string;
  fecha_alta?: string;
  anio?: number | null;
};

export const LISTA_SORT_OPTIONS: Array<{ value: ListaSortKey; label: string }> = [
  { value: "titulo-asc", label: "Alfabético (A–Z)" },
  { value: "titulo-desc", label: "Alfabético (Z–A)" },
  { value: "fecha_alta-desc", label: "Fecha de alta (más recientes)" },
  { value: "fecha_alta-asc", label: "Fecha de alta (más antiguos)" },
  { value: "anio-desc", label: "Año del juego (más recientes)" },
  { value: "anio-asc", label: "Año del juego (más antiguos)" },
];

export const DEFAULT_LISTA_SORT: ListaSortKey = "titulo-asc";

function compareNullableNumber(a: number | null | undefined, b: number | null | undefined) {
  const av = a ?? -1;
  const bv = b ?? -1;
  return av - bv;
}

function parseTimestamp(value: string | undefined) {
  if (!value) return null;
  const parsed = Date.parse(value);
  return Number.isNaN(parsed) ? null : parsed;
}

/** Fechas ausentes/inválidas van al final en cualquier dirección. */
function compareDate(
  a: string | undefined,
  b: string | undefined,
  direction: "asc" | "desc",
) {
  const at = parseTimestamp(a);
  const bt = parseTimestamp(b);
  if (at === null && bt === null) return 0;
  if (at === null) return 1;
  if (bt === null) return -1;
  return direction === "desc" ? bt - at : at - bt;
}

export function formatFechaAlta(value: string | undefined) {
  if (!value) return "";
  const day = value.slice(0, 10);
  return /^\d{4}-\d{2}-\d{2}$/.test(day) ? day : value;
}

export function sortListaItems<T extends ListaSortableFields>(
  items: T[],
  sortKey: ListaSortKey,
): T[] {
  const sorted = [...items];
  sorted.sort((a, b) => {
    switch (sortKey) {
      case "titulo-desc":
        return b.titulo.localeCompare(a.titulo, "es");
      case "fecha_alta-desc":
        return compareDate(a.fecha_alta, b.fecha_alta, "desc") || a.titulo.localeCompare(b.titulo, "es");
      case "fecha_alta-asc":
        return compareDate(a.fecha_alta, b.fecha_alta, "asc") || a.titulo.localeCompare(b.titulo, "es");
      case "anio-desc":
        return compareNullableNumber(b.anio, a.anio) || a.titulo.localeCompare(b.titulo, "es");
      case "anio-asc":
        return compareNullableNumber(a.anio, b.anio) || a.titulo.localeCompare(b.titulo, "es");
      case "titulo-asc":
      default:
        return a.titulo.localeCompare(b.titulo, "es");
    }
  });
  return sorted;
}
