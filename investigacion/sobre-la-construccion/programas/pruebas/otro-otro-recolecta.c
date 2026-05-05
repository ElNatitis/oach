/* RECOLECTA DATOS DEL CSV PARA CONSTRUIR LOS ARREGLOS 'instrumento' Y APLICAR ADF

script diseñado para ejecutarse, en conjunto con los modulos 1, 2, 3 y 4, en la carpeta 'canciones-{genero}'

Antes de correr el script es necesario especificar, en el arreglo 'archivos[]': SRTUCT<
  - Nombre del archivo, 
  - Número de instrumentos en la variable 'numero_de_instrumentos'
  - Número de semifusas en la variable 'numero_de_semifusas'

Los últimos dos datos se consultan en un archivo .txt con el mismo nombre que se encuentra en la misma carpeta 

Se visita el archivo especificado y para cada instrumento dentro del mismo, se llevan a cabo los siguientes procesos
  1 - Se declara la variable 'instrumento' usando la librería 'instrumento.h'
  2 - Se almacenan los datos 'nota', 'volumen' y 'dura', correspondientes a ese instrumento, en el arreglo declarado
  3 - Integramos las series construidas con la función 'integrar_instrumento' 
  4 - Con respecto a cada tamaño de segmento, se realiza lo siguiente
        4.1 - Se segmentan las series construidas con al función 'segmentar_instrumento' en variables llamadas 'seg_x_int'
        4.2 - Para cada grado de polinomio especificado se realiza lo siguiente
                4.2.1 - Se simulan esos segmentos con la función 'simular_segmento' en variables llamadas 'sim_seg_x'
                4.2.2 - Se determina la magnitud promedio de fluctuación de las notas volumenes y duraciones, con respecto al tamaño de segmento en cuestión, utilizando la función 'fluctuaciones'

El programa genera un .txt en donde se almacenan los datos correspondientes al proceso, además de un csv que contiene los resultados bajo el siguiente formato

'fluctuaciones-archivo[].csv' = { instrumento | tamano_segmento | polinomio | f_nota | f_volumen | f_dura  }


*/

#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <string.h>
#include <unistd.h> 
#include "instrumento.h"
#include "matrices.h"

// struct para tener una manera ordenada de visitar los archivos que quieren analizar 
struct cancion {
    int numero_de_instrumentos; 
    int numero_de_semifusas; 
    char archivo[100];
};

// para enlistar las canciones a analizar
struct cancion *canciones_a_revisar(int n)
{
  struct cancion *canciones = calloc(n,sizeof(struct cancion)); // arreglo de n elementos donde cada elemento es una 'cancion'
  
  // estos datos deben declararse antes de correr el script y aún no diseño dónde y cómo serán consultables:)
  // para enlistar las canciones a analizar
struct cancion *canciones_a_revisar(int n)
{
  struct cancion *canciones = calloc(n,sizeof(struct cancion)); // arreglo de n elementos donde cada elemento es una 'cancion'
  
  // estos datos deben declararse antes de correr el script y aún no diseño dónde y cómo serán consultables:)
  canciones[0].numero_de_instrumentos = 7;
  canciones[0].numero_de_semifusas = 24573;
  strcpy(canciones[0].archivo, "frankie-ruiz---la-cura-(karaoplay.com)-norm.csv");
  
  canciones[1].numero_de_instrumentos = 5;
  canciones[1].numero_de_semifusas = 24303;
  strcpy(canciones[1].archivo, "the-latin-brothers---patrona-de-los-reclusos-(midi)-(karaoplay.com)-norm.csv");
  
  canciones[2].numero_de_instrumentos = 6;
  canciones[2].numero_de_semifusas = 22589;
  strcpy(canciones[2].archivo, "comprendelo---luis-enrique-(karaoplay.com)-norm.csv");
    
  canciones[3].numero_de_instrumentos = 4;
  canciones[3].numero_de_semifusas = 22200;
  strcpy(canciones[3].archivo, "richie-ray---aguzate-(karaoplay.com)-norm.csv");

