#ifndef INSTRUMENTO_H
#define INSTRUMENTO_H
/* MODULO INSTRUMENTO_H

Se define el formato del dato 'instrumento'

*/ 


struct instrumento {
    int nombre;
    float* tono; 
    float* volumen; 
    float* duracion; 
};

//  funciones básicas
void declarar_instrumento(struct instrumento* inst, int N);
void declarar_instrumento_segmentado(struct instrumento* inst, int s, int st);
void liberar_instrumento(struct instrumento* inst);
void imprimir_instrumento(struct instrumento inst, int N);
void imprimir_instrumento_segmentado(struct instrumento inst, int N, int s);


// funciones para el aft
struct instrumento integrar_instrumento(struct instrumento* inst, int N);
struct instrumento segmentar_instrumento(struct instrumento* inst, int N, int s);
struct instrumento simular_segmentos(struct instrumento inst, int N, int s, int g);
float* fluctuaciones(struct instrumento inst, struct instrumento inst_sim, int N, int s);


#endif

