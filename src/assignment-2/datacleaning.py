import pandas as pd
import json
import os
import random


def clean_and_sample_yelp_lines(
    review_json_path,
    business_json_path,
    sample_size,
    output_csv_path="data/processed/yelp_sample.csv.gz"
):
    """
    Reads Yelp review.json and business.json line by line to avoid memory errors.
    Cleans, samples, merges with business info, and optionally saves compressed CSV.
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

    # Step 2: Sample reviews only if sample_size is given
    if sample_size is None:
        sampled = sampled_reviews
    elif sample_size > len(sampled_reviews):
        print(f"Sample size {sample_size} > available reviews. Using full dataset.")
        sampled = sampled_reviews
    else:
        sampled = random.sample(sampled_reviews, sample_size)

    sample_df = pd.DataFrame(sampled)

    # Step 3: Merge with business info
    sample_df = sample_df.merge(business_df, on="business_id", how="left")

    # Step 4: Sort by stars and reset index
    sample_df = sample_df.sort_values(by="stars").reset_index(drop=True)

    # Step 5: Save compressed CSV only if output path is provided
    if output_csv_path is not None:
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        sample_df.to_csv(output_csv_path, index=False, compression="gzip")
        print(f"Compressed CSV saved: {output_csv_path} ({len(sample_df)} rows)")

    return sample_df


def evaluate_sample_sizes(df, sample_sizes):
    results = []

    for size in sample_sizes:
        sample = df.sample(n=min(size, len(df)), random_state=42)

        avg_stars = sample["stars"].mean()
        std_stars = sample["stars"].std()
        review_count = len(sample)

        results.append({
            "sample_size": size,
            "avg_stars": avg_stars,
            "std_stars": std_stars,
            "num_reviews": review_count
        })

    return pd.DataFrame(results)


# Sampling
if __name__ == "__main__":

    # First load full cleaned dataset (without sampling yet)
    df = clean_and_sample_yelp_lines(
        review_json_path="data/raw/yelp_academic_dataset_review.json",
        business_json_path="data/raw/yelp_academic_dataset_business.json",
        sample_size=None,
        output_csv_path=None
    )

    # Then test different sample sizes
    sample_sizes = [1000, 3000, 10000, 25000, 30000, 50000, 100000, 200000]

    results = evaluate_sample_sizes(df, sample_sizes)

    print(results.sort_values("sample_size"))

    # 50k seems to be a good balance between representativeness and computational efficiency
    best_size = 50000

    # Finally save the final sample of 50k reviews for analysis
    final_sample = df.sample(n=best_size, random_state=42)

    final_sample.to_csv(
        "data/processed/yelp_sample.csv.gz",
        index=False,
        compression="gzip"
    )

    print(f"Final 50k sample saved: data/processed/yelp_sample.csv.gz ({len(final_sample)} rows)")