  canciones[4].numero_de_instrumentos = 3;
  canciones[4].numero_de_semifusas = 20736;
  strcpy(canciones[4].archivo, "the-latin-brothers---la-guayaba-(karaoplay.com)-norm.csv");

  canciones[5].numero_de_instrumentos = 5;
  canciones[5].numero_de_semifusas = 19283;
  strcpy(canciones[5].archivo, "celia-cruz---toro-mata-(karaoplay.com)-norm.csv");

  canciones[6].numero_de_instrumentos = 6;
  canciones[6].numero_de_semifusas = 18242;
  strcpy(canciones[6].archivo, "hector-lavoe---déjala-que-siga-(karaoplay.com)-norm.csv");

  canciones[7].numero_de_instrumentos = 8;
  canciones[7].numero_de_semifusas = 16847;
  strcpy(canciones[7].archivo, "gran-combo---la-loma-del-tamarindo-(karaoplay.com)-norm.csv");

  canciones[8].numero_de_instrumentos = 7;
  canciones[8].numero_de_semifusas = 16257;
  strcpy(canciones[8].archivo, "orquesta-guayacán---un-vestido-bonito-(karaoplay.com)-norm.csv");

  canciones[9].numero_de_instrumentos = 6;
  canciones[9].numero_de_semifusas = 14490;
  strcpy(canciones[9].archivo, "rubén-blades---pedro-navaja-(karaoplay.com)-norm.csv");

  canciones[10].numero_de_instrumentos = 6;
  canciones[10].numero_de_semifusas = 14458;
  strcpy(canciones[10].archivo, "jerry-rivera---amores-como-el-nuestro-(karaoplay.com)-norm.csv");

  canciones[11].numero_de_instrumentos = 7;
  canciones[11].numero_de_semifusas = 14348;
  strcpy(canciones[11].archivo, "frankie-ruiz---amor-de-un-momento-(karaoplay.com)-norm.csv");

  canciones[12].numero_de_instrumentos = 6;
  canciones[12].numero_de_semifusas = 13810;
  strcpy(canciones[12].archivo, "el-gran-combo-de-puerto-rico---me-libere-(karaoplay.com)-norm.csv");

  canciones[13].numero_de_instrumentos = 6;
  canciones[13].numero_de_semifusas = 13751;
  strcpy(canciones[13].archivo, "frankie-ruiz---quiero-llenarte-(karaoplay.com)-norm.csv");

  canciones[14].numero_de_instrumentos = 7;
  canciones[14].numero_de_semifusas = 13744;
  strcpy(canciones[14].archivo, "the-latin-brothers---sobre-las-olas-(karaoplay.com)-norm.csv");

  canciones[15].numero_de_instrumentos = 5;
  canciones[15].numero_de_semifusas = 12613;
  strcpy(canciones[15].archivo, "el-gran-combo-de-puerto-rico---cupido-(karaoplay.com)-norm.csv");

  canciones[16].numero_de_instrumentos = 5;
  canciones[16].numero_de_semifusas = 11835;
  strcpy(canciones[16].archivo, "richie-ray---sonido-bestial-(karaoplay.com)-norm.csv");

  canciones[17].numero_de_instrumentos = 6;
  canciones[17].numero_de_semifusas = 9735;
  strcpy(canciones[17].archivo, "el-gran-combo-de-puerto-rico---por-mas-que-yo-quiera-(karaoplay.com)-norm.csv");

  canciones[18].numero_de_instrumentos = 8;
  canciones[18].numero_de_semifusas = 9008;
  strcpy(canciones[18].archivo, "gilberto-santa-rosa---vivir-sin-ella-(karaoplay.com)-norm.csv");

  canciones[19].numero_de_instrumentos = 7;
  canciones[19].numero_de_semifusas = 8656;
  strcpy(canciones[19].archivo, "the-latin-brothers---fuma-el-barco-(karaoplay.com)-norm.csv");

