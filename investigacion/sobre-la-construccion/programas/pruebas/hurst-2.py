""" CALCULA EXPONENTES DE HURST 
Se determina, utilizando el documento "flutuaciones-{genero}.csv", el exponente de hurst (en promedio y de cada canción) correspondiente a las fluctuaciones en relación del tamaño de segmento y grado de polinomio de simulación utilizado.

Se aplica la propiedad 

$t^{2\alpha} = t^{2+2H} -> H = \alpha -1$

Donde \alpha viene a ser el exponente que se determina calculando el cambio de las fluctuaciones con respecto al tamaño de los segmentos. 
Las fluctuaciones a su vez se sub dividen en fluctuaciones con simulaicones de grado 1, 2, 3,..,N

Por cada grado de polinomio tenemos un exponente diferente, por lo que el programa detemina un exponente para cada grado de poliniomio disponible en el documento

El exponente se calcula restandole 1 a la pendiente de la recta ajustada en una grafica log log

Tambien se guardan las graficas de esas rectas (de cada cancion y en promedio) en la carpeta {graficas-log-log}
"""

import pandas 
import matplotlib.pyplot as plt
from pathlib import Path
import numpy
from scipy.stats import linregress

columnas_necesarias = ['cancion_id','instrumento','tamano_segmento','grado_polinomio','f_nota','f_volumen','f_dura']

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
    
    plt.figure(figsize=(10, 7))

    # 3. Graficar Tonos (Nota)
    plt.scatter(x, y_n, label=f"Tonos (H={s1-1:.2f})", color='blue', marker='o')
    plt.plot(x, s1 * x + int1, color='blue', linestyle='--', alpha=0.6)

    # 4. Graficar Volumen
    plt.scatter(x, y_v, label=f"Volumen (H={s2-1:.2f})", color='green', marker='s')
    plt.plot(x, s2 * x + int2, color='green', linestyle='--', alpha=0.6)

    # 5. Graficar Duración
    plt.scatter(x, y_d, label=f"Duración (H={s3-1:.2f})", color='red', marker='^')
    plt.plot(x, s3 * x + int3, color='red', linestyle='--', alpha=0.6)

    # Configuración de etiquetas
    plt.xlabel("log10(Tamaño de segmento)")
    plt.ylabel("log10(Fluctuaciones)")
    plt.title(f"Canción: {i} | Inst: {inst} | Polinomio: {grado}")
    plt.legend(loc='best') 
    plt.grid(True, alpha=0.3)
    
    # Guardar
    plt.savefig(f'loglog-c{i}-i{inst}-g{grado}.png')
    plt.close() 
    
   
          
    
    
 


# Hace falta diseñar una función que solo revica el csv y luego lo trabaje para gernar los graficos log log log, de paso seria buenoq ue los guarde con sus nombres epecificos para que ṕodamos llamar la funcion para cada cancion y tambien al podamos llamar para el promedio de las canciones

## algo deberíamos hacer tambien con el almacenar los datos, ya que hay un grafico ginal que generar que consiste en tener la recta de el rpiomedio de todas lacs caiconoes y las demas rectas individuales apra observar categoricamente como se comportan
### el punto es poder revisar minusiosamente a ojo las fluctuaciones y me agrada el engoque de por instrumento mas que por cancion




# Ruta de trabajo (misma carpeta donde está el script)
carpeta = Path(__file__).parent
genero = "fluctuaciones-salsa-p.csv"
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
    print("No se armó:(")
