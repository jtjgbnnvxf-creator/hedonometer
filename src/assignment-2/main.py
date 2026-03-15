# ORCHESTRATION FILE
# each operation should be contained in each function, 
# which are consequently executed here

import pandas as pd
from datacleaning import clean_and_sample

# 1. IMPORT THE DATASET
df_business = pd.read_json(
    'data/raw/assignment-2/yelp_sample.json',
    lines=True
)

# 2. DATASET CLEANING
clean_df = clean_and_sample(df_business, sample_size=250000) # change the sample size according to research logic

# 3. SCORING
pass

# 4. ANALYSIS
pass

# 5. VISUALIZATION
pass