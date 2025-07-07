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
    # para saber si el isntrumento corresponde a percuciones
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

# convertimos la lista en un dat frame para poder operar con ella
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

duracion = max(max_t) - min(min_t)
espacios = int(duracion/min(min_d))
print(f'\nentonces sabemos que todos las notas de todos los instrumentos ocurren en un intervalo de {duracion} segundos y que el intérvalo más pequeño es {min(min_d)}')
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
    
    
for i, evento in rolita:
    
    
