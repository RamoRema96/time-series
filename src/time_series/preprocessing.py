import pandas as pd

class PrePro:
    def __init__(self) -> None:
        pass

    def to_datetime(self, df:pd.DataFrame, name_column:str):
        df[f"{name_column}_datetime"] = pd.to_datetime(df[name_column])