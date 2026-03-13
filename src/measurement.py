import pandas as pd

pd.set_option("display.max_columns", None)

reviews = pd.DataFrame([
    {"review_id": 1, "business_id": "a", "stars": 5, "text": "I love this place great food"},
    {"review_id": 2, "business_id": "b", "stars": 1, "text": "terrible service bad experience"},
])
# dummy DF - replace

business = pd.DataFrame([
    {"business_id": "a", "state": "Washington", "category": "restaurant"},
    {"business_id": "b", "state": "California", "category": "prison"},
])
# dummy DF - replace

labmt = pd.DataFrame([
    {"word": "love", "happiness_score": 8.4},
    {"word": "great", "happiness_score": 7.9},
    {"word": "terrible", "happiness_score": 2.1},
    {"word": "bad", "happiness_score": 2.5},
])
# dummy DF - replace

reviews = reviews.merge(business, on="business_id", how="left")
# adds business metadata to review DF based on shared business IDs

reviews["tokens"] = (
    reviews["text"]
    .str.lower()
    .str.findall(r"[a-z]+")
)
print(reviews["tokens"])
# tokenization: lowercases, keeps only sequences of letters (no emojis, whitespace, punctuation)

token_df = reviews.explode("tokens")
print(token_df)
# new DF where each token gets one row

token_df = token_df.merge(labmt, left_on="tokens", right_on="word", how="left")
# matches tokens in yelp data with words in labMT data, merges them - keeps unmatched tokens

token_df["is_oov"] = token_df["happiness_score"].isna()
# defines OOVs as tokens that aren't matched with a happiness score

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
review_summary["oov_rate"] = review_summary["oov_tokens"] / review_summary["total_tokens"]
# produces mean hedonometer score of each review and count of tokens (matched/OOV)

scores = reviews.merge(review_summary, on="review_id", how="left")
scores.info()
print(scores)
# merges summary back into review DF
# prints