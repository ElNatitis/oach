/* MODULO  SIMULADO

Se simula una serie correspondiente a un instrumento con el formato

instrumento_i = { [t₁,...,tₙ], [v₁,...,vₙ], [d₁,...,dₙ] }


donde: t = tono, v = volumen y d = duración

y se realizan los siguientes procedimientos sobre cada una de las series

1 - "integramos" las series ejecutando el {modulo1.c} en cada una






El programa termina generando la serie {flucxseg} con el formato

serie_int = { [s₁,Fs₁],...,[sₙ,Fsₙ] }

donde: sₙ  = tamaño de el segmento 
       Fsₙ = fluctuación cuadrática media de ese segmento

*/ 
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>


int main(void)
{
  srand(time(NULL)); // Inicializar la semilla para obtener números aleatorios distintos cada vez
  
  
  int N = 1024; // Número de datos
  float* x = calloc(N, sizeof(float)); // Arreglo
  for(int i=0;i<N;i++) x[i] = rand() % 599;// Llenar el arreglo con números aleatorios del 0 al 599
  
}
