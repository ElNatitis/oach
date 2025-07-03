"""
queremos visitar todos los archivos midi dentro de una carpeta y con cada uno hacer los siguientes procedimientos
    1 - extraer del midi los datos correpondientes de 
        'Track', 'Event Type', 'Midi Note', 'Note Name', 'Velocity', 'Duration (seconds)' y 'Time (seconds)'
    2 - guardar esos datos en un csv
    3 - a partir del csv generado, se genera uno nuevo donde uniformamos los intervalos de cambio 
"""

import pretty_midi
import pandas

midi = pretty_midi.PrettyMIDI('frankieruiz-tu-con-el.mid')
datos = []
for instrument in midi.instruments:
    for note in instrument.notes:
        datos.append({
            'nombre': f'{instrument.program}',
            'nota': f'{note.pitch}',
            'empieza': f'{note.start}',
            'termina': f'{note.end}',
            'volumen': f'{note.velocity}'
        })
        


print(f'{datos}')
    

