"""
Buscador de gurpos de lanzamietnos, en la API de musicbrainz, pertenecientes a un genero especifico
Esto, independientemente de si es un album, sencillo, ep, etc
"""

import requests
import pandas as pd
import time

base_url = "https://musicbrainz.org/ws/2"
url = f'{base_url}/release-group'
headers = {'User-Agent': 'buscador-natits/1.0 (a357417@uach.mx)'}

datos = []

# Cíclo para tener un total de 1000 canciones, recopilando de 100 en 100
for offset in range(0, 1000, 100):  # 0, 100, ..., 900
    params = {
        'query': 'tag:cumbia',
        'fmt': 'json',
        'limit': 100,
        'offset': offset
    }

    print(f'Consultando offset {offset}...')
    canciones = requests.get(url, headers=headers, params=params).json().get('release-groups', [])

    for cancion in canciones:
        try:
            datos.append({
                'titulo': cancion['title'],
                'tipo': cancion['primary-type'],
                'artista': cancion['artist-credit'][0]['name'],
                'fecha-lanzamiento': cancion.get('first-release-date', ''),
                'generos':', '.join([tag['name'] for tag in cancion.get('tags', [])])
            })
        except Exception as e:
            print(f'Error al procesar canción: {e}')
            
    # para imprimir los datos
    i=0
    for cancion in canciones:
        try: 
            print(f'{i+1} - {(cancion["title"], cancion["artist-credit"][0]["name"], cancion.get("first-release-date", "Sin fecha"), cancion.get("tags", "Sin tags")), cancion["primary-type"]}\n')
        except:
            print("Alguno de los campos está vacío\n")
        i=i+1

    time.sleep(10)  # para no saturar la API


bd = pd.DataFrame(datos) # crear dataframe 
print(f'Total canciones guardadas: {len(bd)}')
bd.drop_duplicates() # eliminar duplicados
print(f'Total canciones sin duplicados: {len(bd)}')
bd.to_csv('1000-lanzamientos-de-cumbia.csv', index=False)
