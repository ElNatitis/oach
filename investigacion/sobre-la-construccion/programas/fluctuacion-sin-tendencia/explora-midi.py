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
    
    
    
print(grupos.size())

