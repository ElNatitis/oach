""" 
queremos visitar todos los archivos midi dentro de la carpeta 'midi-{genero}' y con cada uno hacer los siguientes procedimientos 
    1 - extraer, de cada instrumento, los siguientes datos 
            - 'name' : nombre del instrumento
            - 'note.pitch' : número entero correspondiente a una nota musical del teclado de un piano
            - 'note.velocity' : volumen al que se toca esa nota
            - 'note.start' : momento de la canción en que empieza la nota (en segundos)
            - 'note.end' : momento de la canción en que termina la nota (en segundos)
        con esto tambien calculamos la variable 'dura' que es simplemente ('note.end' - 'note.start) y lo almacenamos un dataframe llamado 'cancion'
    2 - se visita el dataframe 'cancion' generado para:
            - identificar las notas simultaneas  
            - generar promedios de cada uno de sus valores
            - reemplazar las notas simultaneas por una sola fila con promedios
        almacenamos eso en un dataframe llamado 'cancion_prom'
    3 - se visita el dataframe 'cancion_prom' generado para:
            - identificar los intervalos de tiempo en lo que no hay notas sonando
            - llenar espacios de silencios dentro de la cancion con columnas con volumen 0 y nota -1
        almacenamos eso en un dataframe llamado 'cancion_cc'
    4 - con respecto al tempo de la canción: [esta parte esta en progreso]
            - genera una lista (que tiene la estructura de los dataframes anteriores) con la acantidad de 'semidifusas' (en segundos) que abarcan la canción 
            - se rellena esa lista con respecto a 'cancion_cc'
        almacenamos eso en un dataframe llamado 'cancion_norm'
    5 - guardar esos dataframes en formato csv dentro de otra carpeta llamada 'nombre_formateado'
            - cancion       -> 'nombre_formateado'.csv
            - cancion_prom  -> 'nombre_formateado'-prom.csv
            - cancion_cc    -> 'nombre_formateado'-cc.csv
            - cancion_norm  -> 'nombre_formateado'-norm.csv ------- *(de este csv se generarán los arreglos para el DFA)* 
""" 
import pretty_midi 
import pandas 
import os

##################################################### (1)
# Género musical con el que estamos trabajando
genero = 'salsa'

# ruta del script
ruta_base = os.path.dirname(os.path.abspath(__file__))
# ruta de la carpeta en la que guardaremos los datos tratados
os.makedirs(f'canciones-{genero}', exist_ok=True)
ruta_resultados = os.path.join(ruta_base, f"canciones-{genero}")
# ruta de la carpeta con los midis
ruta_midis = os.path.join(ruta_base, f"midis-{genero}") 
archivos = os.listdir(ruta_midis) # lista que guarda los nombres de los archivos dentro de la carptea señalada



# visitamos la carpeta correspondiente a los midis de este genero

terminal = 1

