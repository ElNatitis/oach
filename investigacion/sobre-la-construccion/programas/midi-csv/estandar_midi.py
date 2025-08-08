""" 
El programa visita todos los arcivhos midi contenidos en una carpeta y, para cada uno de ellos realiza el siguiente procedimeinto: 

    1 - almacena en un DataFrame llamado 'cancion' los datos pertinenetes de cada evento de cada instrumento que compone el archivo midi, los cuales son: 'instrumento', 'nota', 'volumen', 'dura', 'empieza', 'termina'  
    2 - se analiza 'cancion' para identificar y almacenar en variables el intervalo mínimo de tiempo presente ('interv') y la duración total de los eventos de la cancion ('duracion')
    3 - almacena en un DataFrame llamado 'cancion-prom' los promedios de los datos pertinentes de las notas simultaneas presentes en cada instrumento
    4 - almacena en un DaraFrame llamado 'cancion-prom-cc' los mismos datos que hay en 'cancion-prom' con la diferencia de que los intervalos de segundos sin notas se almacenan como un silencio o dato 0 (para la continuidad de las series de tiempo)
    5 - a partir de la variable 'interv', se genera '{nombre-del-archivo}.csv', en donde se almacenan todos los eventos (notas y silencios) promediados divididos en eventos de duración 'interv'

Todo lo anterior debería ayudar a construir, a aprtir del archivo midi de una canción, una serie de tiempo multivariada con el formato:

cancion = {
            instrumento_1 = {
                                tono  = {t1, t2,..., tt}
                                volumen = {v1, v2,..., vt}
                                duracion = {d1, d2,..., dt}
                            },
                            
            instrumento_2 = {
                                tono  = {t1, t2,..., tt}
                                volumen = {v1, v2,..., vt}
                                duracion = {d1, d2,..., dt}
                            },
            .
            .
            .,
            
            instrumento_n = {
                                tono  = {t1, t2,..., tt}
                                volumen = {v1, v2,..., vt}
                                duracion = {d1, d2,..., dt}
                            }
        }
"""


