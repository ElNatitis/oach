# Comportamiento de escala múltiple y rasgos no lineales en partituras musicales.

## Resumen

Presentamos un **análisis estadístico de partituras musicales de diferentes compositores** utilizando el _análisis de fluctuaciones sin tendencia (Detrended Fluctuation Analysis, DFA)._ 

Encontramos:
- distintos **perfiles de fluctuación** que corresponden a **estructuras de autocorrelación** específicas en las piezas musicales. 
- evidencia de la presencia de **autocorrelaciones no lineales** al _estimar el DFA de la serie de magnitudes_, resultado que fue validado mediante un estudio correspondiente con datos sustitutos apropiados. _(La cantidad y el tipo de correlaciones no lineales varían entre compositores.)_

Finalmente, realizamos:
- un experimento simple para evaluar _la agradabilidad de piezas musicales sustitutas en comparación con la música original_

encontramos que las **correlaciones no lineales** podrían desempeñar un papel importante en la _percepción estética de una pieza musical._


## Introducción

La música es una construcción compleja que involucra factores culturales, características acústicas, técnicas de interpretación y percepción del público. 

### El estudio de la música desde la perspectiva de la física estadística

Uno de los trabajos pioneros en este contexto, utilizando técnicas de física estadística, fue publicado por **Voss y Clarke** [1]. Estimaron _la densidad espectral de las fluctuaciones de intensidad_ y encontraron un comportamiento de _ley de potencia_ cercano al _ruido 1/f._ 

Este resultado inspiró a muchos investigadores a estudiar las **propiedades estadísticas de la música** coion enfoques como:
- la identificación de **patrones temporales** o _leyes de potencia_
- el desarrollo de algoritmos para la composición musical [2–11].

Entre estos estudios se incluyen:
- la identificación de tonalidades mayores y menores en el Clave bien temperado de Bach mediante una parametrización estadística [6]
- el papel del ruido correlacionado en la "humanización" de melodías generadas por computadora [8]
- el análisis de la interacción entre voces en las invenciones a tres voces de Bach [10].

##### Sobre las leyes de potencia o de escalamiento

Son manifestaciones de autosimilitud en el mundo que nos rodea [12–15].

En música, los espectros 1/f^β con β = 1 se han interpretado en [9,16] como un _equilibrio entre previsibilidad y sorpresa_ 

- Si β tiende a valores bajos (siendo cero el caso de ruido blanco), la secuencia temporal de notas es altamente no correlacionada y suena _desagradable._ 
- Si β es muy alto, la música se vuelve monótona. 

Se han encontrado con frecuencia comportamientos de escalamiento, en particular con 1 < β < 2, en la música [2,4,5,9–11]. Sin embargo, pocos estudios se han enfocado en partituras musicales [4,10,16], y hasta donde sabemos, ninguno ha presentado un análisis detallado del comportamiento de escalamiento en las fluctuaciones de tono (pitch) en piezas de distintos compositores.

### En este trabajo 

Nos enfocamos en partituras musicales, interpretándolas como series de tiempo multivariadas a las que aplicamos diferentes tipos de análisis de fluctuaciones. 

- Proporcionamos una interpretación coherente de los perfiles de fluctuación, que son marcadamente distintos entre compositores. 

- La estructura de las piezas musicales se refleja en parte en su autocorrelación, lo que proporciona elementos para caracterizar el proceso de composición. 

- Tratamos de detectar y clasificar diferentes perfiles de autocorrelación en piezas musicales provenientes de distintos períodos de tiempo. Esta caracterización podría contribuir al desarrollo de modelos de composición. Además, 

- Buscamos la presencia de características no lineales, que podrían estar presentes en diferentes escalas temporales. 

- Finalmente, presentamos un primer intento de evaluar si tales características no lineales influyen en la percepción _estética de la música._


