import assert from "node:assert/strict";
import { games } from "../src/lib/games";
import {
  EMPTY_CATALOG_FILTERS,
  filterGames,
  parseCatalogFilters,
} from "../src/lib/filterGames";
import { gamesForRecorrido, getRecomendadosRecorrido } from "../src/lib/recorridos";

const jugables = filterGames(games, { ...EMPTY_CATALOG_FILTERS, jugable: "si" });
assert.ok(jugables.length >= 90, "debe haber al menos 90 juegos jugables");

const malvinas = filterGames(games, {
  ...EMPTY_CATALOG_FILTERS,
  tema: "malvinas",
});
assert.ok(malvinas.length > 0, "filtro tema malvinas debe devolver resultados");

const params = parseCatalogFilters({ jugable: "si", eje: "folclore" });
assert.equal(params.jugable, "si");
assert.equal(params.eje, "folclore");

const recomendados = gamesForRecorrido(getRecomendadosRecorrido());
assert.equal(recomendados.length, 18);

console.log("OK: tests de filtros y recorridos");
