# Conocimientos previos

## Autocovarianza
La autocovarianza en el rezago _k_ mide la **relación lineal** entre z(t) y z(t−_k_)
Esta depende de la escala de los datos, por lo que no es fácil interpretarla directamente.

## Autocorrelación
Para obtener un valor más _intuitivo y comparable_, **normalizamos la autocovarianza** dividiéndola entre la varianza de la serie. Esto hace que el valor de autocorrelación siempre esté entre 0 y 1 y se interprete de la siguiente manera:
- **Si es cercano a 1** entonces z(t) y z(t−_k_) están _FUERTEMENTE_ correlacionados
- **Si es cercano a 0** entonces z(t) y z(t−_k_) _NO_ tienen relación aparente
- **Si es negativo** entonces z(t) y z(t−_k_) están _INVERSAMENTE_ relacionados


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

Los **modelos de procesos estacionarios** representan _la dependencia de los valores de una serie temporal con su propio pasado._ 

Un tipo básico de estos **modelos de procesos estacionarios** es el **Modelo autorregresivo (AR)**, que "extiende" el concepto de _regresión_ al ámbito de las series temporales, permitiendo **modelar la relación lineal entre valores pasados y presentes.**

Las series temporales, en general, presentan que _sus valores actuales dependen en cierta medida de valores previos._ (No me encanta este parafraseo pero es lo que hay)

Para cuantificar esta dependencia, se utilizan dos herramientas clave:

- **1. Función de autocovarianza:** mide la relación entre valores de la serie en distintos momentos del tiempo.
- **2. Función de autocorrelación:** normaliza la autocovarianza para expresar la relación en términos de correlación, facilitando su interpretación.

Ambas funciones "extienden" los conceptos clásicos de _covarianza_ y _correlación_, pero en lugar de aplicarse entre dos variables diferentes, las utilizan para analizar la relación de una misma serie a lo largo del tiempo. 

## Proceso autoregresivo de primer orden AR(1)
Diremos que una serie z_t sigue un **proceso autorregresivo de primer orden**, o un **AR(1)**, si ha sido generada por:

z_t = c + φ z_{t-1} + a_t

donde:
- **c** es una constante a determinar 
- **-1 < φ < 1** es el coeficiente que determina la influencia de los valores pasados en el valor presente 
- **a_t** es un proceso de _ruido blanco_ con varianza σ².

Las variables **a_t**, representan _la nueva información que se añade al proceso en cada instante_, por eso tambien se les llama **innovaciones**.

### Observación
Se puede demostrar que la condición **-1 < φ < 1** es necesaria para que el proceso sea estacionario.

## Proceso autoregresivo de segundo orden AR(2)
El proceso AR(1) modela la dependencia de un valor presente con su valor inmediatamente anterior. 

Esta idea puede "extenderse" permitiendo que también dependa de un valor aún más antiguo, introduciendo así el **proceso autorregresivo de segundo orden**, o **AR(2)**.

Diremos que una serie z_t sigue un **proceso autorregresivo de segundo orden**, o un **AR(2)**, si ha sido generada por:

z_t = c + φ_1 z_{t-1} + φ_2 z_{t-2} + a_t

Donde:
- **c** es una constante a determinar
- **φ_1 y φ_2** son los coeficientes que determinan la inluencia de los valores pasados en el valor presente
- **a_t** es un proceso de _ruido blanco_ con varianza σ².

## Proceso autoregresivo general AR(p)

### Ecuación característica


## Función de autocorrelación parcial
Determinar el orden de un proceso autorregresivo a partir de su **función de autocorrelación simple** es difícil.

Sobre estas funciones, en general sabemos
- Son una mezcla de decrecimientos exponenciales y sinusoidales
- Se amortigua al avanzar el retardo
- No presenta rasgos identificables para determinar el orden

Atendiendo a esta problemática se introduce la **Función de autocorrelación parcial.**





