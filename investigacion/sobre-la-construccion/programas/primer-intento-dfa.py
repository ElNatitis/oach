# Para hacer un DFA con respecto a datos random
import random
import numpy as np

N = 100 
# Arreglo de N números aleatorios entre 0 y 100
lista = [random.randint(0, 1000) for _ in range(N)] 
arreglo = np.array(lista)
print(f'Arreglo random de {N} elementos\n{arreglo}')

# Para calcular el promedio
promedio = np.mean(arreglo)
print(promedio)

# Para calular el Arreglo-Integrado
arreglo_int = np.zeros(N)
# print(arreglo_int)
n = 0
for elemento in arreglo_int:
    suma = 0
    for i in range(N - n):
        dif = arreglo[i] - promedio
        # print(f'{suma}+={dif}')
        suma += dif  
    # print(f'terminamos por ahora\nel término {n} del arreglo integrado es {suma}')
    arreglo_int[n]=suma
    n+=1

print(f'arreglo integrado \n{arreglo_int}')

# Para dividir el arreglo integrado en segmentos 
segmentos = np.array([10,N/4])
print(segmentos)
