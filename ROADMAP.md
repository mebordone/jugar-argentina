# Roadmap de Jugar Argentina

## Vision

Convertir Jugar Argentina en una cartografia curada, federal y explorable del vinculo entre videojuegos y Argentina: juegos hechos en el pais, juegos ambientados en sus territorios, referencias culturales, politicas, historicas, deportivas y educativas.

El objetivo no es solo acumular fichas. El sitio tiene que ordenar informacion, explicar criterios, permitir descubrimiento y hacer que una persona pueda entender rapidamente que esta viendo, por que importa y como seguir explorando.

## Principios

- **Claridad editorial:** cada ficha, recorrido y lista debe explicar su criterio sin repetir etiquetas de forma mecanica.
- **Evidencia verificable:** todo vinculo argentino importante deberia apoyarse en fuentes, enlaces o notas curatoriales.
- **Explorabilidad:** el sitio tiene que ayudar a navegar por tema, provincia, disponibilidad, recorrido, lista o recomendacion.
- **Orden progresivo:** no hace falta construir un CMS completo de entrada; primero conviene mejorar datos, reportes y flujos de edicion.
- **Separacion de capas:** fichas, candidatos, recorridos, listas y home no cumplen la misma funcion y no deberian administrarse igual.
- **Federalizacion:** el crecimiento del catalogo debe mirar fuera de Buenos Aires, CABA y conurbano.

## Que hay que administrar

### Fichas de juegos

Son el CRUD principal del proyecto. Deben poder crearse, editarse, validarse y publicarse con datos estructurados: titulo, anio, estado, desarrollador, pais, plataformas, generos, vinculo argentino, contexto, enlaces, imagenes, fuentes, disponibilidad, sensibilidad y grado de relevancia.

### Candidatos

No son fichas publicadas. Necesitan otro flujo: deteccion, triage, score, notas, fuente, estado, motivo de descarte o pase a ficha. Mezclar candidatos con fichas finales vuelve mas confusa la curaduria.

### Recorridos

Son piezas editoriales. Agrupan juegos por fecha, tema, territorio, memoria, tradicion o criterio cultural. Tienen titulo, descripcion, fecha opcional, criterios, destacados curados y relacionados automaticos.

### Listas

Las listas deben funcionar mayormente como filtros automaticos con criterio claro. Sirven para dar vistas rapidas del catalogo: juegos verificados, candidatos, escenario argentino, protagonistas argentinos, deporte argentino, descartes explicados. No deberian mantenerse juego por juego salvo casos curatoriales especiales como recomendados.

### Home editorial

La home necesita una programacion simple: que mostrar hoy, que recorrido destacar, que recomendar para empezar y que hacer cuando no hay efemeride. No deberia caer siempre en Independencia como fallback permanente.

### Taxonomias y calidad

Provincias, regiones, ejes culturales, generos, tipos de obra, grados de relevancia y estados editoriales deben estar controlados. Tambien hacen falta reportes de calidad para detectar huecos, inconsistencias y oportunidades de mejora.

## Release 1: Orden y calidad editorial

Objetivo: mejorar la claridad del sitio sin cambiar todavia la arquitectura de datos.

### Alcance

- Pulir descripciones repetidas, genericas o demasiado automaticas.
- Revisar textos de listas, recorridos y carpetas para evitar que repitan una sola categoria en la descripcion.
- Mejorar fichas centrales con una explicacion mas clara del vinculo argentino.
- Detectar fichas con descripcion corta, vaga o duplicada.
- Revisar juegos de referencia menor para que no compitan editorialmente con obras centrales.
- Crear un primer reporte de calidad de datos.

### Reportes utiles

- Juegos sin portada.
- Juegos sin capturas.
- Juegos sin anio.
- Juegos sin link jugable.
- Juegos sin provincia.
- Juegos con descripcion muy corta.
- Juegos con descripcion similar a otra ficha.
- Distribucion por provincia.
- Distribucion por eje cultural.
- Distribucion entre central, importante y menor.

### Resultado esperado

