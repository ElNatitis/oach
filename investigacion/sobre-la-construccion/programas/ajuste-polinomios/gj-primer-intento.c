/*
GAUSS-JORDAN CON PIVOTEO
Se recive una matriz cuadrada con el formato de "matrices.h" y, con respecto a sus dimensiones, se realizan, visitando los elementos de la diagonal principal en orden acendente, las siguientes operaciones 

  1 - Se garantiza que la elección del pivote sea óptima y se intercambian renglones de ser necesario
  2 - Se divide el renglón en cuestión entre el pivote
  3 - Aplicamos 'truco-1' para que la columna en cuestión coincida con la matriz identidad por abajo 

Una vez que terminada la visita acendente hacemos ahora una visita en orden contrario aplicando el 'truco-2' para que las columnas coincidan con la matriz identidad por arriba
*/

#include <stdlib.h>
#include <stdio.h>
#include "matrices.h"

struct matriz inversa(struct matriz m)
{
  // garantizamos que la matriz sea cuadrada
  if(m.filas!=m.columnas)
  {
    printf("\nError. La matriz no es cuadrada.\n");
    exit(1);
  }

  double *dp = calloc(m.filas,sizeof(double)); // arreglo para almacenar la diagonal principal
  for(int i=0;i<m.columnas;i++) // ciclo para visitar la diagonal principal y guardarla en 'dp'
  {
    dp[i]=m.elemento[i*m.columnas+i];
  }
  
  
  
  
  // para ver la matriz y la diagonal principal alamacenadas
  imprimir_matriz(m);
  for(int i=0;i<m.columnas;i++) printf("%.2f, ", dp[i]);

  
  
 // visitando los elementos de la diagonal principal en orden acendente 
 // -------------------------------------
  for(int i=0;i<m.columnas;i++)
  {
    //  1 - Se garantiza que la elección del pivote sea óptima y se intercambian renglones de ser necesario
    if(dp[i]==0) 
    {
      double aux1=dp[i];
      int aux2;
      for(int j=i;j<m.columnas;j++)
      {
        printf("\nm.elemento[%d]=%.2f \n",j*m.columnas+i,m.elemento[j*m.columnas+i]);
        if(m.elemento[j*m.columnas+i]>aux1) 
        {
          aux1=m.elemento[j*m.columnas+i];
          aux2=j; 
        }
      }
      printf("\ndentro de la columna %d, el elemento que mejor queda para pivote se encuentra en la fila %d y es %.2f\n",i,aux2,aux1);
      intercambia_filas(m,i,aux2);imprimir_matriz(m);
    }
    
    // 2 - Se divide el renglón en cuestión entre el pivote
    for(int k=0;k<m.columnas;k++) dp[k]=m.elemento[k*m.columnas+k];
    for(int k=0;k<m.columnas;k++) printf("%.2f, ", dp[k]);
    
    multiplica_fila(m,i,1/dp[i]);imprimir_matriz(m);
    // 3 - Aplicamos 'truco-1' para que la columna en cuestión coincida con la matriz identidad por abajo
    for(int j=i+1;j<m.columnas;j++)
    {
      printf("\nj=%d,i=%d,-m.elemento[j*m.columnas+i] = - %.2f\n",j,i,m.elemento[j*m.columnas+i]);
      suma_multiplo_de_fila(m,j,i,-m.elemento[j*m.columnas+i]);
    }
    imprimir_matriz(m);

  }
  
  // visitando los elementos de la diagonal principal en orden descendente 
 // -------------------------------------
  for(int i=m.columnas-1;i>=0;i--)
  {
    // aplicando el 'truco-2' para que las columnas coincidan con la matriz identidad por arriba
    for(int j=i-1;j>=0;j--)
    {
      printf("\nj=%d,i=%d,-m.elemento[j*m.columnas+i] = - %.2f\n",j,i,m.elemento[j*m.columnas+i]);
      suma_multiplo_de_fila(m,j,i,-m.elemento[j*m.columnas+i]);
    }
    imprimir_matriz(m);
    
  }
}
