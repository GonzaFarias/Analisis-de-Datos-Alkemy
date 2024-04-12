# 1) Calcular sumatoria del 1 al 100 con while.
contador = 0
sumatoria = 0
while (contador < 100):
    contador += 1
    sumatoria += contador
print(f'El resultado de la sumatoria es: {sumatoria}')
print((100*(100+1))/2)

# 2) Crear una lista con 5 elementos y luego hacer:
# ↪ Imprimir el último elemento
# ↪ Modificar el valor del tercer elemento
# ↪ Agregar dos elementos
# ↪ Eliminar algún elemento

lista = [5, 10, 15, 20, 25]
print(lista)
print(lista[-1])
lista[2] = 3
print(lista)
lista.append(30)
lista.append(35)
print(lista)
lista.remove(3)
print(lista)

# 3) Crea una función llamada verificar_calificacion que reciba tres parámetros: nota1, nota2 y nota3
# ↪ Dentro de la función calcular el promedio de notas
# Si el promedio es mayor o igual a 6, entonces la función debe retornar un mensaje “Aprobado”, en caso contrario “Reprobado”


def verificar_calificacion(nota1, nota2, nota3):
    if ((nota1+nota2+nota3)/3 >= 6):
        return 'Aprobado'
    return 'Reprobado'


print(verificar_calificacion(8, 9, 6))
print(verificar_calificacion(4, 7, 4))
print(verificar_calificacion(10, 10, 9))
