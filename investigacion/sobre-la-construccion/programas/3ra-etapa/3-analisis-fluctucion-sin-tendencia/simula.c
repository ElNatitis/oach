/* MODULO  SIMULADO

Se simula (con ayuda de instrumento.h) una serie correspondiente a un instrumento con el formato

instrumento_i = { [t₁,...,tₙ], [v₁,...,vₙ], [d₁,...,dₙ] }

donde: t = tono, v = volumen y d = duración

y se realizan los siguientes procedimientos sobre cada una de las series

1 - "integramos" las series ejecutando el {modulo1.c} 

2 - segmentamos la serie

3 - simulamos cada segmento

4 - calculamos la magnitud promedio de fluctuaciones para ese tamaño de segmento




El programa termina generando la serie {flucxseg} con el formato

serie_int = { [s₁,Fs₁],...,[sₙ,Fsₙ] }

donde: sₙ  = tamaño de el segmento 
       Fsₙ = fluctuación cuadrática media de ese segmento

*/ 
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "instrumento.h"

int main(void)
{
    srand(time(NULL));  //para que salgan datos diferentes cada vez
    
    // declaramos una tuba
    struct instrumento tuba;
    declarar_instrumento(&tuba);
    
    // simulamos sobre cada una de sus series
    for (int i = 0; i < N; i++) 
    {
        tuba.tono[i] = rand() % 100;
        tuba.volumen[i] = rand() % 100;
        tuba.duracion[i] = rand() % 100;
    }
    
    // observamos los datos
    printf("\n------- TUBA SIMULADA ------- \n\n");
    imprimir_instrumento(tuba);
    
    // integramos la serie 
    printf("\n------- TUBA INTEGRADA ------- \n\n");
    struct instrumento tuba_int = integrar_instrumento(&tuba);
    imprimir_instrumento(tuba_int);
    
    int* segmentos; 
    float* final;
    segmentos = calloc(3,sizeof(int));
    final = calloc(12,sizeof(float));
    segmentos[0] = 16;
    segmentos[1] = 32;
    segmentos[2] = 64;
    
    for(int u=0; u<3; u++)
    {
      printf("\n### PARA EL SEGMENTOS DE TAMAÑO %d ###\n",segmentos[u]);
      // segmentamos la serie
      printf("\n------- TUBA SEGMENTADA ------- \n\n");
      int s = segmentos[u]; //tamaño del segmento
      struct instrumento seg_tuba_int = segmentar_instrumento(&tuba_int,s);
      imprimir_instrumento_segmentado(seg_tuba_int,s); 
      
      // simulamos los segmentos de la serie
      printf("\n------- TUBA SIMULADA ------- \n\n");
      struct instrumento sim_seg_tuba = simular_segmentos(seg_tuba_int,s);
      imprimir_instrumento_segmentado(sim_seg_tuba,s);
      
      // magnitud promedio de fluctuaciones
      printf("\n------- RESULTADOS ------- \n\n");
      float* resulatos = fluctuaciones(seg_tuba_int,sim_seg_tuba,s);
      int index = u*4;
      final[index] = resulatos[0];
      final[index+1] = resulatos[1];
      final[index+2] = resulatos[2];
      final[index+3] = resulatos[3];
    }
    printf("\n--- RESUMEN DE RESULTADOS ---\n");
    
    printf("s\tft\tfv\tfd\n");
    for(int y=0;y<3;y++)
    {
      int ind = y*4;
      printf("%.0f\t%.2f\t%.2f\t%.2f\n",final[ind],final[ind+1],final[ind+2],final[ind+3]);
    }
        
}

