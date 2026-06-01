"""
Nombre:
    3-midi2csv.py
Objetivo:
    transformar archivos MIDI pertenecientes al género '{genero}' en distintos dataframes que contienen los tonos volumenes y duraciones de cada instrumento presente en el MIDI.
Autor:
    natits.
Fecha:
    8 de mayo 2026
Versión:
    1.0.0
Dependencias:
    pretty_midi
    pandas
    os
Entradas:
    genero (str)
    carpeta 'midis-{genero}'
Formatos de entrada esperados:
    - archivos .mid
    - archivos .midi
Salidas:
    carpeta 'canciones-{genero}'
    para cada canción:
        - {nombre_formateado}-norm.csv
Columnas generadas:
    dataframe 'cancion_normalizada':
        - instrumento_nombre
        - instrumento
        - nota
        - nota_nombre
        - volumen
        - dura
        - empieza
        - termina

Descripción del pipeline:
    Se realizan los siguientes procesos:
        0.- se valida la existencia de la carpeta 'midis-{genero}'                                                              
        1.- se genera la carpeta 'canciones-{genero}'                                                                           
        2.- se visitan todos los archivos MIDI dentro de la carpeta                                                             
        3.- para cada instrumento del MIDI se extraen:                                                                          
                - nombre del instrumento
                - número de nota MIDI
                - nombre de la nota
                - volumen
                - instante de inicio
                - instante de término
                - duración de la nota
        4.- se genera un dataframe llamado 'cancion' con los eventos musicales de todos los instrumentos                        
        5.- se agrupan notas simultáneas pertenecientes al mismo instrumento para:                                              
                - identificar acordes o eventos paralelos
                - calcular promedios de nota, volumen y duración
                - reemplazar múltiples eventos simultáneos por uno solo
        6.- se almacena el resultado anterior en el dataframe 'cancion_promediada'                                              
        7.- se identifican intervalos de silencio entre eventos consecutivos                                                    
        8.- los silencios son representados mediante:                                                                               
                - nota = -1
                - volumen = 0
                - nota_nombre = 'Silencio'
        9.- se almacena el resultado anterior en el dataframe 'cancion_con_ceros'                                               
        10.- se estima el tempo de la canción utilizando pretty_midi
        11.- se calcula la duración temporal correspondiente a una semidifusa dentro del tempo detectado
        12.- se normaliza temporalmente la canción mediante saltos delta uniformes
        13.- se rellena la estructura normalizada con:
                - eventos musicales
                - silencios
              para representar toda la duración de la canción
        14.- se almacena el resultado anterior en el dataframe 'cancion_normalizada'
        15.- se guarda 'cancion_normalizada' en formato CSV bajo el nombre '{nombre_formateado}-norm' en la carpeta 'canciones-{genero}'
        17.- se genera un archivo de registro '{nombre_formateado}-info.txt'
              con información detallada del procesamiento de cada canción
"""
# librerías
import pretty_midi 
import pandas 
import os

# Género musical con el que estamos trabajando
genero = 'prueba'

# archivo .log que tendrá el registro del pipeline
log_path = os.path.join(f'{genero}', f'pipeline-{genero}.log')
open(log_path, 'w', encoding='utf-8').close()

# función para escribir en el log
def log(mensaje, nivel="INFO"):
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f'[{nivel}] {mensaje}\n')
        
# ruta de la carpeta en la que guardaremos los datos tratados
os.makedirs(f'canciones-{genero}', exist_ok=True)

# validar la existencia de la carpeta
ruta_base = os.path.dirname(os.path.abspath(__file__)) # ruta del script
ruta_resultados = os.path.join(ruta_base, f"canciones-{genero}") # ruta de la carpeta con los midis
ruta_midis = os.path.join(ruta_base, f"midis-{genero}") 
log(f'Confirmando al existencia de la carpeta "midis-{genero}"')
if not os.path.exists(ruta_midis):
    log(f'No existe la carpeta {ruta_midis}','ERROR')
    raise FileNotFoundError(f"No existe la carpeta {ruta_midis}")

log(f'La carpeta midis-{genero} existe') 
archivos = os.listdir(ruta_midis) # lista que guarda los nombres de los archivos dentro de la carpeta señalada
log(f'Contiene {len(archivos)} canciones')
log(f'{archivos}')

