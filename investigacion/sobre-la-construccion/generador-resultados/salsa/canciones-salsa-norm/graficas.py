import pandas as pd
import matplotlib.pyplot as plt
import os

# === 1. Cargar el archivo CSV ===
filename = "frankie-ruiz---tu-con-el-(karaoplay.com)-norm.csv"

if not os.path.exists(filename):
    raise FileNotFoundError(f"No se encontró el archivo {filename} en el directorio actual.")

df = pd.read_csv(filename)

# === 3) Normalizaciones ===
# nota y volumen: escalas MIDI 0-127
df['nota_norm'] = (df['nota'].clip(lower=0, upper=127)) / 127.0
df['volumen_norm'] = (df['volumen'].clip(lower=0, upper=127)) / 127.0


# === 2. Verificar columnas esperadas ===
# Se asume que las columnas son: 'instrumento', 'tono', 'volumen', 'dura'
columnas_esperadas = {'instrumento', 'nota', 'volumen', 'dura'}
if not columnas_esperadas.issubset(df.columns):
    raise ValueError(f"Faltan columnas en el CSV. Se esperaban: {columnas_esperadas}")

# === 3. Agrupar por instrumento ===
grupos = df.groupby('instrumento')

# Crear carpeta para guardar gráficos
os.makedirs("plots", exist_ok=True)

# === 4. Generar gráficos ===
for instr, datos in df.groupby('instrumento'):
    datos = datos.reset_index(drop=True)

    # === Crear subplots alineados ===
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    fig.suptitle(f"Instrumento: {instr} (Normalizado)", fontsize=14)

    # --- Subplot 1: nota ---
    axes[0].plot(datos.index, datos['nota_norm'], color='tab:blue')
    axes[0].set_ylabel("Nota\n[0-1]")
    axes[0].grid(True, linestyle='--', alpha=0.6)

    # --- Subplot 2: volumen ---
    axes[1].plot(datos.index, datos['volumen_norm'], color='tab:orange')
    axes[1].set_ylabel("Volumen\n[0-1]")
    axes[1].grid(True, linestyle='--', alpha=0.6)

    # --- Subplot 3: duración ---
    #axes[2].plot(datos.index, datos['dura_norm'], color='tab:green')
    #axes[2].set_ylabel("Duración\n[0-1]")
    #axes[2].set_xlabel("Índice (tiempo o muestra)")
    #axes[2].grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Guardar gráfico
    out_path = os.path.join("plots", f"{instr}_subplots.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"✅ Gráfico con subplots guardado: {out_path}")

print("🎵 Todos los gráficos fueron generados correctamente.")

