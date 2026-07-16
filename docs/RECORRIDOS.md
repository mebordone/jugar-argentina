# Recorridos editoriales

Los recorridos son puertas de entrada al catálogo. No son listas automáticas: tienen una mirada editorial, una fecha o tema de lectura, y destacados elegidos a mano con motivos curatoriales explícitos.

## Prioridad de Release 2

La prioridad es cubrir fechas patrias argentinas usando como referencia el calendario oficial de feriados nacionales: https://www.argentina.gob.ar/feriados.

Fechas patrias prioritarias:

- `03-24`: Día Nacional de la Memoria por la Verdad y la Justicia.
- `04-02`: Día del Veterano y de los Caídos en la Guerra de Malvinas.
- `05-25`: Día de la Revolución de Mayo.
- `06-20`: Día de la Bandera.
- `07-09`: Día de la Independencia.
- `08-17`: Paso a la Inmortalidad del General José de San Martín.
- `10-12`: Día del Respeto a la Diversidad Cultural.
- `11-20`: Día de la Soberanía Nacional.

No todos los feriados deben transformarse en recorridos. Los feriados turísticos, religiosos o administrativos quedan fuera salvo que haya una lectura cultural clara para el catálogo.

## Modelo de datos

Los recorridos viven en `src/content/efemerides.json`.

Campos principales:

- `slug`: identificador de URL.
- `tipo`: `fecha_patria`, `efemeride`, `permanente`, `territorial` o `recomendado`.
- `fecha`: fecha exacta `MM-DD`, si aplica.
- `ventana`: rango `inicio` / `fin` para activar el recorrido durante varios días.
- `titulo`, `bajada`, `descripcion`: capas de texto público.
- `criterio`: explica por qué existe el recorrido.
- `temas`: temas para chips y búsqueda.
- `territorios`: escala geográfica o cultural del recorrido.
- `destacados_editoriales`: juegos elegidos a mano con `id` y `motivo`.
- `relacionados`: reglas internas opcionales para explorar afinidad, sin formar parte del conteo ni de la lista pública del recorrido.

## Destacados curados

Los destacados son curatoriales: deben tener motivo propio y orden intencional. Son los únicos juegos que se muestran y cuentan públicamente en cada recorrido.

Las reglas de relacionados pueden existir como herramienta interna de exploración, pero no completan automáticamente la página del recorrido.

## Tipos editoriales

Los recorridos no cumplen todos la misma función:

- Las efemérides críticas del calendario parten de una fecha concreta y proponen una lectura cultural. Por ejemplo, el 12 de octubre se trabaja como `Diversidad cultural, conquista y resistencias`, con foco en conquista, colonialismo, resistencias indígenas y revisión crítica del relato de descubrimiento.
- Los recorridos permanentes de culturas y territorios no dependen de una fecha. `Pueblos originarios, territorios y memorias vivas` reúne obras sobre pueblos, comunidades, lenguas, territorios, mitologías y memorias indígenas con vínculo argentino verificable.
- Los recorridos territoriales organizan el catálogo por lugar o escala geográfica cuando el territorio estructura la experiencia.
- Las selecciones editoriales permanentes, como `Los mejores juegos del catálogo`, funcionan como puerta de entrada curada y no como ranking automático ni lista de juegos necesariamente disponibles hoy.

Una obra puede aparecer en más de un recorrido si el motivo editorial cambia. `Anahí`, por ejemplo, puede servir tanto para una lectura crítica del 12 de octubre como para un recorrido permanente sobre memoria guaraní y culturas originarias.

Los recorridos territoriales requieren que el lugar organice la experiencia, el argumento o el aprendizaje. `Patagonia jugable` y `Provincias argentinas en juego` no incluyen un título solo porque su estudio sea argentino: exigen un territorio reconocible y relevante dentro de la obra.

Los recorridos educativos reúnen obras donde aprender sobre Argentina es parte central del sistema jugable —fauna, patrimonio, ciencia, provincias o infraestructura— y no solo un contexto accesorio.

## Reglas de calidad

El comando `npm run validate:recorridos` revisa:

- slugs únicos;
- fechas y ventanas válidas;
- tipo de recorrido válido;
- textos editoriales obligatorios;
- destacados existentes en `data/games.json`;
- destacados sin duplicados;
- motivos curatoriales presentes;
- cobertura de fechas patrias prioritarias.

`npm run validate` incluye esta validación junto con datos y enlaces.

## Criterio de edición

Al crear o ajustar un recorrido:

1. Definir qué fecha, territorio o tema propone.
2. Escribir un criterio que explique la selección.
3. Elegir pocos destacados fuertes antes que completar por volumen.
4. Escribir un motivo para cada destacado.
5. Separar efemérides de recorridos permanentes cuando una fecha no alcanza para explicar todo un campo cultural.
6. Usar reglas de relacionados solo como apoyo interno de revisión, no como listado público.
7. Validar con `npm run validate:recorridos`.
