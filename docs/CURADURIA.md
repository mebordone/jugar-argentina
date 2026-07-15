# Guía de curaduría y taxonomía

Esta guía documenta cómo leer y mantener el catálogo después de la separación entre formato, tema, vínculo argentino, acceso y datos editoriales.

## Criterio central

Jugar Argentina incluye juegos y contenidos jugables con vínculo argentino verificable. No alcanza con que el desarrollador sea argentino: la ficha necesita una dimensión argentina reconocible en el contenido, la ambientación, los personajes, el deporte, la historia, la cultura, la memoria o los imaginarios locales.

## Qué puede entrar

- Juegos base con territorio, historia, personajes, cultura o deporte argentino como parte relevante.
- Mods, mapas, campañas, DLCs, expansiones o contenido licenciado con vínculo argentino claro.
- Fan games, prototipos y colecciones educativas cuando el vínculo sea verificable y tenga valor cultural o histórico.

## Qué queda afuera

- Juegos donde Argentina es solo un país o equipo seleccionable entre muchos, sin peso jugable o cultural.
- Obras hechas por estudios argentinos pero sin contenido argentino reconocible.
- Referencias decorativas, mínimas o sin fuente verificable.

## Capas públicas

Estas capas ayudan a quien entra por primera vez a entender una tarjeta del catálogo:

- `formato`: qué tipo de contenido es, por ejemplo juego base, mod, mapa, campaña, DLC o contenido licenciado.
- `ejes_culturales` y `contexto_argentino.temas`: los temas principales que se muestran como chips breves.
- `contexto_argentino.provincias` y `contexto_argentino.regiones`: lugar o escala geográfica.
- `vinculo_argentina`: motivo legible de inclusión, traducido en tarjeta como "Ambientado en Argentina", "Protagonista argentino", "Fútbol argentino" o "Referencia argentina".
- `disponibilidad` y enlaces jugables: acceso actual, como gratis, a la venta, Steam Workshop, descarga, preservación o sin link actual.
- `sensibilidad`: aviso público solo cuando el tema requiere contexto adicional.

## Capas editoriales

Estas capas sostienen la curaduría y aparecen con más detalle en la ficha completa o en reportes:

- `grado_relevancia_argentina`: central, importante o menor. Mide cuánto organiza Argentina la experiencia.
- `calidad_fuente`: tipo de fuente principal disponible para verificar la ficha.
- `verificado` y `fecha_actualizacion`: estado editorial de la entrada.
- `tipo_obra`: origen o naturaleza editorial de la obra, por ejemplo comercial, indie, educativo, fan game o institucional.

## Diferencia entre `formato` y `tipo_obra`

`formato` responde qué se incorpora al catálogo. `tipo_obra` responde qué clase de producción es.

Ejemplos:

- Un mapa comunitario puede tener `formato: "mapa"` y `tipo_obra: "mod"`.
- Un DLC oficial puede tener `formato: "dlc"` y `tipo_obra: "comercial"`.
- Un juego escolar puede tener `formato: "juego_base"` o `formato: "coleccion"` y `tipo_obra: "educativo"`.
- Un fan game puede tener `formato: "juego_base"` y `tipo_obra: "fan_game"`.

## Lectura de tarjetas

La tarjeta evita mostrar etiquetas internas crudas. En lugar de `central`, `escenario` o `protagonista`, muestra una lectura humana:

```text
[Campaña] [Cultura urbana] [Terror]
Buenos Aires · Ambientado en Argentina · Steam Workshop
```

El primer chip identifica el formato o tipo visible. Los otros chips resumen temas principales. La línea inferior combina lugar, vínculo argentino y acceso.

## Sensibilidad

La sensibilidad no mide calidad ni importancia. Sirve para indicar cuándo conviene contextualizar una ficha antes de recomendarla o usarla en ámbitos educativos.

- `baja`: no requiere advertencia especial.
- `media`: conviene contextualizar, por ejemplo en guerra, violencia política o memoria.
- `alta`: requiere lectura cuidadosa, por ejemplo dictadura, terrorismo de Estado u otros temas delicados.

## Sugerencias nuevas

Una sugerencia útil debe incluir:

- fuente verificable;
- explicación breve del vínculo argentino;
- formato sugerido, si aplica;
- enlace de acceso o preservación cuando exista.
