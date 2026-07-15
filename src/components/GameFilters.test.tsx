import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import GameFilters from "./GameFilters";
import { EMPTY_CATALOG_FILTERS } from "../lib/filterGames";
import { baseGameView } from "../test/fixtures/game";

const options = {
  ejes: ["folclore", "historia"],
  plataformas: ["PC", "Web"],
  provincias: ["Buenos Aires", "Mendoza"],
  regiones: ["Pampeana"],
  disponibilidades: ["gratis", "a_la_venta"],
  sensibilidades: ["baja", "alta"],
  tiposObra: ["indie", "comercial"],
  formatos: ["juego_base", "mapa", "campania"],
};

const games = [
  baseGameView({
    id: "tango-game",
    titulo: "Tango: The Adventure Game",
    ejes_culturales: ["cultura_urbana"],
    contexto_argentino: {
      regiones: [],
      provincias: [],
      periodo_historico: [],
      temas: ["tango"],
    },
  }),
  baseGameView({
    id: "otro-game",
    titulo: "Otro juego",
    ejes_culturales: ["historia"],
    contexto_argentino: {
      regiones: [],
      provincias: [],
      periodo_historico: [],
      temas: ["historia"],
    },
  }),
];

function expectResultCount(count: number) {
  expect(document.getElementById("catalog-results")).toHaveTextContent(
    `${count} juegos encontrados`,
  );
}

