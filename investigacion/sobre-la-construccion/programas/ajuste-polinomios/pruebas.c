#include <stdio.h>
#include "matrices.h"

int main() 
{
  struct matriz m = declara_matriz(3,3);
  
  // valores prueba
  m.elemento[0] = 2;m.elemento[1] = 4;m.elemento[2] = 6; // fila 1
  m.elemento[3] = 4;m.elemento[4] = 5;m.elemento[5] = 6; // fila 2
  m.elemento[6] = 3;m.elemento[7] = 1;m.elemento[8] = -2; // fila 3
  struct matriz inv = inversa(m);
  
  
  struct matriz a = declara_matriz(3,3);
  // valores prueba
  a.elemento[0] = 2;a.elemento[1] = 4;a.elemento[2] = 6; // fila 1
  a.elemento[3] = 4;a.elemento[4] = 5;a.elemento[5] = 6; // fila 2
  a.elemento[6] = 3;a.elemento[7] = 1;a.elemento[8] = -2; // fila 3
  
  imprimir_matriz(producto(a,inv));
  
  
  
  
  
  
}
