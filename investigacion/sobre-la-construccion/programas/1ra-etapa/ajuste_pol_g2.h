#ifndef AJUSTE_POL_G2_H
#define AJUSTE_POL_G2_H

float* coeficientes(float* x_seg, int st, int s);
void llenar_columnas(float* c1, float* c2, float* c3,float* cb, float* y, float* x,int N);
void prn(float* arr, int n);
float det(float* c1, float* c2, float* c3);

#endif
