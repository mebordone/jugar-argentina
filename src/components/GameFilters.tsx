import { useEffect, useMemo, useRef, useState } from "react";
import type { GameView } from "../lib/games";
import {
  countActiveFilters,
  FILTERS_OPEN_KEY,
  FILTER_LABELS,
  formatFilterValue,
  isSearchOnlyChange,
  joinBase,
  readFiltersOpenPreference,
  scrollToResultsAndFocus,
} from "../lib/catalogUi";
import {
  EMPTY_CATALOG_FILTERS,
  filterGames,
  type CatalogFilters,
} from "../lib/filterGames";
import { humanize, placeholderClass, tipoObraTone } from "../lib/filters";
import { gameReleasePrimary } from "../lib/release";
import { reportGameUrl } from "../lib/report";
import {
  cardChipLabels,
  cardMetaParts,
  sensitivityCardLabel,
} from "../lib/cardMetadata";

const PAGE_SIZE = 24;

type Options = {
  ejes: string[];
  plataformas: string[];
  provincias: string[];
  regiones: string[];
  disponibilidades: string[];
  sensibilidades: string[];
  tiposObra: string[];
  formatos: string[];
};

type Props = {
  games: GameView[];
  options: Options;
  basePath: string;
  initialFilters?: CatalogFilters;
};

