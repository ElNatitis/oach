import pandas as pd
import os

cancion = pd.read_csv('frankie-ruiz---tu-con-el-(karaoplay.com).csv') # Tomar el csv


# agrupamos para tener por separado cada instrumento de los eventos 
instrumentos = cancion.groupby('instrumento') 
print(f'\ntenemos un total de {len(instrumentos)} instrumentos que componen la canción') 

# para almacenar los máximos y minimos de cada instrumento 
max_t = [] # tiempos máximos 
min_t = [] # tiempos mínimose 
min_d = [] # duraciones mínimas 

# iteramos sobre los intrumentos para almacenar los datos en los arreglos 
for i, ins in instrumentos: 
    print(f'\npara el instrumento {i} son {len(ins)} notas') 
    print(f'con tiempos que van desde {ins["empieza"].min()} hasta {ins["termina"].max()}') 
    print(f'el intervalo más pequeño es de {ins["dura"].min()}') 
    # almacenamos los mínimos y máximos en cada arreglo 
    max_t.append(float(ins["termina"].max())) 
    min_t.append(float(ins["empieza"].min())) 
    min_d.append(float(ins["dura"].min())) 
    interv = min(min_d) 
    duracion = max(max_t) - min(min_t) 
    espacios = int(duracion/interv) 

print(f'\nentonces sabemos que todos las notas de todos los instrumentos ocurren en un intervalo de {duracion} segundos y que el intérvalo más pequeño es {interv}') 
print(f'\nla canción dura entonces {duracion/60} minutos y vamos a ocupar listas de {espacios} espacios para almacenar todos los eventos') 

