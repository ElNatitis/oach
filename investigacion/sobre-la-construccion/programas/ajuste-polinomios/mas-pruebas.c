#include <stdio.h>
#include "matrices.h"

int main() 
{
  // datos sumulados
  struct matriz xt = declara_matriz(8,1);
  for(int i=0;i<8;i++)
  { 
    xt.elemento[i] = -(double)23/9 + 34*i - 3*i*i;
  }
  imprimir_matriz(xt);
  
  
  struct matriz A = vandermonde(8,3);
  struct matriz At = transpuesta(A);
  struct matriz AtA = producto(At,A);
  imprimir_matriz(AtA);
  struct matriz inv_AtA = inversa(AtA);
  struct matriz a = producto(producto(inv_AtA,At),xt);
  imprimir_matriz(a);
  
  struct matriz xts = declara_matriz(8,1);
  for(int i=0;i<8;i++)
  { 
    xts.elemento[i] = a.elemento[0] + a.elemento[1]*(i) + a.elemento[2]*(i)*(i);
  }
  imprimir_matriz(xts);
  
  
  
  
}
