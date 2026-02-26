import pandas as pd

pd.set_option("display.max_columns", None)
# added because df.info() didn't display all columns before

df = pd.read_csv("data/raw/Data_Set_S1.txt", 
    sep="\t",
    skiprows=3,
    na_values=["--"],
    encoding="utf-8")

df.info()
print(df.head())
# no missing values for word, happiness_rank, _average & _standard_deviation
# 5222 missing values for all _rank
# all numeric columns are already numeric types (_rank is int64, rest is float64)
# 8 columns, 1022 rows

data_dictionary = {}
for col in df.columns:
    formatted_name = col.replace("_", " ")

    data_dictionary[formatted_name] = {
        "dtype": str(df[col].dtype),
        "missing values": int(df[col].isna().sum())
    }

print(data_dictionary)

df_dictionary = pd.DataFrame.from_dict(data_dictionary, orient="index")
df_dictionary = df_dictionary.reset_index().rename(columns={"index": "column name"})

print(df_dictionary)