"""
Buscador de gurpos de lanzamietnos en la API de musicbrainz con las siguientes características 

    - Correspondientes a sencillos (no albums, EP, LP, etc)
    - Pertenecientes a un genero especifico
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
        'query': 'tag:cumbia AND primarytype:Single',
        'fmt': 'json',
        'limit': 100,
        'offset': offset
    }

    print(f'Consultando offset {offset}...')
    canciones = requests.get(url, headers=headers, params=params).json().get('release-groups', [])

    for cancion in canciones:
        try:
            datos.append({
                'cancion': cancion['title'],
                'artista': cancion['artist-credit'][0]['name'],
                'fecha-lanzamiento': cancion.get('first-release-date', ''),
                'generos':', '.join([tag['name'] for tag in cancion.get('tags', [])])
            })
        except Exception as e:
            print(f'Error al procesar canción: {e}')

    time.sleep(1)  # Esperar para no saturar la API

# Crear DataFrame y guardar
bd = pd.DataFrame(datos)
print(f'Total canciones guardadas: {len(bd)}')
bd.drop_duplicates()
bd.to_csv('1000-canciones-de-cumbia.csv', index=False)
print(f'Total canciones guardadas: {len(bd)}')

