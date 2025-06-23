/* MODULO 2 - SEGMENTAR LA SERIE INTEGRADA

Se recibe un 'instrumento_int' que es un dato con la siguiente estructura

instrumento_int = { [t_int₁,...,t_intₙ], [v_int₁,...,v_intₙ], [d_int₁,...,d_intₙ] }

y se realizan los siguientes procedimientos sobre cada una de las series que componen el instrumento

1 - se calcula, con resdpecto al tamaño de segmento, el número de segmetnos posibles 
2 - se crea una variable 'seg_instrumento_int' que tiene la estructura de instrumento_int pero sus arreglos están segmentados
3 - guardamos los datos correspondientes en cada espacio de los segmentos
4 - regresamos la variable 'seg_instrumento_int'

El programa regresa la serie segmentada con el formato

instrumento_int = { [(d1,...,ds)₁,...,()], [(),...,()ₙ], [()₁,...,(d_int)ₙ] }
*/ 

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "instrumento.h"


struct instrumento segmentar_instrumento(struct instrumento* inst, int s)
{
  // decalramos el arreglo que vamos a regresar
  struct instrumento seg_x_int;
  declarar_instrumento_segmentado(&seg_x_int,s);

  imprimir_instrumento(seg_x_int); 

}
