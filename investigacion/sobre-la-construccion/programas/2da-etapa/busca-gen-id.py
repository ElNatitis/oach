"""
Buscador que solicita 1000 gurpos de lanzamientos, en la API de musicbrainz, pertenecientes a un '{genero}' especifico.
Los grupos de lanzamientos pueden ser álbum, sencillo, ep, etc.

El buscador realiza los siguientes procesos:
    1.- se genera una carpeta llamada '{genero}'
    2.- se realiza la solicitud de 1000 lanzamientos pertenecientes a '{genero}'
    3.- se enlistan unicamente 'title', 'primary-type', 'artist-credit', 'first-release-date', 'tags' y 'id'
    4.- se estandariza la 'fecha-de-lanzamiento' bajo el formato 'YYYY'
    5.- se enlistan los índices de lanzamientos en los que no hay fecha de lanzamiento registrada 
    6.- las 1000 solicitudes, sin errores, se guardan en la carpeta bajo el nombre '1000-lanzamientos-{genero}.csv'
    7.- se generan y guardan en la carpeta archivos csv distintos cada tipo de lanzamiento bajo el nombre '{tipo}-{genero}.csv'
    8.- se genera y guarda en la carpeta un archivo csv con los erores bajo el nombre 'errores-{genero}.csv'
    9.- se genera y guarda en la carpeta un .txt que contenga un resumen bajo el nombre 'resumen-{genero}.txt' con el formato:
        "De los {n} lanzamientos recolectados pertenecientes al genero {genero} se recolectaron:
            - {m} albums
            - {ñ} sencillos
        con total de {o} lanzamientos que no sabemos en qué fecha salieron jsjs"
"""

import pandas as pd
import requests, time, os

genero = 'salsa' # genero a buscar

# 1 carpeta para guardar los archivos csv resultantes ------
os.makedirs(f'{genero}', exist_ok=True) 
# archivo .txt que tendrá el resumen
resumen_path = os.path.join(f'{genero}', f'resumen-{genero}.txt')
open(resumen_path,'a',encoding='utf-8').close()

base_url = "https://musicbrainz.org/ws/2" # endpoint de la api
url = f'{base_url}/release-group' # url a visitar
headers = {'User-Agent': 'buscador-natits/1.0 (a357417@uach.mx)'} # identificador
datos = [] # lista para guardar los datos específicos de cada lanzamiento solicitado

# cíclo para tener un total de 1000 canciones, recopilando de 100 en 100 para no saturar la api
for offset in range(0, 1000, 100): 
    # parametros de las solicitudes
    params = {
        'query': f'tag:{genero}',
        'fmt': 'json',
        'limit': 100,
        'offset': offset
    }
    print(f'Consultando offset {offset}...') # para saber en qué parte de las solicitudes vamos
    # realizamos la solicitud
    lanzamientos = requests.get(url, headers=headers, params=params).json().get('release-groups', [])
    
    # de los datos encontrados, guardamos unicamente los que necesitamos
    for lanzamiento in lanzamientos:
        try:
            # Buscar el primer id catalogado como oficial
            realizaciones = lanzamiento.get('releases', [])
            id_oficial = ''
            for ids in realizaciones:
                if ids.get('status') == 'Official':
                    id_oficial = ids.get('id')
                    break
                    
            datos.append({
                'titulo': lanzamiento['title'],
                'tipo': lanzamiento['primary-type'],
                'artista': lanzamiento['artist-credit'][0]['name'],
                'fecha-lanzamiento': lanzamiento.get('first-release-date', ''),
                'generos':', '.join([tag['name'] for tag in lanzamiento.get('tags', [])]),
                'id': id_oficial
            })
        except Exception as e:
            print(f'Error al procesar canción: {e}')
            
    # para imprimir los datos
    for i in range(offset,offset+100,1):
        try: 
            print(f'{datos[i]}\n')
        except:
            print("Alguno de los campos está vacío\n")

    time.sleep(1)  # para no saturar la API

print(f'Fin de las solicitudes\nProcesando datos...\n')

bd = pd.DataFrame(datos) # crear dataframe 
bd.drop_duplicates(inplace=True) # eliminar duplicados
print(f'eliminando duplicados...\n')

# se estandariza el formato de la fecha y se enlistan índices de los errores ---------------
errores = [] # para guardar los lanzamientos que no tengan fechas
print(f'estandarizando fechas...\n')
for i, fecha in bd['fecha-lanzamiento'].items(): # iteramos en la columna fecha-lanzmainto teniendo en cuenta el indice
    if pd.isna(fecha) or fecha == '': # revisamos que sí haya un dato en la casilla
        errores.append(i) # guardamos el indice del lanzamiento con error
    else:# guardamos unicamente los primeros 4 caracteres (el año)
        fecha_str = str(fecha) # lo hacemos string  
        if len(fecha_str) != 4: 
            bd.at[i, 'fecha-lanzamiento'] = fecha_str[:4 ]

print(f'separando lanzamientos sin fecha...\n')
print(f'{errores}')
bd_errores = bd.loc[errores] # creamos un csv para los erroes
bd_errores.to_csv(os.path.join(f'{genero}', f'errores-{genero}.csv'), index=False) # lo guardamos en la carpeta
bd.drop(index=errores, inplace=True) # eliminamos los errores de la base original

print(f'ordenando cronológicamente los lanzamientos...\n')
bd.sort_values('fecha-lanzamiento', inplace=True) # ordenamos de menor a mayor

print(f'generando carpeta {genero}...\n')
print(f'guardando archivo carpeta 1000-lanzamientos-{genero}.csv ...\n')
bd.to_csv(os.path.join(f'{genero}', f'1000-lanzamientos-{genero}.csv'), index=False) # guardamos el csv en la carpeta

print(f'guardando un archivo csv con lanzamientos "unicos" de salsa...')
bd_unicos = bd[bd['generos'].apply(lambda x: ',' not in str(x))]
bd_unicos.to_csv(os.path.join(f'{genero}', f'lanzamientos-unicos-{genero}.csv'), index=False) 



print(f'generando archivo resumen-{genero}.txt ...\n')
with open(resumen_path, 'a', encoding='utf-8') as f:
    f.write(f'----- reusmen {genero} -----\n')
    f.write(f'se recolectaron un total de \t{len(bd)} lanzamientos\n')
    f.write(f'que incluyen:\n')
    

print(f'generando archivos csv para cada tipo de lanzamiento ...\n')
tdl = bd.groupby('tipo').size() # tdl := tipos de lanzamientos
for tipo, n in tdl.items(): # creamos un csv para cada tipo de lanzamiento
    bd_tipo = bd[bd['tipo'] == tipo]
    # escribimos en el resumen 
    with open(resumen_path, 'a', encoding='utf-8') as f:
        f.write(f'\t{tipo} {len(bd_tipo)}\n')
    
    # lo guardamos en la carpeta creada    
    ruta = os.path.join(f'{genero}', f'{tipo}-{genero}.csv') 
    bd_tipo.to_csv(ruta, index=False)

with open(resumen_path, 'a', encoding='utf-8') as f:
    f.write(f'además de {len(bd_errores)} lanzamientos sin fechas registradas\n')
    f.write(f'y {len(bd_unicos)} lanzamientos únicos\n')



print(f'Listo.\n')

