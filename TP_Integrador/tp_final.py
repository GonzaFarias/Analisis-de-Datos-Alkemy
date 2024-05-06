# Trabajo Práctico Integrador - Análisis de Datos
# Gonzalo Farías
# 07/05/2024

# Importación de recursos necesarios
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from config import Config
from abc import ABC, abstractmethod
import gc

# Estrategia para la lectura de datasets
class FileReader(ABC):
    @abstractmethod
    def read(self, path: str) -> pd.DataFrame:
        """Lee un archivo y devuelve un DataFrame."""
        pass

class CSVFileReader(FileReader): # Lector csv
    def read(self, path: str) -> pd.DataFrame:
        """Lee un archivo CSV y devuelve un DataFrame."""
        return pd.read_csv(path)

class ExcelFileReader(FileReader): # Lector excel
    def read(self, path: str) -> pd.DataFrame:
        """Lee un archivo Excel y devuelve un DataFrame."""
        return pd.read_excel(path)

class JSONFileReader(FileReader): # Lector json
    def read(self, path: str) -> pd.DataFrame:
        """Lee un archivo JSON y devuelve un DataFrame."""
        return pd.read_json(path)

class TXTFileReader(FileReader): # Lector txt
    def read(self, path: str) -> np.ndarray:
        """Lee un archivo de texto y devuelve un array de NumPy."""
        return np.loadtxt(path)      

class FileReaderContext: 
    def __init__(self, reader: FileReader):
        self.reader = reader

    def read_file(self, path: str) -> pd.DataFrame:
        """Utiliza el FileReader proporcionado para leer un archivo y devolver un DataFrame."""
        return self.reader.read(path)

# Lectura de datasets
def read_file(path: str) -> pd.DataFrame:
    """Devuelve un DataFrame según el tipo de archivo leído.
    
    Args:
        path (str): La ruta al archivo que se va a leer.

    Raises:
        ValueError: Si la extensión del archivo no es soportada.

    Returns:
        pd.DataFrame: El DataFrame resultante de leer el archivo.
    """
    extension = path.split(".")[-1].lower()
    if extension == "csv":
        reader = CSVFileReader()
    elif extension in ["xls", "xlsx"]:
        reader = ExcelFileReader()
    elif extension == "json":
        reader = JSONFileReader()
    elif extension == 'txt':
        reader = TXTFileReader()    
    else:
        raise ValueError("Extensión no soportada")
    context = FileReaderContext(reader)
    return context.read_file(path)

# Limpieza de datos
def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia el DataFrame proporcionado eliminando duplicados y valores nulos.

    Args:
        df (pd.DataFrame): El DataFrame a limpiar.

    Returns:
        pd.DataFrame: El DataFrame limpio.
    """
    df.drop_duplicates()
    # numeric_columns = df.select_dtypes(include=['number']).columns 
    # df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean()) """ # Decidi no utilizarlo al no ser aplicable en este caso
    df.dropna(how='all')
    return df

# Obtener información de cada conjunto de datos  
def dataset_info(df: pd.DataFrame):
    """Imprime información descriptiva del DataFrame proporcionado.

    Args:
        df (pd.DataFrame): El DataFrame del cual se obtendrá la información.
    """
    print(4 * '-------------------------------' + '\nDatos descriptivos:')
    print(f'{df.info()}\n')
    print(f'{df.describe()}\n')

# Adicional - Uso de NumPy para cálculos de álgebra lineal
def calculos_numpy():
    """Realiza y muestra varios cálculos de álgebra lineal utilizando NumPy."""
    x = np.array([1,2])
    y = np.array([3,4])
    sum_list = x + y
    print(f'Suma de listas {x} e {y} con numpy: ',sum_list)

    # Matriz identidad:
    print(f'\nCreación de matriz identidad:\n{np.eye(3)}\n')

    # Producto punto:
    print(f'El resultado del producto punto entre {x} e {y} es:{np.dot(x, y)}')
    
    # Calcular determinante:
    matrix = np.array([[1, 2], [3, 4]])
    print(f'\nEl determinante de la matriz {matrix} es:\n{np.linalg.det(matrix)}')

    # Matriz de ceros:
    print ('\nMatriz de ceros: \n',np.zeros((4,4)))

    # Producto cruzado:
    print(f'\nEl resultado del producto cruzado entre {x} e {y} es: {np.cross(x, y)}' )

# Creación de datasets
df_customers = read_file(Config.customers_path())
df_items = read_file(Config.items_path())
df_payments = read_file(Config.payments_path())
df_orders = read_file(Config.orders_path())
df_products = read_file(Config.products_path())

# Aplicar la limpieza a todos los datasets y ordenamiento
df_customers_copy = clean_dataset(df_customers)
df_items_copy = clean_dataset(df_items)
df_payments_copy = clean_dataset(df_payments)
df_orders_copy = clean_dataset(df_orders).sort_values(by='order_approved_at', ascending=False).iloc[1:] # Ordenado por fecha de aprobación de la compra
df_products_copy = clean_dataset(df_products)

# Asignación de indices a los datasets
df_customers_copy.set_index('customer_id', inplace=True)
df_items_copy.set_index(['order_id','product_id'], inplace=True) 
df_payments_copy.set_index(['order_id','payment_sequential'], inplace=True) 
df_orders_copy.set_index('order_id', inplace=True) 
df_products_copy.set_index('product_id', inplace=True) 