describe("GameFilters", () => {
  it("renderiza catálogo y permite buscar", async () => {
    const user = userEvent.setup();
    render(<GameFilters games={games} options={options} basePath="/" />);

    expectResultCount(2);

    const search = screen.getByLabelText("Buscar juegos en el catálogo");
    await user.type(search, "tango");

    expect(search).toHaveValue("tango");
    expectResultCount(1);
    expect(screen.getByRole("link", { name: "Tango: The Adventure Game" })).toBeInTheDocument();
  });

  it("filtra por select y limpia filtros", async () => {
    const user = userEvent.setup();
    render(<GameFilters games={games} options={options} basePath="/" />);

    await user.selectOptions(screen.getByLabelText("Eje cultural"), "historia");
    expectResultCount(1);

    await user.click(screen.getByRole("button", { name: "Limpiar" }));
    expectResultCount(2);
  });

  it("pagina resultados cuando hay más de 24 juegos", async () => {
    const user = userEvent.setup();
    const manyGames = Array.from({ length: 30 }, (_, index) =>
      baseGameView({ id: `game-${index}`, titulo: `Juego ${index}` }),
    );

    render(<GameFilters games={manyGames} options={options} basePath="/" />);

    expect(screen.getByText(/página 1 de 2/)).toBeInTheDocument();
    await user.click(screen.getAllByRole("button", { name: "Página siguiente" })[0]);
    expect(screen.getByText(/página 2 de 2/)).toBeInTheDocument();
  });

  it("sincroniza URL al cambiar filtros", async () => {
    const user = userEvent.setup();
    const replaceState = vi.spyOn(window.history, "replaceState");

    render(<GameFilters games={games} options={options} basePath="/" />);
    await user.type(screen.getByLabelText("Buscar juegos en el catálogo"), "tango");

    expect(replaceState).toHaveBeenCalled();
    const lastCall = replaceState.mock.calls.at(-1);
    expect(String(lastCall?.[2])).toContain("q=tango");
  });

  it("muestra estado vacío y permite limpiar desde el panel", async () => {
    const user = userEvent.setup();
    render(<GameFilters games={games} options={options} basePath="/" />);

    await user.type(screen.getByLabelText("Buscar juegos en el catálogo"), "inexistente");
    expect(screen.getByRole("heading", { name: "Sin resultados" })).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: "Limpiar filtros" }));
    expectResultCount(2);
  });

  it("quita filtros activos desde chips y oculta panel avanzado", async () => {
    const user = userEvent.setup();
    render(<GameFilters games={games} options={options} basePath="/" />);

    await user.selectOptions(screen.getByLabelText("Eje cultural"), "historia");
    expect(screen.getByRole("button", { name: "Filtros (1)" })).toBeInTheDocument();

    await user.click(
      screen.getByRole("button", { name: "Quitar filtro Eje cultural: Historia" }),
    );
    expectResultCount(2);

    await user.click(screen.getByRole("button", { name: "Filtros" }));
    expect(screen.queryByLabelText("Eje cultural")).not.toBeInTheDocument();
  });

  it("navega hacia atrás en paginación", async () => {
    const user = userEvent.setup();
    const manyGames = Array.from({ length: 30 }, (_, index) =>
      baseGameView({ id: `game-${index}`, titulo: `Juego ${index}` }),
    );

    render(<GameFilters games={manyGames} options={options} basePath="/" />);
    await user.click(screen.getAllByRole("button", { name: "Página siguiente" })[0]);
    expect(screen.getByText(/página 2 de 2/)).toBeInTheDocument();

    await user.click(screen.getAllByRole("button", { name: "Página anterior" })[0]);
    expect(screen.getByText(/página 1 de 2/)).toBeInTheDocument();
  });

  it("renderiza variantes de tarjeta con portada, mod y sin link jugable", () => {
    const richGames = [
      baseGameView({
        id: "con-portada",
        titulo: "Con portada",
        tipo_obra: "mod",
        formato: "mapa",
        imagenes: { portada: "https://example.com/cover.jpg", capturas: [] },
        enlaces: { itch: "https://itch.io/con-portada" },
      }),
      baseGameView({
        id: "sin-link",
        titulo: "Sin link",
        enlaces: {},
        disponibilidad: "desconocida",
      }),
    ];

    render(
      <GameFilters
        games={richGames}
        options={options}
        basePath="/jugar-argentina/"
        initialFilters={EMPTY_CATALOG_FILTERS}
      />,
    );

    expect(screen.getByAltText("Portada de Con portada")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Jugar ahora/ })).toHaveAttribute(
      "href",
      "https://itch.io/con-portada",
    );
    expect(screen.getAllByText("Sin link de juego").length).toBeGreaterThan(0);
    expect(screen.getByRole("link", { name: "Con portada" })).toHaveAttribute(
      "href",
      "/jugar-argentina/juegos/con-portada",
    );
  });

  it("aplica filtros avanzados de catálogo", async () => {
    const user = userEvent.setup();
    const playable = baseGameView({
      id: "jugable-pc",
      titulo: "Jugable PC",
      plataformas: ["PC"],
      tipo_obra: "indie",
      formato: "juego_base",
      disponibilidad: "gratis",
      sensibilidad: "baja",
      enlaces: { itch: "https://itch.io/jugable" },
      contexto_argentino: {
        regiones: [],
        provincias: ["Mendoza"],
        periodo_historico: [],
        temas: [],
      },
      vinculo_argentina: {
        escenario: { activo: true, presencia: "principal" },
        protagonista: { activo: false, presencia: null },
        deporte_argentino: { activo: false, presencia: null },
      },
    });
    const hidden = baseGameView({
      id: "oculto",
      titulo: "Oculto",
      plataformas: ["Web"],
      tipo_obra: "comercial",
      formato: "campania",
      disponibilidad: "a_la_venta",
      sensibilidad: "alta",
      enlaces: {},
    });

    render(
      <GameFilters
        games={[playable, hidden]}
        options={options}
        basePath="/"
      />,
    );

    await user.selectOptions(screen.getByLabelText("Tipo de obra"), "indie");
    await user.selectOptions(screen.getByLabelText("Formato"), "juego_base");
    await user.selectOptions(screen.getByLabelText("Jugable hoy"), "si");
    await user.selectOptions(screen.getByLabelText("Vínculo"), "escenario");
    await user.selectOptions(screen.getByLabelText("Plataforma"), "PC");
    await user.selectOptions(screen.getByLabelText("Provincia/región"), "Mendoza");
    await user.selectOptions(screen.getByLabelText("Disponibilidad"), "gratis");
    await user.selectOptions(screen.getByLabelText("Sensibilidad"), "baja");

    expectResultCount(1);
    expect(screen.getByRole("link", { name: "Jugable PC" })).toBeInTheDocument();
  });
});