Un catalogo mas legible y confiable, con menos ruido editorial y mejores seniales para decidir que pulir despues.

## Release 2: Administracion basica de fichas

Objetivo: facilitar el alta y edicion de juegos sin obligar a escribir estructuras largas a mano.

### Alcance

- Crear un generador de ficha desde CLI.
- Agregar plantillas por tipo de ficha.
- Mejorar validaciones con mensajes editoriales claros.
- Separar mental y operativamente fichas publicadas de candidatos.
- Documentar el flujo: candidato -> triage -> ficha -> validacion -> publicacion.

### Plantillas sugeridas

- Juego argentino central.
- Escenario argentino.
- Protagonista argentino.
- Deporte argentino.
- Referencia menor.
- Educativo.
- Mod.
- Abandonware.
- Candidato sin verificar.

### Campos importantes para editar

- Datos basicos.
- Vinculo argentino.
- Contexto argentino.
- Enlaces y fuentes.
- Imagenes.
- Provincias y regiones.
- Ejes culturales.
- Disponibilidad.
- Grado de relevancia.
- Sensibilidad.
- Estado editorial.

### Resultado esperado

Agregar juegos nuevos deberia ser mas facil, mas consistente y menos propenso a errores de formato.

## Release 3: Recorridos como curaduria editorial

Objetivo: tratar los recorridos como una capa editorial propia, no solo como una lista de IDs.

### Alcance

- Revisar recorridos existentes con juegos ya cargados.
- Agregar descripcion editorial mas fuerte.
- Definir criterios de inclusion por recorrido.
- Separar destacados curados de relacionados automaticos.
- Evitar recorridos sobrecargados.
- Permitir fechas exactas y ventanas temporales.
- Pensar recorridos permanentes, efemerides, campanias y recorridos territoriales.

### Modelo editorial deseable

Cada recorrido deberia poder responder:

1. Que tema, fecha o territorio propone?
2. Por que estos juegos pertenecen al recorrido?
3. Cuales son los destacados curados?
4. Que juegos relacionados se pueden completar automaticamente?

### Recorridos a fortalecer

- Malvinas y memoria.
- Folclore, monstruos y leyendas.
- Politica, crisis y satira.
- Gauchos, frontera y siglo XIX.
- Patagonia jugable.
- Buenos Aires como escenario.
- Juegos hechos en provincias.
- Videojuegos educativos argentinos.
- Argentina en juegos internacionales.
- Juegos argentinos disponibles hoy.

### Resultado esperado

Los recorridos deberian convertirse en una de las principales puertas de entrada al sitio: mas narrativos, compartibles y utiles para descubrir juegos.

## Release 4: Listas automaticas y vistas rapidas

Objetivo: ordenar las listas como vistas automaticas del catalogo, con criterios transparentes.

### Alcance

- Mantener las listas como filtros automaticos cuando sea posible.
- Administrar titulo, descripcion, criterio, orden y visibilidad.
- Evitar listas manuales salvo selecciones curatoriales especiales.
- Explicar el criterio de cada lista en lenguaje claro.
- Revisar que cada lista sea una puerta de entrada util y no una repeticion del catalogo.

### Listas automaticas utiles

- Juegos verificados.
- Candidatos rastreados.
- Con escenario argentino.
- Con protagonistas argentinos.
- Con deporte argentino.
- Descartes explicados.
- Juegos disponibles para jugar hoy.
- Juegos por provincia.
- Juegos por eje cultural.
- Referencias menores.

### Criterio

Las listas no deberian competir con los recorridos. Una lista responde "mostrame todos los juegos que cumplen esta condicion". Un recorrido responde "guiame por un tema con una mirada editorial".

### Resultado esperado

Vistas rapidas mas claras, utiles para exploracion, investigacion y mantenimiento del catalogo.

## Release 5: Home editorial

Objetivo: hacer que "Hoy en Jugar Argentina" sea una decision editorial flexible y no un fallback fijo.

### Problema actual

