/*
Pretendemos poner este script en la carpeta 'canciones-{genero}' y tomar el archivo '{cancion}-norm.csv' para construir series con la forma:

cancion = {
            instrumento_1 = { [t_{1,1},...,t_{n,1}], [v_{1,1},...,v_{n,1}], [d_{1,1},...,d_{n,1}] },
            instrumento_2 = { [t_{1,2},...,t_{n,2}], [v_{1,2},...,v_{n,2}], [d_{1,2},...,d_{n,2}] },
            ...,
            instrumento_m = { [t_{1,m},...,t_{n,m}], [v_{1,m},...,v_{n,m}], [d_{1,m},...,d_{n,m}] }
        }
esta pensado para empaquetarse cada que se quiera leer un documetno diferente, necesitan cambiarse las variables 
  - numero_de_instrumentos
  - numero_de_semidifusas
  - archivo[]

las primeras dos corresponden a numeros que se pueden consultar en el .txt que aparece en la carpeta que tiene el mimso nombre que el archivo que intentamos analizar
mientras que archivo es el nombre del archivo con al estencion -norm, el cual se encuantra en la misma carpeta mencionada anteriormente
(prometo redactarlo de mejor manera en un futuro no muy lejano)
*/
#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <string.h>
#include <unistd.h> 
#include "instrumento.h"




int fabrica_vectores();

int main()
{
  // El valor de estas variables se consulta en el .txt de la canción a analizar
  int numero_de_instrumentos = 7;
  struct instrumento* instrumentos = calloc(numero_de_instrumentos, sizeof(struct instrumento)); //  arreglo en el que guardaremos los datos de cada instrumento
  int numero_de_semidifusas = 24573;
  
  char ruta[512]; // para almacenar la ruta del directorio actual
  char archivo[] = "frankie-ruiz---la-cura-(karaoplay.com)-norm.csv";  // nombre del archivo a analizar

  // para obtener la ruta del directorio actual
  if (getcwd(ruta, sizeof(ruta)) != NULL) 
  {
    // concatenar el nombre del archivo al directorio actual
    strcat(ruta, "/");
    strcat(ruta, archivo);
    // intentar abrir el archivo
    FILE *fp = fopen(ruta, "r");
    if (fp) 
    {
      printf("Archivo encontrado y abierto: %s\n", ruta);
      char linea[256];              // Buffer para leer cada línea
      int indx = 0;                 // Índice de la fila actual
      // Leer la primera línea del archivo
      fgets(linea, sizeof(linea), fp);
      printf("%s",linea);
      
      for(int i=0;i<numero_de_instrumentos;i++)
      {
        printf("iniciando el instrumento %d\n",i);
        // declaramos la variable instrumentoooooo :)
        struct instrumento inst;
        declarar_instrumento(&inst,numero_de_semidifusas);
        for(int j=0;j<numero_de_semidifusas;j++)
        {
          if (j == 0)
          {
            fgets(linea, sizeof(linea), fp); // para leer la linea después del encabezado
            printf("ojo que aqui lo guardamos %s",linea);
            int aux;
            // Usamos sscanf para extraer los valores de cada línea
            sscanf(linea, "%d,%f,%f,%f", &aux, &inst.tono[j], &inst.volumen[j], &inst.duracion[j]);
            inst.nombre = aux;
            printf("\n%d\n",inst.nombre);
          }
          else
          {
            fgets(linea, sizeof(linea), fp); // para leer la linea después del encabezado
            //printf("%s",linea);
            // Usamos sscanf para extraer los valores de cada línea
            sscanf(linea, "%*f,%f,%f,%f", &inst.tono[j], &inst.volumen[j], &inst.duracion[j]);
          }
         
        }
        // imprimir_instrumento(inst,numero_de_semidifusas);
        instrumentos[i] = inst; // guardamos el instrumento generado en nuestro arreglo donde cada elemento es un instrumento
      }
    }  
    
    else 
    {
      printf("Error al abrir el archivo");
    }
    fclose(fp);
  }
  else 
  {
    printf("No se pudo obtener la ruta del directorio actual");
  }
  
  
  
  
  printf("\n########### Comenzamos ajua!\n\n");
  
  //imprimir_instrumento(x,numero_de_semidifusas);
  for(int w=0;w<numero_de_instrumentos;w++)
  {
  struct instrumento x = instrumentos[w];
  printf("\n\t* instrumento %d *",x.nombre);
  // integramos la serie 
  //printf("\n------- INTEGRACIÓN ------- \n\n");
  struct instrumento x_int = integrar_instrumento(&x,numero_de_semidifusas);
  //imprimir_instrumento(x_int,numero_de_semidifusas);
  
  // declaramos todo lo necesario para poder segmentar la serie
  int* segmentos; 
  float* final;
  segmentos = calloc(9,sizeof(int)); // arreglo de 3 elementos donde cada elemento es un numero entero 
  final = calloc(36,sizeof(float)); // 4 x len(segmentos)
  segmentos[0] = 8;
  segmentos[1] = 16;
  segmentos[2] = 32;
  segmentos[3] = 64;
  segmentos[4] = 128;
  segmentos[5] = 256;
  segmentos[6] = 512;
  segmentos[7] = 1024;
  segmentos[8] = 2048;
  
  
  
  
  
  
  
  for(int u=0; u<9; u++)
    {
      printf("\n### PARA EL SEGMENTOS DE TAMAÑO %d ###\n",segmentos[u]);
      // segmentamos la serie
      //printf("\n------- SEGMENTACIÓN ------- \n\n");
      int s = segmentos[u]; //tamaño del segmento
      struct instrumento seg_x_int = segmentar_instrumento(&x_int,numero_de_semidifusas,s);
      //imprimir_instrumento_segmentado(seg_x_int,numero_de_semidifusas,s); 
      
      
      // simulamos los segmentos de la serie
      //printf("\n------- SIMULADA ------- \n\n");
      struct instrumento sim_seg_x = simular_segmentos(seg_x_int,numero_de_semidifusas,s);
      //imprimir_instrumento_segmentado(sim_seg_x,numero_de_semidifusas,s);
      
      // magnitud promedio de fluctuaciones
      printf("\n------- RESULTADOS ------- \n\n");
      float* resultaos = fluctuaciones(seg_x_int,sim_seg_x,numero_de_semidifusas,s);
      int index = u*4;
      final[index] = resultaos[0];
      final[index+1] = resultaos[1];
      final[index+2] = resultaos[2];
      final[index+3] = resultaos[3];
      
    }
  
  
  }
  
  
  return 0;
}


