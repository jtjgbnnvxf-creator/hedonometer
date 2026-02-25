import pandas as pd

pd.set_option("display.max_columns", None)

df = pd.read_csv("data/raw/Data_Set_S1.txt", 
    sep="\t",
    skiprows=3,
    na_values=["--"],
    encoding="utf-8")

df.info()
print(df.head())