import { useEffect, useMemo, useState } from "react";
import type { GameView } from "../lib/games";
import {
  EMPTY_CATALOG_FILTERS,
  filterGames,
  type CatalogFilters,
} from "../lib/filterGames";
import { humanize, placeholderClass, tipoObraTone } from "../lib/filters";
import { reportGameUrl } from "../lib/report";

const PAGE_SIZE = 24;

type Options = {
  ejes: string[];
  plataformas: string[];
  provincias: string[];
  regiones: string[];
  disponibilidades: string[];
  sensibilidades: string[];
  tiposObra: string[];
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

  useEffect(() => {
    setPage(1);
  }, [filters]);

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

  const activeTema = filters.tema;

  function update(key: keyof CatalogFilters, value: string) {
    setFilters((current) => ({ ...current, [key]: value }));
  }

  function clear() {
    setFilters(EMPTY_CATALOG_FILTERS);
  }

  function removeTema() {
    update("tema", "");
  }

  return (
    <section className="catalog-panel">
      <div className="filters">
        <label className="search-field">
          <span>Buscar</span>
          <input
            value={filters.q}
            onChange={(event) => update("q", event.target.value)}
            placeholder="Malvinas, truco, Mendoza, San Martín..."
            aria-label="Buscar juegos en el catálogo"
          />
        </label>
        <Select label="Eje cultural" value={filters.eje} onChange={(v) => update("eje", v)} values={options.ejes} />
        <Select label="Tipo de obra" value={filters.tipo_obra} onChange={(v) => update("tipo_obra", v)} values={options.tiposObra} />
        <Select label="Jugable hoy" value={filters.jugable} onChange={(v) => update("jugable", v)} values={["si", "no"]} labels={{ si: "Sí", no: "Sin link de juego" }} />
        <Select label="Vínculo" value={filters.vinculo} onChange={(v) => update("vinculo", v)} values={["escenario", "protagonista", "deporte"]} />
        <Select label="Plataforma" value={filters.plataforma} onChange={(v) => update("plataforma", v)} values={options.plataformas} />
        <Select label="Provincia/región" value={filters.provincia} onChange={(v) => update("provincia", v)} values={[...options.provincias, ...options.regiones]} />
        <Select label="Disponibilidad" value={filters.disponibilidad} onChange={(v) => update("disponibilidad", v)} values={options.disponibilidades} />
        <Select label="Sensibilidad" value={filters.sensibilidad} onChange={(v) => update("sensibilidad", v)} values={options.sensibilidades} />
      </div>

      {activeTema && (
        <div className="active-filters">
          <span className="chip chip-active">
            Tema: {humanize(activeTema)}
            <button type="button" className="chip-remove" onClick={removeTema} aria-label={`Quitar filtro ${humanize(activeTema)}`}>
              ×
            </button>
          </span>
        </div>
      )}

      <div className="result-heading">
        <p>
          <strong>{filtered.length}</strong> juegos encontrados
          {pageCount > 1 && (
            <span className="result-page">
              {" "}
              · página {currentPage} de {pageCount}
            </span>
          )}
        </p>
        <button className="link-button" type="button" onClick={clear}>
          Limpiar filtros
        </button>
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
          <div className="game-grid">
            {visible.map((game) => (
              <GameCard key={game.id} game={game} basePath={basePath} />
            ))}
          </div>
          {pageCount > 1 && (
            <div className="pagination">
              <button
                className="button button-secondary"
                type="button"
                disabled={currentPage <= 1}
                onClick={() => setPage((value) => Math.max(1, value - 1))}
              >
                Anterior
              </button>
              <span className="pagination-meta">
                Página {currentPage} de {pageCount}
              </span>
              <button
                className="button button-secondary"
                type="button"
                disabled={currentPage >= pageCount}
                onClick={() => setPage((value) => Math.min(pageCount, value + 1))}
              >
                Siguiente
              </button>
            </div>
          )}
        </>
      )}
    </section>
  );
}

function GameCard({ game, basePath }: { game: GameView; basePath: string }) {
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
          {game.anio ?? "Sin fecha"} · {game.plataformas.slice(0, 3).join(", ")}
        </p>
        <h3>
          <a href={joinBase(basePath, `/juegos/${game.id}`)}>{game.titulo}</a>
        </h3>
        <p>{game.culturalSummary || game.descripcion}</p>
        <div className="badge-row">
          <span className={`badge badge-${tipoObraTone(game.tipo_obra)}`}>
            {humanize(game.tipo_obra)}
          </span>
          {game.badges.slice(0, 4).map((badge) => (
            <span className="badge" key={badge}>{badge}</span>
          ))}
          <span className="badge badge-warm">
            {humanize(game.grado_relevancia_argentina)}
          </span>
          {!game.isPlayableToday && (
            <span className="badge badge-muted">Sin link de juego</span>
          )}
        </div>
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

function joinBase(basePath: string, path: string) {
  const cleanBase = basePath.endsWith("/") ? basePath.slice(0, -1) : basePath;
  return `${cleanBase}${path}`;
}
