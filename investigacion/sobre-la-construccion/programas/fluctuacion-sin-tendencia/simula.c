/* MODULO  SIMULADO

Se simula (con ayuda de instrumento.h) una serie correspondiente a un instrumento con el formato

instrumento_i = { [t₁,...,tₙ], [v₁,...,vₙ], [d₁,...,dₙ] }

donde: t = tono, v = volumen y d = duración

y se realizan los siguientes procedimientos sobre cada una de las series

1 - "integramos" las series ejecutando el {modulo1.c} 

2 - segmentamos la serie




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
    
    // segmentamos la serie
    printf("\n------- TUBA SEGMENTADA ------- \n\n");
    int s = 16; //tamaño del segmento
    segmentar_instrumento(&tuba_int,s);
    
}

