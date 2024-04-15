import numpy as np
from random import randint

lista = [[1,2,3],[4,5,6],[7,8,9]]

matriz = np.array(lista)
print(matriz[2][2])
print(matriz[2])

print(np.eye(3)) # Matriz identidad
print(np.eye(3)[1][1]) 

# Sistema de ecuaciones lineal 
# x + 2y = 1
# 3x + 5y = 2
a = [[1,2,3],[4,5,6]]
b = [7,8,9]
print(np.linalg.solve(a,b)) # Hayar la solucion a este sistema de ecuaciones

x = np.array([[randint(0,10) for _ in range (3)] for _ in range(3)]) # Creacion de matriz con números random
print(x)
print(x[2][2])
 
