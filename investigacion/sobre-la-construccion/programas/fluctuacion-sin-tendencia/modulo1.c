/* MODULO 1 - INTEGRAR LA SERIE

Se recibe una serie de tiempo con el formato

serie = { [s₁,...,sₙ] }

donde serie puede corresponder a: tono, volumen o duración

y se realizan los siguientes procedimientos sobre cada una de las series

1 - Se calcula el promedio 
2 - "integramos" la serie
3 - regresamos la serie integrada en un arreglo diferente

El programa regresa la serie integrada con el formato

serie_int = { [s_int₁,...,s_intₙ] }

*/ 

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

float* integrar_x(float* x, int N)
{
  float* x_int = calloc(N, sizeof(float)); // Arreglo que devolveremos
  
  // 1 - Se calcula el promedio 
  float sum = 0;
  for(int i=0;i<N;i++) sum += x[i];
  float prom = (sum/N); 
  
  // 2 - "integramos" la serie
  for(int j=0;j<N;j++)  
  {
    sum=0; // reiniciamos la variable
    for(int i=0;i<=j;i++) sum += x[i]-prom;      
    x_int[j]=sum;
  }
  
  // 3 - regresamos la serie integrada en un arreglo diferente
  return x_int;
}
