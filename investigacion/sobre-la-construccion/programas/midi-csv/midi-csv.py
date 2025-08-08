"""
queremos visitar todos los archivos midi dentro de una carpeta y con cada uno hacer los siguientes procedimientos
    1 - extraer del midi los datos correpondientes de 
        'Track', 'Event Type', 'Midi Note', 'Note Name', 'Velocity', 'Duration (seconds)' y 'Time (seconds)'
    2 - guardar esos datos en un csv
    3 - a partir del csv generado, se genera uno nuevo donde uniformamos los intervalos de cambio 
"""

import pretty_midi
import pandas

# leemos el midi y lo guardamos con la estructura de pretty_midi
midi = pretty_midi.PrettyMIDI('frankieruiz-tu-con-el.mid')

# para almacenar los diferentes datos que componen la canción
eventos = []

# iteramos en cada instrumento del midi
for instrument in midi.instruments:
    # para saber si el instrumento corresponde a percuciones
    if instrument.is_drum:
        print("\nmira nomais")
        name = -1
    else:
        name = instrument.program
        
    # iteramos en cada nota compone la canción
    for note in instrument.notes:
        eventos.append({
            'instrumento': name,
            'nota': note.pitch,
            'volumen': note.velocity,
            'dura': note.end - note.start,
            'empieza': note.start,
            'termina': note.end
        })

# convertimos la lista en un data frame para poder operar con ella
cancion = pandas.DataFrame(eventos)   
cancion.to_csv('cancion.csv', index=False) # lo guardamos en la carpeta
# agrupamos para tener por separado cada instrumento de los eventos
instrumentos = cancion.groupby('instrumento')

print(f'\ntenemos un total de {len(instrumentos)} instrumentos que componen la canción')

# para almacenar los máximos y minimos de cada instrumento
max_t = [] # tiempos máximos
min_t = [] # tiempos mínimose
min_d = [] # duraciones mínimas

# iteramos sobre los intrumentos para almacenar los datos en los arreglos
for i, ins in instrumentos:
    print(f'\npara el instrumento {i} son {len(ins)} notas')
    print(f'con tiempos que van desde {ins["empieza"].min()} hasta {ins["termina"].max()}')
    print(f'el intervalo más pequeño es de {ins["dura"].min()}')
    
    # almacenamos los mínimos y máximos en cada arreglo
    max_t.append(float(ins["termina"].max()))
    min_t.append(float(ins["empieza"].min()))
    min_d.append(float(ins["dura"].min()))

interv = min(min_d)
duracion = max(max_t) - min(min_t)
espacios = int(duracion/interv)
print(f'\nentonces sabemos que todos las notas de todos los instrumentos ocurren en un intervalo de {duracion} segundos y que el intérvalo más pequeño es {interv}')
print(f'\nla canción dura entonces {duracion/60} minutos y vamos a ocupar listas de {espacios} espacios para almacenar todos los eventos')


# construimos la lista con ceros que contendrá los datos
rolita = []
for i in range(espacios):
    estructura = {
        'instrumento': 0,
        'nota': 0,
        'volumen': 0,
        'dura': 0
    }
    rolita.append(estructura)
    
    
# visitamos cada espacio guardando datos o dejando ceros cuando corresponde

# variables para hacer pruebas 
stop=5
aux=0 # variable que se reinicia
i=0 # indice
piano = instrumentos.get_group(0) # extraemos el grupo 0 de el df instrumentos
indx = piano.index.min() # vemos el indice inicial
print(piano.index)

for j, nota in piano.iterrows():
    if aux != stop:
        if 1: # este no es el if real pero quiero dejarlo porque se que necesito uno solo no se que condicion ocupo
            print(f'\n*** evento {i} ***')
            print(f'\ndentro de piano tenemos\n{nota}\n')
            delta = nota["dura"] # extraemos la cantidad de tiempo que dura la nota que eestamos analizando
            espacios = int(delta/interv) # caluclamos la cantidad de espacios que va a ocupar esa duracion
            print(f'\nesta nota dura {delta} segundos, entonces necesitamos {espacios} espacios de nuestro arrelgo')
            for seg in range(espacios): # iteramos solo esa cantidad de veces
                print(f'\n------ segmento {seg}')
                # guardamos los datos en nuestro arreglo rolita
                rolita[i]['instrumento'] = nota['instrumento']
                rolita[i]['nota'] = nota['nota']
                rolita[i]['volumen'] = nota['volumen']
                rolita[i]['dura'] = nota['dura']
                print(f'entonces en el momento {i} tenemos\n{rolita[i]}')
                i+=1
            
        #else:
        indx+=1
        aux+=1

    else:
        input("\nPresiona Enter para continuar...")
        aux = 0
  
      
