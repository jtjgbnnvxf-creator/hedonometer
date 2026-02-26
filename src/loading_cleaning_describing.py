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

expected_columns = [
    "word",
    "happiness_rank",
    "happiness_average",
    "happiness_standard_deviation",
    "twitter_rank",
    "google_rank",
    "nyt_rank",
    "lyrics_rank"]
print("Schema check:", set(expected_columns) == set(df.columns))
# sanity check 1: prints True if all expected columns are in DF
# catches (returns False if) wrong file, wrong delimiter, shifted header, column rename

print("Min happiness:", df["happiness_average"].min())
print("Max happiness:", df["happiness_average"].max())
print("Min std dev:", df["happiness_standard_deviation"].min())

print((df["word"] != df["word"].str.lower()).sum())
print((df["word"] != df["word"].str.strip()).sum())
print(df["word"].str.contains(" ").sum())
print(df["word"].duplicated().sum())
# checks to make sure "word" doesn't need to be normalized (no uppercase, no leading/trailing whitespaces, no spaces inside words)
# checks for duplicates
# prints "0" for all checks (no normalization needed, no duplicates)

data_dictionary = {}
for col in df.columns:
    formatted_name = col.replace("_", " ")

    data_dictionary[formatted_name] = {
        "dtype": str(df[col].dtype),
        "missing values": int(df[col].isna().sum())
    }

print(data_dictionary)
# creates data dict with neat column names (no _)

df_dictionary = pd.DataFrame.from_dict(data_dictionary, orient="index")
df_dictionary = df_dictionary.reset_index().rename(columns={"index": "column name"})

print(df_dictionary)
# turns data dict into a table (for README?)

cols = ["word", "happiness_average", "twitter_rank"]
print(df[cols].sample(15, random_state=42))
# prints fixed sample (sample doesn't change)
# only includes three columns: can't figure out how to include all columns and keep return readable

print(df.nlargest(10, "happiness_average"))
print(df.nsmallest(10, "happiness_average"))
# prints ten most and least positive words by average happiness
# most positive: laughter, happiness, love, happy, laughed, laugh, laughing, excellent, laughs, joy
# least positive: suicide, terrorist, rape, murder, terrorism, cancer, death, died, kill, killed