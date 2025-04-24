#ifndef REGLA_DE_CRAMER_H
#define REGLA_DE_CRAMER_H



float* llenar_aux(int N);
float* llenar_arr_polg2(int N);
void ajustar_seg_a_pol2(float* arreglo_int_seg, int s, int st);
float det(float* c1, float* c2, float* c3);
void llenar_columnas(float* c1, float* c2, float* c3,float* cb, float* y, float* x,int N);
void simular(float* x, float a0, float a1, float a2, int N);
void imprimir(float* arr, int n);


#endif

