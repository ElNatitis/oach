/* MODULO 3 - SIMULAR LOS SEGMENTOS DE LA SERIE INTEGRADA

Se recibe un 'seg_instrumento_int' que es un dato con la siguiente estructura

seg_instrumento_int = { [(d1,...,ds)₁,...,()], [(),...,()ₙ], [()₁,...,(d_int)ₙ] }

y se realizan los siguientes procedimientos sobre cada una de los segmentos de las series que componen el instrumento

1 - se calculan los coeficientes de un pol_g2 que se apoxime al comportamiento del segmento aplicando cramer
2 - se simula el comportamiento a partir de esos coeficientes
3 - guardamos los datos simulados en un arreglo llamado 'sim_seg_instrumento'

El programa regresa la serie segmentada simulada con el formato

sim_seg_instrumento = { [(d1,...,ds)₁,...,()], [(),...,()ₙ], [()₁,...,(d_int)ₙ] }
*/ 

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "instrumento.h"

float* coeficientes(float* x_seg, int st, int s);
void llenar_columnas(float* c1, float* c2, float* c3,float* cb, float* y, float* x,int s);
float det(float* c1, float* c2, float* c3);
struct instrumento simular_segmentos(struct instrumento inst, int s);

float* coeficientes(float* x_seg, int st, int s)
{
  float* coef = calloc(st*3, sizeof(float)); // Arreglo donde guardaremos los coeficientes
  for(int i=0;i<st;i++)
  {
    float* seg = x_seg+i*s; // para trabajar con el i-ésiumo segmento 
    float* ind = calloc(s, sizeof(int)); // Arreglo índice
    for(int i=0;i<(s);i++) ind[i] = i; // Llenar el indice 
    
    // Los arreglos que cumplirán la función de columnas
    float* c1 = calloc(3, sizeof(float));
    float* c2 = calloc(3, sizeof(float)); 
    float* c3 = calloc(3, sizeof(float));
    float* cb = calloc(3, sizeof(float)); 
    
    llenar_columnas(c1,c2,c3,cb,seg,ind,s);
    
    // Determinantes de las matrices que formamos con las columnas
    float dete, det0, det1, det2;
    dete = det(c1,c2,c3);
    det0 = det(cb,c2,c3);
    det1 = det(c1,cb,c3);
    det2 = det(c1,c2,cb);
    
    // Coeficientes que determinan el polinomio de grado 2
    float a0,a1,a2;
    a0 = det0 / dete;
    a1 = det1 / dete;
    a2 = det2 / dete;
    
    coef[3*i+0] = a0; 
    coef[3*i+1] = a1; 
    coef[3*i+2] = a2; 
  }
  return coef; 
}

void llenar_columnas(float* c1, float* c2, float* c3,float* cb, float* y, float* x,int s)
{
  float sum_x = 0, sum_x2 = 0, sum_x3 = 0, sum_x4 = 0;
  float sum_y = 0, sum_xy = 0, sum_x2y = 0;
  // Para calcular todas las sumas que vamos a necesitar para las matrices
  for (int i=0; i<s; i++) 
  {
    sum_x  += x[i];
    sum_x2 += x[i]*x[i];
    sum_x3 += x[i]*x[i]*x[i];
    sum_x4 += x[i]*x[i]*x[i]*x[i];
    sum_y   += y[i];
    sum_xy  += x[i]*y[i];
    sum_x2y += x[i]*x[i]*y[i];
  }

  // Columna 1
  c1[0] = s; c1[1] = sum_x; c1[2] = sum_x2;

  // Columna 2
  c2[0] = sum_x; c2[1] = sum_x2; c2[2] = sum_x3;

  // Columna 3
  c3[0] = sum_x2; c3[1] = sum_x3; c3[2] = sum_x4;
  
  // Coolumna B
  cb[0] = sum_y; cb[1] = sum_xy; cb[2] = sum_x2y;
}

float det(float* c1, float* c2, float* c3)
{
  return ( c1[0]*(c2[1]*c3[2] - c2[2]*c3[1]) ) - ( c2[0]*(c1[1]*c3[2] - c1[2]*c3[1]) ) + ( c3[0]*(c1[1]*c2[2] - c1[2]*c2[1]) );
}

struct instrumento simular_segmentos(struct instrumento inst, int s)
{
    int st = ((N - (N % s)) / s); // número de segmentos
    struct instrumento simulado;
    simulado.tono = calloc(st * s, sizeof(float));
    simulado.volumen = calloc(st * s, sizeof(float));
    simulado.duracion = calloc(st * s, sizeof(float));

    // Simulación para TONO
    float* coef_tono = coeficientes(inst.tono, st, s);
    for (int i = 0; i < st; i++) {
        float a0 = coef_tono[3*i];
        float a1 = coef_tono[3*i + 1];
        float a2 = coef_tono[3*i + 2];
        for (int j = 0; j < s; j++) {
            int idx = i * s + j;
            simulado.tono[idx] = a0 + a1 * j + a2 * j * j;
        }
    }

    // Simulación para VOLUMEN
    float* coef_volumen = coeficientes(inst.volumen, st, s);
    for (int i = 0; i < st; i++) {
        float a0 = coef_volumen[3*i];
        float a1 = coef_volumen[3*i + 1];
        float a2 = coef_volumen[3*i + 2];
        for (int j = 0; j < s; j++) {
            int idx = i * s + j;
            simulado.volumen[idx] = a0 + a1 * j + a2 * j * j;
        }
    }

    // Simulación para DURACIÓN
    float* coef_duracion = coeficientes(inst.duracion, st, s);
    for (int i = 0; i < st; i++) {
        float a0 = coef_duracion[3*i];
        float a1 = coef_duracion[3*i + 1];
        float a2 = coef_duracion[3*i + 2];
        for (int j = 0; j < s; j++) {
            int idx = i * s + j;
            simulado.duracion[idx] = a0 + a1 * j + a2 * j * j;
        }
    }

    return simulado;
}

