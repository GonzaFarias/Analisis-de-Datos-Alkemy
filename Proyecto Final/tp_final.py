import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from config import Config
from abc import ABC, abstractmethod

# Estrategia para la lectura de datasets
class FileReader(ABC):
    @abstractmethod
    def read(self, path: str) -> pd.DataFrame:
        pass

class CSVFileReader(FileReader):
    def read(self, path: str) -> pd.DataFrame:
        return pd.read_csv(path)

class ExcelFileReader(FileReader):
    def read(self, path: str) -> pd.DataFrame:
        return pd.read_excel(path)

class JSONFileReader(FileReader):
    def read(self, path: str) -> pd.DataFrame:
        return pd.read_json(path)

class FileReaderContext:
    def __init__(self, reader: FileReader):
        self.reader = reader

    def read_file(self, path: str) -> pd.DataFrame:
        return self.reader.read(path)

# Lectura de datasets
def read_file(path: str) -> pd.DataFrame:
    extension = path.split(".")[-1]
    if extension == "csv":
        reader = CSVFileReader()
    elif extension in ["xls", "xlsx"]:
        reader = ExcelFileReader()
    elif extension == "json":
        reader = JSONFileReader()
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

    # Eliminar filas con valores nulos en columnas de tipo string
    df.dropna(subset=df.select_dtypes(include=['object']).columns, inplace=True)

    # Rellenar los valores nulos con la media en columnas numéricas
    numeric_columns = df.select_dtypes(include=['number']).columns
    df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

    # Eliminar filas completas si contienen valores nulos
    df.dropna(inplace=True)
    return df

# Aplicar la limpieza a todos los datasets
df_customers_copy = clean_dataset(df_customers)
df_items_copy = clean_dataset(df_items)
df_payments_copy = clean_dataset(df_payments)
df_orders_copy = clean_dataset(df_orders)
df_products_copy = clean_dataset(df_products)

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

# Crear y visualizar boxplot de precios
plt.boxplot(df_items_copy['price'])
plt.xlabel('Precio')
plt.ylabel('Valor')
plt.title('Boxplot de precio')
plt.show()

# Al ver el boxplot de los precios, podemos identificar la gran variacion entre estos
# mostrando gran distancia entre el maximo y minimo valor.
print('\nDatos estadisticos del precio de productos\n',df_items_copy['price'].describe(),'\n')


