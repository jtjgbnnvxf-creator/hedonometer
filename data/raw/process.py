import pandas as pd

df = pd.read_csv(
    '/Users/danielsitumeang/Desktop/coding-humanities/data/raw/Data_Set_S1.txt',
    sep='\t',
    skiprows=3,        # skip the intro lines at the top
    on_bad_lines='skip'
)

print(df.head())
print(df.columns.tolist())

df.to_csv('/Users/danielsitumeang/Desktop/coding-humanities/data/processed/Data_Set_S1.csv', index=False)
print("Done! CSV saved.")
