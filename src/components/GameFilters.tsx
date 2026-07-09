import { useEffect, useMemo, useState } from "react";
import type { GameView } from "../lib/games";
import { humanize, normalizeText, tipoObraTone } from "../lib/filters";

type Options = {
  ejes: string[];
  plataformas: string[];
  provincias: string[];
  regiones: string[];
  disponibilidades: string[];
  sensibilidades: string[];
  tiposObra: string[];
};

type Filters = {
  q: string;
  eje: string;
  vinculo: string;
  plataforma: string;
  provincia: string;
  disponibilidad: string;
  sensibilidad: string;
  tipo_obra: string;
  jugable: string;
  tema: string;
};

type Props = {
  games: GameView[];
  options: Options;
  basePath: string;
};

const EMPTY_FILTERS: Filters = {
  q: "",
  eje: "",
  vinculo: "",
  plataforma: "",
  provincia: "",
  disponibilidad: "",
  sensibilidad: "",
  tipo_obra: "",
  jugable: "",
  tema: "",
};

export default function GameFilters({ games, options, basePath }: Props) {
  const [filters, setFilters] = useState<Filters>(EMPTY_FILTERS);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    setFilters({
      ...EMPTY_FILTERS,
      q: params.get("q") || "",
      eje: params.get("eje") || "",
      vinculo: params.get("vinculo") || "",
      plataforma: params.get("plataforma") || "",
      provincia: params.get("provincia") || "",
      disponibilidad: params.get("disponibilidad") || "",
      sensibilidad: params.get("sensibilidad") || "",
      tipo_obra: params.get("tipo_obra") || "",
      jugable: params.get("jugable") || "",
      tema: params.get("tema") || "",
    });
  }, []);

  useEffect(() => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value) params.set(key, value);
    });
    const query = params.toString();
    const next = query ? `${window.location.pathname}?${query}` : window.location.pathname;
    window.history.replaceState(null, "", next);
  }, [filters]);

  const filtered = useMemo(() => {
    const textQuery = normalizeText([filters.q, filters.tema].filter(Boolean).join(" "));
    return games.filter((game) => {
      if (textQuery && !game.searchText.includes(textQuery)) return false;
      if (filters.eje && !game.ejes_culturales.includes(filters.eje)) return false;
      if (filters.tipo_obra && game.tipo_obra !== filters.tipo_obra) return false;
      if (filters.jugable === "si" && !game.isPlayableToday) return false;
      if (filters.jugable === "no" && game.isPlayableToday) return false;
      if (filters.plataforma && !game.plataformas.includes(filters.plataforma)) return false;
      if (
        filters.provincia &&
        !game.contexto_argentino.provincias.includes(filters.provincia) &&
        !game.contexto_argentino.regiones.includes(filters.provincia)
      ) {
        return false;
      }
      if (
        filters.disponibilidad &&
        game.disponibilidad !== filters.disponibilidad
      ) {
        return false;
      }
      if (filters.sensibilidad && game.sensibilidad !== filters.sensibilidad) {
        return false;
      }
      if (filters.vinculo) {
        const vinculo = game.vinculo_argentina;
        if (
          filters.vinculo === "escenario" &&
          !vinculo.escenario.activo
        ) return false;
        if (
          filters.vinculo === "protagonista" &&
          !vinculo.protagonista.activo
        ) return false;
        if (
          filters.vinculo === "deporte" &&
          !vinculo.deporte_argentino.activo
        ) return false;
      }
      return true;
    });
  }, [filters, games]);

  function update(key: keyof Filters, value: string) {
    setFilters((current) => ({ ...current, [key]: value }));
  }

  function clear() {
    setFilters(EMPTY_FILTERS);
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

      <div className="result-heading">
        <p>
          <strong>{filtered.length}</strong> juegos encontrados
        </p>
        <button className="link-button" type="button" onClick={clear}>
          Limpiar filtros
        </button>
      </div>

      <div className="game-grid">
        {filtered.map((game) => (
          <article className="game-card" key={game.id}>
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
                  rel="noreferrer"
                >
                  {game.primaryAction.label}
                </a>
              ) : (
                <span className="button button-disabled">Sin link de juego</span>
              )}
              <a className="button button-secondary" href={joinBase(basePath, `/juegos/${game.id}`)}>
                Ver ficha
              </a>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

function placeholderClass(ejes: string[]) {
  const eje = ejes[0] || "historia";
  return `cover-placeholder cover-${eje}`;
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
  return (
    <label>
      <span>{label}</span>
      <select value={value} onChange={(event) => onChange(event.target.value)}>
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