for i, nombre_archivo in enumerate(archivos, start=1): # para visitar cada archivo de la carpeta
    print(f'\n{i}/{len(archivos)}')
    log(f"{nombre_archivo} es el archivo {i} de {len(archivos)}")
    nombre_formateado = os.path.splitext(nombre_archivo)[0].lower().replace(" ", "-") # para los nombres de la carpeta y los archivos 
    log(f'El nombre formateado es {nombre_formateado}')
    if nombre_archivo.endswith('.mid') or nombre_archivo.endswith('.midi'): # garantizamos que el archivo sea midi por su nombre
        try:
            ruta = os.path.join(f'{ruta_midis}', nombre_archivo) # ruta del archivo midi a trabajar
            midi = pretty_midi.PrettyMIDI(ruta) # leemos el midi y lo guardamos con la estructura de pretty_midi 
            eventos = [] # para almacenar los diferentes datos que componen la canción 
            instrumentos = midi.instruments
            if instrumentos:
                try:
                    log(f'Iniciando la construcción de la canción ')
                    for j, instrument in enumerate(instrumentos, start=1): # inicio construcción de canción
                        log(f'Leyendo el instrumento {j} de {len(instrumentos)}')
                        if instrument.is_drum: # para saber si el isntrumento corresponde a percuciones 
                            log(f'El instrumento {j} es una percusión')
                            nombre = "Percussion"
                            name = -1
                        else: 
                            name = instrument.program 
                            nombre = pretty_midi.program_to_instrument_name(instrument.program)
                        log(f'El instrumento {j} es tiene el nombre de {nombre} con id={name}')
                        
                        # iteramos en cada nota compone la canción
                        notas = instrument.notes
                        if notas:
                            try:
                                for note in notas: 
                                    eventos.append({ 
                                        'instrumento_nombre': nombre,
                                        'instrumento': name, 
                                        'nota': note.pitch, 
                                        'nota_nombre': pretty_midi.note_number_to_name(note.pitch),
                                        'volumen': note.velocity, 
                                        'dura': note.end - note.start, 
                                        'empieza': note.start, 
                                        'termina': note.end 
                                        }) 
                            except Exception as e:
                                log(f'Error leyendo las notas del el instrumento {j}: {e}','ERROR')
                        else:
                            log(f'No hay notas disponibles del instrumento {nombre}','ERROR')
                    
                    
                    # fin de construcción de canción
                    log(f'Fin de la construcción de la cancion')
                    cancion = pandas.DataFrame(eventos)
                    ruta_csv = os.path.join(ruta_resultados, f"{nombre_formateado}.csv") # ruta
                    cancion.to_csv(ruta_csv, index=False, encoding='utf-8') # creamos archivo csv
                    log(f'archivo {nombre_formateado}.csv" generado')
                    
                    # inicio de construcción cancion_prom
                    log('Iniciando la construcción de la cancion_prom ')
                    cancion_prom = [] # para almacenar los promedios
                    instrumentos = cancion.groupby('instrumento')# agrupamos para tener por separado cada instrumento de los eventos
                    log(f'{instrumentos}')
                    for i, ins in instrumentos: # iteramos sobre los instrumentos
                        ins = ins.sort_values(by="empieza").reset_index(drop=True) # reiniciamos el índice y ordenamos de menor a mayor con respecto a la columna "empieza"
                        log(f"{ins}")
                        log(f'el instrumento {ins["instrumento_nombre"]} tiene {len(ins)} notas en total')
                        j = 0
                        while j < len(ins): # iteramos en los renglones del instrumento, que son sus notas 
                            nota = ins.loc[j]
                            simultaneas = [] # para almacenar las notas que tengan el mismo valor en "empieza"
                            simultaneas.append(nota) # almacenamos la primer nota
                            k=1
                            momento = nota["empieza"]
                            log(f'la nota {j} empieza en el momento {momento}')
                            while j + k < len(ins):
                                siguiente = ins.loc[j+k,"empieza"]
                                if siguiente == momento:
                                    log(f'la nota {j+k} empieza en {siguiente}, entonces las tomamos como simultaneas, la almacenamos y revisamos la siguiente')
                                    simultaneas.append(ins.loc[j+k])
                                    k+=1
                                else:
                                    log(f'la nota {j+k} empieza en {siguiente}, entonces no las tomamos como simultaneas')
                                    break
                            log(f'hubo un total de {len(simultaneas)} notas simultaneas y son las siguientes')
                            j+=k
                            log(f'{simultaneas}')
                            log(f'almacenaremos el promedio de estas notas simultaneas que es el siguiente')
                            acorde = pandas.DataFrame(simultaneas)
                            promedio_simultaneas =  acorde[['instrumento','nota', 'volumen', 'dura', 'empieza']].mean()
                            log(f'{promedio_simultaneas}')
                            
                            cancion_prom.append({ 
                                'instrumento_nombre': nota["instrumento_nombre"],
                                'instrumento': nota["instrumento"], 
                                'nota': int(promedio_simultaneas["nota"]), 
                                'nota_nombre': pretty_midi.note_number_to_name(promedio_simultaneas["nota"]),
                                'volumen': int(promedio_simultaneas["volumen"]), 
                                'dura': promedio_simultaneas["dura"], 
                                'empieza': promedio_simultaneas["empieza"], 
                                'termina': promedio_simultaneas["empieza"] + promedio_simultaneas["dura"] 
                            })
                    
                    log('Fin de la construcción de la canción_prom')    
                    cancion_promediada = pandas.DataFrame(cancion_prom)
                    ruta_csv = os.path.join(ruta_resultados, f"{nombre_formateado}-prom.csv") # ruta
                    cancion_promediada.to_csv(ruta_csv, index=False, encoding='utf-8') # creamos archivo csv
                    log(f'archivo {nombre_formateado}-prom.csv" generado')
                    
                    
                    # inicio de la construcción de cancion_con_ceros
                    log('Iniciando la construcción de la cancion_con_ceros')
                    cancion_con_ceros = [] # para almacenar los promedios          
                    instrumentos_promediados = cancion_promediada.groupby('instrumento')# agrupamos para tener por separado cada instrumento de los eventos        
                    for i, ins in instrumentos_promediados: # iteramos sobre los instrumentos
                        log(f"{ins}")
                        log(f'el instrumento {ins["instrumento_nombre"]} tiene {len(ins)} notas en total')
                        j = 0
                        while j+1 < len(ins): # iteramos en los renglones del instrumento, que son sus notas 
                            ins = ins.reset_index(drop=True)
                            nota = ins.loc[j]
                            log(f"la nota {j} empieza en {nota['empieza']}")
                            log(f"almacenamos la nota en 'cancion_con_ceros'")        
                            cancion_con_ceros.append({ 
                                                    'instrumento_nombre': nota["instrumento_nombre"],
                                                    'instrumento': nota["instrumento"], 
                                                    'nota': nota["nota"], 
                                                    'nota_nombre': nota["nota_nombre"],
                                                    'volumen': nota["volumen"], 
                                                    'dura': nota["dura"], 
                                                    'empieza': nota["empieza"], 
                                                    'termina': nota["termina"] 
                                                })
                                                
                            log(f'verificamos si hay silencio antes de la nota {j+1}')
                            siguiente_nota = ins.loc[j+1]
                            termina_actual = float(nota["termina"])
                            empieza_siguiente = float(siguiente_nota["empieza"])
                            silencio = empieza_siguiente - termina_actual
                            if silencio > 0:
                                log(f"aquí va un silencio que duraría {silencio}")
                                # guardamos el silencio
                                nombre_nota_silencio = "Silencio"
                                cancion_con_ceros.append({
                                                    'instrumento_nombre': nota["instrumento_nombre"],
                                                    'instrumento': nota["instrumento"], 
                                                    'nota': -1, 
                                                    'nota_nombre': nombre_nota_silencio,
                                                    'volumen': 0.0, 
                                                    'dura': silencio, 
                                                    'empieza': termina_actual, 
                                                    'termina': empieza_siguiente 
                                                  })
                            elif silencio < 0:
                                log(f"aqui la nota {j+1} empieza antes de que la nota {j} termine")
                                cancion_con_ceros[-1]["termina"] = empieza_siguiente
                                cancion_con_ceros[-1]["dura"] = (empieza_siguiente - cancion_con_ceros[-1]["empieza"])
                                
                            else:
                                log(f'entre estas notas no hay silencios')
                            
                            j+=1

                    log('Fin de la construcción de la cancion_con_ceros')    
                    cancion_cc = pandas.DataFrame(cancion_con_ceros)
                    ruta_csv = os.path.join(ruta_resultados, f"{nombre_formateado}-cc.csv") # ruta
                    cancion_cc.to_csv(ruta_csv, index=False, encoding='utf-8') # creamos archivo csv
                    log(f'archivo {nombre_formateado}-cc.csv" generado')
                    
                    # inicio de la construcción de cancion_normalizada
                    log('Iniciando la construcción de la cancion_normalizada')
                    log('Para normalizar por semifusas tenemos:')
                    tempo = midi.get_tempo_changes()[1][0] # para obtener una estimacion del tempo de la cancion
                    log(f'la canción 0 tiene un tempo estimado por prettymidi de {tempo}, lo redondeamos a {round(tempo)}')
                    delta = (60 / round(tempo) ) / 16 # para saber cuántos segundos dura una 'semidifusa' en ese tempo
                    log(f'en la canción 0 una semifusa dura {delta} segundos con respecto a su tempo')
                    duracion_total = midi.get_end_time() # para saber la duración total en segundos
                    espacios_necesarios = round(duracion_total/delta) # semidifusas totales en la cancion
                    log(f'en la canción 0 tiene una duración total de {duracion_total} por lo que vamos a necesitar un total de {espacios_necesarios} espacios para almacenar los eventos de la canción')
                    cancion_norm = [] # para guardar los datos normalizados en saltos delta
                    instrumentos_con_ceros = cancion_cc.groupby('instrumento') # agrupamos la base de datos que contiene los silencios como ceros

                    for i, ins in instrumentos_con_ceros: # iteramos sobre los instrumentos
                        # verificamos si el instrumento empieza desde el segundo 0, sino, llenamos de silencios los espacios correspondientes del tiempo 0 al momento en que empieza
                        ins = ins.reset_index(drop=True)
                        nota_inicial = ins.loc[0]
                        nota_final = ins.loc[len(ins)-1]
                        log(f"iniciamos con el instrumento {nota_inicial['instrumento_nombre']}")
                        log(f'el instrumento {nota_inicial["instrumento_nombre"]} tiene {len(ins)} notas en total')
                        duracion_instrumento =  nota_final['termina'] - nota_inicial['empieza'].min()
                        espacios_por_datos = round(duracion_instrumento/delta)
                        espacios_sin_datos = espacios_necesarios - espacios_por_datos 
                        empieza = nota_inicial['empieza']
                        log(f'el instrumento {i} dura {duracion_instrumento} segundos que corresponden a {espacios_por_datos} espacios con datos y {espacios_sin_datos} espacios sin datos')
                        log(f'el instrumento {i} inicia en el segundo {empieza}')
                        espacios_llenados = 0 # variable auxiliar por si hay silencio al inicio de la canción
                        
                        if empieza != 0: # rellenar de ceros si el instrumento no empieza en el segundo cero
                            espacios_llenados = round(empieza/delta)
                            log(f'este instrumento no empieza en el segundo cero, empieza en el segundo {empieza} que corresponde a {espacios_llenados} espacios en silencio')    
                            k=0
                            while k < espacios_llenados:
                                k+=1
                                cancion_norm.append({
                                                        'instrumento_nombre': nota["instrumento_nombre"],
                                                        'instrumento': nota["instrumento"], 
                                                        'nota': -1, 
                                                        'nota_nombre': nombre_nota_silencio,
                                                        'volumen': 0.0, 
                                                        'empieza': 0,
                                                        'dura': nota["empieza"]
                                                    })
                            log(f'hemos llenado {espacios_llenados} eventos correspondientes a el silencio al principio de la canción')
                        else:
                            log(f'este instrumento empieza en el segundo cero')
                        
                        
                        # comenzamos a almacenar los eventos del instrumento en cancion_norm
                        j = 0
                        auxi = espacios_llenados*delta
                        
                        while j < len(ins): # iteramos en los renglones del instrumento, que son sus notas 
                            nota = ins.loc[j]
                            if j+1 < len (ins):
                                siguiente_nota = ins.loc[j+1]
                                if siguiente_nota["empieza"]!=nota["termina"]:
                                    log('aquí hay un empalme, podemos generar datos de más', 'WARNING')
                            espacio_inicio = round(nota["empieza"]/delta)
                            espacio_final = round(nota["termina"]/delta)
                            espacios_a_llenar = espacio_final - espacio_inicio 
                            log(f'los espacios a llenar son {espacios_a_llenar} ')
                            log(f'la nota {j} de {len(ins)} ({nota["nota_nombre"]}) empieza en {nota["empieza"]} y dura {nota["dura"]} segundos, lo que corresponde a {espacios_a_llenar} espacios por llenar')
                            
                            if espacios_a_llenar != 0: 
                                if espacio_final < espacios_necesarios:
                                    espacios_llenados += espacios_a_llenar
                                    k=0
                                    while k < espacios_a_llenar:
                                        cancion_norm.append({
                                                            'instrumento_nombre': nota["instrumento_nombre"],
                                                            'instrumento': nota["instrumento"], 
                                                            'nota': nota["nota"], 
                                                            'nota_nombre': nota["nota_nombre"],
                                                            'volumen': nota["volumen"], 
                                                            'empieza': nota["empieza"],
                                                            'dura': nota["dura"]
                                                        })
                                        k+=1
                                    log(f'se han almacenado {espacios_a_llenar} semifusas, llevamos {espacios_llenados} de las {espacios_necesarios} correspondientes a la canción')
                                else:
                                    log(f'llevamos {espacios_llenados} semifusas de {espacios_necesarios} y esta nota contiene {espacios_a_llenar},  faltan {len(ins)-j} notas del instrumento', 'ERROR')
                                    exit()
                                    
                            else:
                                log('La duración de la nota no alcanza para dividirla en semifusas')
                                   
                            j+=1
                            log(f'llevamos {espacios_llenados} espacios de {espacios_necesarios}')
                            

                        log(f'ya no hay más notas en el instrumento {nota["instrumento_nombre"]}')
                        
                        nota = ins.loc[len(ins)-1]
                        log(f'la última nota termina en el segundo {nota["termina"]}, mientras que la canción tiene una duración total de {duracion_total}')
                        if nota["termina"] < duracion_total:
                            segundos_silencio =  duracion_total - nota["termina"]
                            espacios_silencio_final = round(segundos_silencio/delta)
                            log(f'habíamos calculado un arreglo con {espacios_necesarios} espacios, llevamos {espacios_llenados} espacios llenados y con el silencio final serían {espacios_llenados + espacios_silencio_final}')
                            if espacios_llenados + espacios_silencio_final == espacios_necesarios:
                                k=0
                                while k < espacios_silencio_final:
                                    k+=1
                                    cancion_norm.append({
                                                            'instrumento_nombre': nota["instrumento_nombre"],
                                                            'instrumento': nota["instrumento"], 
                                                            'nota': -1, 
                                                            'nota_nombre': nombre_nota_silencio,
                                                            'volumen': 0.0, 
                                                            'empieza': nota["empieza"],
                                                            'dura': segundos_silencio
                                                        })
                                log(f'se han almacenado los {k} espacios correspondientes a silencio, tenemos un total de {espacios_llenados+k}')
                        elif espacios_llenados + espacios_silencio_final > espacios_necesarios:
                            log(f'vamos a ignorar {espacios_llenados + espacios_silencio_final - espacios_necesarios} espacios para evitar problemas')
                            espacios_silencio_final -= (espacios_llenados + espacios_silencio_final - espacios_necesarios)
                            k=0
                            while k < espacios_silencio_final:
                                k+=1
                                cancion_norm.append({
                                                        'instrumento_nombre': nota["instrumento_nombre"],
                                                        'instrumento': nota["instrumento"], 
                                                        'nota': -1, 
                                                        'nota_nombre': nombre_nota_silencio,
                                                        'volumen': 0.0, 
                                                        'empieza': nota["empieza"],
                                                        'dura': segundos_silencio
                                                    })
                            else:
                                log(f'el instrumento {nota["instrumento_nombre"]} debería tener {espacios_necesarios} espacios y generamos {espacios_llenados + espacios_silencio_final}','ERROR')
                                log(f'el instrumento {nota["instrumento_nombre"]} no se almacenará con los espacios necesarios','WARNING')
                                exit()

                        log(f'fin de la construcción del instrumento {nota["instrumento_nombre"]}')

                    log('Fin de la construcción de la cancion_norm')    
                    cancion_normalizada = pandas.DataFrame(cancion_norm)
                    cancion_normalizada = cancion_normalizada.sort_values(by=['instrumento', 'empieza']).reset_index(drop=True)
                    ruta_csv = os.path.join(ruta_resultados, f"{nombre_formateado}-norm.csv") # ruta
                    cancion_normalizada.to_csv(ruta_csv, index=False, encoding='utf-8') # creamos archivo csv
                    log(f'archivo {nombre_formateado}-norm.csv" generado')

                    
                except Exception as e:
                    log(f'Error leyendo el instrumento {j}: {e}','ERROR')
            else:
                log(f'No es posible leer los instrumentos del archivo {nombre_archivo}','ERROR')
        except Exception as e:
            log(f'Error leyendo el archivo {nombre_archivo}: {e}','ERROR')
    else:
        log(f'Se omite {nombre_archivo} porque no es un arhivo .midi o .mid', 'WARNING')

