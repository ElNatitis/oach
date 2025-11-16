import os
import pandas as pd

def analizar_csvs():
    carpeta = os.path.join(os.getcwd(), "canciones-salsa-norm")

    if not os.path.exists(carpeta):
        print("❌ No se encontró la carpeta 'mi-carpeta' en el directorio actual.")
        return

    resultados = []

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".csv"):
            ruta = os.path.join(carpeta, archivo)

            try:
                df = pd.read_csv(ruta)

                if 'instrumento' not in df.columns:
                    print(f"⚠️  El archivo {archivo} no tiene una columna llamada 'instrumento'. Se omite.")
                    continue

                # Agrupar por instrumento y contar filas
                conteos = df.groupby('instrumento').size()

                if not conteos.empty:
                    filas_por_instrumento = conteos.iloc[0]  # todas las filas por grupo son iguales
                    num_instrumentos = len(conteos)         # número total de instrumentos
                    resultados.append([archivo, filas_por_instrumento, num_instrumentos])
                else:
                    print(f"⚠️  El archivo {archivo} no contiene datos tras agrupar.")
            except Exception as e:
                print(f"⚠️  Error procesando {archivo}: {e}")

    # Ordenar de mayor a menor por número de filas por instrumento
    resultados.sort(key=lambda x: x[1], reverse=True)

    # Mostrar resultados
    print("\n📊 Resultados (ordenados de mayor a menor por filas/instrumento):")
    print(f"{'Archivo':40s} {'Filas por instrumento':>25s} {'# Instrumentos':>18s}")
    print("-" * 85)
    for nombre, filas, num_inst in resultados:
        print(f"{nombre:40s} {filas:>25} {num_inst:>18}")

    return resultados


if __name__ == "__main__":
    analizar_csvs()

