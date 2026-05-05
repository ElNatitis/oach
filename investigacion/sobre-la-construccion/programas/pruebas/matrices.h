#ifndef MATRIZ_H
#define MATRIZ_H
/* MODULO MATRIZ_H

Se definen las siguientes operaciones respecto a las matrices
  1 - Declarar matriz
  2 - Matriz prueba
  3 - Transpuesta de matriz
  4 - Multiplicar matrices
  5 - Matriz de Vandermode

*/ 

struct matriz {
    int filas; 
    int columnas; 
    float *elemento; 
};

struct matriz declara_matriz(int filas, int columnas); // declarar matriz
void imprimir_matriz(struct matriz m); // imprimir

struct matriz transpuesta(struct matriz m); // devolver matriz transpuesta
struct matriz producto(struct matriz a, struct matriz b); // devolver producto de dos matrices
struct matriz vandermonde(int n, int m);// devolver matriz de vandermonde de nxm
void matriz_prueba(struct matriz m); // llenar matriz con 1,2,.. para pruebas 

// devolver la misma matriz con las filas u y v intercambiados
void intercambia_filas(struct matriz m, int u, int v); 

// devolver la matriz con la fila f multiplicada por c
void multiplica_fila(struct matriz m, int f, float c); 

// devolver la matriz con la fila o despues de sumarle c*f 
void suma_multiplo_de_fila(struct matriz m, int o, int f, float c); 

// devolver la inversa de la matriz
struct matriz inversa(struct matriz m);

#endif
