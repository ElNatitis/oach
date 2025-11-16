import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from scipy.stats import linregress

# Ruta de trabajo (misma carpeta donde está el script)
carpeta = Path(__file__).parent

# Lista de nombres de archivos CSV
archivos = [
    "Resumen_Celia_Cruz_-_Toro_Mata.csv", "Resumen_Compr_ndelo_-_Luis_Enrique.csv", "Resumen_El_Gran_Combo_-_Me_Liber_.csv", "Resumen_Frankie_Ruiz_-_Amor_de_un_Momento.csv", "Resumen_Frankie_Ruiz_-_La_Cura.csv",
    "Resumen_Frankie_Ruiz_-_Quiero_Llenarte.csv", "Resumen_Gran_Combo_-_La_Loma_del_Tamarindo.csv", "Resumen_H_ctor_Lavoe_-_D_jala_que_Siga.csv", "Resumen_Jerry_Rivera_-_Amores_como_el_Nuestro.csv", "Resumen_Orquesta_Guayac_n_-_Un_Vestido_Bonito__reconstruido_.csv",
    "Resumen_Richie_Ray_-_Ag_zate.csv", "Resumen_Rub_n_Blades_-_Pedro_Navaja.csv", "Resumen_The_Latin_Brothers_-_La_Guayaba.csv", "Resumen_The_Latin_Brothers_-_Patrona_de_los_Reclusos.csv", "Resumen_The_Latin_Brothers_-_Sobre_las_Olas.csv"
]

# Cargar y unir todos los DataFrames
dataframes = []
for archivo in archivos:
    ruta = carpeta / archivo
    if ruta.exists():
        df = pd.read_csv(ruta)
        dataframes.append(df)
    else:
        print(f"Archivo no encontrado: {archivo}")

# Concatenar todos los CSV
df_total = pd.concat(dataframes, ignore_index=True)

# Asegurar que las columnas clave sean numéricas
df_total["Tamaño_segmento"] = pd.to_numeric(df_total["Tamaño_segmento"], errors="coerce")
df_total["f_tono"] = pd.to_numeric(df_total["f_tono"], errors="coerce")
df_total["f_volumen"] = pd.to_numeric(df_total["f_volumen"], errors="coerce")
df_total["f_duraciones"] = pd.to_numeric(df_total["f_duraciones"], errors="coerce")

# Agrupar por tamaño de segmento y obtener promedio de cada columna
df_promedios = df_total.groupby("Tamaño_segmento")[["f_tono", "f_volumen", "f_duraciones"]].mean().reset_index()

# Mostrar resultado
print(df_promedios)

# Guardar a CSV si lo deseas
# df_promedios.to_csv("promedios_por_segmento.csv", index=False)

# Verifica que ya existe df_promedios (de paso, lo ordenamos)
df_promedios = df_promedios.sort_values(by="Tamaño_segmento")

# Crear gráfico log-log
plt.figure(figsize=(10, 6))
plt.loglog(df_promedios["Tamaño_segmento"], df_promedios["f_tono"], label="f_tono", marker='o')
plt.loglog(df_promedios["Tamaño_segmento"], df_promedios["f_volumen"], label="f_volumen", marker='s')
plt.loglog(df_promedios["Tamaño_segmento"], df_promedios["f_duraciones"], label="f_duraciones", marker='^')

# Etiquetas y formato
plt.xlabel("Tamaño de segmento (log)", fontsize=12)
plt.ylabel("Promedio de fluctuaciones (log)", fontsize=12)
plt.title("Promedios de fluctuaciones por tamaño de segmento (log-log)", fontsize=14)
plt.legend()
plt.grid(True, which="both", ls="--", linewidth=0.5)

# Mostrar gráfico
plt.tight_layout()
plt.show()


# Filtramos y transformamos a log10
x = np.log10(df_promedios["Tamaño_segmento"])
y_1 = np.log10(df_promedios["f_tono"]) 
y_2 = np.log10(df_promedios["f_volumen"]) 
y_3 = np.log10(df_promedios["f_duraciones"]) 

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
plt.title("Estimación de la pendiente tono")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Graficar
plt.figure(figsize=(8, 6))
plt.plot(x, y_2, 'o', label='Datos log-log')
plt.plot(x, y2_fit, 'r--', label=f'Ajuste lineal\npendiente (α) ≈ {slope2:.4f}')
plt.xlabel("log10(Tamaño de segmento)")
plt.ylabel("log10(F)")
plt.title("Estimación de la pendiente volumen")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Graficar
plt.figure(figsize=(8, 6))
plt.plot(x, y_3, 'o', label='Datos log-log')
plt.plot(x, y3_fit, 'r--', label=f'Ajuste lineal\npendiente (α) ≈ {slope3:.4f}')
plt.xlabel("log10(Tamaño de segmento)")
plt.ylabel("log10(F)")
plt.title("Estimación de la pendiente duraciones")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


h_tono = slope1 - 1
h_volumen = slope2 - 1
h_dura = slope3 - 1

print(f"exp_tono = {h_tono}\n exp_volumen = {h_volumen}\n exp_dura = {h_dura}")
