# Conocimientos previos

## Proceso estacionario.
Le llamamos *Proceso estacionario* a una serie de tiempo cuyas **propiedades estadísticas** (media, varianza y autocorrelación) se mantienen constantes en el tiempo.

## Proceso estocástico.
Un proceso estocástico es aquel en el que los valores futuros dependen de alguna forma de los valores pasados, pero con un componente de _aleatoriedad_ que introduce _incertidumbre._

## Ruido blanco
Una serie de tiempo que cumple con las siguientes propiedades 
- **Media cero:** En promedio, los valores no tienden a aumentar ni disminuir con el tiempo.
- **Varianza constante:** La dispersión de los valores del ruido es la misma en cualquier instante.
- **Independencia temporal:** No hay relación entre los valores de la serie en distintos tiempos. _Esto se intepreta como que no tiene memoria_

## Caminata aleatoria
Un tipo de proceso estocástico no estacionario, donde cada valor en el tiempo se obtiene sumando al valor anterior a un término aleatorio (ruido blanco)

# Procesos autoregresivos

## Introducción

Los modelos de procesos estacionarios representan la dependencia de los valores de una serie temporal con su propio pasado. 

Un tipo básico de estos modelos es el **Modelo autorregresivo (AR)**, que "extiende" el concepto de _regresión_ al ámbito de las series temporales, permitiendo **modelar la relación lineal entre valores pasados y presentes.**

Las series temporales, en general, presentan una cierta inercia, lo que significa que sus valores actuales dependen en cierta medida de valores previos. Para cuantificar esta dependencia, se utilizan dos herramientas clave:

- **Función de autocovarianza:** mide la relación entre valores de la serie en distintos momentos del tiempo.
- **Función de autocorrelación:** normaliza la autocovarianza para expresar la relación en términos de correlación, facilitando su interpretación.

Ambas funciones "extienden" los conceptos clásicos de _covarianza_ y _correlación_, pero en lugar de aplicarse entre dos variables diferentes, las utilizan para analizar la relación de una misma serie a lo largo del tiempo. 

## Proceso autoregresivo de primer orden AR(1)
Diremos que una serie z_t sigue un proceso autorregresivo de primer orden, o un **AR(1)**, si ha sido generada por:

z_t = c + φ z_{t-1} + a_t

donde c y -1 < φ < 1 son constantes a determinar, y a_t es un proceso de **ruido blanco** con varianza σ².

Las variables a_t, que representan _la nueva información que se añade al proceso en cada instante_, se conocen como **innovaciones**.

### Observación
Se puede demostrar que la condición -1 < φ < 1 es necesaria para que el proceso sea estacionario.

## Proceso autoregresivo de segundo orden

## Proceso autoregresivo general

## Función de autocorrelación parcial



