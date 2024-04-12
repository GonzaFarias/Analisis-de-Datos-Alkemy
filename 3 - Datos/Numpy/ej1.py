import numpy as np
from time import time

lista = [i for i in range (100000000)]
## Ejemplo de como cambian las clases
lista_numpy = np.array(lista)
print(type(lista[0]))
print(type(lista_numpy[0]))

## Ejemplo de tiempo de ejecución en numpy
start = time()
sum(lista)
print('Tiempo de ejecucion con lista: ', time() - start)

start = time()
sum(lista_numpy)
print('Tiempo de ejecucion con numpy: ', time() - start)


lista1 = [1,2]
lista2 = [3,4]

print(lista1 + lista2)

lista_numpy1 = np.array(lista1)
lista_numpy2 = np.array(lista2)

lista_suma_numpy = lista_numpy1 + lista_numpy2
print('Lista con numpy: ',lista_suma_numpy) # En numpy la suma de listas se hace sumando los mismos indices entre cada vector, ambas listas deben ser de mismo tamaño

