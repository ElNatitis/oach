#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "ajuste_pol_g2.h"

// A partir de una serie simulada de datos, se realizan los siguientes pasos como método de Análisis de Fluctuación sin tendencia

// 1 - Integrar la serie
float* integrar_x(float* x, int N);
// 2 - Dividir en segmentos de tamaño s
float* segmentar_x(float* x, int s, int st);
// 3 - Ajustar cada segmento con un polinomio grado 2 (externo)
// Parte de esto pasa en el código "ajuste_pol_g2.c"
void simular_x(float* coef, float* seg, int s);
// 4 - Calcular Fluctuacion cuadratica media respecto al polinomio (externo)
float fcm(float* x_seg, float* x_seg_sim, int N);


void imprimir(float* x, int N);


int main(void)
{
  srand(time(NULL)); // Inicializar la semilla para obtener números aleatorios distintos cada vez
  int N = 100; // Número de datos
  float* x = calloc(N, sizeof(float)); // Arreglo
  
  // Llenar el arreglo con números aleatorios del 0 al 99
  for(int i=0;i<N;i++)
    x[i] = rand() % 100;
  
  // Integrar el arreglo generado
  float* x_int = integrar_x(x,N);
  
  // Segmentar el arreglo integrado
  int s=16; // Tamaño del segmento
  int st = ((N-(N%s))/s); // Número de segmentos que habrá en el arreglo de segmentos
  float* x_int_seg = segmentar_x(x_int,s,st);
  
  // Determinar coeficientes de polinomio grado dos para cada segmento
  float* coef = coeficientes(x_int_seg,st,s);
  
  // Simular los segmentos con los coeficientes
  float* x_seg_sim = calloc(st*s, sizeof(float)); // El arreglo en el que cada elemento es un segmento simulado
  for(int i=0;i<st;i++)
  {
    float* coef_i = coef+i*3; // Un apuntador para cada conjunto de coeficientes
    float* seg = x_seg_sim+i*s;  // Un apuntador para cada segmento por simular
    simular_x(coef_i,seg,s);
  }
  
  printf("Arreglo simulado\n"); imprimir(x,N);
  printf("Arreglo integrado\n"); imprimir(x_int,N);
  printf("Arreglo segmentado\n");
  for(int i=0;i<st;i++)
  {
    float* seg = x_int_seg+i*s;  
    imprimir(seg,s);
  }
  printf("Coeficientes que ajustan cada seg a un polg2\n");
  for(int i=0;i<st;i++)
  {
    float* seg = coef+i*3;  
    imprimir(seg,3);
  }
  printf("Segmentos simulados dados los coeficientes\n");
  for(int i=0;i<st;i++)
  {
    float* seg = x_seg_sim+i*s;  
    imprimir(seg,s);
  }
  printf("Fluctuaciones cuadráticas medias de cada segmento\n");
  for(int i=0;i<st;i++)
  {
    float* seg = x_int_seg+i*s;
    float* seg_sim = x_seg_sim+i*s;  
    float fcm_i = fcm(seg, seg_sim, s);
    printf("F(s)_%d\t= %.2f\n",i,fcm_i);
  }
  
  
}

float* integrar_x(float* x, int N)
{
  float* x_int = calloc(N, sizeof(float)); // Arreglo que devolveremos
  // Calculamos el promedio
  float sum = 0;
  for(int i=0;i<N;i++) 
    sum += x[i];
  float prom = (sum/N);

  // Integramos cada elemento y lo guardamos en x_int
  for(int j=0;j<N;j++) 
  {
    sum=0; // Reiniciamos el valor de la variable
    for(int i=0;i<=j;i++)
    {
      //printf("%.2f\t+=\t%.2f - %.2f\n",suma, arr[i],promedio);
      sum += x[i]-prom;     
    }
    //printf("Terminamos, el elemento %d es %.2f ------\n \n",j,suma);
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
      //printf("\nestamos en el elemento %d que tiene el valor %.1f\n",aux,arr[aux]);
      x_int_seg[i*s+j]=x[aux];
      aux++;
    }
  }
  return x_int_seg;
}

float fcm(float* x_seg, float* x_seg_sim, int N)
{
  float sum=0,resta;
  for(int i=0;i<N;i++)
  {
    resta = x_seg[i] - x_seg_sim[i];
    sum += resta*resta;
  }
  return sqrt(sum/N);
}






void simular_x(float* coef, float* x, int s)
{
  for(int i=0;i<s;i++)
  {
    x[i] = coef[0] + coef[1]*i + coef[2]*i*i;
  }
}

void imprimir(float* x, int N)
{
  printf("[");
  for(int i=0;i<N;i++) 
    printf("%.2f, ", x[i]);
  printf("]\n");
}




