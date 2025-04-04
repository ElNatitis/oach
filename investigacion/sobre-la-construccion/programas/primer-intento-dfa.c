// Para hacer un DFA con respecto a datos random
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void imprimir(float arr[], int n);
float promedio(float arr[], int n);
void integrar_arreglo(float arr[], float arr_int[], float promedio, int n);



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
  int ns = N%s; // Número de sementos posibles dado el tamaño de s y el total de datos
  int es = N - ns; // Número de elementos que habrá dado el número de segmentos posibles
  float arreglo_int_seg[ns][]
  
  
  
  printf("\n\n----pruebas-----\n");
  printf("%d\n",(8%5));
}

void imprimir(float arr[], int n)
{
  for(int i = 0; i < n; i++) 
    printf("%.2f, ", arr[i]);
    
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
