#ifndef INSTRUMENTO_H
#define INSTRUMENTO_H
/* MODULO INSTRUMENTO_H

Se define el formato del dato 'instrumento'

*/ 
#define N 1064

struct instrumento {
    float* tono; 
    float* volumen; 
    float* duracion; 
};

//  funciones básicas
void declarar_instrumento(struct instrumento* inst);
void declarar_instrumento_segmentado(struct instrumento* inst, int s, int st);
void liberar_instrumento(struct instrumento* inst);
void imprimir_instrumento(struct instrumento inst);
void imprimir_instrumento_segmentado(struct instrumento inst, int s);


// funciones para el aft
struct instrumento integrar_instrumento(struct instrumento* inst);
struct instrumento segmentar_instrumento(struct instrumento* inst, int s);
struct instrumento simular_segmentos(struct instrumento inst, int s);
float* fluctuaciones(struct instrumento inst, struct instrumento inst_sim, int s);


#endif

