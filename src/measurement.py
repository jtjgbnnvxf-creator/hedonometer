import pandas as pd

def happiness_scoring(clean_df):

    pd.set_option("display.max_columns", None)

    # loads yelp dataset
    reviews = pd.read_csv("data/raw/yelp_sample.csv.gz", compression="gzip")
    reviews = clean_df

    # check column names
    print(reviews.columns)
    print(reviews.head())

     # tokenizes yelp review text
    reviews["tokens"] = (
        reviews["text"]
        .fillna("")
        .str.lower()
        .str.findall(r"[a-z]+")
    )

    print(reviews[["review_id", "tokens"]].head())

    # new df with one row per token
    token_df = reviews.explode("tokens")

    # drops empty token rows
    token_df = token_df[token_df["tokens"].notna()]

    # loads labMT dataset
    labmt = pd.read_csv(
        "data/raw/Data_Set_S1.txt",
        sep=r"\s+",
        engine="python",
        skiprows=3
    )

    # check column names
    print(labmt.head())
    print(labmt.columns)

    # rename labMT columns to match rest of script, diregard irrelevant columns
    labmt = labmt.rename(columns={
        "word": "word",
        "happiness_average": "happiness_score"
    })

    labmt = labmt[["word", "happiness_score"]]

    # Remove neutral words (labMT stop words)
    # Standard hedonometer filter: remove scores between 4 and 6
    labmt = labmt[(labmt["happiness_score"] <= 4) | (labmt["happiness_score"] >= 6)]
    print("LabMT size after neutral-word removal:", len(labmt))

    # merge tokens with labMT scores
    token_df = token_df.merge(
        labmt,
        left_on="tokens",
        right_on="word",
        how="left"
    )

    # marks OOV words
    token_df["is_oov"] = token_df["happiness_score"].isna()

    # review-level summary
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

    # dataset-level token statistics
    total_tokens_all = token_df["tokens"].count()
    total_oov_all = token_df["is_oov"].sum()
    oov_rate_all = total_oov_all / total_tokens_all

    print("Total tokens:", total_tokens_all)
    print("Total OOV tokens:", total_oov_all)
    print("Overall OOV rate:", oov_rate_all)

    # merges scores back onto original yelp rows
    scores = reviews.merge(review_summary, on="review_id", how="left")

    scores.info()
    print(scores.head())

    # saves full df as csv (includes full reviews, reviews as tokens, review and business metadat, hedonometer score, OOV info)
    output_path = "data/processed/yelp_hedonometer_scores.csv.gz"
    scores.to_csv(output_path, index=False, compression="gzip")
    print("Saved file to:", output_path)

    return scores

if __name__ == "__main__":
    import pandas as pd

    clean_df = pd.read_csv("data/raw/yelp_sample.csv.gz", compression="gzip")

    happiness_scoring(clean_df)

 