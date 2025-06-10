"""
Filtro que hace los siguientes procesos en los archivos 1000-lanzamientos-de-{genero}.csv
    - Estandarizar el formato de 'fecha-lanzamiento'
    - Apartar en un csv diferente los erorres (cuando no hay fecha de lanzamiento)
    - Divir en otros 2 csv de albums y sencillos
    - Generar un .txt que contenga un resumen con el formato:
        "De los {n} lanzamientos recolectados pertenecientes al genero {genero} se recolectaron:
            - {m} albums
            - {ñ} sencillos
        con total de {o} lanzamientos que no sabemos en qué fecha salieron jsjs"
    - Generar una carpeta llamada "filtro-{genero}" que contenga los dos csv y el .txt
"""

import pandas as pd
import os

genero = 'cumbia' # genero a analizar


bd = pd.read_csv(f'1000-lanzamientos-{genero}.csv') # Tomar el csv
errores = [] # para guardar los lanzamientos que no tengan fechas

# estandarizar el formato de la fecha y apartar los errores ---------------
for i, fecha in bd['fecha-lanzamiento'].items(): # iteramos en la columna fecha-lanzmainto teniendo en cuenta el indice
    if pd.isna(fecha): # revisamos que sí haya un dato en la casilla
        errores.append(i) # guardamos el indice del lanzamiento con error
    else:
        fecha_str = str(fecha) # lo hacemos string  
        if len(fecha_str) != 4: # guardamos unicamente los primeros 4 caracteres (el año)
            bd.at[i, 'fecha-lanzamiento'] = fecha_str[:4]

bd.sort_values('fecha-lanzamiento', inplace=True) # ordenamos de menor a mayor
bd.to_csv(f'lanzamientos-{genero}.csv', index=False) # guardamos en formato csv

# carpeta para guardar un csv para cada tipo de lanzamiento ------
os.makedirs(f'tipos-de-lanzamientos-{genero}', exist_ok=True) 
# archivo .txt que tendrá el resumen
resumen_path = os.path.join(f'tipos-de-lanzamientos-{genero}', f'resumen-{genero}.txt')
open(resumen_path,'a',encoding='utf-8').close()


# errores ----
bd_errores = bd.loc[errores] # creamos un csv para los erroes
bd_errores.to_csv(os.path.join(f'tipos-de-lanzamientos-{genero}', f'errores-{genero}.csv'), index=False) # lo guardamos en la carpeta
bd_sin_errores = bd.drop(index=errores) # eliminar los errores
 
# escribimos en el resumen
with open(resumen_path, 'a', encoding='utf-8') as f:
    f.write(f'----- reusmen {genero} -----\n')
    f.write(f'se recolectaron un total de \t{len(bd)} lanzamientos\n')
    f.write(f'que incluyen:\n')

# tipos de lanzamientos ----
tdl = bd_sin_errores.groupby('tipo').size() # tdl := tipos de lanzamientos
for tipo, n in tdl.items(): # creamos un csv para cada tipo de lanzamiento
    bd_tipo = bd_sin_errores[bd_sin_errores['tipo'] == tipo]
    # escribimos en el resumen 
    with open(resumen_path, 'a', encoding='utf-8') as f:
        f.write(f'\t{tipo} {len(bd_tipo)}\n')
    
    # lo guardamos en la carpeta creada    
    ruta = os.path.join(f'tipos-de-lanzamientos-{genero}', f'{tipo}-{genero}.csv') 
    bd_tipo.to_csv(ruta, index=False)

with open(resumen_path, 'a', encoding='utf-8') as f:
    f.write(f'\terrores {len(bd_errores)}\n')






