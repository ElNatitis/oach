""" EXPONENTES DE HURST PARA GRÁFICOS
Se visitan los datos disponibles en el archivo "flutuaciones-{genero}.csv" el cual debe encontrarse en la misma carpeta que este script. Dicho archivo deberá contener las 'columnas_necesarias' declaradas. Se realizarán los siguientes procesos sobre el arhcivo:

    1) Se agrupan los datos en función de la columna "cancion_id"
    2) Dentro de cada cancion, agrupamos en función de la columna "instrumento"
    3) Dentro de cada instrumento, agrupamos en función de la columna "grado_polinomio"
    4) Para cada grado disponible llevamos a cabo lo siguiente:
        4.1) Aplicamos 'numpy.log10()' tanto en la columna "tamano_segmento" como en las columnas "f_nota", "f_volumen" y "f_dura"
        4.2) Determinamos la pendiente y la instersección con 'linregress(,)' del "tamano_segmento" con respecto a las columnas "f_nota", "f_volumen" y "f_dura"
             Los resultados se almacenan en un dataframe con el siguiente formato
             exponentes.append({
                                            'cancion_id': ,
                                            'instrumento',
                                            'grado_polinomio': ,
                                            'variable': (tono,volumen o duracion),
                                            'pendiente': ,
                                            'interseccion': ,
                                            'x_min': x.min(),
                                            'x_max': x.max()
                                        })
    5) Una vez visitado todas las canciones del archivo, se guarda el dataframe en un csv llamado 'exponentes-{genero}.csv'
""" 

import pandas 
import matplotlib.pyplot as plt
from pathlib import Path
import numpy
from scipy.stats import linregress

columnas_necesarias = ['cancion_id','instrumento','tamano_segmento','grado_polinomio','f_nota','f_volumen','f_dura']

exponentes = []

def graficas_log_log(datos, i, inst, grado):
    # 1. Transformamos a log10 (Trabajaremos todo en este espacio)
    x = numpy.log10(datos["tamano_segmento"])
    y_n = numpy.log10(datos["f_nota"]) 
    y_v = numpy.log10(datos["f_volumen"]) 
    y_d = numpy.log10(datos["f_dura"]) 

    # 2. Ajustes lineales
    s1, int1, _, _, _ = linregress(x, y_n)
    s2, int2, _, _, _ = linregress(x, y_v)
    s3, int3, _, _, _ = linregress(x, y_d)
    
    exponentes.append({
            'cancion_id': i,
            'instrumento': inst,
            'grado': grado,
            'variable': "nota",
            'pendiente': s1,
            'interseccion': int1,
            'x_min': x.min(),
            'x_max': x.max()
        })
        
    exponentes.append({
            'cancion_id': i,
            'instrumento': inst,
            'grado': grado,
            'variable': "volumen",
            'pendiente': s2,
            'interseccion': int2,
            'x_min': x.min(),
            'x_max': x.max()
        })
        
    exponentes.append({
            'cancion_id': i,
            'instrumento': inst,
            'grado': grado,
            'variable': "dura",
            'pendiente': s3,
            'interseccion': int3,
            'x_min': x.min(),
            'x_max': x.max()
        })




# Ruta de trabajo (misma carpeta donde está el script)
carpeta = Path(__file__).parent
genero = "fluctuaciones-salsa.csv"
ruta = carpeta/genero
if ruta.exists():
    print("\nSe encontró el archivo. Todo tranqui por aquí")
    canciones = pandas.read_csv(ruta)
    if set(canciones.columns) == set(columnas_necesarias):
        print("El archivo tiene todas las columnas necesarias")
        for i, cancion in canciones.groupby("cancion_id"):
            print(f"Para la cancion {i} tenemos...")
            for inst, datos in cancion.groupby("instrumento"):
                print(f"\tpara el instrumento {inst} tenemos...")
                for grado, fluctuaciones in datos.groupby("grado_polinomio"):
                    print(f"\t\ten el grado {grado}")
                    graficas_log_log(fluctuaciones, i, inst, grado)
    else:
        print("ERROR - el archivo no contiene las columnas necesarias")
else:
    print("ERROR - no se encontró el archivo")
    
exp = pandas.DataFrame(exponentes)
exp.to_csv(carpeta/"exponentes-salsa.csv", index=False, encoding='utf-8')
