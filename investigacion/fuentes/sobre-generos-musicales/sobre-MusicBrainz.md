# MusicBrainz
https://musicbrainz.org/

## Acerca de

**MusicBrainz es una enciclopedia de información musical de código abierto mantenida por la comunidad.**
Esto significa que cualquiera puede contribuir al proyecto agregando información sobre sus artistas favoritos y sus obras.

En el año 2000, _Gracenote_ asumió el control del proyecto gratuito CDDB y lo comercializó, cobrando a los usuarios por acceder a los datos que ellos mismos aportaban.

En respuesta, **Robert Kaye** fundó _MusicBrainz_. Desde entonces, el proyecto pasó a ser una comunidad internacional de entusiastas que aprecian tanto la música como sus metadatos. 

Como enciclopedia y comunidad, MusicBrainz existe únicamente para recopilar la mayor cantidad posible de información sobre música. 

## Sobre su manera de entender los generos musicales

Existe una **lista de generos**, la cual se genera y actualiza gracias al _sistema de etiquetas_ en el cual la lista se amplía según las solicitudes de los usuarios. Se puede resumir su postura ante los generos con el siguiente parrafo:

_"Los géneros son subjetivos, por lo que, al igual que con cualquier otra etiqueta, puedes votar a favor o en contra de los géneros con los que estás de acuerdo o en desacuerdo en cualquier entidad determinada, y también puedes enviar géneros para la entidad que nadie haya agregado todavía."_

### Sistema de etiquetas

- Cada editor puede votar a favor o en contra añadiendo una etiqueta a una entidad. 
- Añadir una nueva etiqueta cuenta como voto a favor. 
- El total de votos debe ser positivo para que la etiqueta se muestre.
- No todos los géneros están aún en la **lista de géneros** permitidos , pero puede usar cualquiera como etiqueta y proponer su inclusión. 

### Entidades

Una entidad es un tipo de objeto dentro de su base de datos que representa un elemento específico del mundo musical. Estas entidades están interrelacionadas y permiten estructurar y describir la música de manera detallada. 

- **Artista (Artist)**: Representa a una persona, grupo o entidad que crea música. Por ejemplo, "Shakira" o "Los Fabulosos Cadillacs".
- **Lanzamiento (Release)**: Es una edición específica de una grabación publicada, como un CD, vinilo o lanzamiento digital. Incluye detalles como la fecha de lanzamiento, país, sello discográfico y formato.
MusicBrainz
- **Grupo de Lanzamientos (Release Group)**: Agrupa varios lanzamientos que comparten el mismo contenido musical esencial. Por ejemplo, diferentes ediciones de un mismo álbum en distintos formatos o países.
- **Grabación (Recording)**: Es una instancia específica de una interpretación de una obra musical. Una grabación puede aparecer en múltiples lanzamientos.
- **Obra (Work)**: Representa la composición musical en sí, como la melodía y la letra. Por ejemplo, la obra "Imagine" de John Lennon.
- **Etiqueta (Label)**: Es la compañía discográfica responsable de la producción y distribución de lanzamientos. Por ejemplo, "Sony Music" o "EMI".
- **Área (Area)**: Define una región geográfica, como un país o ciudad, asociada a artistas, lanzamientos o eventos.
- **Instrumento (Instrument)**: Representa instrumentos musicales utilizados en grabaciones o interpretaciones.
- **Género (Genre)**: Clasifica la música según estilos o categorías, como "salsa", "rock" o "jazz".

### Endpoints Principales de la API de MusicBrainz

#### Busqueda `/ws/2/{entidad}?query=...`
Permite buscar **entidades** específicas utilizando consultas basadas en _Lucene_. Las entidades disponibles incluyen:
- `artist` (artista)
- `recording` (grabación)
- `release` (lanzamiento)
- `release-group` (grupo de lanzamientos)
- `work` (obra)
- `label` (sello discográfico)
- `area` (área geográfica)
- `instrument` (instrumento)
- `genre` (género)

**Parámetros comunes**
- `query`: Consulta de búsqueda en formato _Lucene_
- `fmt`: Formato de respuesta (json o xml).
- `limit`: Número máximo de resultados a devolver (hasta 100).
- `offset`: Desplazamiento para paginación.

**Sintaxis de Lucene usada por MusicBrainz**
 __________________________________________________________________________
| Elemento           | Descripción                                         |
| ------------------ | --------------------------------------------------- |
| `field:value`      | Busca en una _Campo_ específico (ej. `artist:TINI`) |
| `AND`, `OR`, `NOT` | Operadores booleanos                                |
| `"palabra exacta"` | Comillas para búsqueda exacta                       |
| `field:[a TO b]`   | Rango (fechas, números, etc.)                       |
| `*`                | Comodín (ej. `artist:"Juan *"`)                     |
| `-`                | Negación (ej. `-tag:rock` para excluir)             |

**Lista de Campos**
- `artist`
- `release`
- `recording`
- `releasegroup`
- `isrc`, `barcode`, `date`
- `tag`, `genre`
- `country`, `status`, `format`
