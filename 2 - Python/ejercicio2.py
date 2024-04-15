# Ejercicio Bicicleta
class Bicicleta:
    def __init__(self, marca:str, rodado:int, modelo:str, precio:float) -> None:
        self.marca = marca
        self.rodado = rodado
        self.modelo = modelo
        self.precio = precio
    def modificarPrecio(self,precioNuevo:float) -> None:
        self.precio = precioNuevo
    def __str__(self) -> str:
        return f'{self.marca} R{self.rodado} {self.modelo} - ${self.precio}'
    def getPrecio(self) -> float:
        return self.precio

b1 = Bicicleta('Lamborghini', 29, 'Ventur Shimano', 249999.99)
print(f'Datos de la bicicleta: {b1.__str__()}')
b1.modificarPrecio(280500.00)
print(f'El precio nuevo es $ {b1.getPrecio()}') 

# Ejercicio Animal
# ↪ La clase Animal tiene:
# ○ atributo cantidad_patas: numérico

# ○ atributo tipo: vertebrado/invertebrado
# ○ método comer(): retorna un string “estoy comiendo”

class Animal:
    def __init__(self, cantidad_patas:int, tipo:str) -> None:
        self.cantidad_patas = cantidad_patas
        self.tipo = tipo
    def comer(self) -> str:
        return 'estoy comiendo'    
   

class Perro(Animal):
    def __init__(self, cantidad_patas: int, tipo: str, nombre:str, raza:str) -> None:
        super().__init__(cantidad_patas, tipo)
        self.nombre = nombre
        self.raza = raza
    def correr(self) -> str:
        return f'estoy corriendo en {self.cantidad_patas} patas, nombre {self.nombre} y raza {self.raza}'   

class Aguila(Animal):
    def volar(self) -> str:
        return 'estoy volando'       

# ↪ La clase Perro hereda de Animal y agrega:
# ○ atributo nombre: texto
# ○ atributo raza: texto
# ○ método correr(): retorna un string “estoy corriendo”
# ↪ La clase Aguila hereda de Animal y agrega:
# ○ método volar(): retorna un string “estoy volando”

perro = Perro(4,'Vertebrado','Aslan', 'Pitbull')
print(perro.correr())
print(perro.comer())

aguila = Aguila(2, 'Vertebrado')
print(f'{aguila.volar()} y soy un ave')
