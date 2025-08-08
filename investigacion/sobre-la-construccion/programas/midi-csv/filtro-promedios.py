"""
Lo que queremos es generar los promedios de las notas simultaneas dentro del midi
Se recibe un .csv que luego se visita para identeificar las notas simultaneas y generar promedios de cada uno de sus valores

"""
import pandas as pd
import os

cancion = pd.read_csv('cancion.csv') # Tomar el csv
cancion_prom = []

# agrupamos para tener por separado cada instrumento de los eventos
instrumentos = cancion.groupby('instrumento')
s=0

for _, ins in instrumentos: # iteramos sobre cada instrumento
    i=0
    ins = ins.reset_index(drop=True) # reiniciamos el índice
    while i < len(ins): # iteramos sobre cada elemento dentro del instrumento
        nota = ins.loc[i] # localizamos la nota
        momento = nota["empieza"] 
        print(f'la {i} nota empieza en el momento {momento}')
        
        simultaneas = [] # para almacenar las notas que esten sonando en un momento específico
        simultaneas.append(nota)
        
        
        for dato in simultaneas:
                    print(f'\n{dato}')
       
        
        
        # más variables auxiliares
        aux = True
        j=1 
        while i + j < len(ins):
            siguiente = ins.loc[i+j, 'empieza']
            print(f'\nla siguiente empieza en el momento {siguiente} entonces...')
            if momento == siguiente:
                simultaneas.append(ins.loc[i+j])
                print(f'\nla guardamos\n')
                j+=1
            else:
                print('\nnos detenemos:)')
                break

        s+=1
        
        i+=j # para saltar los renglones promediados
        print(f'\n{s} de {len(cancion)}')
        df_simultaneas = pd.DataFrame(simultaneas)

        # los datos que nos importan de las notas simultáneas
        print(f'\ntrabajamos con:')
        print(df_simultaneas[['nota', 'volumen', 'dura', 'empieza', 'termina']])

        # calculamos promedios
        promedios = df_simultaneas[['instrumento','nota', 'volumen', 'dura', 'empieza', 'termina']].mean()
        print(f"\npromedios:\nnota={int(promedios['nota'])}, volumen={int(promedios['volumen'])}, duración={promedios['dura']}, empieza={promedios['empieza']}, termina={promedios['termina']}")
        
        cancion_prom.append({
            'instrumento': promedios['instrumento'],
            'nota': int(promedios['nota']),
            'volumen': int(promedios['volumen']),
            'dura': promedios['dura'],
            'empieza': promedios['empieza'],
            'termina': promedios['empieza'] + promedios['dura']
        })
        
            
df_final = pd.DataFrame(cancion_prom)     
df_final.to_csv('cancion-prom.csv', index=False) # lo guardamos en la carpeta
