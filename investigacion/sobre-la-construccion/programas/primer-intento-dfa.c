// Para hacer un DFA con respecto a datos random
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>


void imprimir(float arr[], int n);
float promedio(float arr[], int n);
void integrar_arreglo(float arr[], float arr_int[], float promedio, int n);
void imprimir_segmentos(float* arr_seg, int st, int s);
void llenar_segmentos(float* arr_seg, float arr[],int st, int s);

int main(void)
{
  // Inicializar la semilla para obtener números aleatorios distintos cada vez
  srand(time(NULL));

  // Número de datos
  int N = 100;
  float arreglo[N];
  float arreglo_int[N];
  
  // Llenar el arreglo con números aleatorios del 0 al 99
  for(int i = 0; i < N; i++)
    arreglo[i] = rand() % 100;
    
  // Imprimir el arreglo
  printf("Arreglo aleatorio con %d elementos:\n",N);
  imprimir(arreglo, N);
  
  // Calcular promedio
  float prom;
  prom = promedio(arreglo,N);
  printf("El promedio de ese arreglo es\n%.2f\n",prom);
  
  // Integrar el arreglo
  integrar_arreglo(arreglo,arreglo_int,prom,N);
  printf("Arreglo integrado\n");
  imprimir(arreglo_int,N);
  
  // Segmentar el arreglo integrado 
  int s = 16; // Tamaño de los segmentos 
  int es = N%s; // Número de elementos que van a sobrar luego de la segmentacion 
  int et = N - es; // Número de elementos que habrá dado el número de segmentos posibles
  int st = et/s; // Número de segmentos que habrá en el arreglo de segmentos
  printf("\n\n----segmentación-----\n");
  printf("haremos segmentos de %d elementos\nsignifica que van a sobrarnos %d elementos\nnuestro arreglo segmentado tendrá un total de %d elementos, osea %d segmentos\n",s,es,et,st);
  
  // Generar un arreglo en el que cada elemento sea un segmento 
  float* arreglo_int_seg = calloc(st*s, sizeof(float));
  llenar_segmentos(arreglo_int_seg,arreglo_int,st,s);
  imprimir_segmentos(arreglo_int_seg, st,s);
  
  // Ajustar cada segemento de datos usando un polinomio de grado 2
  printf("\n----Ajuste de cada segmento a un polinomio de grado 2----\n\n");
  float x[s];
  float sum_x,sum_x2,sum_x3,sum_x4,sum_y,sum_xy,sum_x2y;
  for(int j=0;j<s;j++) x[j]=j; // Para generar un arreglo x = {1,2,..,s}
  for(int i=0;i<s;i++)
  {
    printf("%.2f, ",x[i]);
  }
  printf("\n");
  for (int l=0; l<s; l++) // Para calcular todas las sumas que vamos a necesitar para las matrices
  {
    sum_x  += x[l];
    sum_x2 += pow(x[l],2);
    sum_x3 += pow(x[l],3);
    sum_x4 += pow(x[l],4);
    sum_y   += arreglo_int[l];
    sum_xy  += x[l] * arreglo_int[l];
    sum_x2y += pow(x[l],2) * arreglo_int[l];
  }
  printf("\n##sumas calculadas\nsum_x=%.1f\nsum_x2=%.1f\nsum_x3=%.1f\nsum_x4=%.1f\nsum_y=%.1f\nsum_xy=%.1f\nsum_x2y=%.1f\n",sum_x,sum_x2,sum_x3,sum_x4,sum_y,sum_xy,sum_x2y);
  
  
}

void imprimir(float arr[], int n)
{
  for(int i = 0; i < n; i++) 
    printf("%.2f, ", arr[i]);
    
  printf("\n");
}

void imprimir_segmentos(float* arr_seg, int st, int s)
{
  printf("\n");
  for(int i=0;i<st;i++)
  {
    printf("[");
    for (int j=0;j<s;j++)
    {
      printf(" %.1f,",arr_seg[i*s+j]);
    }
    printf("]\n");
  }
  printf("\n");
}


float promedio(float arr[], int n)
{
  float sum = 0;
  for(int i = 0; i < n; i++) 
    sum += arr[i];
    
  return(sum / n);
}

void integrar_arreglo(float arr[], float arr_int[], float promedio, int n)
{
  float suma;
  for(int j=0; j < n; j++) 
  {
    suma = 0;
    for(int i=0; i<=j; i++)
    {
      //printf("%.2f\t+=\t%.2f - %.2f\n",suma, arr[i],promedio);
      suma += arr[i] - promedio;     
    }
    //printf("Terminamos, el elemento %d es %.2f ------\n \n",j,suma);
    arr_int[j]=suma;
  }
}

void llenar_segmentos(float* arr_seg, float arr[],int st, int s)
{
  int aux=0;
  for(int i=0;i<st;i++)
  {
    for(int j=0;j<s;j++)
    {
      //printf("\nestamos en el elemento %d que tiene el valor %.1f\n",aux,arr[aux]);
      arr_seg[i*s+j]=arr[aux];
      aux++;
    }
  }
}
