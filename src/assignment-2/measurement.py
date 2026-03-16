import pandas as pd

def happiness_scoring(clean_df):

    pd.set_option("display.max_columns", None)

    # 1) Load the Yelp file that already contains reviews + business metadata
    # reviews = pd.read_csv("/Users/anna/coding-humanities/projects/hedonometer-project/hedonometer/data/processed/yelp_sample.csv.gz", compression="gzip")
    reviews = clean_df

    # Check column names once so you know what you're working with
    print(reviews.columns)
    print(reviews.head())

    # 2) Load the real LabMT file
    # Try tab-separated first; if that looks wrong, use sep=r"\s+" instead
    labmt = pd.read_csv(
        "data/raw/Data_Set_S1.txt",
        sep=r"\s+",
        engine="python",
        skiprows=3
    )

    print(labmt.head())
    print(labmt.columns)

    # 3) Rename LabMT columns to match the rest of your code
    # Replace these names with the actual column names from your file
    labmt = labmt.rename(columns={
        "word": "word",
        "happiness_average": "happiness_score"
    })

    # Keep only the columns you need
    labmt = labmt[["word", "happiness_score"]]

    # Optional: clean LabMT words
    labmt["word"] = labmt["word"].astype(str).str.lower()

    # Remove neutral words (labMT stop words)
# Standard hedonometer filter: remove scores between 4 and 6

# Remove neutral words (labMT stop words)
# Standard hedonometer filter: remove scores between 4 and 6
    labmt = labmt[(labmt["happiness_score"] <= 4) | (labmt["happiness_score"] >= 6)]
    print("LabMT size after neutral-word removal:", len(labmt))

    # 4) Tokenize Yelp review text
    reviews["tokens"] = (
        reviews["text"]
        .fillna("")
        .str.lower()
        .str.findall(r"[a-z]+")
    )

    print(reviews[["review_id", "tokens"]].head())

    # 5) One row per token
    token_df = reviews.explode("tokens")

    # Optional: drop empty token rows
    token_df = token_df[token_df["tokens"].notna()]

    # 6) Merge tokens with LabMT scores
    token_df = token_df.merge(
        labmt,
        left_on="tokens",
        right_on="word",
        how="left"
    )

    # 7) Mark out-of-vocabulary words
    token_df["is_oov"] = token_df["happiness_score"].isna()

    # 8) Review-level summary
    review_summary = (
        token_df.groupby("review_id")
        .agg(
            hedonometer_score=("happiness_score", "mean"),
            total_tokens=("tokens", "size"),
            matched_tokens=("happiness_score", lambda x: x.notna().sum()),
            oov_tokens=("is_oov", "sum")
        )
        .reset_index()
    )

    review_summary["oov_rate"] = (
        review_summary["oov_tokens"] / review_summary["total_tokens"]
    )

    # 9) Merge scores back onto original Yelp rows
    scores = reviews.merge(review_summary, on="review_id", how="left")

    scores.info()
    print(scores.head())

    output_path = "data/processed/yelp_hedonometer_scores.csv.gz"

    scores.to_csv(output_path, index=False, compression="gzip")

    print("Saved file to:", output_path)

    return scores

if __name__ == "__main__":
    import pandas as pd

    clean_df = pd.read_csv("data/raw/yelp_sample.csv.gz", compression="gzip")

    happiness_scoring(clean_df)