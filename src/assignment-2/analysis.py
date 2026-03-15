# FILE FOR ANALYSIS

import pandas as pd

def analyze_data(df):
    print("Sample size:", len(df))

    print("\nStar rating distribution:")
    print(df["stars"].value_counts(normalize=True))

    print("\nCities in sample:", df["city"].nunique())

    print("\nTop cities:")
    print(df["city"].value_counts().head())

if __name__ == "__main__":
    import pandas as pd

    clean_df = pd.read_csv("data/processed/yelp_hedonometer_scores.csv.gz", compression="gzip")

    analyze_data(clean_df)
