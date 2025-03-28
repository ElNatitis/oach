# Universalidad de las distribuciones de ordenamiento jerárquico en las artes y las ciencias

## Resumen

Buscar comportamientos genéricos ha sido una de las fuerzas impulsoras para entender y clasificar diversos fenómenos. 

Usualmente **se comienza desarrollando una fenomenología basada en observaciones.** Tal es el caso de las *distribuciones tipo ley de potencias* que se encuentran en una gran variedad de situaciones provenientes de la física, geofísica, biología, lexicografía, así como en redes sociales y financieras. 

Sin embargo, este hallazgo suele estar restringido a un rango de valores, fuera del cual se invocan correcciones por tamaño finito. 

Aquí revelamos **un comportamiento universal en la forma en que los elementos de un sistema se distribuyen según su rango respecto a una propiedad dada**, válido en todo el rango de valores, _independientemente de si se ha sugerido previamente una ley de potencias._ 

### Proponemos 

**Una forma funcional de dos parámetros** para estas _distribuciones ordenadas por rango_, que ofrece ajustes excelentes para una cantidad impresionante de fenómenos muy diversos, provenientes de las artes, las ciencias sociales y naturales

 Es una versión discreta de una distribución beta generalizada, dada por:
 
 f(r) = A * [(N-1-r)^b / r^a ]
 
 donde:
 - **r** es el rango
 - **N** su valor máximo 
 - **A** una constante de normalización 
 - **a** y **b** son dos exponentes de ajuste.
 
Motivados por nuestras observaciones en secuencias genéticas, presentamos un **modelo probabilístico de crecimiento** que _incorpora características de mutación y duplicación_, y que _genera datos que se ajustan a esta distribución._ 

La competencia entre permanencia y cambio parece ser una característica relevante, aunque no necesaria. 

Además, nuestras observaciones —principalmente de fenómenos sociales— sugieren que una cualidad multifactorial, resultante de la convergencia de varios procesos subyacentes heterogéneos, es una característica importante. 

También exploramos el significado de los parámetros de la distribución y su potencial para clasificar. La ubicuidad de nuestros hallazgos sugiere que debe haber una explicación fundamental subyacente, muy probablemente de naturaleza estadística, como una formulación apropiada del teorema del límite central.

## Introducción

Durante la última década, una gran cantidad de investigaciones se han dedicado a los _comportamientos tipo ley de potencias_, especialmente en lo que respecta a redes complejas. Sin embargo, cuando se analizan datos reales, en la mayoría de los casos, **la tendencia tipo ley de potencias sólo se mantiene para un rango intermedio de valores; hay una ruptura en la cola de la distribución.** Tanto el punto de ruptura como las formas funcionales en las colas son de interés. 

Se han propuesto varias explicaciones para este fenómeno, como efectos de tamaño finito (por ejemplo, datos insuficientes para una buena estadística), dilución de redes, restricciones de crecimiento en redes, y diferentes regímenes dinámicos subyacentes, que conducen a correcciones de la ley de potencias (a veces llamadas correcciones de escalamiento) en forma de distribuciones exponenciales, gaussianas, exponenciales estiradas, gamma y varios tipos de distribuciones de valor extremo.

En este trabajo **nos centramos en distribuciones ordenadas por rango,** a menudo relacionadas con _funciones de distribución acumulada_: muestran cómo una propiedad dada de un sistema se ordena decrecientemente según su importancia (rango). 

### Nuestro resultado principal 

Una sorprendente cantidad de situaciones siguen una distribución de dos parámetros que incorpora el producto de dos leyes de potencias definidas sobre el conjunto completo de datos, una medida de "izquierda a derecha" y otra de "derecha a izquierda". 

El ajuste se mantiene en todo el rango de valores, incluidas las colas, con correlaciones que rivalizan o generalmente mejoran respecto a los esquemas de corrección de ley de potencias propuestos en la literatura.

En nuestro trabajo se revela una **universalidad funcional para las distribuciones ordenadas por rango**, que abarca _fenómenos aparentemente no relacionados_ provenientes de la música, la pintura, la ecología, el urbanismo, la neurociencia, la genética y las redes sociales, entre otros. 

Desarrollamos una **fenomenología** basada en una _selección de la gran cantidad de casos donde hemos encontrado esta forma funcional._ 

Motivados por algunas de estas observaciones, implementamos un modelo de dinámica en conflicto que genera esta distribución y contribuye a identificar características subyacentes relevantes de los procesos que conducen a ella, así como a una caracterización de sus parámetros. 

En nuestra exploración también detectamos que la convergencia de múltiples procesos heterogéneos parece ser un factor importante. En general, nuestros hallazgos sugieren que debe haber una explicación profunda subyacente, posiblemente de naturaleza estadística.

## Femnomenología


