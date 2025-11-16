"""
Buscador de gurpos de lanzamietnos en la API de musicbrainz con las siguientes características 

    - Correspondientes a sencillos (no albums, EP, LP, etc)
    - Pertenecientes a un genero especifico
    - Con un intervalo de fechas de lanzamiento 
"""

import requests 


base_url = "https://musicbrainz.org/ws/2" # endpoint
url = f'{base_url}/release-group' # url a visitar
headers = {'User-Agent': 'buscador-natits/1.0 (a357417@uach.mx)'} # identificador

# parametros de la consulta
params = {
    'query': 'tag:cumbia AND primarytype:Single', 
    'fmt': 'json',
    'limit': 100
    'offset':0
}

canciones = requests.get(url, headers=headers, params=params).json()['release-groups'] # para realizar la consulta
i=0 # aux

# para imprimir los datos
for cancion in canciones:
    try: 
        print(f'{i+1} - {(cancion["title"], cancion["artist-credit"][0]["name"], cancion.get("first-release-date", "Sin fecha"), cancion.get("tags", "Sin tags"))}\n')
    except:
        print("Alguno de los campos está vacío\n")
    i=i+1

# para convertirlos a csv
datos = []
for cancion in canciones:
    try:
        datos.append({
            'cancion': cancion['title'],
            'artista': cancion['artist-credit'][0]['name'],
            'fecha-lanzamiento': cancion.get('first-release-date', ''),
            'generos':', '.join([tag['name'] for tag in cancion.get('tags', [])])
        })
    except Exception as e:
        print(f'Error en cancion: {e}')
        
for dato in datos:
    print(f"{dato}\n")