export default function GameFilters({
  games,
  options,
  basePath,
  initialFilters = EMPTY_CATALOG_FILTERS,
}: Props) {
  const [filters, setFilters] = useState<CatalogFilters>(initialFilters);
  const [page, setPage] = useState(1);
  const [filtersOpen, setFiltersOpen] = useState(readFiltersOpenPreference);
  const resultsRef = useRef<HTMLDivElement>(null);
  const skipFilterScrollRef = useRef(true);
  const skipPageScrollRef = useRef(true);
  const previousFiltersRef = useRef(initialFilters);

  useEffect(() => {
    setPage(1);
  }, [filters]);

  useEffect(() => {
    const previous = previousFiltersRef.current;
    previousFiltersRef.current = filters;

    if (skipFilterScrollRef.current) {
      skipFilterScrollRef.current = false;
      return;
    }
    if (isSearchOnlyChange(previous, filters)) {
      return;
    }
    scrollToResultsAndFocus(resultsRef);
  }, [filters]);

  useEffect(() => {
    if (skipPageScrollRef.current) {
      skipPageScrollRef.current = false;
      return;
    }
    scrollToResultsAndFocus(resultsRef);
  }, [page]);

  useEffect(() => {
    window.localStorage.setItem(FILTERS_OPEN_KEY, String(filtersOpen));
  }, [filtersOpen]);

  useEffect(() => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value) params.set(key, value);
    });
    const query = params.toString();
    const next = query ? `${window.location.pathname}?${query}` : window.location.pathname;
    window.history.replaceState(null, "", next);
  }, [filters]);

  const filtered = useMemo(() => filterGames(games, filters), [filters, games]);
  const pageCount = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const currentPage = Math.min(page, pageCount);
  const visible = filtered.slice(
    (currentPage - 1) * PAGE_SIZE,
    currentPage * PAGE_SIZE,
  );
  const activeCount = countActiveFilters(filters);
  const activeEntries = (
    Object.entries(filters) as Array<[keyof CatalogFilters, string]>
  ).filter(([, value]) => Boolean(value));

  function update(key: keyof CatalogFilters, value: string) {
    setFilters((current) => ({ ...current, [key]: value }));
  }

  function clear() {
    setFilters(EMPTY_CATALOG_FILTERS);
  }

  function removeFilter(key: keyof CatalogFilters) {
    update(key, "");
  }

  function goToPage(nextPage: number) {
    setPage(Math.min(pageCount, Math.max(1, nextPage)));
  }

  return (
    <section className="catalog-panel">
      <div className="filters-toolbar">
        <label className="search-field toolbar-search">
          <span>Buscar</span>
          <input
            value={filters.q}
            onChange={(event) => update("q", event.target.value)}
            placeholder="Malvinas, truco, Mendoza, San Martín..."
            aria-label="Buscar juegos en el catálogo"
          />
        </label>
        <button
          type="button"
          className="button button-secondary filters-toggle"
          aria-expanded={filtersOpen}
          aria-controls="filters-advanced"
          onClick={() => setFiltersOpen((open) => !open)}
        >
          Filtros{activeCount > 0 ? ` (${activeCount})` : ""}
        </button>
        {activeCount > 0 && (
          <button className="link-button toolbar-clear" type="button" onClick={clear}>
            Limpiar
          </button>
        )}
      </div>

      {filtersOpen && (
        <div className="filters-advanced" id="filters-advanced">
          <Select label="Eje cultural" value={filters.eje} onChange={(v) => update("eje", v)} values={options.ejes} />
          <Select label="Tipo de obra" value={filters.tipo_obra} onChange={(v) => update("tipo_obra", v)} values={options.tiposObra} />
          <Select label="Formato" value={filters.formato} onChange={(v) => update("formato", v)} values={options.formatos} />
          <Select label="Jugable hoy" value={filters.jugable} onChange={(v) => update("jugable", v)} values={["si", "no"]} labels={{ si: "Sí", no: "Sin link de juego" }} />
          <Select label="Vínculo" value={filters.vinculo} onChange={(v) => update("vinculo", v)} values={["escenario", "protagonista", "deporte"]} />
          <Select label="Plataforma" value={filters.plataforma} onChange={(v) => update("plataforma", v)} values={options.plataformas} />
          <Select label="Provincia/región" value={filters.provincia} onChange={(v) => update("provincia", v)} values={[...options.provincias, ...options.regiones]} />
          <Select label="Disponibilidad" value={filters.disponibilidad} onChange={(v) => update("disponibilidad", v)} values={options.disponibilidades} />
          <Select label="Sensibilidad" value={filters.sensibilidad} onChange={(v) => update("sensibilidad", v)} values={options.sensibilidades} />
        </div>
      )}

      {activeEntries.length > 0 && (
        <div className="active-filters">
          {activeEntries.map(([key, value]) => (
            <span className="chip chip-active" key={key}>
              {FILTER_LABELS[key]}: {formatFilterValue(key, value)}
              <button
                type="button"
                className="chip-remove"
                onClick={() => removeFilter(key)}
                aria-label={`Quitar filtro ${FILTER_LABELS[key]}: ${formatFilterValue(key, value)}`}
              >
                ×
              </button>
            </span>
          ))}
        </div>
      )}

      <div
        className="result-heading"
        id="catalog-results"
        ref={resultsRef}
        tabIndex={-1}
      >
        <p aria-live="polite" aria-atomic="true">
          <strong>{filtered.length}</strong> juegos encontrados
          {pageCount > 1 && (
            <span className="result-page">
              {" "}
              · página {currentPage} de {pageCount}
            </span>
          )}
        </p>
      </div>

      {filtered.length === 0 ? (
        <div className="empty-state panel">
          <h2>Sin resultados</h2>
          <p>
            No hay juegos que coincidan con estos filtros. Probá ampliar la búsqueda o
            limpiar los filtros activos.
          </p>
          <button className="button button-secondary" type="button" onClick={clear}>
            Limpiar filtros
          </button>
        </div>
      ) : (
        <>
          {pageCount > 1 && (
            <Pagination
              currentPage={currentPage}
              pageCount={pageCount}
              onPageChange={goToPage}
              className="pagination-top"
            />
          )}
          <div className="game-grid">
            {visible.map((game) => (
              <GameCard key={game.id} game={game} basePath={basePath} />
            ))}
          </div>
          {pageCount > 1 && (
            <Pagination
              currentPage={currentPage}
              pageCount={pageCount}
              onPageChange={goToPage}
            />
          )}
        </>
      )}
    </section>
  );
}

