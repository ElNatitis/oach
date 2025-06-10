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

bd = pd.read_csv('1000-lanzamientos-de-cumbia.csv') # Tomar el csv
errores = [] # para guardar los lanzamientos que no tengan fechas

# estandarizar el formato de la fecha y apartar los errores ---------------
for i, fecha in bd['fecha-lanzamiento'].items(): # iteramos en la columna fecha-lanzmainto teniendo en cuenta el indice
    if pd.isna(fecha): # revisamos que sí haya un dato en la casilla
        errores.append(i)
    else:
        fecha_str = str(fecha) # hacemos string el contenido 
        if len(fecha_str) != 4: # guardamos unicamente los primeros 4 caracteres (el año)
            bd.at[i, 'fecha-lanzamiento'] = fecha_str[:4]

bd.sort_values('fecha-lanzamiento', inplace=True) # ordenamos de menor a mayor
bd.to_csv('lanzamientos-de-cumbia.csv', index=False) # guardamos en 
# dividir en albums y senciilo
print(f"{bd.groupby('tipo').size()}")


