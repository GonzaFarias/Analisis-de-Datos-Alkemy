import pandas as pd

def read_file(path: str) -> pd.DataFrame:
    extension = path.split(".")[-1] # archivo.csv = ["archivo", "csv"]
    if extension == "csv":
        return pd.read_csv(path)
    elif extension in ["xls", "xlsx"]:
        return pd.read_excel(path)
    elif extension == "json":
        return pd.read_json(path)
    else: 
        raise ValueError("Extension no soportada")

 