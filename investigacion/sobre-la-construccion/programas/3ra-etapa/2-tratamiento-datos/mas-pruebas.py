import pretty_midi 
import pandas 
import os

cancion_cc = pandas.read_csv('frankie-ruiz---tu-con-el-(karaoplay.com)-cc.csv') # Tomar el csv
la_cancion = pandas.DataFrame(cancion_cc)


midi = pretty_midi.PrettyMIDI('Frankie Ruiz - Tu con el (karaoplay.com).mid')
tempo = round(midi.get_tempo_changes()[1][0])  # para obtener una estimacion del tempo de la cancion
delta = (60 / tempo) / 16 # para saber cuántos segundos dura una 'semidifusa' en ese tempo
duracion_total = midi.get_end_time() # para saber la duración total en segundos
espacios_necesarios = round(duracion_total/delta)
print(tempo)
print(delta)
print(f"La duración total es de {duracion_total} segundos")
print(f'entonces haremos un arreglo con {espacios_necesarios} espacios')
cancion_norm = []

decimales = 3
instrumentos = la_cancion.groupby('instrumento')
for i, inst in instrumentos:
    j=0
    duracion_instrumento =  inst['termina'].max() - inst['empieza'].min()
    espacios_por_datos = round(duracion_instrumento/delta)
    espacios_sin_datos = espacios_necesarios - espacios_por_datos 
    print(f'el instrumento {i} dura {duracion_instrumento} segundos que corresponden a {espacios_por_datos} espacios con datos y {espacios_sin_datos} espacios sin datos')
    auxi = 0
    
    
    # rellenar de ceros si el instrumento no empieza en el segundo cero
    if inst['empieza'].min() != 0:
        espacios_silencio = int(inst['empieza'].min()/delta)
        print(f'este instrumento no empieza en el segundo cero, empieza en el {inst["empieza"].min()} que corresponde a {espacios_silencio} espacios en silencio')
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
    for _, evento in inst.iterrows():
        espacios_a_llenar = round((evento["termina"]-auxi)/delta)
        if espacios_a_llenar != 0:
            print(f'estamos en {auxi} y el evento termina en {evento["termina"]}, llenamos {espacios_a_llenar}, actualmente tenemos {j} de los {espacios_por_datos},{evento["termina"] - auxi} > {delta/2}')
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
        print(f'estamos en {auxi} y no hay más eventos, la cancion termina en {duracion_total}, llevamos {j} de {espacios_necesarios} agregaremos {resta_final} de espacios de silencio')
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
print('listote\n') 
    


df_norm = pandas.DataFrame(cancion_norm)
df_norm.to_csv('cancion-normalizada.csv', index=False)

cuenta_eventos = df_norm.groupby('instrumento').size()
print(cuenta_eventos)

print(tempo)
print(delta)
print(f"La duración total es de {duracion_total} segundos")
print(f'\n entonces haremos un arreglo con {espacios_necesarios} espacios')



