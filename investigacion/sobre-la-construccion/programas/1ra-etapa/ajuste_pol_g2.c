// Para ajustar los segmentos realizados a un polinomio de grado 2
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "ajuste_pol_g2.h"

float* coeficientes(float* x_seg, int st, int s);
void llenar_columnas(float* c1, float* c2, float* c3,float* cb, float* y, float* x,int N);
void prn(float* arr, int n);
float det(float* c1, float* c2, float* c3);

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
    //printf("\ncolumna 1\n"); prn(c1,3);
    //printf("columna 2\n"); prn(c2,3);
    //printf("columna 3\n"); prn(c3,3);
    //printf("columna B\n"); prn(cb,3);
    
    // Determinantes de las matrices que formamos con las columnas
    float dete, det0, det1, det2;
    dete = det(c1,c2,c3);
    det0 = det(cb,c2,c3);
    det1 = det(c1,cb,c3);
    det2 = det(c1,c2,cb);
    //printf("\nDeterminantes calculados.\ndet\t%.2f\ndet0\t%.2f\ndet1\t%.2f\ndet2\t%.2f",dete,det0,det1,det2);
    // Coeficientes que determinan el polinomio de grado 2
    float a0,a1,a2;
    a0 = det0 / dete;
    a1 = det1 / dete;
    a2 = det2 / dete;
    //printf("\n----- Coeficientes determinados para el segmento %d\na0\t%.2f\na1\t%.2f\na2\t%.2f\n",i,a0,a1,a2);
    coef[3*i+0] = a0; 
    coef[3*i+1] = a1; 
    coef[3*i+2] = a2; 
  }
  return coef;
  
}

void llenar_columnas(float* c1, float* c2, float* c3,float* cb, float* y, float* x,int N)
{
  float sum_x = 0, sum_x2 = 0, sum_x3 = 0, sum_x4 = 0;
  float sum_y = 0, sum_xy = 0, sum_x2y = 0;

  for (int i=0; i<N; i++) // Para calcular todas las sumas que vamos a necesitar para las matrices
  {
    sum_x  += x[i];
    sum_x2 += x[i]*x[i];
    sum_x3 += x[i]*x[i]*x[i];
    sum_x4 += x[i]*x[i]*x[i]*x[i];
    sum_y   += y[i];
    sum_xy  += x[i]*y[i];
    sum_x2y += x[i]*x[i]*y[i];
  }
  //printf("\n##sumas calculadas\nsum_x\t=%.1f\nsum_x2\t=%.1f\nsum_x3\t=%.1f\nsum_x4\t=%.1f\nsum_y\t=%.1f\nsum_xy\t=%.1f\nsum_x2y\t=%.1f\n",sum_x,sum_x2,sum_x3,sum_x4,sum_y,sum_xy,sum_x2y);
  
  // Columna 1
  c1[0] = N; c1[1] = sum_x; c1[2] = sum_x2;

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

void prn(float* arr, int n)
{
  for(int i=0;i<n;i++) printf("%.2f, ", arr[i]);
  printf("\n");
}