# Ver información de los datasets
dataset_info(df_customers_copy)
dataset_info(df_items_copy)
dataset_info(df_payments_copy)
dataset_info(df_orders_copy)
dataset_info(df_products_copy)

# Cantidad total de clientes únicos en el conjunto de datos
unique_customers = df_customers_copy['customer_unique_id'].nunique()
print("\nCantidad de clientes únicos:", unique_customers)

# Cantidad promedio del valor de pago por pedido
average_payment_value = df_payments_copy['payment_value'].mean()
print("\nPromedio del valor de pago por pedido:", average_payment_value)

# Merge de df_order_items y df_products para poder calcular la cantidad de ventas por categoría
merged_df_order_products = pd.merge(df_items_copy, df_products_copy, on='product_id', how='inner')

# Agrupación por categoria de producto
grouped_df_order_products = merged_df_order_products.groupby('product_category_name').size().reset_index(name='count')

# Visualización de la venta por categorías de producto, para identificar
# cual es la más vendida.
plt.figure(figsize=(15, 6))
plt.bar(grouped_df_order_products['product_category_name'], grouped_df_order_products['count'])
plt.xlabel('Categoría')
plt.ylabel('Ventas')
plt.title('Ventas por categoría de producto')
plt.xticks(rotation=90)  
plt.savefig("TP_Integrador\plots\plot1.png")
plt.show() # Podemos observar como la categoría de productos más vendida es cama_mesa_banho,
# que serian los productos relacionados con cama, mesa y baños.

# Cálculo de la categoría de productos más vendida
max_selling_category = grouped_df_order_products.sort_values(by='count', ascending=False).iloc[0]['product_category_name']
print('Categoría de productos más vendida:',max_selling_category)

# Cálculo del número total de pedidos completados, o sea, excluyendo los cancelados
total_orders = len(df_orders_copy[df_orders_copy['order_status'] != 'canceled'])
print(f'Número total de pedidos realizados: {total_orders}')

# Visualizar boxplot de precios
plt.boxplot(df_items_copy['price'])
plt.xlabel('Precio')
plt.ylabel('Valor')
plt.title('Boxplot de precio')
plt.savefig("TP_Integrador\plots\plot2.png")
plt.show() # Al ver el boxplot de los precios, podemos identificar la variacion entre estos
# mostrando gran distancia entre el maximo y minimo valor.
print('\nDatos estadisticos del precio de productos\n',df_items_copy['price'].describe(),'\n')

gc.collect()

# Visualización cantidad de clientes por estado
plt.figure(figsize=(15, 6))
df_customers_copy['customer_state'].hist()
plt.xlabel('Estado')
plt.ylabel('Clientes')
plt.title('Clientes por estado')
plt.savefig("TP_Integrador\plots\plot3.png")
plt.show()

# Visualización frecuencia de tipos de pago
df_payments_copy['payment_type'].hist()
plt.xlabel('Tipo de pago')
plt.ylabel('Cantidad')
plt.title('Frecuencia tipos de pago')
plt.savefig("TP_Integrador\plots\plot4.png")
plt.show()

# Gráfico de dispersión entre precio del producto y valor del flete
plt.scatter(df_items_copy['price'], df_items_copy['freight_value'])
plt.xlabel('Precio')
plt.ylabel('Valor del flete')
plt.title('Gráfico de dispersión')
plt.savefig("TP_Integrador\plots\plot5.png")
plt.show() # Se observa que el valor del flete no está relacionado con el costo del producto

# Visualización cantidad de compras por mes
df_orders_copy['order_approved_at'] = pd.to_datetime(df_orders_copy['order_approved_at'])
# Las ordenes de compra se ordenan por mes excluyendo las canceladas
orders_per_month = df_orders_copy[df_orders_copy['order_status'] != 'canceled'].groupby([df_orders_copy['order_approved_at'].dt.to_period('M')]).size()
orders_per_month.plot(kind='line', marker='o', linestyle='-')
plt.xlabel('Mes')
plt.ylabel('Cantidad de Ventas')
plt.title('Cantidad de Ventas por Mes')
plt.xticks(rotation=45)  
plt.tight_layout() 
plt.grid(True)  
plt.savefig("TP_Integrador\plots\plot6.png")
plt.show()

# Reporte descriptivo
df_report = pd.DataFrame({'total_orders': [total_orders], 'max_selling_category': [max_selling_category],
'avg_payment_value':[average_payment_value], 'unique_customers': [unique_customers]})

# Exportación de datos limpios (del mismo generado hice una copia llamada datos_limpios_reporte
# para poder aplicar los formatos personalizados y estilos visuales)
with pd.ExcelWriter('TP_Integrador\data\clean_data.xlsx') as writer:
    df_customers_copy.to_excel(writer, sheet_name='ecommerce_customers_clean', index=True)
    df_items_copy.to_excel(writer, sheet_name='ecommerce_items_clean', index=True)
    df_payments_copy.to_excel(writer, sheet_name='ecommerce_payments_clean', index=True)
    df_orders_copy[df_orders_copy['order_status'] != 'canceled'].to_excel(writer, sheet_name='ecommerce_orders_clean', index=True)
    df_products_copy.to_excel(writer, sheet_name='ecommerce_products_clean', index=True)
    df_report.to_excel(writer, sheet_name='descriptive report', index=False)

# Vemos algunos de los calculos que se puedenr realizar con NumPy
calculos_numpy()























































































































   