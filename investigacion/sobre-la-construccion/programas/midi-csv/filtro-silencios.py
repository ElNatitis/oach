"""
Queremos visitar el archivo csv que contenga los promedios de las notas que componen la cancion para llenar espacios correspondientes a ceros en cada instrumento
"""
import pandas as pd
import os

cancion = pd.read_csv('cancion-prom.csv') # Tomar el csv
cancion_cc = [] # para guardar la cacnion con ceros

# agrupamos para tener por separado cada instrumento de los eventos
instrumentos = cancion.groupby('instrumento')
s=0

for _, ins in instrumentos: # iteramos sobre cada instrumento
    i=0
    ins = ins.reset_index(drop=True) # reiniciamos el índice
    while i < len(ins): # iteramos sobre cada elemento dentro del instrumento
        cancion_cc.append(ins.loc[i].to_dict()) # guardamos la nota actual en el arreglo con ceros
        if i+1 < len(ins):
            termina = ins.loc[i,'termina']
            siguiente = ins.loc[i+1, 'empieza']
            silencio = siguiente - termina
            if silencio > 0:
                print(f"\naquí va un silencio que duraría {silencio}")
                # guardamos el silencio
                cancion_cc.append({
                        'instrumento': float(ins.loc[i,'instrumento']),
                        'nota': -1,
                        'volumen': 0.0,
                        'dura': float(silencio),
                        'empieza': float(termina),
                        'termina': float(siguiente)
                    })
            else:
                print(f'\nentre estas notas no hay silencios')
        else:
            print('\nterminamos el instrumento:)')
        i+=1
        s+=1


df_final = pd.DataFrame(cancion_cc)     
df_final.to_csv('cancion-prom-cc.csv', index=False) # lo guardamos en la carpeta

