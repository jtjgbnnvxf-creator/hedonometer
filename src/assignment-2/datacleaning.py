import pandas as pd
<<<<<<< HEAD
import json
import os
import random

def clean_and_sample_yelp_lines(review_json_path, business_json_path, sample_size=200_000, output_csv_path="data/yelp_sample.csv.gz"):
    """
    Reads Yelp review.json and business.json line by line to avoid memory errors.
    Cleans, samples, merges with business info, and saves compressed CSV.
    """
    
    # Load business data (small)
    print("Loading business data...")
    business_df = pd.read_json(business_json_path, lines=True)
    business_df = business_df[["business_id", "name", "city", "state", "categories"]]

    # Step 1: Process reviews line by line
    print("Processing reviews line by line...")
    sampled_reviews = []
    with open(review_json_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                review = json.loads(line)
                # Keep essential fields
                keep_keys = ["review_id", "user_id", "business_id", "stars", "text", "date"]
                review_row = {k: review[k] for k in keep_keys}
                # Skip empty text
                if review_row["text"].strip():
                    sampled_reviews.append(review_row)
            except json.JSONDecodeError:
                continue  # skip malformed lines

    print(f"Total valid reviews: {len(sampled_reviews)}")

    # Step 2: Sample 200k reviews
    if sample_size > len(sampled_reviews):
        print(f"Sample size {sample_size} > available reviews. Using full dataset.")
        sampled = sampled_reviews
    else:
        sampled = random.sample(sampled_reviews, sample_size)

    sample_df = pd.DataFrame(sampled)

    # Step 3: Merge with business info
    sample_df = sample_df.merge(business_df, on="business_id", how="left")

    # Step 4: Sort by stars and reset index
    sample_df = sample_df.sort_values(by="stars").reset_index(drop=True)

    # Step 5: Ensure output folder exists
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    # Step 6: Save compressed CSV
    sample_df.to_csv(output_csv_path, index=False, compression="gzip")
    print(f"Compressed CSV saved: {output_csv_path} ({len(sample_df)} rows)")

    return sample_df


if __name__ == "__main__":
    clean_and_sample_yelp_lines(
        review_json_path="data/raw/yelp_academic_dataset_review.json",
        business_json_path="data/raw/yelp_academic_dataset_business.json",
        sample_size=200_000,
        output_csv_path="data/yelp_sample.csv.gz"
    )
=======

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
>>>>>>> afcf13e41c98b13d2a2bf8469347f390b6f6ec99
