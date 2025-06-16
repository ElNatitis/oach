"""
Se consulta el endpoint de Musicbrainz necesario para obtener el 'tracklist' de los lanzamientos únicos de un género 
"""

import pandas as pd
import requests, time, os




id_lanzamiento = '63030607-6ae1-425c-9c61-c896b631716d' 
base_url = 'https://musicbrainz.org/ws/2/release' # endpoint de la api
headers = {'User-Agent': 'buscador-natits/1.0 (a357417@uach.mx)'} # identificador
params = {'fmt': 'json', 'inc': 'recordings'}
url = f'{base_url}/{id_lanzamiento}' # url a visitar


media = requests.get(url, headers=headers, params=params).json()
canciones = media['media'][0]['tracks']
for cancion in canciones:
    n = cancion['number']
    titulo = cancion['title']
    print(f'{n} \t {titulo}\n')

