import pandas as pd
from pathlib import Path

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

