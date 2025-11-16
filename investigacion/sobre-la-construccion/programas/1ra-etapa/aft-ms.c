/* Con esto pretendo poder, apartir de un arreglo simulado, realizar las siguientes tareas
  1 - integrar la serie 
  2 - para cada uno de los 15 tamaños de segmento
    2.1 -- segmentar la serie integrada
    2.2 -- ajustar polinomios de grado 2 en cada segmento
    2.3 -- calcular la fluctuacion cuadrática media
  3 - Determinar el valor de alfa */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "ajuste_pol_g2.h"

float* integrar_x(float* x, int N); 
float* segmentar_x(float* x, int s, int st);
float fcm(float* x_seg, float* x_seg_sim, int N);
void simular_x(float* coef, float* seg, int s);
void imprimir(float* x, int N);

int main(void)
{
  srand(time(NULL)); // Inicializar la semilla para obtener números aleatorios distintos cada vez
  
  
  int N = 1024; // Número de datos
  float* x = calloc(N, sizeof(float)); // Arreglo
  for(int i=0;i<N;i++) x[i] = rand() % 599;// Llenar el arreglo con números aleatorios del 0 al 599
  printf("------------ Arreglo simulado ------------\n"); 
  imprimir(x,N);
  
  
  
  float* x_int = integrar_x(x,N); // 1 - Integrar el arreglo generado
  printf("------------ Arreglo integrado ------------\n"); imprimir(x_int,N);
  
  
  
  int S[3] = {16, 20, 25};
  for(int i=0;i<3;i++)
  {
    int s = S[i];
    int st = ((N-(N%s))/s); // Número de segmentos que habrá en el arreglo de segmentos
    float* x_int_seg = segmentar_x(x_int,s,st); // 2.1 -- Segmentar el arreglo integrado
    float* coef = coeficientes(x_int_seg,st,s);// 2.2 -- Coeficientes de polinomio grado dos para cada segmento
    float* x_seg_sim = calloc(st*s, sizeof(float)); // El arreglo en el que cada elemento es un segmento simulado
    for(int i=0;i<st;i++)
    {
      float* coef_i = coef+i*3; // Un apuntador para cada conjunto de coeficientes
      float* seg = x_seg_sim+i*s;  // Un apuntador para cada segmento por simular
      simular_x(coef_i,seg,s);
    }
    printf("------------ Arreglo segmentado ------------\n");
    for(int i=0;i<st;i++)
    {
      float* seg = x_int_seg+i*s;  
      imprimir(seg,s);
    }
    printf("------------ Coeficientes que ajustan cada seg a un polg2 ------------\n");
    for(int i=0;i<st;i++)
    {
      float* seg = coef+i*3;  
      imprimir(seg,3);
    }
    printf("------------ Arreglo simulado  ------------\n");
    for(int i=0;i<st;i++)
    {
      float* seg = x_seg_sim+i*s;  
      imprimir(seg,s);
    }
    
  }
}

float* integrar_x(float* x, int N)
{
  float* x_int = calloc(N, sizeof(float)); // Arreglo que devolveremos
  float sum = 0;
  for(int i=0;i<N;i++) sum += x[i];
  float prom = (sum/N); // Calculamos el promedio
  for(int j=0;j<N;j++)  // Integramos cada elemento y lo guardamos en x_int
  {
    sum=0; // Reiniciamos el valor de la variable
    for(int i=0;i<=j;i++) sum += x[i]-prom;     
    x_int[j]=sum;
  }
  return x_int;
}

float* segmentar_x(float* x, int s, int st)
{
  int aux=0; // Variable auxiliar
  float* x_int_seg = calloc(st*s, sizeof(float)); // El arreglo en el que cada elemento es un segmento 
  // llenamos los segmentos del arreglo 
  for(int i=0;i<st;i++)
  {
    for(int j=0;j<s;j++)
    {
      x_int_seg[i*s+j]=x[aux];
      aux++;
    }
  }
  return x_int_seg;
}

void simular_x(float* coef, float* x, int s)
{
  for(int i=0;i<s;i++) x[i] = coef[0] + coef[1]*i + coef[2]*i*i;
}

void imprimir(float* x, int N)
{
  printf("[");
  for(int i=0;i<N;i++) printf("%.2f, ", x[i]);
  printf("]\n");
}

