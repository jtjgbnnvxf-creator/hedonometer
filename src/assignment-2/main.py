# ORCHESTRATION FILE

import pandas as pd

from datacleaning import clean_and_sample_yelp_lines
from measurement import happiness_scoring
from analysis import analyze_data
from visualization import visualize_data

# 1. IMPORT THE DATASET:
##df_reviews = pd.read_json( 'data/raw/yelp_academic_dataset_review.json', lines=True


# 2. DATASET CLEANING AND SAMPLING:

# 2.1 GENERATION:
#clean_df = clean_and_sample_yelp_lines('data/raw/yelp_academic_dataset_review.json', 'data/raw/yelp_academic_dataset_business.json', sample_size=200_000, output_csv_path="data/yelp_sample.csv.gz")

# 2.2 READING:
clean_df = pd.read_csv('data/processed/yelp_hedonometer_scores.csv.gz', compression="gzip")

# 3. SCORING

# 3.1 GENERATION:
scored_df = happiness_scoring(clean_df)

# 3.2 READING:
#scored_df = pd.read_csv('data/processed/yelp_hedonometer_scores.csv.gz')
# new fiels: tokens, happiness_score, total_tokens, matched_tokens, oov_tokens, oov_rate

# 4. ANALYSIS
analyze_data(scored_df)

# 5. VISUALIZATION
visualize_data(scored_df)

print("pipeline executed successfully")