  canciones[20].numero_de_instrumentos = 7;
  canciones[20].numero_de_semifusas = 8561;
  strcpy(canciones[20].archivo, "grupo-niche---cali-aji-(karaoplay.com)-norm.csv");

  canciones[21].numero_de_instrumentos = 10;
  canciones[21].numero_de_semifusas = 8489;
  strcpy(canciones[21].archivo, "el-gran-combo-de-puerto-rico---regresa-ya-(karaoplay.com)-norm.csv");

  canciones[22].numero_de_instrumentos = 5;
  canciones[22].numero_de_semifusas = 7584;
  strcpy(canciones[22].archivo, "frankie-ruiz---tu-con-el-(karaoplay.com)-norm.csv");

  canciones[23].numero_de_instrumentos = 10;
  canciones[23].numero_de_semifusas = 6590;
  strcpy(canciones[23].archivo, "grupo-niche---sin-sentimiento-(karaoplay.com)-norm.csv");

  canciones[24].numero_de_instrumentos = 7;
  canciones[24].numero_de_semifusas = 6240;
  strcpy(canciones[24].archivo, "guayacan---como-una-hoguera-(karaoplay.com)-norm.csv");

  canciones[25].numero_de_instrumentos = 7;
  canciones[25].numero_de_semifusas = 6199;
  strcpy(canciones[25].archivo, "luis-enrique---no-te-quites-la-ropa-(karaoplay.com)-norm.csv");

  canciones[26].numero_de_instrumentos = 6;
  canciones[26].numero_de_semifusas = 5872;
  strcpy(canciones[26].archivo, "héctor-lavoe---plazos-traicioneros-(karaoplay.com)-norm.csv");

  canciones[27].numero_de_instrumentos = 7;
  canciones[27].numero_de_semifusas = 5628;
  strcpy(canciones[27].archivo, "the-latin-brothers---dime-que-paso-(karaoplay.com)-norm.csv");

  canciones[28].numero_de_instrumentos = 5;
  canciones[28].numero_de_semifusas = 4743;
  strcpy(canciones[28].archivo, "celia-cruz---vieja-luna-(karaoplay.com)-norm.csv");

  canciones[29].numero_de_instrumentos = 11;
  canciones[29].numero_de_semifusas = 3751;
  strcpy(canciones[29].archivo, "héctor-lavoe---la-fama-(karaoplay.com)-norm.csv");

  canciones[30].numero_de_instrumentos = 6;
  canciones[30].numero_de_semifusas = 2304;
  strcpy(canciones[30].archivo, "artista-desconocido---ceora-(karaoplay.com)-norm.csv");
    