function Pagination({
  currentPage,
  pageCount,
  onPageChange,
  className = "",
}: {
  currentPage: number;
  pageCount: number;
  onPageChange: (page: number) => void;
  className?: string;
}) {
  return (
    <nav
      className={`pagination ${className}`.trim()}
      aria-label="Paginación del catálogo"
    >
      <button
        className="button button-secondary"
        type="button"
        disabled={currentPage <= 1}
        aria-label="Página anterior"
        onClick={() => onPageChange(currentPage - 1)}
      >
        Anterior
      </button>
      <span className="pagination-meta">
        Página <span aria-current="page">{currentPage}</span> de {pageCount}
      </span>
      <button
        className="button button-secondary"
        type="button"
        disabled={currentPage >= pageCount}
        aria-label="Página siguiente"
        onClick={() => onPageChange(currentPage + 1)}
      >
        Siguiente
      </button>
    </nav>
  );
}

function GameCard({ game, basePath }: { game: GameView; basePath: string }) {
  const chipLabels = cardChipLabels(game);
  const metaParts = cardMetaParts(game);
  const sensitivityLabel = sensitivityCardLabel(game);

  return (
    <article className="game-card">
      {game.imagenes?.portada ? (
        <img
          className="game-card-cover"
          src={game.imagenes.portada}
          alt={`Portada de ${game.titulo}`}
          loading="lazy"
          decoding="async"
        />
      ) : (
        <div
          className={`game-card-cover ${placeholderClass(game.ejes_culturales)}`}
          aria-hidden="true"
        />
      )}
      <div className="game-card-content">
        <p className="eyebrow">
          {gameReleasePrimary(game)} · {game.plataformas.slice(0, 3).join(", ")}
        </p>
        <h3>
          <a href={joinBase(basePath, `/juegos/${game.id}`)}>{game.titulo}</a>
        </h3>
        <p>{game.culturalSummary || game.descripcion}</p>
        <div className="badge-row">
          {chipLabels.map((badge, index) => (
            <span
              className={`badge ${index === 0 ? `badge-${tipoObraTone(game.tipo_obra)}` : ""}`.trim()}
              key={badge}
            >
              {badge}
            </span>
          ))}
          {sensitivityLabel && (
            <span className="badge badge-alert">{sensitivityLabel}</span>
          )}
        </div>
        {metaParts.length > 0 && (
          <p className="game-card-meta">{metaParts.join(" · ")}</p>
        )}
      </div>
      <div className="game-card-actions">
        {game.primaryAction ? (
          <a
            className="button button-primary"
            href={game.primaryAction.url}
            target="_blank"
            rel="noreferrer noopener"
          >
            {game.primaryAction.label}
            <span className="sr-only"> (se abre en una pestaña nueva)</span>
          </a>
        ) : (
          <span className="button button-disabled" aria-disabled="true">
            Sin link de juego
          </span>
        )}
        <a className="button button-secondary" href={joinBase(basePath, `/juegos/${game.id}`)}>
          Ver ficha
        </a>
        <a
          className="game-card-report"
          href={reportGameUrl(game)}
          target="_blank"
          rel="noreferrer noopener"
        >
          Sugerir corrección
        </a>
      </div>
    </article>
  );
}

function Select({
  label,
  value,
  values,
  labels,
  onChange,
}: {
  label: string;
  value: string;
  values: string[];
  labels?: Record<string, string>;
  onChange: (value: string) => void;
}) {
  const id = `filter-${label.toLowerCase().replace(/\W+/g, "-")}`;
  return (
    <label htmlFor={id}>
      <span>{label}</span>
      <select id={id} value={value} onChange={(event) => onChange(event.target.value)}>
        <option value="">Todos</option>
        {values.map((item) => (
          <option value={item} key={item}>
            {labels?.[item] || humanize(item)}
          </option>
        ))}
      </select>
    </label>
  );
}

