/* MODULO  SIMULADO

Se simula una serie correspondiente a un instrumento con el formato

instrumento_i = { [t₁,...,tₙ], [v₁,...,vₙ], [d₁,...,dₙ] }


donde: t = tono, v = volumen y d = duración

y se realizan los siguientes procedimientos sobre cada una de las series

1 - "integramos" las series ejecutando el {modulo1.c} en cada una






El programa termina generando la serie {flucxseg} con el formato

serie_int = { [s₁,Fs₁],...,[sₙ,Fsₙ] }

donde: sₙ  = tamaño de el segmento 
       Fsₙ = fluctuación cuadrática media de ese segmento

*/ 
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#define N 1024

struct instrumento {
  float* tono; 
  float* volumen; 
  float* duracion; 
};

void imprimir(struct instrumento x);

int main(void)
{
  srand(time(NULL)); // Inicializar la semilla para obtener números aleatorios distintos cada vez
  
  // Generamos el tipo de variable
  struct instrumento tuba;
  // Asignar memoria a cada arreglo
  tuba.tono = calloc(N, sizeof(float));
  tuba.volumen = calloc(N, sizeof(float));
  tuba.duracion = calloc(N, sizeof(float));
  
  // Simulamos su comportamiento
  for(int i=0;i<N;i++)// Llenar el arreglo con números aleatorios del 0 al 599
  {
    tuba.tono[i] = rand() % 100;
    tuba.volumen[i] = rand() % 100;
    tuba.duracion[i] = rand() % 100;
  }
    
    
  imprimir(tuba);
  
}


void imprimir(struct instrumento x)
{
  printf("--- tono ---\n");
  printf("[");
  for(int i=0;i<N;i++) 
    printf("%.2f, ", x.tono[i]);
  printf("]\n");
  
  printf("--- volumen ---\n");
  printf("[");
  for(int i=0;i<N;i++) 
    printf("%.2f, ", x.volumen[i]);
  printf("]\n");
  
  printf("--- duracion ---\n");
  printf("[");
  for(int i=0;i<N;i++) 
    printf("%.2f, ", x.duracion[i]);
  printf("]\n");
}