  return canciones;
}


int main(void)
{
  int n=31;
  struct cancion *canciones = canciones_a_revisar(n);
  
  // para verificar que todo esté bien
  printf("\nla primer cancion es %s, tiene %d instrumentos y %d semifusas\n",canciones[0].archivo,canciones[0].numero_de_instrumentos,canciones[0].numero_de_semifusas);
  
  // declaramos todo lo necesario para poder segmentar la serie
  int *segmentos; 
  segmentos = calloc(9,sizeof(int)); // arreglo de 3 elementos donde cada elemento es un numero entero
  segmentos[0] = 8;
  segmentos[1] = 16;
  segmentos[2] = 32;
  segmentos[3] = 64;
  segmentos[4] = 128;
  segmentos[5] = 256;
  segmentos[6] = 512;
  segmentos[7] = 1024;
  segmentos[8] = 2048;
  
  // declaramos todo lo necesario para poder simular la serie
  int *grado;
  grado = calloc(6,sizeof(int));
  grado[0]=2;
  grado[1]=3;
  grado[2]=4;
  grado[3]=5;
  grado[4]=6;
  grado[5]=7;
  
  
  // creamos el .txt que contendrá la información de todo el proceso
  FILE *reporte = fopen("reporte.txt", "w");
  // para validar
  if (reporte == NULL)
  {
    printf("\nERROR, no se pudo crear el reporte\n");
    exit(1);
  }
        
        
  // creamos el .csv que contendrá los resultados finales
  FILE *resultados = fopen("fluctuaciones-salsa-p.csv", "w");
  // para validar
  if (resultados == NULL)
  {
    printf("\nERROR, no se pudo crear el csv\n");
    exit(1);
  }
  fprintf(resultados, "cancion_id,instrumento,tamano_segmento,grado_polinomio,f_nota,f_volumen,f_dura\n");  // encabezado
  
  
  
  
  for(int i=0;i<n;i++)
  {
    char ruta[512]; // para almacenar la ruta del directorio actual
    if (getcwd(ruta, sizeof(ruta)) != NULL) // para obtener la ruta del directorio actual
    {
      // concatenar el nombre del archivo al directorio actual
      strcat(ruta, "/"); strcat(ruta, canciones[i].archivo);
      FILE *fp = fopen(ruta, "r");// intentar abrir el archivo
      if(fp)
      {
        // guardamos el nombre del archivo para usarlo en el .txt y .csv
        char nombre_archivo[100];
        strncpy(nombre_archivo, canciones[i].archivo, sizeof(nombre_archivo));
        nombre_archivo[strlen(nombre_archivo) - 4] = '\0';  // corta ".csv"
        
        printf("\nArchivo encontrado y abierto: %s\n", ruta); //imprimir en la terminal
        fprintf(reporte, "Archivo encontrado y abierto: %s\n", ruta); // imprimir en el reporte
        
        char linea[256];// buffer para leer cada línea
        int indx = 0;// índice de la fila actual
        fgets(linea, sizeof(linea), fp);// leer la primera línea del archivo
        printf("primera linea\n%s",linea);
        fprintf(reporte, "primera linea\n%s",linea);
        
        // iniciamooooooooos
        
        // arreglo donde guardaremos los instrumentos de la canción
        struct instrumento *instrumentos = calloc(canciones[i].numero_de_instrumentos, sizeof(struct instrumento)); 
        
        // ciclo para almacenar lo que hay en csv en el arreglo
        for(int j=0;j<canciones[i].numero_de_instrumentos;j++)
        {
          printf("\niniciando el instrumento %d\n",j);
          fprintf(reporte,"\niniciando el instrumento %d\n",j);
          
          // declaramos la variable instrumentoooooo :)
          struct instrumento inst;
          declarar_instrumento(&inst,canciones[i].numero_de_semifusas);
          for(int k=0;k<canciones[i].numero_de_semifusas;k++)
          {
            if(k==0) // cuando leemos la primer linea de datos almacenamos el nombre del instrumento
            {
              fgets(linea, sizeof(linea), fp); // para leer la siguiente linea del archivo
              //printf("ojo que aqui lo guardamos %s",linea);
              int aux;
              sscanf(linea, "%d,%f,%f,%f", &aux, &inst.tono[k], &inst.volumen[k], &inst.duracion[k]);// para guardar los valores de la linea actual
              inst.nombre = aux;
              printf("\n%d\n",inst.nombre);
              fprintf(reporte,"\n%d\n",inst.nombre);
            }
            else
            {
              fgets(linea, sizeof(linea), fp); // para leer la siguiente linea del archivo
              sscanf(linea, "%*f,%f,%f,%f", &inst.tono[k], &inst.volumen[k], &inst.duracion[k]);// para guardar los valores de la linea actual
            }
          }
          instrumentos[j] = inst; // guardamos el instrumento generado en nuestro arreglo donde cada elemento es un instrumento
          //imprimir_instrumento(inst,canciones[i].numero_de_semifusas);//para garantizar que todo esté bien
          printf("\nFinalizando el instrumento %d\n",j);
          fprintf(reporte,"\nFinalizando el instrumento %d\n",j);
        }
        fprintf(reporte,"--------- Fin de la etapa de construir los instrumentos\n");
        fprintf(reporte,"--------- Inicio de la etapa AFT\n");
        printf("\n--------- Inicio de la etapa AFT\n");
        for(int w=0;w<canciones[i].numero_de_instrumentos;w++)
        {
          struct instrumento x = instrumentos[w];
          fprintf(reporte,"\n\t* instrumento %d *",instrumentos[w].nombre);
          fprintf(reporte,"\n------- INTEGRACIÓN ------- \n\n");
          
          printf("\n\t* instrumento %d *",x.nombre);
          printf("\n------- INTEGRACIÓN ------- \n\n");
          struct instrumento x_int = integrar_instrumento(&x,canciones[i].numero_de_semifusas);
          fprintf(reporte,"\nfin de integración del instrumento %d\n\n",w);
          printf("\nfin de integración del instrumento %d\n\n",w);
          
          fprintf(reporte,"\n------- SEGMENTACIÓN ------- \n\n");
          printf("\n------- SEGMENTACIÓN ------- \n\n");
          for(int u=0;u<9;u++)
          {
            fprintf(reporte,"\n### PARA EL SEGMENTOS DE TAMAÑO %d ###\n",segmentos[u]);
            printf("\n### PARA EL SEGMENTOS DE TAMAÑO %d ###\n",segmentos[u]);
            struct instrumento seg_x_int = segmentar_instrumento(&x_int,canciones[i].numero_de_semifusas,segmentos[u]);
            seg_x_int.nombre = x.nombre;
            for(int g=0;g<6;g++)
            {
              fprintf(reporte,"\n------- SIMULADA ------- \n\n");
              printf("\n------- SIMULADA ------- \n\n");
              
              
              struct instrumento sim_seg_x = simular_segmentos(seg_x_int,canciones[i].numero_de_semifusas,segmentos[u],grado[g]);
              sim_seg_x.nombre = x.nombre;
              fprintf(reporte,"\n### POLINOMIO DE GRADO %d ###\n",grado[g]);
              printf("\n### POLINOMIO DE GRADO %d ###\n",grado[g]);
              
              //printf("\nJaja nimodo\n");
              //imprimir_instrumento_segmentado(seg_x_int,canciones[i].numero_de_semifusas,segmentos[u]);
              //imprimir_instrumento_segmentado(sim_seg_x,canciones[i].numero_de_semifusas,segmentos[u]);
              fprintf(reporte,"\nfin de simulacion de grado %d del instrumento %d\n\n",grado[g],w);
              printf("\nfin de simulacion de grado %d del instrumento %d\n\n",grado[g],w);
              // magnitud promedio de fluctuaciones
              
              printf("\n------- RESULTADOS ------- \n\n");
              fprintf(reporte,"\n------- RESULTADOS ------- \n\n");
              float *resultaos = fluctuaciones(seg_x_int,sim_seg_x,canciones[i].numero_de_semifusas,segmentos[u]);
              fprintf(resultados, "%d,%d,%d,%d,%f,%f,%f\n",i,x.nombre,segmentos[u],grado[g],resultaos[1],resultaos[2],resultaos[3]);
              //printf("\nPresiona Enter para continuar...");getchar();  // espera entrada
              
            }
            
            
            
            
            fprintf(reporte,"\nfin de segmentación de tamaño %d del instrumento %d\n\n",segmentos[u],w);
            printf("\nfin de segmentación de tamaño %d del instrumento %d\n\n",segmentos[u],w);
            
          }
          
        }
        
        
      }
      else
      {
        printf("\nERROR, No se pudo obtener la ruta del directorio actual%s\n", ruta);
        exit(1);
      }
    }
    else
    {
      printf("\nERROR, No se pudo abrir el archivo\n");
      exit(1);
    }
    printf("########################################## %d / %d", i,n);
  }
  printf("################## FIN DE TODO");
  
  
  
}



