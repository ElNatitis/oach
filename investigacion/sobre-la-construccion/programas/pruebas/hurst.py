""" CALCULA EXPONENTES DE HURST 
Se determina, utilizando el documento "flutuaciones-{genero}.csv", el exponente de hurst correspondiente a las fluctuaciones en relación del tamaño de segmento y grado de polinomio de simulación utilizado.

Se aplica la propiedad 

$t^{2\alpha} = t^{2+2H} -> H = \alpha -1$

Donde \alpha viene a ser el exponente que se determina calculando el cambio de las fluctuaciones con respecto al tamaño de los segmentos. 
Las fluctuaciones a su vez se sub dividen en fluctuaciones con simulaicones de grado 1, 2, 3,..,N

Por cada grado de polinomio tenemos un exponente diferente, por lo que el programa detemina un exponente para cada grado de poliniomio disponible en el documento

El exponente se calcula restandole 1 a la pendiente de la recta ajustada en una grafica log log

Tambien se guardan las graficas de esas rectas en la carpeta {graficas-log-log}
"""

import pandas 
import matplotlib.pyplot as plt
from pathlib import Path
import numpy
from scipy.stats import linregress

columnas_necesarias = ['cancion_id','instrumento','tamano_segmento','grado_polinomio','f_nota','f_volumen','f_dura']

# Ruta de trabajo (misma carpeta donde está el script)
carpeta = Path(__file__).parent
genero = "fluctuaciones-salsa.csv"
ruta = carpeta/genero
if ruta.exists():
    print("\nSe encontró el archivo. Todo tranqui por aquí")
    fluctuaciones = pandas.read_csv(ruta)
    if set(fluctuaciones.columns) == set(columnas_necesarias):
        print("El archivo tiene todas las columnas necesarias")
        for grado, fluc_gn in fluctuaciones.groupby("grado_polinomio"):
            print(f"Para el polinomio de grado {grado} tenemos...")
            fluc_gn_prom = fluc_gn.groupby("tamano_segmento")[["f_nota","f_volumen","f_dura"]].mean().reset_index()
            #print(fluc_gn_prom)
            # Crear gráfico log-log
            plt.figure(figsize=(10, 6))
            plt.loglog(fluc_gn_prom["tamano_segmento"], fluc_gn_prom["f_nota"], label="f_tono", marker='o')
            plt.loglog(fluc_gn_prom["tamano_segmento"], fluc_gn_prom["f_volumen"], label="f_volumen", marker='s')
            plt.loglog(fluc_gn_prom["tamano_segmento"], fluc_gn_prom["f_dura"], label="f_duraciones", marker='^')
            
            # Etiquetas y formato
            plt.xlabel("Tamaño de segmento (log)", fontsize=12)
            plt.ylabel("Promedio de fluctuaciones (log)", fontsize=12)
            plt.title(f"Promedios de fluctuaciones por tamaño de segmento (log-log) simuladas con polinomio de grado {grado}", fontsize=14)
            plt.legend()
            plt.grid(True, which="both", ls="--", linewidth=0.5)
            
            print("Guardando graficas log-log")
            plt.savefig(f'grafica-log-log-grado{grado}.png')
            
            # Filtramos y transformamos a log10
            x = numpy.log10(fluc_gn_prom["tamano_segmento"])
            y_1 = numpy.log10(fluc_gn_prom["f_nota"]) 
            y_2 = numpy.log10(fluc_gn_prom["f_volumen"]) 
            y_3 = numpy.log10(fluc_gn_prom["f_dura"]) 

            # Ajuste lineal
            slope1, intercept1, r_value1, p_value1, std_err1 = linregress(x, y_1)
            slope2, intercept2, r_value2, p_value2, std_err2 = linregress(x, y_2)
            slope3, intercept3, r_value3, p_value3, std_err3 = linregress(x, y_3)

            # Línea ajustada
            y1_fit = slope1 * x + intercept1
            y2_fit = slope2 * x + intercept2
            y3_fit = slope3 * x + intercept3

            # Graficar
            plt.figure(figsize=(8, 6))
            plt.plot(x, y_1, 'o', label='Datos log-log')
            plt.plot(x, y1_fit, 'r--', label=f'Ajuste lineal\npendiente (α) ≈ {slope1:.4f}')
            plt.xlabel("log10(Tamaño de segmento)")
            plt.ylabel("log10(F)")
            plt.title(f"Estimación de la pendiente tono simulada con grado {grado}")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f'estimacion-pendiente-tono-grado-{grado}.png')

            # Graficar
            plt.figure(figsize=(8, 6))
            plt.plot(x, y_2, 'o', label='Datos log-log')
            plt.plot(x, y2_fit, 'r--', label=f'Ajuste lineal\npendiente (α) ≈ {slope2:.4f}')
            plt.xlabel("log10(Tamaño de segmento)")
            plt.ylabel("log10(F)")
            plt.title(f"Estimación de la pendiente volumen simulada con grado {grado}")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f'estimacion-pendiente-volumen-grado-{grado}.png')


            # Graficar
            plt.figure(figsize=(8, 6))
            plt.plot(x, y_3, 'o', label='Datos log-log')
            plt.plot(x, y3_fit, 'r--', label=f'Ajuste lineal\npendiente (α) ≈ {slope3:.4f}')
            plt.xlabel("log10(Tamaño de segmento)")
            plt.ylabel("log10(F)")
            plt.title(f"Estimación de la pendiente duraciones simuladas con grado {grado}")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f'estimacion-pendiente-duraciones-grado-{grado}.png')
            
            h_tono = slope1 - 1
            h_volumen = slope2 - 1
            h_dura = slope3 - 1

            print(f"exp_tono = {h_tono}\texp_volumen = {h_volumen}\texp_dura = {h_dura}")


            
        
else:
    print("\nArchivo no encontrado")
    
    

