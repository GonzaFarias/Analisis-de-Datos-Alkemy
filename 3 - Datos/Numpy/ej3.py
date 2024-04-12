import numpy as np
from random import randint

v = np.array([randint(1,10) for _ in range (3)])
x = np.array([[randint(1,10) for _ in range (3)] for _ in range(3)])
print(x)

# Producto punto:
w = np.dot(x, v)
print(w)

# Producto cruzado:
w2 = np.cross(x, v)
print(w2)

# Matriz de ceros
z = np.zeros((3,3))
print (z)
