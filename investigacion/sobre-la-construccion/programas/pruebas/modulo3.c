/* NUEVO MODULO 3 - SIMULAR LOS SEGMENTOS DE LA SERIE INTEGRADA

Se recibe un 'seg_instrumento_int' que es un dato con la siguiente estructura

seg_instrumento_int = { [(t_int_1,...,t_int_s)₁,...,()ₙ], [(v_int_1,...,v_int_s)₁,...,()ₙ], [(d_int_1,...,d_int_s)₁,...,()ₙ] }

y se realizan los siguientes procedimientos sobre cada una de los segmentos de las series que componen el instrumento

1 - se calculan los coeficientes de un polinomio de grado 'n' que simulen el segmento mediante minimos cuadrados y la librería 'matrices.h'
2 - se simulan los segmentos a partir de esos coeficientes
3 - guardamos los datos simulados en un arreglo llamado 'sim_seg_instrumento'

El programa regresa la serie segmentada simulada con el mismo formato que el arreglo 'seg_instrumento_int'
*/ 

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "instrumento.h"
#include "matrices.h"

float *coeficientes(float *x_seg, int st, int s, int g);
struct instrumento simular_segmentos(struct instrumento inst, int N, int s, int g);

float *coeficientes(float *x_seg, int st, int s, int g)
{ 
  float* coeff = calloc(st*g, sizeof(float)); // Arreglo donde guardaremos los coeficientes
  int index = 0; // auxiliar para almacenar los coeficientes 
  for(int i=0;i<st;i++)
  {
    float *seg = x_seg+i*s; // para trabajar con el i-ésiumo segmento 
    struct matriz xt = declara_matriz(s,1);
    for(int j=0;j<s;j++) xt.elemento[j] = seg[j];
    struct matriz A = vandermonde(s,g);
    struct matriz AtA = producto(transpuesta(A),A);
    //imprimir_matriz(AtA);
    struct matriz inv_AtA = inversa(AtA);
    struct matriz coef = producto(producto(inv_AtA,transpuesta(A)),xt);
    //imprimir_matriz(coef);
    for(int k=0;k<g;k++) coeff[i*g + k] = coef.elemento[k];
  }
  return coeff; 
}


struct instrumento simular_segmentos(struct instrumento inst, int N, int s, int g)
{
    int st = ((N - (N % s)) / s); // número de segmentos
    struct instrumento simulado;
    simulado.tono = calloc(st * s, sizeof(float));
    simulado.volumen = calloc(st * s, sizeof(float));
    simulado.duracion = calloc(st * s, sizeof(float));

    // Simulación para TONO
    float* coef_tono = coeficientes(inst.tono, st, s, g);
    for(int j=0;j<st;j++)
    {
      for(int i=0;i<s;i++)
      {
        for(int k=0;k<g;k++)
        {
          simulado.tono[j*s+i]+=coef_tono[j*g + k]*pow(i,k);
        }
      }
    }
    

    // Simulación para VOLUMEN
    float* coef_volumen = coeficientes(inst.volumen, st, s, g);
    for(int j=0;j<st;j++)
    {
      for(int i=0;i<s;i++)
      {
        for(int k=0;k<g;k++)
        {
          simulado.volumen[j*s+i]+=coef_volumen[j*g + k]*pow(i,k);
        }
      }
    }

    // Simulación para DURACIÓN
    float* coef_duracion = coeficientes(inst.duracion, st, s, g);
    for(int j=0;j<st;j++)
    {
      for(int i=0;i<s;i++)
      {
        for(int k=0;k<g;k++)
        {
          simulado.duracion[j*s+i]+=coef_duracion[j*g + k]*pow(i,k);
        }
      }
    }

    return simulado;
}

