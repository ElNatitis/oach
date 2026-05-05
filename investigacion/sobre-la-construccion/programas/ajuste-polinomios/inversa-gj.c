/*    
INVERSA DE UNA MATRIZ UTILIZANDO GAUSS JORDAN
Se recibe una matriz cuadrada en el formato definido en matrices.h. 
Para calcular su inversa mediante el método de Gauss-Jordan, se trabaja simultáneamente con una matriz identidad 'inv' del mismo tamaño, la cual se irá transformando conforme se aplican las operaciones elementales.

El procedimiento consiste en recorrer los elementos de la diagonal principal en orden ascendente y, en cada paso, realizar las siguientes operaciones:

  1 - Se selecciona un pivote adecuado (distinto de cero) y, de ser necesario, se intercambian renglones tanto en la matriz original 'm' como en la matriz 'inv'.
  2 - Se normaliza el renglón del pivote dividiéndolo entre el valor del pivote, aplicando esta operación a ambas matrices.
  3 - Con la función 'truco_uno' se eliminan los elementos por debajo del pivote para que coincida con la matriz identidad por abajo

Una vez completado el recorrido ascendente, se realiza un recorrido descendente sobre la diagonal principal:

  4 - Con la función 'truco_dos' se eliminan los elementos por encima de cada pivote para que coincida con la matriz identidad por arriba

Al finalizar este proceso, la matriz identidad inicial 'inv' se habrá transformado en la matriz inversa de la matriz original 'm'.
*/

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include "matrices.h"


struct matriz inversa(struct matriz m); // función principal declarada en 'matrices.h'
void diag(struct matriz m, double *dp); // recibe una matriz y edita el arreglo 'dp' almacenando su diagonal principal 
void prn(struct matriz m, struct matriz inv); // imprime ambas matrices para monitoriar
void truco_uno(struct matriz m, struct matriz inv, double *dp); // se eliminan los elementos por debajo del pivote para que coincida con la matriz identidad por abajo
void truco_dos(struct matriz m, struct matriz inv); // se eliminan los elementos por encima de cada pivote para que coincida con la matriz identidad por arriba



void prn(struct matriz m, struct matriz inv) // imprime ambas matrices para monitoriar
{
  printf("\n##############");
  printf("\n\tMATRIZ m\n");
  imprimir_matriz(m);
  printf("\n\tMATRIZ inv\n");
  imprimir_matriz(inv);
  printf("##############\n\n");
}

void diag(struct matriz m, double *dp) // recibe una matriz y edita el arreglo 'dp' almacenando su diagonal principal 
{
  for(int i=0;i<m.columnas;i++) dp[i]=m.elemento[i*m.columnas+i];
}

void truco_uno(struct matriz m, struct matriz inv, double *dp) // se eliminan los elementos por debajo del pivote para que coincida con la matriz identidad por abajo
{
  // visitando los elementos de la diagonal principal en orden acendente 
  for(int i=0;i<m.columnas;i++)
  {
    if(fabs(dp[i]) < 1e-10) //  1 - Se garantiza que la elección del pivote sea óptima y se intercambian renglones de ser necesario
    {
      double aux1=dp[i];
      int aux2;
      for(int j=i;j<m.columnas;j++)
      {
        printf("\nm.elemento[%d]=%.2f \n",j*m.columnas+i,m.elemento[j*m.columnas+i]);
        if(fabs(m.elemento[j*m.columnas+i]) > fabs(aux1)) 
        {
          aux1=m.elemento[j*m.columnas+i];
          aux2=j; 
        }
      }
      printf("\ndentro de la columna %d, el elemento que mejor queda para pivote se encuentra en la fila %d y es %.2f\n",i,aux2,aux1);
      intercambia_filas(m,i,aux2);imprimir_matriz(m);
      intercambia_filas(inv,i,aux2);imprimir_matriz(m);
      prn(m,inv);
    }
    diag(m,dp);
    // 2 - Se divide el renglón en cuestión entre el pivote
    multiplica_fila(m,i,1/dp[i]);
    multiplica_fila(inv,i,1/dp[i]);
    prn(m,inv);
    // 3 - Aplicamos 'truco-1' para que la columna en cuestión coincida con la matriz identidad por abajo
    for(int j=i+1;j<m.columnas;j++)
    {
      printf("\nj=%d,i=%d,-m.elemento[j*m.columnas+i] = - %.2f\n",j,i,m.elemento[j*m.columnas+i]);
      double c = -m.elemento[j*m.columnas+i];
      suma_multiplo_de_fila(m,j,i,c);
      suma_multiplo_de_fila(inv,j,i,c);
      prn(m,inv);
    }
  }
}

void truco_dos(struct matriz m, struct matriz inv) // se eliminan los elementos por encima de cada pivote para que coincida con la matriz identidad por arriba
{
  for(int i=m.columnas-1;i>=0;i--) // visitando los elementos de la diagonal principal en orden descendente
  {
    for(int j=i-1;j>=0;j--) // aplicando el 'truco-2' para que las columnas coincidan con la matriz identidad por arriba
    {
      printf("\nj=%d,i=%d,-m.elemento[j*m.columnas+i] = - %.2f\n",j,i,m.elemento[j*m.columnas+i]);
      double c = -m.elemento[j*m.columnas+i];
      suma_multiplo_de_fila(m,j,i,c);
      suma_multiplo_de_fila(inv,j,i,c);
    }
    prn(m,inv);  
  } 
}


struct matriz inversa(struct matriz m) // función principal declarada en 'matrices.h'
{
  if(m.filas!=m.columnas) // regresa 1 si la matriz es cuadrada y 0 si no
  {
    printf("\nError. La matriz no es cuadrada.\n");exit(1);
  }
  struct matriz inv = declara_matriz(m.filas,m.columnas); // se declara la matriz 'inv'
  for(int i=0;i<inv.filas;i++) inv.elemento[i*inv.columnas+i]=1; // para que 'inv' coincida con la matriz identidad
  prn(m,inv);
  double *dp = calloc(m.filas,sizeof(double));diag(m,dp); // se declara el arreglo 'dp' para almacenar la diagonal principal
  truco_uno(m,inv,dp);
  truco_dos(m,inv);
  return inv;
}