Cuando no hay efemeride exacta, la home puede caer siempre en el recorrido de Independencia. Eso no representa necesariamente el momento del sitio ni ayuda a mostrar variedad.

### Prioridad sugerida

1. Efemeride exacta.
2. Ventana temporal alrededor de una efemeride.
3. Campania manual activa.
4. Recorrido rotativo o estacional.
5. Fallback a recomendados.

### Slots de home a administrar

- Hoy en Jugar Argentina.
- Para empezar a jugar.
- Recorrido destacado.
- Provincia o region destacada.
- Nuevas incorporaciones.
- Juegos disponibles hoy.

### Resultado esperado

Una home mas viva y mas coherente, capaz de destacar fechas, recorridos, provincias o campanias sin depender de un unico fallback.

## Release 6: Federalizacion y nuevas fuentes

Objetivo: ampliar el catalogo fuera del eje Buenos Aires/CABA/conurbano y no depender solo de Steam.

### Federalizacion

- Crear reporte de cobertura por provincia.
- Detectar provincias sin juegos o con pocas fichas.
- Hacer micro-batches provinciales de 3 a 8 fichas.
- Priorizar regiones subrepresentadas.

### Lineas territoriales

- Patagonia: Neuquen, Rio Negro, Chubut, Santa Cruz, Tierra del Fuego.
- NOA: Salta, Jujuy, Tucuman, Catamarca, Santiago del Estero.
- Cuyo: Mendoza, San Juan, San Luis.
- NEA: Misiones, Corrientes, Chaco, Formosa.
- Centro y Litoral: Cordoba, Santa Fe, Entre Rios, La Pampa.

### Fuentes a incorporar

- itch.io.
- Game Jolt.
- Google Play.
- App Store.
- Archive.org.
- GitHub.
- Universidades.
- Museos y proyectos educativos.
- Prensa local.
- ADVA, Indie Hoy, Press Over, Malditos Nerds.
- Game jams argentinas y latinoamericanas.

### Resultado esperado

Un catalogo mas federal, diverso y menos condicionado por los juegos que aparecen en Steam.

## Release 7: Administracion avanzada

Objetivo: hacer que el sitio sea mas facil de mantener a largo plazo.

### Alcance

- Separar `data/games.json` en archivos individuales por juego.
- Mantener `data/games.json` como salida compilada para el sitio.
- Crear un script que compile fichas individuales hacia el JSON final.
- Evaluar un mini admin local para editar fichas sin tocar JSON a mano.
- Agregar previsualizacion de portada, validacion de campos y busqueda de fichas.

### Estructura deseable

```text
data/
  games/
    atuel-2022.json
    malvinas-2032.json
    ethereal.json

src/content/
  recorridos/
    independencia.json
    malvinas.json
    folclore-terror.json

  listas/
    escenario-argentino.json
    recomendados.json

  home.json
```

### Resultado esperado

Una base mas modular, facil de revisar, compatible con aportes externos y preparada para una interfaz de administracion local.

## Backlog comunitario

Objetivo: abrir el proyecto a sugerencias y correcciones sin perder criterio editorial.

### Ideas

- Mejorar la pagina "Sugerir juego".
- Conectar sugerencias con GitHub Issues o formulario externo.
- Publicar criterios de inclusion y exclusion.
- Crear una lista de juegos "en investigacion".
- Acreditar colaboradores.
- Permitir reportar errores en fichas existentes.

## Norte editorial

Jugar Argentina deberia crecer como una base cultural curada, no solo como un listado de juegos.

Cada ficha deberia responder tres preguntas:

1. Cual es el vinculo con Argentina?
2. Que evidencia sostiene ese vinculo?
3. Por que vale la pena conservar o destacar esta obra?

Cada recorrido deberia responder:

1. Que lectura propone sobre el catalogo?
2. Que juegos son destacados curatoriales?
3. Que juegos se suman automaticamente por afinidad?

Cada lista deberia responder:

1. Que criterio automatico aplica?
2. Para que le sirve a quien explora el sitio?
3. Como ayuda a entender mejor el catalogo?
