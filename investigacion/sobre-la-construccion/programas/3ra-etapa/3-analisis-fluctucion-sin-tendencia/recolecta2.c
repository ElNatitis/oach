/*
Pretendemos poner este script en la carpeta 'canciones-{genero}' y tomar el archivo '{cancion}-norm.csv' para construir series con la forma:

cancion = {
            instrumento_1 = { [t_{1,1},...,t_{n,1}], [v_{1,1},...,v_{n,1}], [d_{1,1},...,d_{n,1}] },
            instrumento_2 = { [t_{1,2},...,t_{n,2}], [v_{1,2},...,v_{n,2}], [d_{1,2},...,d_{n,2}] },
            ...,
            instrumento_m = { [t_{1,m},...,t_{n,m}], [v_{1,m},...,v_{n,m}], [d_{1,m},...,d_{n,m}] }
        }
    
*/
#include <stdio.h>
#include <dirent.h>
#include <string.h>
#include <unistd.h> 

// para poder leer una fila del csv
struct fila_csv {
    int instrumento;
    int tono;
    int volumen;
    float duracion;
};


int fabrica_vectores();

int main()
{
  // El valor de estas variables se consulta en el .txt de la canción a analizar
  int numero_de_instrumentos = 5;
  int numero_de_semidifusas = 7584;
  
  char ruta[512]; // para almacenar la ruta del directorio actual
  char archivo[] = "frankie-ruiz---tu-con-el-(karaoplay.com)-norm.csv";  // nombre del archivo a analizar

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
      struct fila_csv fila[10];   // cantidad de filas que podemos almacenar en el sruct
      char linea[256];              // Buffer para leer cada línea
      int indx = 0;                 // Índice de la fila actual
      // Leer cada línea del archivo
      while (fgets(linea, sizeof(linea), fp)) 
      {
        // Salteamos la primera línea si es un encabezado
        if (indx == 0 && strncmp(linea, "instrumento", 11) == 0)
          continue;  // Omitimos el encabezado
      

        // Usamos sscanf para extraer los valores de cada línea
        sscanf(linea, "%d,%d,%d,%f", eventos[indx].instrumento,
                                        &eventos[indx].tono,
                                        &eventos[indx].volumen,
                                        &eventos[indx].duracion);

        // Mostrar lo que hemos leído en esta fila (con el índice)
        printf("Fila %d - Instrumento: %d, Tono: %d, Volumen: %d, Duración: %.2f\n",
               indx + 1, eventos[indx].instrumento, eventos[indx].tono,
               eventos[indx].volumen, eventos[indx].duracion);

        // Incrementar el índice para la siguiente fila
        indx++;
      }
      
      
      
      
      
      
      fclose(fp);
    } 
    else 
    {
      printf("Error al abrir el archivo");
    }
  } 
  else 
  {
    printf("No se pudo obtener la ruta del directorio actual");
  }
  
}


