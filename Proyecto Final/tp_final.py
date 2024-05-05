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
        pass

class CSVFileReader(FileReader): # Lector csv
    def read(self, path: str) -> pd.DataFrame:
        return pd.read_csv(path)

class ExcelFileReader(FileReader): # Lector excel
    def read(self, path: str) -> pd.DataFrame:
        return pd.read_excel(path)

class JSONFileReader(FileReader): # Lector json
    def read(self, path: str) -> pd.DataFrame:
        return pd.read_json(path)

class TXTFileReader(FileReader): # Lector txt
    def read(self, path: str):
        return np.loadtxt(path)      

class FileReaderContext: 
    def __init__(self, reader: FileReader):
        self.reader = reader

    def read_file(self, path: str) -> pd.DataFrame:
        return self.reader.read(path)

# Lectura de datasets
def read_file(path: str) -> pd.DataFrame: # Devuelve un dataframe según el tipo de archivo leido
    extension = path.split(".")[-1]
    if extension == "csv":
        reader = CSVFileReader()
    elif extension in ["xls", "xlsx"]:
        reader = ExcelFileReader()
    elif extension == "json":
        reader = JSONFileReader()
    elif extension == 'txt':
        reader = TXTFileReader()    
    else:
        raise ValueError("Extension no soportada")
    context = FileReaderContext(reader)
    return context.read_file(path)

# Creación de datasets
df_customers = read_file(Config.customers_path())
df_items = read_file(Config.items_path())
df_payments = read_file(Config.payments_path())
df_orders = read_file(Config.orders_path())
df_products = read_file(Config.products_path())

# Limpieza de datos
def clean_dataset(df:pd.DataFrame) -> pd.DataFrame:
    # Eliminar registros duplicados
    df.drop_duplicates()

    # Rellenar los valores nulos con la media en columnas numéricas
    numeric_columns = df.select_dtypes(include=['number']).columns
    df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

    # Eliminar filas completas si todos son valores nulos
    df.dropna(how='all',inplace=True)
    return df

# Aplicar la limpieza a todos los datasets y ordenamiento
df_customers_copy = clean_dataset(df_customers)
df_items_copy = clean_dataset(df_items)
df_payments_copy = clean_dataset(df_payments)
df_orders_copy = clean_dataset(df_orders).sort_values(by='order_approved_at', ascending=False) # Ordenado por fecha de aprobación de la compra
df_products_copy = clean_dataset(df_products)

# Asignación de indices a los datasets
df_customers_copy.set_index('customer_id', inplace=True, drop=False)
df_items_copy.set_index(['order_id','order_item_id'], inplace=True, drop=False) 
df_payments_copy.set_index(['order_id','payment_sequential'], inplace=True, drop=False) 
df_orders_copy.set_index(['order_id','customer_id'], inplace=True, drop=False) 
df_products_copy.set_index('product_id', inplace=True, drop=False) 

# Obtener información de cada conjunto de datos  
def dataset_info(df: pd.DataFrame):
    print(4 * '-------------------------------' + '\nDatos descriptivos:')
    print(f'{df.info()}\n')
    print(f'{df.describe()}\n')

dataset_info(df_customers_copy)
dataset_info(df_items_copy)
dataset_info(df_payments_copy)
dataset_info(df_orders_copy)
dataset_info(df_products_copy)

# Cantidad total de clientes únicos en el conjunto de datos
print("\nCantidad de clientes únicos:", df_customers_copy['customer_unique_id'].nunique())

# Visualizar boxplot de precios
plt.boxplot(df_items_copy['price'])
plt.xlabel('Precio')
plt.ylabel('Valor')
plt.title('Boxplot de precio')
plt.show()

# Al ver el boxplot de los precios, podemos identificar la variacion entre estos
# mostrando gran distancia entre el maximo y minimo valor.
print('\nDatos estadisticos del precio de productos\n',df_items_copy['price'].describe(),'\n')

gc.collect()

# Visualización cantidad de clientes por estado
df_customers_copy['customer_state'].hist()
plt.xlabel('Estado')
plt.ylabel('Clientes')
plt.title('Ciudades por cliente')
plt.show()

# Visualización frecuencia de tipos de pago
df_payments_copy['payment_type'].hist()
plt.xlabel('Tipo de pago')
plt.ylabel('Cantidad')
plt.title('Frecuencia tipos de pago')
plt.show()

# Gráfico de dispersión entre precio del producto y valor del flete
plt.scatter(df_items_copy['price'], df_items_copy['freight_value'])
plt.xlabel('Precio')
plt.ylabel('Valor del flete')
plt.title('Gráfico de dispersión')
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
plt.show()

# Exportación de datos limpios
df_orders_copy.to_excel('Proyecto Final\data\datos_limpios.xlsx', index=True)
