import pandas as pd
import matplotlib.pyplot as plt
import os

# === 0. Diccionario General MIDI (0–127) ===
MIDI_INSTRUMENTS = {
    0: "Acoustic Grand Piano", 1: "Bright Acoustic Piano", 2: "Electric Grand Piano",
    3: "Honky-tonk Piano", 4: "Electric Piano 1", 5: "Electric Piano 2",
    6: "Harpsichord", 7: "Clavinet", 8: "Celesta", 9: "Glockenspiel",
    10: "Music Box", 11: "Vibraphone", 12: "Marimba", 13: "Xylophone",
    14: "Tubular Bells", 15: "Dulcimer", 16: "Drawbar Organ", 17: "Percussive Organ",
    18: "Rock Organ", 19: "Church Organ", 20: "Reed Organ", 21: "Accordion",
    22: "Harmonica", 23: "Tango Accordion", 24: "Acoustic Guitar (nylon)",
    25: "Acoustic Guitar (steel)", 26: "Electric Guitar (jazz)",
    27: "Electric Guitar (clean)", 28: "Electric Guitar (muted)",
    29: "Overdriven Guitar", 30: "Distortion Guitar", 31: "Guitar Harmonics",
    32: "Acoustic Bass", 33: "Electric Bass (finger)", 34: "Electric Bass (pick)",
    35: "Fretless Bass", 36: "Slap Bass 1", 37: "Slap Bass 2", 38: "Synth Bass 1",
    39: "Synth Bass 2", 40: "Violin", 41: "Viola", 42: "Cello", 43: "Contrabass",
    44: "Tremolo Strings", 45: "Pizzicato Strings", 46: "Orchestral Harp",
    47: "Timpani", 48: "String Ensemble 1", 49: "String Ensemble 2",
    50: "Synth Strings 1", 51: "Synth Strings 2", 52: "Choir Aahs", 53: "Voice Oohs",
    54: "Synth Choir", 55: "Orchestra Hit", 56: "Trumpet", 57: "Trombone",
    58: "Tuba", 59: "Muted Trumpet", 60: "French Horn", 61: "Brass Section",
    62: "Synth Brass 1", 63: "Synth Brass 2", 64: "Soprano Sax", 65: "Alto Sax",
    66: "Tenor Sax", 67: "Baritone Sax", 68: "Oboe", 69: "English Horn",
    70: "Bassoon", 71: "Clarinet", 72: "Piccolo", 73: "Flute", 74: "Recorder",
    75: "Pan Flute", 76: "Blown Bottle", 77: "Shakuhachi", 78: "Whistle",
    79: "Ocarina", 80: "Lead 1 (square)", 81: "Lead 2 (sawtooth)",
    82: "Lead 3 (calliope)", 83: "Lead 4 (chiff)", 84: "Lead 5 (charang)",
    85: "Lead 6 (voice)", 86: "Lead 7 (fifths)", 87: "Lead 8 (bass+lead)",
    88: "Pad 1 (new age)", 89: "Pad 2 (warm)", 90: "Pad 3 (polysynth)",
    91: "Pad 4 (choir)", 92: "Pad 5 (bowed)", 93: "Pad 6 (metallic)",
    94: "Pad 7 (halo)", 95: "Pad 8 (sweep)", 96: "FX 1 (rain)", 97: "FX 2 (soundtrack)",
    98: "FX 3 (crystal)", 99: "FX 4 (atmosphere)", 100: "FX 5 (brightness)",
    101: "FX 6 (goblins)", 102: "FX 7 (echoes)", 103: "FX 8 (sci-fi)",
    104: "Sitar", 105: "Banjo", 106: "Shamisen", 107: "Koto", 108: "Kalimba",
    109: "Bagpipe", 110: "Fiddle", 111: "Shanai", 112: "Tinkle Bell", 113: "Agogo",
    114: "Steel Drums", 115: "Woodblock", 116: "Taiko Drum", 117: "Melodic Tom",
    118: "Synth Drum", 119: "Reverse Cymbal", 120: "Guitar Fret Noise",
    121: "Breath Noise", 122: "Seashore", 123: "Bird Tweet", 124: "Telephone Ring",
    125: "Helicopter", 126: "Applause", 127: "Gunshot"
}

# === Función para obtener el nombre del instrumento ===
def get_instrument_name(num):
    if num == -1:
        return "Percusión"
    return MIDI_INSTRUMENTS.get(num, f"Instrumento {num}")

# === 1. Cargar el archivo CSV ===
filename = "frankie-ruiz---tu-con-el-(karaoplay.com).csv"

if not os.path.exists(filename):
    raise FileNotFoundError(f"No se encontró el archivo {filename} en el directorio actual.")

df = pd.read_csv(filename)

# === 2. Verificar columnas esperadas ===
columnas_esperadas = {'instrumento', 'nota', 'volumen', 'dura'}
if not columnas_esperadas.issubset(df.columns):
    raise ValueError(f"Faltan columnas en el CSV. Se esperaban: {columnas_esperadas}")

# === 3. Normalizaciones ===
df['nota_norm'] = (df['nota'].clip(lower=0, upper=127)) / 127.0
df['volumen_norm'] = (df['volumen'].clip(lower=0, upper=127)) / 127.0

# Normalización de duraciones por duración máxima global
max_dura = df['dura'].max()
df['dura_norm'] = df['dura'] / max_dura if max_dura > 0 else df['dura']

# === 4. Agrupar y graficar ===
os.makedirs("plots", exist_ok=True)

for instr, datos in df.groupby('instrumento'):
    datos = datos.reset_index(drop=True)
    nombre_instr = get_instrument_name(instr)

    fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
    fig.suptitle(f"{nombre_instr} (número {instr})", fontsize=14)

    # Nota
    axes[0].plot(datos.index, datos['nota_norm'], color='tab:blue')
    axes[0].set_ylabel("Nota\n[0–1]")
    axes[0].grid(True, linestyle='--', alpha=0.6)

    # Volumen
    axes[1].plot(datos.index, datos['volumen_norm'], color='tab:orange')
    axes[1].set_ylabel("Volumen\n[0–1]")
    axes[1].grid(True, linestyle='--', alpha=0.6)

    # Duración
    axes[2].plot(datos.index, datos['dura_norm'], color='tab:green')
    axes[2].set_ylabel("Duración\n[0–1]")
    axes[2].set_xlabel("Índice (tiempo o muestra)")
    axes[2].grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout(rect=[0, 0, 1, 0.96])

    out_path = os.path.join("plots", f"{instr}_{nombre_instr.replace(' ', '_')}.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"✅ Gráfico guardado: {out_path}")

print("🎵 Todos los gráficos fueron generados correctamente.")

