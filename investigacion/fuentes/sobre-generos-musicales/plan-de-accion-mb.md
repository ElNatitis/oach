# Plan de Acción para el Programa de Consulta de Canciones por Género

## Objetivo general 

Desarrollar un programa en Python que permita obtener una lista de canciones (grabaciones individuales) clasificadas dentro de un género musical determinado (por ejemplo, "salsa") y filtradas por un rango de años, utilizando la API pública de MusicBrainz.

## Metodología

### Paso 1: Buscar `release-groups` etiquetados con el género deseado
- Endpoint: `/ws/2/release-group`
- Método: búsqueda por `tag:{género}`
- Formato de respuesta: JSON (`?fmt=json`)
- Campos útiles: `title`, `first-release-date`, `id`
- Lógica: se realiza una búsqueda por etiquetas (tags) con el nombre del género.
- Resultado esperado: lista de álbumes o compilaciones relacionados con el género.

### Paso 2: Filtrar los `release-groups` por el intervalo de años requerido
- Validar que `first-release-date` esté definido.
- Comparar el año contra los valores mínimos y máximos definidos.
- Conservar solo aquellos `release-groups` que estén dentro del rango.

### Paso 3: Obtener los `releases` de cada `release-group` seleccionado
- Endpoint: `/ws/2/release-group/{mbid}?inc=releases`
- Cada `release-group` puede tener múltiples ediciones (CD, digital, etc.).
- Guardar los `mbid` de cada `release` para el siguiente paso.

### Paso 4: Obtener las `recordings` (canciones) de cada `release`
- Endpoint: `/ws/2/release/{mbid}?inc=recordings`
- Extraer de cada `media > tracks`:
  - `title` (nombre de la canción)
  - `length` (duración en milisegundos, si está disponible)
  - `position` (número de pista)

### Paso 5: Armar una tabla con la información consolidada
- Crear una estructura tipo DataFrame con columnas como:
  - `Título`, `Álbum`, `Año`, `Duración (min:seg)`, `Track #`
- Ordenar por año y pista.
- Exportar a CSV o visualizar como tabla.

## Consideraciones Técnicas
- Añadir `User-Agent personalizado obligatorio.
- Respetar el límite de 1 solicitud por segundo.
- Manejar errores y solicitudes vacías.
- Posibilidad de paginación en las búsquedas (`param offset`).
