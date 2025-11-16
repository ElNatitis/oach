// Para apoximar un polinomio de grado dos que simule el comportamiento de una lista de n datos.

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "regla-de-cramer.h"

float* llenar_arr(int N);
float* llenar_aux(int N);
float* llenar_arr_polg2(int N);
void ajustar_seg_a_pol2(float* arreglo_int_seg, int s, int st);

float det(float* c1, float* c2, float* c3);
void llenar_columnas(float* c1, float* c2, float* c3,float* cb, float* y, float* x,int N);
void simular(float* x, float a0, float a1, float a2, int N);

void imprimir(float* arr, int n);



int main(void)
{
  // Inicializar la semilla para obtener números aleatorios distintos cada vez
  srand(time(NULL));
  // Número de datos
  int N = 20;
  // Arreglo que queremos aproximar
  float* arr = llenar_arr_polg2(N);
  // Arreglo índice
  float* aux = llenar_aux(N);
  printf("\n--- índice ---\n");
  imprimir(aux,N);  
  printf("\n--- arreglo que intentaremos aproximar ---\n");
  imprimir(arr,N);
  
  // Los arreglos que cumplirán la función de columnas
  float* c1 = calloc(3, sizeof(float));
  float* c2 = calloc(3, sizeof(float)); 
  float* c3 = calloc(3, sizeof(float));
  float* cb = calloc(3, sizeof(float)); 
  
  llenar_columnas(c1,c2,c3,cb,arr, aux, N);
  printf("\ncolumna 1\n");
  imprimir(c1,3);
  printf("columna 2\n");
  imprimir(c2,3);
  printf("columna 3\n");
  imprimir(c3,3);
  printf("columna B\n");
  imprimir(cb,3);
  
  // Determinantes de las matrices que formamos con las columnas
  float dete, det0, det1, det2;
  dete = det(c1,c2,c3);
  det0 = det(cb,c2,c3);
  det1 = det(c1,cb,c3);
  det2 = det(c1,c2,cb);
  printf("\nDeterminantes calculados.\ndet\t%.2f\ndet0\t%.2f\ndet1\t%.2f\ndet2\t%.2f",dete,det0,det1,det2);
  // Coeficientes que determinan el polinomio de grado 2
  float a0,a1,a2;
  a0 = det0 / dete;
  a1 = det1 / dete;
  a2 = det2 / dete;
  printf("\nCoeficientes determinados\na0\t%.2f\na1\t%.2f\na2\t%.2f\n",a0,a1,a2);
  
  // Simular datos con respecto al polinomio encontrado
  float* sim = llenar_aux(N);
  simular(sim,a0,a1,a2,N);
  
  
  printf("\n\n---- Resultados obtenidos ----\n\n");
  printf("Datos originales\n");
  imprimir(arr,N);
  printf("Datos simulados\n");
  imprimir(sim,N);
}

// Función que llama el programa "primer-intento-dfa.c"
void ajustar_seg_a_pol2(float* arreglo_int_seg, int s, int st)
{
  int N = s*st;// Determinamos el total de datos
  float* aux = llenar_aux(N); // Arreglo índice
  printf("\n--- índice ---\n");
  imprimir(aux,N);  
  printf("\n--- arreglo que intentaremos aproximar ---\n");
  float* segmento = &arreglo_int_seg[0 * s];
  imprimir(segmento,N);

  
}

float* llenar_arr(int N)
{
  // Arreglo que queremos aproximar
  float* arr = calloc(N, sizeof(float));
  
  // Llenar el arreglo con números aleatorios del 0 al 99
  for(int i = 0; i < N; i++)
    arr[i] = rand() % 40;
  
  return arr;
}

float* llenar_arr_polg2(int N)
{
  // Arreglo que queremos aproximar
  float* arr = calloc(N, sizeof(float));
  
  // Llenar el arreglo con números aleatorios del 0 al 99
  for(int i = 0; i < N; i++)
    arr[i] = 3 + 2*i + 0.5*i*i + (rand() % 5);  // polinomio real con ruido
  
  return arr;
}

float* llenar_aux(int N)
{
  // Arreglo que queremos aproximar
  float* arr = calloc(N, sizeof(int));
  
  // Llenar el indice con números del 1 al N
  for(int i = 0; i < N; i++) arr[i] = i;
  
  return arr;
}

void imprimir(float* arr, int n)
{
  for(int i = 0; i < n; i++) printf("%.2f, ", arr[i]);
    
  printf("\n");
}

void llenar_columnas(float* c1, float* c2, float* c3,float* cb, float* y, float* x,int N)
{
  float sum_x = 0, sum_x2 = 0, sum_x3 = 0, sum_x4 = 0;
  float sum_y = 0, sum_xy = 0, sum_x2y = 0;

  for (int i=0; i<N; i++) // Para calcular todas las sumas que vamos a necesitar para las matrices
  {
    sum_x  += x[i];
    sum_x2 += pow(x[i],2);
    sum_x3 += pow(x[i],3);
    sum_x4 += pow(x[i],4);
    sum_y   += y[i];
    sum_xy  += x[i] * y[i];
    sum_x2y += pow(x[i],2) * y[i];
  }
  printf("\n##sumas calculadas\nsum_x\t=%.1f\nsum_x2\t=%.1f\nsum_x3\t=%.1f\nsum_x4\t=%.1f\nsum_y\t=%.1f\nsum_xy\t=%.1f\nsum_x2y\t=%.1f\n",sum_x,sum_x2,sum_x3,sum_x4,sum_y,sum_xy,sum_x2y);
  
  // Columna 1
  c1[0] = N;
  c1[1] = sum_x;
  c1[2] = sum_x2;

  // Columna 2
  c2[0] = sum_x;
  c2[1] = sum_x2;
  c2[2] = sum_x3;

  // Columna 3
  c3[0] = sum_x2;
  c3[1] = sum_x3;
  c3[2] = sum_x4;
  
  // Coolumna B
  cb[0] = sum_y;
  cb[1] = sum_xy;
  cb[2] = sum_x2y;
}


float det(float* c1, float* c2, float* c3)
{
  return ( c1[0]*(c2[1]*c3[2] - c2[2]*c3[1]) ) - ( c2[0]*(c1[1]*c3[2] - c1[2]*c3[1]) ) + ( c3[0]*(c1[1]*c2[2] - c1[2]*c2[1]) );
}

void simular(float* x, float a0, float a1, float a2, int N)
{
  for(int i=0;i<N;i++)
  {
    x[i] = a0 + a1*x[i] + a2*pow(x[i],2);
  }
}


