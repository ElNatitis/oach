#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "matrices.h"


// declarar matriz
struct matriz declara_matriz(int filas, int columnas) 
{
  struct matriz m;
  m.filas = filas;
  m.columnas = columnas;
  m.elemento = calloc(filas * columnas, sizeof(double)); // consultamos como m.elemento[i*columnas+j]
  return m;
}

// devolver la matriz transpuesta
struct matriz transpuesta(struct matriz m)
{
  struct matriz tm = declara_matriz(m.columnas,m.filas);
  int aux = 0;
  for(int i=0;i<m.filas;i++)
  {
    for(int j=0;j<(m.columnas);j++)
    {
      tm.elemento[i+(m.filas*j)] = m.elemento[aux];
      aux++;
    }
  }
  return tm;
}

// devolver matriz de vandermonde de nxm
struct matriz vandermonde(int n, int m)
{
  struct matriz v = declara_matriz(n,m);
  for(int i=0;i<n;i++)
  {
    for(int j=0;j<m;j++)
    {
      v.elemento[i*v.columnas+j] = pow(i,j);
    }
  }
  return v;
}


// devolver producto de dos matrices
struct matriz producto(struct matriz a, struct matriz b)
{
  if(a.columnas!=b.filas) // nos aseguramos que la operación pueda acerse
  {
    printf("Operación no permitida, las dimenciones no coinciden\n");
    exit(1);
  }
  else 
  {
    // declaramos la matriz respuesta
    struct matriz mr = declara_matriz(a.filas,b.columnas);
    imprimir_matriz(a);
    imprimir_matriz(b);
    
    for(int i=0;i<a.filas;i++)
    {
      //printf("\n\ni=%d",i);
      for(int k=0;k<b.columnas;k++)
      {
        //printf("\nk=%d",k);
        for(int j=0;j<a.columnas;j++)
        {
          mr.elemento[i*mr.columnas+k]+=a.elemento[i*a.columnas+j]*b.elemento[j*b.columnas+k];
          //printf("\nmr[%d]+=(a[%d]*b[%d])=%lf*%lf",i*mr.columnas+k,i*a.columnas+j,j*b.columnas+k,a.elemento[i*a.columnas+j],b.elemento[j*b.columnas+k]);
        }
      }
    }
    return mr;
  }
  
}

// devolver la misma matriz con las filas u y v intercambiados
void intercambia_filas(struct matriz m, int u, int v)
{
  // m[i][j] = m.elemento[i*columnas+j]
  if(m.filas<u||m.filas<v)
  {
    printf("Operación no permitida, una de las filas no existe\n");
    exit(1);
  }
  else
  {
    double aux;
    for(int i=0;i<m.columnas;i++)
    {
      aux = m.elemento[u*m.columnas+i];
      m.elemento[u*m.columnas+i] = m.elemento[v*m.columnas+i];
      m.elemento[v*m.columnas+i] = aux;
    }
  }  
}

// devolver la matriz con la fila f multiplicada por c
void multiplica_fila(struct matriz m, int f, double c)
{
  if(f>m.filas)
  {
    printf("Operación no permitida, la fila no existe\n");
    exit(1);
  }
  else
  {
    for(int i=0;i<m.columnas;i++)
    {
      m.elemento[f*m.columnas+i]*=c;
    }
  }
}

// devolver la matriz con la fila objetivo 'o' despues de sumarle su correspondiente en la fila 'f' multiplicada por 'c' 
void suma_multiplo_de_fila(struct matriz m, int o, int f, double c)
{
  if(f>m.filas||o>m.filas)
  {
    printf("Operación no permitida, la fila no existe\n");
    exit(1);
  }
  else
  {
    for(int i=0;i<m.columnas;i++)
    {
      printf("\nm.elemento[%d] = %.2f += %.2f x %.2f",o*m.columnas+i, m.elemento[o*m.columnas+i], c,m.elemento[f*m.columnas+i]);
      m.elemento[o*m.columnas+i] += c*m.elemento[f*m.columnas+i];
      
    } 
  }
}

void imprimir_matriz(struct matriz m) 
{
  printf("\n(%dx%d)\n",m.filas,m.columnas);
  for(int i=0;i<m.filas;i++) 
  {
    for(int j=0;j<m.columnas;j++) 
    {
      printf("%8.3f\t",m.elemento[i*m.columnas+j]);
    }
    printf("\n");
  }
}

void matriz_prueba(struct matriz m)
{
  for(int i=0;i<(m.filas*m.columnas);i++)
  {
    m.elemento[i]=i;
  }
}


