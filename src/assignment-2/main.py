# ORCHESTRATION FILE
# each operation should be contained in each function, 
# which are consequently executed here

import pandas as pd

from datacleaning import clean_and_sample
from measurement import happiness_scoring
from analysis import analyze_data
from visualization import visualize_data

# 1. IMPORT THE DATASET
df_business = pd.read_json(
    'data/raw/yelp_academic_dataset_review.json',
    lines=True
)

# 2. DATASET CLEANING
clean_df = clean_and_sample(df_business, sample_size=250000) # change the sample size according to research logic
#clean_df = pd.read_csv('data/processed/yelp_sample.csv')

# 3. SCORING
scored_df = happiness_scoring(clean_df)
# new fiels: tokens, happiness_score, total_tokens, matched_tokens, oov_tokens, oov_rate

# 4. ANALYSIS
analyze_data(scored_df)

# 5. VISUALIZATION
visualize_data(scored_df)

print("pipeline executed successfully")