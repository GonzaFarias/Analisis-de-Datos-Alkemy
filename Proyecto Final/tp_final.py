import pandas as pd
import numpy as np
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

# Obtener descripciones de cada conjunto de datos limpios
print(df_customers_copy.describe())
print(df_items_copy.describe())
print(df_payments_copy.describe())
print(df_orders_copy.describe())
print(df_products_copy.describe())

