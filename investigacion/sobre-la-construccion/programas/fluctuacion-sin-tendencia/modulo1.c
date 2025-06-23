/* MODULO 1 - INTEGRAR LA SERIE

Se recibe un 'instrumento' que es un dato con la siguiente estructura

instrumento = { [t₁,...,tₙ], [v₁,...,vₙ], [d₁,...,dₙ] }

y se realizan los siguientes procedimientos sobre cada una de las series que componen el instrumento

1 - Se calcula el promedio 
2 - "integramos" la serie
3 - regresamos la serie integrada en un arreglo diferente

El programa regresa la serie integrada con el formato

instrumento_int = { [t_int₁,...,t_intₙ], [v_int₁,...,v_intₙ], [d_int₁,...,d_intₙ] }

todo lo anterior sucede usando la funcion declarada en instrumento.h llamada 'integrar_instrumento'

*/ 

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "instrumento.h"


struct instrumento integrar_instrumento(struct instrumento* inst)
{
  // decalramos el arreglo que vamos a regresar
  struct instrumento x_int;
  declarar_instrumento(&x_int);
  
  // inicializamos las variables para los promedios
  float prom_tono = 0, prom_volumen = 0, prom_duracion = 0;

  // calculamos promedios
  for (int i = 0; i < N; i++) 
  {
      prom_tono += inst->tono[i];
      prom_volumen += inst->volumen[i];
      prom_duracion += inst->duracion[i];
  }
  prom_tono /= N;
  prom_volumen /= N;
  prom_duracion /= N;
  
  
  // "integramos" cada serie del instrumento
  for (int i = 0; i < N; i++) 
  {
      float suma_tono = 0, suma_volumen = 0, suma_duracion = 0;
      for (int j = 0; j <= i; j++) 
      {
          suma_tono += inst->tono[j] - prom_tono;
          suma_volumen += inst->volumen[j] - prom_volumen;
          suma_duracion += inst->duracion[j] - prom_duracion;
      }
      x_int.tono[i] = suma_tono;
      x_int.volumen[i] = suma_volumen;
      x_int.duracion[i] = suma_duracion;
  }
  return x_int;
}




