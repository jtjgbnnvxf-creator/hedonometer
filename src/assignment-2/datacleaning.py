import pandas as pd

def clean_and_sample(df, sample_size=25):
    # cleans the Yelp dataset and returns a sampled version

    # remove duplicate reviews
    df = df.drop_duplicates(subset="review_id")

    # remove rows with missing review text
    df = df.dropna(subset=["text"])

    # remove empty reviews
    df = df[df["text"].str.strip() != ""]

    # keep relevant columns
    df = df[["review_id", "user_id", "business_id", "stars", "text", "date"]]

    print("original size:", df.shape)

    # random sample
    sample_df = df.sample(n=sample_size, random_state=42)

    # organize dataset
    sample_df = sample_df.sort_values(by="stars")
    sample_df = sample_df.reset_index(drop=True)

    print("sample size:", sample_df.shape)
    return df