import assert from "node:assert/strict";
import { buildCulturalSummary } from "../src/lib/culturalSummary";
import { gameById, type Game } from "../src/lib/games";

function baseGame(overrides: Partial<Game> = {}): Game {
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
    descripcion: "Descripción editorial larga del juego para usar como fallback cuando el resumen automático queda demasiado genérico.",
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

assert.equal(
  buildCulturalSummary(
    baseGame({
      ejes_culturales: ["geografia"],
      contexto_argentino: {
        regiones: ["Pampeana"],
        provincias: ["Buenos Aires"],
        periodo_historico: ["contemporaneo"],
        temas: ["geografia"],
      },
      vinculo_argentina: {
        escenario: { activo: true, presencia: "principal" },
        protagonista: { activo: false, presencia: null },
        deporte_argentino: { activo: false, presencia: null },
      },
    }),
  ),
  "Geografía. Escenario argentino. Ambientado en Buenos Aires.",
  "deduplica geografia en eje y tema",
);

assert.equal(
  buildCulturalSummary(
    baseGame({
      contexto_argentino: {
        regiones: ["Patagonia"],
        provincias: [],
        periodo_historico: ["contemporaneo"],
        temas: ["historia"],
      },
      ejes_culturales: ["historia"],
      vinculo_argentina: {
        escenario: { activo: true, presencia: "principal" },
        protagonista: { activo: false, presencia: null },
        deporte_argentino: { activo: false, presencia: null },
      },
    }),
  ),
  "Historia. Escenario argentino. Una mirada jugable sobre la región Patagonia.",
  "usa frase de región macro",
);

assert.equal(
  buildCulturalSummary(
    baseGame({
      ejes_culturales: ["geografia"],
      tipo_obra: "educativo",
      contexto_argentino: {
        regiones: ["Nacional"],
        provincias: [],
        periodo_historico: ["contemporaneo"],
        temas: [],
      },
      vinculo_argentina: {
        escenario: { activo: true, presencia: "principal" },
        protagonista: { activo: false, presencia: null },
        deporte_argentino: { activo: false, presencia: null },
      },
    }),
  ),
  "Experiencia educativa sobre geografía.",
  "omite frase de lugar para Nacional",
);

assert.match(
  buildCulturalSummary(
    baseGame({
      contexto_argentino: {
        regiones: ["Patagonia"],
        provincias: [],
        periodo_historico: ["contemporaneo"],
        temas: ["guerra_de_malvinas"],
      },
      ejes_culturales: ["memoria"],
      vinculo_argentina: {
        escenario: { activo: true, presencia: "principal" },
        protagonista: { activo: false, presencia: null },
        deporte_argentino: { activo: false, presencia: null },
      },
    }),
  ),
  /^Memoria y Guerra de Malvinas\./,
  "humaniza temas crudos",
);

assert.equal(
  buildCulturalSummary(
    baseGame({
      ejes_culturales: ["deporte"],
      contexto_argentino: {
        regiones: [],
        provincias: [],
        periodo_historico: ["contemporaneo"],
        temas: ["deporte"],
      },
      descripcion:
        "Segunda edición argentina de PC Fútbol con el torneo Apertura 1995 y base de datos elaborada por periodistas locales.",
      vinculo_argentina: {
        escenario: { activo: false, presencia: null },
        protagonista: { activo: false, presencia: null },
        deporte_argentino: { activo: true, presencia: "principal", subtipo: "liga_futbol" },
      },
    }),
  ),
  "Deporte. Deporte y cultura argentina.",
  "enriquece resumen deportivo sin duplicar slug",
);

const slender = gameById.get("slender-threads");
assert.ok(slender, "slender-threads existe");
assert.equal(
  slender!.culturalSummary,
  "Geografía. Escenario argentino. Ambientado en Buenos Aires.",
  "regresión Slender Threads",
);

const menem = gameById.get("super-menem-bros");
assert.ok(menem, "super-menem-bros existe");
assert.equal(
  menem!.culturalSummary,
  "Relectura argentina: Política y Sátira. Una mirada jugable sobre la región Pampeana.",
  "regresión Super Menem Bros",
);

const pcFutbol = gameById.get("pc-futbol-argentina-apertura-95");
assert.ok(pcFutbol, "pc-futbol-argentina-apertura-95 existe");
assert.equal(
  pcFutbol!.culturalSummary,
  "Deporte. Deporte y cultura argentina.",
  "regresión PC Fútbol Apertura 95",
);

const nacional = gameById.get("mapampa");
assert.ok(nacional, "mapampa existe");
assert.doesNotMatch(nacional!.culturalSummary, /desde Nacional/i, "sin frase desde Nacional");
assert.doesNotMatch(
  nacional!.culturalSummary,
  /Para jugar una Argentina/i,
  "sin plantilla antigua de lugar",
);

console.log("OK: tests de resúmenes culturales");
