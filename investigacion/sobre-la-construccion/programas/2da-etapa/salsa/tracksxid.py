"""
Por cada id recabado en el archivo csv de lanzamientos únicos, en caso de que corresponda a una recopilacion (album, ep, etc), se recolectan los nombres de las canciones pertenecientes a dicha recopilacion
"""

import pandas as pd
import requests, time, os

base_url = 'https://musicbrainz.org/ws/2/release' # endpoint de la api
headers = {'User-Agent': 'buscador-natits/1.0 (a357417@uach.mx)'} # identificador
params = {'fmt': 'json', 'inc': 'recordings'}

bd = pd.read_csv('lanzamientos-unicos-salsa.csv') # Tomar el csv
datos = [] # para guardar los datos generados
i=1
print(f'haremos esto {len(bd)} veces')
for _, lanzamiento in bd.iterrows():  # Iterar por filas

    print(f'{i}/{len(bd)}\n')
    i+=1
    tipo = lanzamiento['tipo']
    print(f'Tenemos un {tipo}\n')
    if str(tipo) != 'Single':
        try:
            lanz_id = ''
            lanz_id = lanzamiento['id']
            url = f'{base_url}/{lanz_id}' # url a visitar
            media = requests.get(url, headers=headers, params=params).json() # solicitud
            canciones = media['media'][0]['tracks']
            if canciones: # si existen elementos en 'media'0'traks'
                print(f'con {len(canciones)} canciones\n')
                for cancion in canciones:
                    try:
                        datos.append({
                        'cancion': cancion['title'],
                        'artista': lanzamiento['artista'],
                        'tipo': lanzamiento['tipo'],
                        'lanzamiento': lanzamiento['titulo'],
                        'fecha-lanzamiento': lanzamiento['fecha-lanzamiento']
                        })
                    except Exception as e:
                        print(f'Error al procesar canción: {e}')
                    
                    print('guardadas:)\n')
                    time.sleep(1)  # pa no saturar la api
        except:
            print('Este lanzamiento no es una recopilacion\n')


canciones_unicas = pd.DataFrame(datos)
canciones_unicas.to_csv('canciones-de-lanzamientos-unicos.csv', index=False)

print('\nlisto:)')



       

