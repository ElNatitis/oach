"""
Lo que intento hacer con esto es relaizar busquedas simples y terminar de dimencionar cómo funcionan las consultas
A futuro busco generar un buscador de canciones pertenecientes a ciertos generos en un intervalo de años especifico
"""


import requests # libreria para acceder a la API 

# endpoint de la base de musicbrainz que vamos a visitar
base_url = "https://musicbrainz.org/ws/2"
# cosas que pide musicbrainz para identificarme
headers = {'User-Agent': 'buscador-natits/1.0 (a357417@uach.mx)'}

# parametros de la consulta
params = {
    'query': 'tag:salsa AND primarytype:Single', 
    'fmt': 'json',
    'limit': 10
}

# url a visitar
url = f'{base_url}/release-group'

respuesta = requests.get(url, headers=headers, params=params).json()['release-groups']

for i in respuesta:
    try: 
        print(f'{i["title"],i["artist-credit"][0]["name"],i["first-release-date"]}\n')
    except:
        print("Alguno de los campos está vacío\n")

