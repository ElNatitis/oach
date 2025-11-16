""" 
queremos analizar un archivo midi, sabe a que tempom esta y poder determianr la cantidad de segundos minima, correspondiente al tempo, en la qu eestan ocurriendo eventos
"""
import pretty_midi 
import pandas 
import os

# Género musical con el que estamos trabajando
genero = 'salsa'
midi = pretty_midi.PrettyMIDI(ruta) # leemos el midi y lo guardamos con la estructura de pretty_midi 
