# Nota Técnica sobre Integración de Datos

## Principales dificultades encontradas
- La búsqueda de datasets por tema es poco intuitiva y los filtros son limitados.
- Algunos conjuntos de datos no tienen documentación clara sobre sus variables ni diccionario de datos.
- La descarga de archivos grandes resultó lenta y en algunos casos los formatos no eran compatibles directamente con Python sin preprocesamiento.
- Aparte hay bastantes datos que causan granulación, hay espacios como "otros", "otras", "otras circunstancias" donde en muchos casos, hay mas datos registrados fuera de una categoría que datos bien registrados, eso ocasiona que en las graficas haya bastante disparidad entre datos reales y la comparación sea bastante dificil.

## Aspectos que considera que pueden mejorar en el portal
- Mayor documentación técnica (diccionario de datos, metadatos completos) por dataset.
- Buscador más potente con filtros por fecha, formato y entidad.
- Estandarización de formatos de fechas entre datasets de distintas entidades.
- API de descarga más estable.

## Elementos que facilitaron el uso del portal
- La disponibilidad de archivos en formato CSV facilitó la carga directa en Python.
- La documentación de algunos datasets incluía descripciones de variables.
- El buscador por palabras clave permitió encontrar rápidamente datasets relevantes.

## Observaciones del ejercicio

### ¿Cuál ha sido el principal reto técnico o metodológico hasta el momento?
Integrar las dos fuentes de datos (mortalidad vial y precipitación) a una escala temporal y territorial compatible: la base de mortalidad está a nivel de localidad y fecha exacta, mientras que los datos de lluvia del IDEAM están por estación (puntos geográficos), lo que requirió asignar a cada localidad la estación más cercana y agregar mensualmente para hacer el cruce. 

### ¿Qué consideran que les hace falta para desarrollar mejor su análisis?
- Diccionario de datos oficial para la base de mortalidad vial.
- Datos de lluvia ya procesados a nivel de localidad (en lugar de por estación).
- Mayor tiempo para el análisis exploratorio previo a la construcción del modelo y la facilidad de hallar mas datos en cuanto a lluvias en Bogotá, pues puede que haya una pagina oficial, pero solo permite descargar los datos 1 a 1 según el mes.

### Comentarios adicionales sobre el DataJam o el uso de datos abiertos
El DataJam es una experiencia muy valiosa para comprender los retos reales del análisis de datos públicos. Recomendamos que en ediciones futuras se comparta un catálogo de datasets mas limpios y amplios, pues hay muchos archivos con lo que no se pueden trabajar como los comparendos en Bogotá y hay muchos datos que causan granulación el limpiar estos datos, permitiría que los equipos dediquen más tiempo al análisis y menos a la limpieza y concordancia de fuentes.
