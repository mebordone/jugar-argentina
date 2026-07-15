import { enrichGame, type Game, type GameView } from "../../lib/games";

export function baseGame(overrides: Partial<Game> = {}): Game {
  return {
    id: "test-game",
    titulo: "Test Game",
    titulo_original: "Test Game",
    anio: 2020,
    estado: "publicado",
    vinculo_argentina: {
      escenario: { activo: false, presencia: null },
      protagonista: { activo: false, presencia: null },
      deporte_argentino: { activo: false, presencia: null },
    },
    personajes_argentinos: [],
    deporte_argentino: null,
    desarrollador: "Dev",
    pais_desarrollo: "Argentina",
    plataformas: ["PC"],
    generos: ["aventura"],
    descripcion:
      "Descripción editorial larga del juego para usar como fallback cuando el resumen automático queda demasiado genérico.",
    contexto_argentino: {
      regiones: [],
      provincias: [],
      periodo_historico: ["contemporaneo"],
      temas: [],
    },
    enlaces: {},
    imagenes: { portada: null, capturas: [] },
    ejes_culturales: [],
    tipo_obra: "comercial",
    formato: "juego_base",
    grado_relevancia_argentina: "importante",
    calidad_fuente: "prensa",
    sensibilidad: "baja",
    serie: null,
    edicion: null,
    relacionado_con: [],
    disponibilidad: "gratis",
    ...overrides,
  };
}

export function baseGameView(overrides: Partial<Game> = {}): GameView {
  return enrichGame(baseGame(overrides));
}
