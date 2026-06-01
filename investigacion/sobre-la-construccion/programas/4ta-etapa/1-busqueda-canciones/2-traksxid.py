"""
Nombre: 
    2-traksxid.py
Objetivo:
    recolectar los nombres de las canciones pertenecientes a recopilaciones (album, ep, etc) dentro del archivo 'lanzamientos-unicos-{'genero'}.csv
Autor:
    natits.
Fecha:
    8 de mayo 2026
Versión:
    1.0.0
Dependencias:
    pandas
    requests
    time
    os
Entradas:
    genero (str)
    lanzamientos-unicos-{genero}.csv
Columnas esperadas:
    - titulo
    - tipo
    - artista
    - fecha-lanzamiento
    - id
Salidas:
    canciones-de-{genero}.csv
Descripción del pipeline:
    Se realizan los siguientes procesos:
        1.- se valida la existencia del documento 'lanzamientos-unicos-{'genero'}.csv'
        2.- se visita cada fila en el documento para que, en caso de que el lanzamiento se trate de una recopilación, recolectar el id 
        3.- a travez del id se solicita a la API de musicbrainz los nombres de las canciones pertenecientes a la recopilación 
        4.- se enlista 'title' junto con su respectivo 'artista', 'tipo', 'lanzamiento', 'fecha-lanzamiento' y 'id'
        5.- se genera y guarda un archivo con la lista final bajo el nombre 'canciones de {genero}.csv'
"""

# librerías
import pandas as pd
import requests, time, os

# para la solicitudes de la API
base_url = 'https://musicbrainz.org/ws/2/release' # endpoint de la api
headers = {'User-Agent': 'buscador-natits/1.0 (a357417@uach.mx)'} # identificador
params = {'fmt': 'json', 'inc': 'recordings'}

genero = 'bachata' # genero con el que se está trabajando

# archivo .log que tendrá el registro del pipeline
log_path = os.path.join(f'{genero}', f'pipeline-traksxid-{genero}.log')
open(log_path, 'w', encoding='utf-8').close()

# función para escribir en el log
def log(mensaje, nivel="INFO"):
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f'[{nivel}] {mensaje}\n')

# validar si existe el archivo
archivo_entrada = os.path.join(f'{genero}', f'lanzamientos-unicos-{genero}.csv')
if not os.path.exists(archivo_entrada):
    log(f'No existe el archivo {archivo_entrada}', 'ERROR')
    raise FileNotFoundError(f'No existe {archivo_entrada}')

log(f'Archivo de entrada encontrado: {archivo_entrada}')
bd = pd.read_csv(archivo_entrada)
log(f'Se cargaron {len(bd)} lanzamientos')

datos = []

# ------------------------------------------------------------
# RECOLECCIÓN DE NOMBRES
# ------------------------------------------------------------

for i, (_, lanzamiento) in enumerate(bd.iterrows(), start=1):
    tipo = lanzamiento['tipo']
    lanz_id = lanzamiento['id']
    
    log(f'[{i}/{len(bd)}] Procesando lanzamiento id={lanz_id}')
    if str(tipo) != 'Single':
        try:
            log(f'El lanzamiento {lanz_id} es una recopilación tipo {tipo}')
            log(f'Revisando url correspondiente')
            url = f'{base_url}/{lanz_id}' # url a visitar
            media = requests.get(url, headers=headers, params=params).json() # solicitud
            canciones = media['media'][0]['tracks']
            if canciones:
                log(f'La recopilación tipo {tipo} tiene {len(canciones)} canciones')
                for cancion in canciones:
                    try:
                        datos.append({
                        'cancion': cancion['title'],
                        'artista': lanzamiento['artista'],
                        'tipo': lanzamiento['tipo'],
                        'lanzamiento': lanzamiento['titulo'],
                        'fecha-lanzamiento': lanzamiento['fecha-lanzamiento'],
                        'id': cancion['recording']['id']
                        })
                    except Exception as e:
                        log(f'Error al procesar canción: {e}','ERROR')
                
                time.sleep(2)  # pa no saturar la api
            else:
                log(f'Esta recopilación no tiene canciones','ERROR')
        except Exception as e:
            log(f'Error consultando id={lanz_id}: {e}','ERROR')
    else:
        log(f'Se omite id={lanz_id} porque es Single', 'WARNING')

# ------------------------------------------------------------
# GUARDAR RESULTADOS
# ------------------------------------------------------------
archivo_salida = os.path.join(f'{genero}', f'canciones-de-{genero}.csv')
canciones_unicas = pd.DataFrame(datos)
canciones_unicas.to_csv(archivo_salida, index=False)
log(f'Archivo generado correctamente')
log('Pipeline finalizado')

