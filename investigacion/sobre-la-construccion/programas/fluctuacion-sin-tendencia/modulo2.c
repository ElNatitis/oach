/* MODULO 2 - SEGMENTAR LA SERIE INTEGRADA

Se recibe un 'instrumento_int' que es un dato con la siguiente estructura

instrumento_int = { [t_int₁,...,t_intₙ], [v_int₁,...,v_intₙ], [d_int₁,...,d_intₙ] }

y se realizan los siguientes procedimientos sobre cada una de las series que componen el instrumento

1 - se calcula, con resdpecto al tamaño de segmento, el número de segmetnos posibles 
2 - se crea una variable 'seg_instrumento_int' que tiene la estructura de instrumento_int pero sus arreglos están segmentados
3 - guardamos los datos correspondientes en cada espacio de los segmentos
4 - regresamos la variable 'seg_instrumento_int'

El programa regresa la serie segmentada con el formato

seg_instrumento_int = { [(d1,...,ds)₁,...,()], [(),...,()ₙ], [()₁,...,(d_int)ₙ] }
*/ 

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "instrumento.h"


struct instrumento segmentar_instrumento(struct instrumento* inst, int s)
{
  int st = ((N-(N%s))/s); // número de segmentos que habrá en el arreglo de segmentos
  
  // decalramos el arreglo que vamos a regresar
  struct instrumento seg_x_int;
  declarar_instrumento_segmentado(&seg_x_int,s,st);
  
  // visitamos cada espacio de cada segmento para almacenar lo que hay en el arreglo original 
  int aux = 0;
  for (int i = 0; i < st; i++) 
  {
    for (int j = 0; j < s; j++) 
    {
      int index = i * s + j;
      seg_x_int.tono[index] = inst->tono[aux];
      seg_x_int.volumen[index] = inst->volumen[aux];
      seg_x_int.duracion[index] = inst->duracion[aux];
      aux++;
    }
  }
  return seg_x_int;
}
