"""
Nombre: 
    buscadorxgenero.py
Objetivo:
    Recolectar gurpos de lanzamientos pertenecientes a un '{genero}' especifico usando la API de MusicBrainz.
    Los grupos de lanzamientos pueden ser álbum, sencillo, ep, etc.
Autor:
    natits.
Fecha:
    7 de mayo 2026
Versión:
    1.0.0
Dependencias:
    pandas
    requests
Entradas:
    genero (str)
Salidas:
    1000-lanzamientos-{genero}.csv
    errores-{genero}.csv
    resumen-{genero}.txt
Descripción del pipeline:
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

# librerías
import pandas as pd
import requests, time, os

genero = 'bachata' # genero a buscar

# 1 carpeta para guardar los archivos csv resultantes ------
os.makedirs(f'{genero}', exist_ok=True) 

# archivo .log que tendrá el registro del pipeline
log_path = os.path.join(f'{genero}', f'pipeline-{genero}.log')
open(log_path, 'a', encoding='utf-8').close()

# función para escribir en el log
def log(mensaje, nivel="INFO"):
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f'[{nivel}] {mensaje}\n')

## SOLICITUDES

# para las solicitudes a la API
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
    log(f'Consultando offset {offset}...')

    # realizamos la solicitud
    lanzamientos = requests.get(url, headers=headers, params=params).json().get('release-groups', [])
    log(f'Se recolectaron {len(lanzamientos)} lanzamientos en offset {offset}')

    # de los datos encontrados, guardamos únicamente los que necesitamos
    for lanzamiento in lanzamientos:
        try:
            # Buscar el primer id catalogado como oficial
            realizaciones = lanzamiento.get('releases', [])
            id_oficial = ''
            for ids in realizaciones:
                if ids.get('status') == 'Official':
                    id_oficial = ids.get('id')
                    break
            
            # Agregamos el lanzamiento a la lista
            datos.append({
                'titulo': lanzamiento['title'],
                'tipo': lanzamiento['primary-type'],
                'artista': lanzamiento['artist-credit'][0]['name'],
                'fecha-lanzamiento': lanzamiento.get('first-release-date', ''),
                'generos': ', '.join([tag['name'] for tag in lanzamiento.get('tags', [])]),
                'id': id_oficial
            })

        except Exception as e:
            log(
                f'Error al procesar lanzamiento: {e}',
                nivel="ERROR"
            )
    
    log(f'Finalizado offset {offset}')
    time.sleep(2)  # para no saturar la API

log('Fin de las solicitudes')
log('Procesando datos...')

## CONSTRUCCIÓN DE CSV

log('Construyendo DataFrame...')
bd = pd.DataFrame(datos)

log(f'Se construyó DataFrame con {len(bd)} registros')

# eliminar duplicados
n_original = len(bd)
bd.drop_duplicates(inplace=True)

n_sin_duplicados = len(bd)
duplicados_eliminados = n_original - n_sin_duplicados

log(f'Se eliminaron {duplicados_eliminados} registros duplicados')
log(f'Base de datos actual: {n_sin_duplicados} registros')

# ---------------------------------------------------------
# estandarización de fechas
# ---------------------------------------------------------

errores = []

log('Iniciando estandarización de fechas...')

for i, fecha in bd['fecha-lanzamiento'].items():
    # revisar datos vacíos
    if pd.isna(fecha) or fecha == '':
        errores.append(i)
    else:
        fecha_str = str(fecha)
        # convertir YYYY-MM-DD -> YYYY
        if len(fecha_str) != 4:
            bd.at[i, 'fecha-lanzamiento'] = fecha_str[:4]

log(f'Se detectaron {len(errores)} lanzamientos sin fecha')

# ---------------------------------------------------------
# separar errores
# ---------------------------------------------------------

log('Separando lanzamientos sin fecha...')

bd_errores = bd.loc[errores]

ruta_errores = os.path.join(f'{genero}',f'errores-{genero}.csv')
bd_errores.to_csv(ruta_errores, index=False)

log(f'Archivo de errores guardado en:')
log(f'{ruta_errores}')

# eliminar errores de la base principal
bd.drop(index=errores, inplace=True)

log(f'Base de datos depurada: {len(bd)} registros válidos')

# ---------------------------------------------------------
# ordenar cronológicamente
# ---------------------------------------------------------

log('Ordenando cronológicamente los lanzamientos...')
bd.sort_values('fecha-lanzamiento', inplace=True)
log('Orden cronológico completado')

# ---------------------------------------------------------
# guardar base principal
# ---------------------------------------------------------

ruta_principal = os.path.join(f'{genero}',f'1000-lanzamientos-{genero}.csv')
log(f'Guardando archivo principal:')
log(f'{ruta_principal}')
bd.to_csv(ruta_principal, index=False)
log('Archivo principal guardado correctamente')

# ---------------------------------------------------------
# lanzamientos únicos
# ---------------------------------------------------------

log('Generando archivo de lanzamientos únicos...')

bd_unicos = bd[bd['generos'].apply(lambda x: ',' not in str(x))]
ruta_unicos = os.path.join(f'{genero}',f'lanzamientos-unicos-{genero}.csv')
bd_unicos.to_csv(ruta_unicos, index=False)
log(f'Se guardaron {len(bd_unicos)} lanzamientos únicos')
log(f'Ruta: {ruta_unicos}')



log(f'Generando archivo resumen-{genero}.txt ...')

# archivo .txt que tendrá el registro del pipeline
resumen_path = os.path.join(f'{genero}', f'resumen-{genero}.txt')
open(resumen_path, 'a', encoding='utf-8').close()

with open(resumen_path, 'a', encoding='utf-8') as f:
    f.write(f'==============================\n')
    f.write(f'RESUMEN DEL GÉNERO: {genero}\n')
    f.write(f'==============================\n\n')
    f.write(f'Total de lanzamientos válidos:\n')
    f.write(f'    {len(bd)}\n\n')
    f.write(f'Lanzamientos sin fecha:\n')
    f.write(f'    {len(bd_errores)}\n\n')
    f.write(f'Lanzamientos únicos:\n')
    f.write(f'    {len(bd_unicos)}\n\n')
    f.write(f'Distribución por tipo:\n')

log('Generando archivos csv por tipo de lanzamiento...')

tdl = bd.groupby('tipo').size()

for tipo, n in tdl.items():
    log(f'Procesando tipo "{tipo}" con {n} registros')
    bd_tipo = bd[bd['tipo'] == tipo]
    # escribir en resumen
    with open(resumen_path, 'a', encoding='utf-8') as f:
        f.write(f'    - {tipo}: {n}\n')
    # guardar csv
    ruta = os.path.join(
        f'{genero}',
        f'{tipo}-{genero}.csv'
    )
    bd_tipo.to_csv(ruta, index=False)
    log(f'Archivo guardado: {ruta}')

with open(resumen_path, 'a', encoding='utf-8') as f:
    f.write(f'\nProceso completado correctamente.\n')

log('Resumen final generado correctamente')
log('Pipeline finalizado')

