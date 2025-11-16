/*
Pretendemos poder visitar la carpeta 'canciones-{genero}' y tomar el archivo '{cancion}-norm.csv' para construir series con la forma:

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

// estructura para poder leer el csv
struct fila_csv {
    int instrumento;
    int tono;
    int volumen;
    float duracion;
};


int ndi; // variable para almacenar el número de instrumentos 
float ;



int main() 
{
    DIR *carpeta_midis;           // puntero a la carpeta 'canciones-salsa'
    struct dirent *dir;           // entrada leída dentro de 'canciones-salsa'
    carpeta_midis = opendir("canciones-salsa"); // abre la carpeta raíz

    if (carpeta_midis) 
    {
        while ((dir = readdir(carpeta_midis)) != NULL) 
        {
            // Ignorar "." y ".."
            if (strcmp(dir->d_name, ".") == 0 || strcmp(dir->d_name, "..") == 0)
                continue;
            
            size_t len = strlen(dir->d_name); // Para saber la longitud del char que ocntiene el nombre del archivo
            if (len >= 8 && strcmp(&dir->d_name[len - 8], "norm.csv") == 0) // si tiene más de 8 caracteres entonces revisamos sea 'norm.csv'
            {
                printf("%s\n", dir->d_name);
            }
        }

        closedir(carpeta_midis);
    } 
    else 
    {
        perror("No se pudo abrir la carpeta principal");
    }

    return 0;
}