for nombre_archivo in archivos: # para visitar cada archivo de la carpeta
    print(f"vamos en el {terminal} de {len(archivos)}")
    terminal+=1
    if nombre_archivo.endswith('.mid') or nombre_archivo.endswith('.midi'): # garantizamos que el archivo sea midi por su nombre
        ##################################################### (5) (1/2)
        # generamos la carpeta con el nombre de la canción y un archivo .txt que tenga un resumen de la operación
        nombre_formateado = os.path.splitext(nombre_archivo)[0].lower().replace(" ", "-") # para los nombres de la carpeta y los archivos 
        ruta_cancion = os.path.join(ruta_resultados, nombre_formateado) # ruta para la carpeta que contendrá los resultados del tratamiento del midi
        os.makedirs(ruta_cancion, exist_ok=True) # creamos la carpeta en esa ruta
        # archivo .txt que tendrá el resumen
        ruta_resumen = os.path.join(ruta_cancion, f"{nombre_formateado}-info.txt")
        with open(ruta_resumen, 'w', encoding='utf-8') as f:
            f.write(f"Trabajaremos con la cancion {nombre_archivo}.\n")
            
        def log(mensaje, ruta):
            with open(ruta, 'a', encoding='utf-8') as f:
                f.write(mensaje + '\n')
        
        ##################################################### (fin de 5)
        ruta = os.path.join(f'{ruta_midis}', nombre_archivo) # ruta del archivo midi a trabajar
        log(f"{ruta}",ruta_resumen)
        
        midi = pretty_midi.PrettyMIDI(ruta) # leemos el midi y lo guardamos con la estructura de pretty_midi 
        eventos = [] # para almacenar los diferentes datos que componen la canción 
        # iteramos en cada instrumento del midi 
        print("instrumentos")
        terminal_instrumentos = 1
        for instrument in midi.instruments: 
            print(f"vamos en {terminal_instrumentos} de {len(midi.instruments)}")
            terminal_instrumentos+=1
            if instrument.is_drum: # para saber si el isntrumento corresponde a percuciones 
                log("\nmira nomais",ruta_resumen)
                nombre = "Percussion"
                name = -1
            else: 
                name = instrument.program 
                nombre = pretty_midi.program_to_instrument_name(instrument.program)
            # iteramos en cada nota compone la canción 
            for note in instrument.notes: 
                eventos.append({ 
                    'Instrumento': nombre,
                    'instrumento': name, 
                    'nota': note.pitch, 
                    'nombre': pretty_midi.note_number_to_name(note.pitch),
                    'volumen': note.velocity, 
                    'dura': note.end - note.start, 
                    'empieza': note.start, 
                    'termina': note.end }) 
        # convertimos la lista en un dataframe para poder operar con ella 
        cancion = pandas.DataFrame(eventos) 
        ##################################################### (2)
        # para almacenar los promedios
        cancion_prom = []
        # agrupamos para tener por separado cada instrumento de los eventos
        instrumentos = cancion.groupby('instrumento') 
        s=0 # variable auxiliar
        for _, ins in instrumentos: # iteramos sobre cada instrumento
            i=0 # contador
            ins = ins.reset_index(drop=True) # reiniciamos el índice
            while i < len(ins): # iteramos sobre cada nota dentro del instrumento
                nota = ins.loc[i] # localizamos la nota correspondiente a i 
                momento = nota["empieza"]  # almacenamos el momento en el que empieza
                log(f'la {i} nota empieza en el momento {momento}',ruta_resumen)
                simultaneas = [] # para almacenar las notas que tengan el mismo valor en "empieza"
                simultaneas.append(nota) # almacenamos la primera nota      
                # para observar durante la ejecución
                for dato in simultaneas:
                    log(f'\n{dato}',ruta_resumen)
                # más variables auxiliares
                aux = True
                j=1 
                while i + j < len(ins): # visitamos los momentos siguientes para revisar si tienen el mismo valor en "empieza"
                    siguiente = ins.loc[i+j, 'empieza'] # localizamos el siguiente
                    log(f'\nla siguiente empieza en el momento {siguiente} entonces...',ruta_resumen)
                    if momento == siguiente: # decidimos si guardarla o no
                        simultaneas.append(ins.loc[i+j])
                        log(f'\nla guardamos\n',ruta_resumen)
                        j+=1
                    else:
                        log('\nnos detenemos:)',ruta_resumen)
                        break
                i+=j # para saltar los renglones promediados
                s+=1
                log(f'\n{s} de {len(cancion)}',ruta_resumen) # honestamente no recuerdo que hace esto 
                log(f'\nencontramos {len(simultaneas)} notas que empiezan en {momento}',ruta_resumen)
                # pasamos el arreglo a un dataframe para trabajar mas fácil
                df_simultaneas = pandas.DataFrame(simultaneas)
                # los datos que nos importan de las notas simultáneas
                log(f'\ntrabajamos con:',ruta_resumen)
                log(f"{df_simultaneas[['nota', 'volumen', 'dura', 'empieza', 'termina']]}",ruta_resumen)
                # calculamos promedios
                promedios = df_simultaneas[['instrumento','nota', 'volumen', 'dura', 'empieza', 'termina']].mean()
                log(f"\npromedios:\nnota={int(promedios['nota'])}, volumen={int(promedios['volumen'])}, duración={promedios['dura']}, empieza={promedios['empieza']}, termina={promedios['termina']}",ruta_resumen)
                # almacenamos dentro de la cancion los datos reemplazando las simultaneas por una sola fila
                cancion_prom.append({
                    'instrumento': promedios['instrumento'],
                    'nota': int(promedios['nota']),
                    'volumen': int(promedios['volumen']),
                    'dura': promedios['dura'],
                    'empieza': promedios['empieza'],
                    'termina': promedios['empieza'] + promedios['dura']
                    })
        cancion_promediada = pandas.DataFrame(cancion_prom)
        ##################################################### (3)
        cancion_cc = [] # para guardar la cacnion con ceros
        s=0 # variable auxiliar
        instrumentos = cancion_promediada.groupby('instrumento') # agrupamos para tener por separado cada instrumento de los eventos
        for _, ins in instrumentos: # iteramos sobre cada instrumento
            i=0
            ins = ins.reset_index(drop=True) # reiniciamos el índice
            while i < len(ins): # iteramos sobre cada elemento dentro del instrumento
                cancion_cc.append(ins.loc[i].to_dict()) # guardamos la nota actual en el arreglo con ceros
                if i+1 < len(ins):
                    termina = ins.loc[i,'termina']
                    siguiente = ins.loc[i+1, 'empieza']
                    silencio = siguiente - termina
                    if silencio > 0:
                        log(f"\naquí va un silencio que duraría {silencio}",ruta_resumen)
                        # guardamos el silencio
                        cancion_cc.append({
                                'instrumento': int(ins.loc[i,'instrumento']),
                                'nota': -1,
                                'volumen': 0.0,
                                'dura': float(silencio),
                                'empieza': float(termina),
                                'termina': float(siguiente)
                            })
                    else:
                        log(f'\nentre estas notas no hay silencios',ruta_resumen)
                else:
                    log('\nterminamos el instrumento:)',ruta_resumen)
                i+=1
                s+=1
        cancion_con_ceros = pandas.DataFrame(cancion_cc) 
        ##################################################### (4)
        tempo = round(midi.get_tempo_changes()[1][0])  # para obtener una estimacion del tempo de la cancion
        delta = (60 / tempo) / 16 # para saber cuántos segundos dura una 'semidifusa' en ese tempo
        duracion_total = midi.get_end_time() # para saber la duración total en segundos
        espacios_necesarios = round(duracion_total/delta) # semidifusas totales en la cancion
        log(f"{tempo}",ruta_resumen)
        log(f"{delta}",ruta_resumen)
        log(f"La duración total es de {duracion_total} segundos",ruta_resumen)
        log(f'\n entonces haremos un arreglo con {int(duracion_total/delta)}',ruta_resumen)
        cancion_norm = [] # para guardar los datos normalizados en saltos delta
        
        instrumentos = cancion_con_ceros.groupby('instrumento') # agrupamos la base de datos que contiene los silencios como ceros
        for i, inst in instrumentos: # iteramos sobre cada instrumento 
            j=0 # un contador de eventos con salto delta
            duracion_instrumento =  inst['termina'].max() - inst['empieza'].min()
            espacios_por_datos = round(duracion_instrumento/delta)
            espacios_sin_datos = espacios_necesarios - espacios_por_datos 
            log(f'el instrumento {i} dura {duracion_instrumento} segundos que corresponden a {espacios_por_datos} espacios con datos y {espacios_sin_datos} espacios sin datos',ruta_resumen)
            auxi = 0 # tiempo en el que estamos por los saltos delta dados
            if inst['empieza'].min() != 0: # rellenar de ceros si el instrumento no empieza en el segundo cero
                espacios_silencio = int(inst['empieza'].min()/delta)
                log(f'este instrumento no empieza en el segundo cero, empieza en el {inst["empieza"].min()} que corresponde a {espacios_silencio} espacios en silencio',ruta_resumen)
                espacios_por_datos += espacios_silencio
                while j<espacios_silencio:
                    j+=1
                    cancion_norm.append({
                            'instrumento': i,
                            'nota': -1,
                            'volumen': 0,
                            'dura': inst['empieza'].min(),
                            'empieza': 0,
                            'termina': inst['empieza'].min()
                            })
                    auxi += delta
            
        
        
            # visitar los eventos haciendo saltos delta para verificar el evento ocurriendo en cada salto     
            for _, evento in inst.iterrows(): # iteramos sobre las filas de cada intrumento
                espacios_a_llenar = round((evento["termina"]-auxi)/delta)
                if espacios_a_llenar != 0:
                    log(f'estamos en {auxi} y el evento termina en {evento["termina"]}, llenamos {espacios_a_llenar}, actualmente tenemos {j} de los {espacios_por_datos},{evento["termina"] - auxi} > {delta/2}',ruta_resumen)
                    cont = 0
                    while cont < espacios_a_llenar:
                        if j < espacios_por_datos:
                            cancion_norm.append({
                                'instrumento': evento['instrumento'],
                                'nota': evento['nota'],
                                'volumen': evento['volumen'],
                                'dura': evento['dura'],
                                'empieza': evento['empieza'],
                                'termina': evento['termina']
                                })
                            auxi += delta
                            j+=1
                            aux_termina = evento['termina']
                        cont+=1
        
            # rellenar de ceros en caso de que el evento final no coincida con el final de la cancion 
            resta_final = espacios_necesarios - j
            if resta_final != 0:
                log(f'estamos en {auxi} y no hay más eventos, la cancion termina en {duracion_total}, llevamos {j} de {espacios_necesarios} agregaremos {resta_final} de espacios de silencio',ruta_resumen)
                k = 0
                while k < resta_final:
                    cancion_norm.append({
                                'instrumento': i,
                                'nota': -1,
                                'volumen': 0,
                                'dura': duracion_total - aux_termina,
                                'empieza': aux_termina,
                                'termina': duracion_total
                            })
                    auxi += delta
                    j+=1
                    k+=1
            log('listote\n',ruta_resumen) 
        cancion_normalizada = pandas.DataFrame(cancion_norm) # lo guardamos en un dataframe
        

        cuenta_eventos = cancion_normalizada.groupby('instrumento').size()
        log(f"{cuenta_eventos}",ruta_resumen)

        log(f"{tempo}",ruta_resumen)
        log(f"{delta}",ruta_resumen)
        log(f"La duración total es de {duracion_total} segundos",ruta_resumen)
        log(f'\n entonces haremos un arreglo con {espacios_necesarios} espacios',ruta_resumen)
        
        ##################################################### (5) (2/2)
        # guardamos lo dataframes como csv en la carpeta de la canción 
        # 'cancion'
        ruta_csv = os.path.join(ruta_cancion, f"{nombre_formateado}.csv") # ruta
        cancion.to_csv(ruta_csv, index=False, encoding='utf-8') # creamos archivo csv
        
        # 'cancion_promediada'
        ruta_csv_prom = os.path.join(ruta_cancion, f"{nombre_formateado}-prom.csv") # ruta
        cancion_promediada.to_csv(ruta_csv_prom, index=False, encoding='utf-8') # creamos archivo csv
        
        # 'cancion_con_ceros'
        ruta_csv_cc = os.path.join(ruta_cancion, f"{nombre_formateado}-cc.csv") # ruta
        cancion_con_ceros.to_csv(ruta_csv_cc, index=False, encoding='utf-8') # creamos archivo csv
        
        # 'cancion_normalizada'
        ruta_csv_norm = os.path.join(ruta_cancion, f"{nombre_formateado}-norm.csv") # ruta
        cancion_normalizada.to_csv(ruta_csv_norm, index=False, encoding='utf-8') # creamos archivo csv
        


