# Lo que dice el artículo de Comportamiento de escala múltiple en parituras

## Construcción de las series temporales

Consideramos las partituras musicales como una secuencia de números enteros, cada uno de los cuales representa una nota distinta. 

Los números fueron extraídos de archivos MIDI obtenidos de diferentes bases de datos en línea [17,18]. Procesamos los archivos MIDI utilizando **midicsv** [19], un software gratuito que _convierte archivos MIDI en archivos CSV_ (valores separados por comas).

# Investigaciones al respecto

El objetivo general de este proyecto es identificar y caracterizar propiedades estadísticas distintivas en el comportamiento del **volumen**, los **tonos (pitch)** y el **ritmo** de canciones pertenecientes a géneros musicales específicos. El propósito final es encontrar patrones cuantificables que puedan contribuir a responder, desde el análisis estadístico, la pregunta: “¿Qué hace que una canción pertenezca a un determinado género?”

## Justificación del enfoque

Los archivos de audio convencionales (como MP3 o WAV) codifican la información sonora en forma de señales continuas, dificultando la extracción directa de información estructural sobre los eventos musicales. En cambio, los archivos **MIDI** almacenan la información musical de manera simbólica, proporcionando datos detallados sobre:

- La nota que se toca (pitch)
- El momento en que comienza (onset)
- Su duración
- El instrumento que la ejecuta
- Su intensidad (velocity, relacionada con volumen)

Esto permite interpretar una pieza musical como una **serie temporal multivariada**, donde cada canal puede representar una voz o instrumento diferente, y cada dimensión de análisis puede enfocarse en una característica musical específica.

### Metodología general

#### Obtención de datos

La primera etapa consiste en construir un corpus de canciones en formato **MIDI** correspondientes a uno o varios géneros musicales (por ejemplo, salsa, jazz, rock, etc.). Este corpus debe ser lo suficientemente representativo para permitir inferencias significativas. Idealmente se busca obtener entre **30 y 50 canciones por género**.

#### Conversión a series temporales

Para cada archivo MIDI:

1. Se convierte a formato **CSV** mediante herramientas como `midicsv`, o se analiza directamente con bibliotecas como `pretty_midi` o `music21` en Python.
2. Se extraen y construyen las siguientes **series temporales multivariadas**:
   - **Pitch**: secuencia de notas en cada canal (voz o instrumento)
   - **Ritmo**: tiempo entre eventos (intervalos entre onsets)
   - **Volumen**: valores de `velocity` como proxy de intensidad sonora

#### Análisis de fluctuaciones sin tendencia (DFA)

Una vez construidas las series temporales, se les aplica el método **Detrended Fluctuation Analysis (DFA)** para estudiar las **autocorrelaciones** presentes a diferentes escalas temporales:

- Este análisis permite detectar **autosimilitud** en las variaciones musicales.
- Se calcula el **exponente de Hurst α**, que indica si hay persistencia, aleatoriedad o alternancia en la estructura temporal.
- En caso de series multivariadas, se emplea **n-DFA** para analizar simultáneamente las voces o instrumentos.

#### Generación de perfiles por género

Se repite el análisis DFA para cada canción del corpus y se construyen **perfiles estadísticos promedio por género**. Estos perfiles pueden incluir:

- Distribución de exponente α para pitch, ritmo y volumen
- Comparación entre autocorrelaciones a corto y largo plazo (cruces entre escalas)
- Presencia o ausencia de no linealidades (con MDFA)

## Siguientes pasos

- Recolección de datos MIDI confiables por género
- Construcción de scripts de procesamiento de datos y extracción de series
- Implementación del algoritmo DFA multivariado
- Visualización y análisis de resultados
- Refinamiento de los perfiles y comparaciones inter-género


