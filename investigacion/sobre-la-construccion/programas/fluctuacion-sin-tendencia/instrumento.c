/* MODULO INSTRUMENTO

Se definen las funciones para declarar e imprimir un instrumento, ademas de una para librar espacio

*/ 
#include <stdio.h>
#include <stdlib.h>
#include "instrumento.h"

void declarar_instrumento(struct instrumento* inst)
{
    inst->tono = calloc(N, sizeof(float));
    inst->volumen = calloc(N, sizeof(float));
    inst->duracion = calloc(N, sizeof(float));
}

void declarar_instrumento_segmentado(struct instrumento* inst, int s, int st)
{
    // arreglos en el que cada elemento es un segmento 
    inst->tono = calloc(st*s, sizeof(float)); 
    inst->volumen = calloc(st*s, sizeof(float)); 
    inst->duracion = calloc(st*s, sizeof(float)); 
}

void liberar_instrumento(struct instrumento* inst)
{
    free(inst->tono);
    free(inst->volumen);
    free(inst->duracion);
}

void imprimir_instrumento(struct instrumento inst)
{
    printf("--- tono ---\n[");
    for(int i = 0; i < N; i++) 
        printf("%.2f, ", inst.tono[i]);
    printf("]\n");

    printf("--- volumen ---\n[");
    for(int i = 0; i < N; i++) 
        printf("%.2f, ", inst.volumen[i]);
    printf("]\n");

    printf("--- duracion ---\n[");
    for(int i = 0; i < N; i++) 
        printf("%.2f, ", inst.duracion[i]);
    printf("]\n");
}

void imprimir_instrumento_segmentado(struct instrumento inst, int s)
{
    int st = ((N-(N%s))/s); // número de segmentos que habrá en el arreglo de segmentos
    printf("---- segmentos de tono ----\n");
    for (int i = 0; i < st; i++) {
        printf("s %d: [", i+1);
        for (int j = 0; j < s; j++) {
            int index = i * s + j;
            printf("%.2f", inst.tono[index]);
            if (j < s - 1) printf(", ");
        }
        printf("]\n");
    }

    printf("---- segmentos de volumen ----\n");
    for (int i = 0; i < st; i++) {
        printf("s %d: [", i+1);
        for (int j = 0; j < s; j++) {
            int index = i * s + j;
            printf("%.2f", inst.volumen[index]);
            if (j < s - 1) printf(", ");
        }
        printf("]\n");
    }

    printf("---- segmentos de duración ----\n");
    for (int i = 0; i < st; i++) {
        printf("s %d: [", i+1);
        for (int j = 0; j < s; j++) {
            int index = i * s + j;
            printf("%.2f", inst.duracion[index]);
            if (j < s - 1) printf(", ");
        }
        printf("]\n");
    }
}
