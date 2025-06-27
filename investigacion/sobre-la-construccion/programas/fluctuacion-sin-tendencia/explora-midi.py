"""
Queremos terminar de entender comos e compone un midi y en cómo adaptar nuestro análisis a esa composición
"""

import pandas as pd
import os

bd = pd.read_csv('frankie-ruiz-tu-con-el.csv') # Tomar el csv

grupos = bd.groupby(['Track'])

print(f'{grupos}')

for nombre, grupo in grupos:
    print(f"\nGrupo: {nombre}")
    print(grupo)

# obtener el mínimo de la columna 'Time (seconds)'
minimos = grupos['Duration (seconds)'].min()
print(minimos)
    
    
    
print(grupos.size())

tiempo_total = 292.918956
segmento_mas_corto = 0.012887
segmentos_necesarios = int(tiempo_total/segmento_mas_corto)


print(f'el segmento mas corto es de {segmento_mas_corto}, mientras que la canción dura un total de {tiempo_total}\n')
print(f'lo que significa que necesitamos un arreglo con {segmentos_necesarios} segmentos para capturar todos los datos')

inst1 = bd[bd['Track']==0]
print(f'{inst1}')

salto = 0

datos = []

# iteramos en la columnas de el csv teniendo en cuenta el indice
for _, evento in inst1.iterrows():
    bloque = float(evento['Duration (seconds)'])
    print(f'dentro de este evento, estamos en un segmento de {bloque} segundos \n')
    print(f'eso significa que necesitamos {int(bloque/segmento_mas_corto)} segmentos para este evento\n')
    print(f'vamos en el segundo {salto}\n')
    if 
    while salto < bloque:
        datos.append({
                'inst': evento['Track'],
                'nota-midi': evento['Midi Note'],
                'volumen': evento['Velocity'],
                'duracion': bloque,
                'momento': salto
            })
        salto+=segmento_mas_corto
        print(f'{salto}\n')
pr = pd.DataFrame(datos)    
pr.to_csv('grupo0.csv', index=False) # lo guardamos en la carpeta
