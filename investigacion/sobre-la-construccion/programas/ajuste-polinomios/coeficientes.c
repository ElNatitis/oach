/*    
COEFICIENTES DE POLINOMIO SIMULADOR

Se recibe un arreglo 'x', su longitud 'N' y el grado del polinomio 'g' del que se desea encontrar los coeficientes, se determinan mediante mínimos cuadrados y regresa un arreglo 'coeff' con los resultados.

Para determinar los coeficientes se calcula (A^TA)^{-1} * A^T * x^T donde

  - A es la matriz de vandermonde que tendrá dimenciones (len(x),'g')
  - (A^TA)^{-1} se determina con funciones disponibles en 'matrices.h'
  - x^T es un vector columna que ocntiene los datos que se desean simular

El programa regresa en el arreglo 'coef' con los 'g' resultados de coefiecinetes.
*/

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "matrices.h"

double *coeficientes(double *x, int N, int g)
{
  struct matriz xt = declara_matriz(N,1);
  for(int i=0;i<N;i++) xt.elemento[i] = x[i];
  struct matriz A = vandermonde(N,g);
  struct matriz AtA = producto(transpuesta(A),A);
  imprimir_matriz(AtA);
  struct matriz inv_AtA = inversa(AtA);
  struct matriz coef = producto(producto(inv_AtA,transpuesta(A)),xt);
  imprimir_matriz(coef); 
  return coef.elemento;
}


int main(void)
{
  int N = 18;
  int g=6;
  double *x = calloc(N,sizeof(double));
  for(int i=0;i<N;i++)
  { 
    x[i] = -(double)23/9 + (34)*i + (3)*i*i + (7)*i*i*i + (-2.5)*i*i*i*i ;
  }
  double *coef = coeficientes(x,N,g);
  
  float *x_sim = calloc(N,sizeof(float));
  for(int i=0;i<N;i++)
  {
    for(int j=0;j<g;j++)
    {
      x_sim[i]+= coef[j]*pow(i,j);
    }
  }
  
  printf("\n[ ");
  for(int i=0;i<N;i++) 
  {
    printf("%f, ",x[i]);
  }
  printf("]\n");
  
  printf("\n[ ");
  for(int i=0;i<N;i++) 
  {
    printf("%f, ",x_sim[i]);
  }
  printf("]\n");
}



