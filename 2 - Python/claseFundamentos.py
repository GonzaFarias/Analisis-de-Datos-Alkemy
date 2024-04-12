import math

def calcularRaizCuadrada(a):
    """Devuelve la raíz cuadrada de a

    Args:
        a (float): número decimal que obtendra su raíz cuadrada

    Returns:
        _type_: raíz cuadrada de a
    """
    return math.sqrt(a)

num = float(input('Ingrese el numero: '))
print(f'La raiz cuadrada de {num} es {calcularRaizCuadrada(num)}')

