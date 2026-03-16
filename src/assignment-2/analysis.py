# ==========================================================
# ANALYSIS FILE
# Purpose of this file:
# 1. check the sample composition
# 2. build the final analytic sample
# 3. create a leave-one-out state average star variable to account for the state-level sentiment context
# 4. estimate the main regression model
# 5. bootstrap the coefficient on Yelp stars
# 6. estimate separate models by state
# 7. estimate separate models by business category
# Main research idea:
# We want to test whether higher Yelp star ratings are
# associated with more positive language in the review text,
# measured here with a hedonometer score.
# -----------------------------
# Import required libraries
from pyexpat import model

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
# Use helper function to add_state_average
# Goal: Create a leave-one-out state-level average of Yelp stars.
# Why do this? If some states have give higher or lower star ratings,then part of the relationship between stars and review tone might reflect state context rather than the review itself.
# To adjust for this, we create a control variable:
# "state_avg_stars"
#
# Important:
# We use a leave-one-out average, meaning:
# for each review, we compute the average star rating in that state but excluding  that review's own star value.
#This prevents the control variable from mechanically containing the outcome review itself.
def add_state_average(df):
    # Make a copy so we do not accidentally change the original dataframe outside this function
    df = df.copy()

    # For every row, calculate the total number of stars assigned across all reviews in the same state
    state_sum = df.groupby("state")["stars"].transform("sum")

    # For every row, calculate how many reviews exist in that same state
    state_count = df.groupby("state")["stars"].transform("count")

    # Leave-one-out state average: subtract the current row's stars from the state total,and subtract 1 from the state count
    # Formula: (sum of all stars in state - this row's stars) / (number of reviews in state - 1)
 
    df["state_avg_stars"] = (state_sum - df["stars"]) / (state_count - 1)

    # If a state has only one review, then the denominator  becomes zero and the leave-one-out mean is impossibleto compute, so we set it to missing
    df.loc[state_count <= 1, "state_avg_stars"] = np.nan

    return df


# bootstrap_stars
#
# Goal: Estimate a bootstrap distribution for the coefficient on Yelp stars from the main regression model.
# Why bootstrap? The bootstrap gives us an additional way to understand the uncertainty around the coefficient estimate.
#
# We use resampling at the business level because reviews from the same business are likely correlated, and we want to preserve that structure in the bootstrap samples.
# Steps inside this function:
# 1. identify all unique businesses
# 2. repeatedly resample businesses with replacement
# 3. rebuild a bootstrap dataset from those businesses
# 4. re-estimate the regression each time
# 5. save the coefficient on "stars"
def bootstrap_stars(df, B=10):
    print("\nStarting bootstrap...", flush=True)

    # Extract unique business IDs from the analytic sample
    businesses = df["business_id"].unique()

    # Pre-group the dataframe by business_id and store each
    # business's reviews in a dictionary.
    # This is much faster than repeatedly doing:
    # df[df["business_id"] == b]
    # inside the bootstrap loop.
    grouped = {b: g for b, g in df.groupby("business_id")}

    # This list will store the coefficient on "stars" from each bootstrap replication
    betas = []

    print(f"Number of unique businesses: {len(businesses)}", flush=True)
    print(f"Bootstrap repetitions: {B}", flush=True)

    # Repeat the bootstrap procedure B times
    for i in range(B):
        print(f"Bootstrap {i + 1}/{B}...", flush=True)

        # Randomly sample businesses WITH replacement by replacement, we mean the same business can appear multiple times in one bootstrap sample, while some businesses may not appear at all in that sample
        sampled_businesses = np.random.choice(
            businesses,
            size=len(businesses),
            replace=True
        )

        # Reconstruct the bootstrap dataframe by concatenating the review subsets for the sampled businesses
        parts = [grouped[b] for b in sampled_businesses]
        boot_df = pd.concat(parts, ignore_index=True)

        try:
            # Fit the same regression model used in the main analysis
            m = smf.ols(
                "hedonometer_score ~ stars + state_avg_stars",
                data=boot_df
            ).fit()

            # Save the coefficient on Yelp star rating
            betas.append(m.params["stars"])

        except Exception as e:
            # If a bootstrap draw fails for any reason, report it
            # and continue with the next replication
            print(f"Bootstrap {i + 1} failed: {e}", flush=True)

    print("Bootstrap complete.", flush=True)

    # Convert the list into a numpy array for easier quantile calculation
    return np.array(betas)


# MAIN FUNCTION: analyze_data
#
# Input:
# scored_df = dataframe that already contains:
# - Yelp star ratings
# - review text
# - business/location info
# - hedonometer_score
#
# This function performs the full analysis and prints results to the terminal.
def analyze_data(scored_df):
    print("\nStarting analysis...", flush=True)

    # STEP 1: SAMPLE AUDIT
    # Goal: Get a general overview of the dataset before filtering.
    # We check:
    # - total sample size
    # - distribution of star ratings
    # - number of states represented
    # - states with the most reviews
 
    print("\n=== SAMPLE AUDIT ===", flush=True)

    # Total number of rows currently in the scored dataset
    print("Sample size:", len(scored_df), flush=True)

    # Proportion of reviews in each star category
    print("\nStar rating distribution:", flush=True)
    print(scored_df["stars"].value_counts(normalize=True).sort_index(), flush=True)

    # Count how many unique states appear in the dataset
    print("\nStates in sample:", scored_df["state"].nunique(), flush=True)

    # Show the states with the largest number of reviews
    print("\nTop states:", flush=True)
    print(scored_df["state"].value_counts().head(), flush=True)

 
    # STEP 2: BUILD THE ANALYTIC SAMPLE
    #Goal:
    # Keep only observations that contain the variables required for the main regression.
    # These required variables are:
    # - hedonometer_score: dependent variable
    # - stars: main explanatory variable
    # - business_id: needed for clustering/bootstrap
    # - state: needed for the state-level control

    required_cols = ["hedonometer_score", "stars", "business_id", "state"]

    # Drop rows with missing values in any of the required columns
    analytic = scored_df.dropna(subset=required_cols).copy()

    print("\n=== ANALYTIC SAMPLE ===", flush=True)
    print("Rows after filtering:", len(analytic), flush=True)
    print("Businesses:", analytic["business_id"].nunique(), flush=True)

    # ======================================================
    # STEP 3: ADD STATE-LEVEL CONTROL VARIABLE
    #
    # Goal:
    # Create the leave-one-out state average of stars and
    # add it to the analytic dataset.
    #
    # Then drop rows where this value could not be computed.
    # ======================================================
    print("\nAdding state average variable...", flush=True)

    analytic = add_state_average(analytic)

    # Drop rows where the state average is missing
    analytic = analytic.dropna(subset=["state_avg_stars"])

    print("State average star rating added.", flush=True)
    print("Rows after dropping invalid state averages:", len(analytic), flush=True)

    # ======================================================
    # STEP 4: DESCRIPTIVE STATISTICS
    #
    # Goal:
    # Before running the regression, look at the simple,
    # raw relationship between Yelp stars and hedonometer score.
    #
    # For each star level, calculate:
    # - mean hedonometer score
    # - number of reviews
    # - standard deviation
    # ======================================================
    descriptives = analytic.groupby("stars")["hedonometer_score"].agg(
        ["mean", "count", "std"]
    )

    print("\n=== MEAN HAPPINESS BY STAR RATING ===", flush=True)
    print(descriptives, flush=True)

    # ======================================================
    # STEP 5: MAIN REGRESSION
    #
    # Model:
    # hedonometer_score ~ stars + state_avg_stars
    #
    # Interpretation:
    # - "stars" tells us how much the hedonometer score changes
    #   when the Yelp rating increases by one star
    # - "state_avg_stars" controls for broader rating tendencies
    #   in the state
    #
    # We cluster standard errors by business_id because reviews
    # from the same business are likely correlated.
    # ======================================================
    print("\nFitting regression model...", flush=True)

    model = smf.ols(
        "hedonometer_score ~ stars + state_avg_stars",
        data=analytic
    ).fit(
        cov_type="cluster",
        cov_kwds={"groups": analytic["business_id"]}
    )
    print("\n=== REGRESSION RESULTS ===", flush=True)
    print(model.summary(), flush=True)

    # clean summary of the main effect
    beta_stars = model.params["stars"]
    se_stars = model.bse["stars"]
    p_stars = model.pvalues["stars"]

    print("\n=== KEY RESULT ===", flush=True)
    print(f"Coefficient on stars: {beta_stars:.4f}", flush=True)
    print(f"Standard error: {se_stars:.4f}", flush=True)
    print(f"P-value: {p_stars:.4g}", flush=True)

    
    
    # ======================================================
    # STEP 6: BOOTSTRAP CONFIDENCE INTERVAL
    #
    # Goal:
    # Use repeated business-level resampling to estimate a
    # bootstrap confidence interval for the coefficient on stars.
    #
    # We take the 2.5th and 97.5th percentiles of the bootstrap
    # distribution to form an approximate 95% confidence interval.
    # ======================================================
    betas = bootstrap_stars(analytic, B=500)

    print("\n=== BOOTSTRAP RESULTS ===", flush=True)

    if len(betas) > 0:
        ci_low = np.quantile(betas, 0.025)
        ci_high = np.quantile(betas, 0.975)
        print("95% CI:", ci_low, ci_high, flush=True)
    else:
        print("No valid bootstrap estimates were produced.", flush=True)

    # ======================================================
    # STEP 7: INTERPRETATION OF MAIN EFFECT
    #
    # Goal:
    # Print a human-readable interpretation of the coefficient
    # on Yelp stars from the main regression.
    # ======================================================
    beta = model.params["stars"]

    print("\n=== INTERPRETATION ===", flush=True)
    print(
        f"A one-star increase in Yelp rating is associated with "
        f"{beta:.3f} increase in hedonometer score, "
        f"controlling for the average star rating in the state.",
        flush=True
    )

    # ======================================================
    # STEP 8: STATE-LEVEL DIFFERENCES
    #
    # Goal:
    # Estimate whether the stars-to-language relationship looks
    # different across states.
    #
    # Important modeling note:
    # In these within-state models, we DO NOT include
    # state_avg_stars, because inside one state it becomes almost
    # a linear function of stars and causes instability.
    #
    # So the state-level model is simply:
    # hedonometer_score ~ stars
    #
    # To avoid very unstable estimates, we only keep states with
    # at least 1000 reviews.
    # ======================================================
    print("\n=== STATE-LEVEL EFFECTS ===", flush=True)

    state_results = []
    skipped_states = 0

    for state, group in analytic.groupby("state"):
        # Skip states that do not have enough observations
        if len(group) < 1000:
            skipped_states += 1
            continue

        print(f"Processing state: {state} (n={len(group)})", flush=True)

        try:
            # Run a within-state regression
            m = smf.ols(
                "hedonometer_score ~ stars",
                data=group
            ).fit()

            # Store the state name, coefficient, and sample size
            state_results.append({
                "state": state,
                "beta_stars": m.params["stars"],
                "n_reviews": len(group)
            })

        except Exception as e:
            print(f"State model failed for {state}: {e}", flush=True)

    # Turn results into a dataframe
    state_results = pd.DataFrame(state_results)

    if not state_results.empty:
        # Sort from largest estimated effect to smallest
        state_results = state_results.sort_values("beta_stars", ascending=False)
        print(state_results, flush=True)
    else:
        print("No state-level results available.", flush=True)

    print(f"Skipped states with too few observations: {skipped_states}", flush=True)

    # ======================================================
    # STEP 9: CATEGORY-LEVEL DIFFERENCES
    #
    # Goal:
    # Estimate whether the stars-to-language relationship differs
    # across business categories.
    #
    # The raw Yelp column is called "categories" and usually
    # contains a comma-separated list such as:
    # "Restaurants, Mexican, Bars"
    #
    # For simplicity, we use only the FIRST listed category and
    # call it "main_category".
    #
    # We then run the model separately within each category.
    #
    # To avoid noisy estimates and huge terminal spam:
    # - first count category sizes
    # - keep only categories with at least 2000 reviews
    # - process only those categories
    # ======================================================
    print("\n=== CATEGORY EFFECTS ===", flush=True)

    # Create a simplified category variable from the first listed category
    analytic["main_category"] = (
        analytic["categories"]
        .fillna("Unknown")   # replace missing category strings
        .astype(str)         # ensure values are strings
        .str.split(",")      # split comma-separated categories
        .str[0]              # keep only the first category
        .str.strip()         # remove extra whitespace
    )

    # Count how many reviews belong to each main category
    cat_counts = analytic["main_category"].value_counts()

    # Keep only categories with 2000 or more reviews
    kept_categories = cat_counts[cat_counts >= 2000].index

    print(f"Categories meeting threshold: {len(kept_categories)}", flush=True)
    print(
        f"Skipped categories with too few observations: {(cat_counts < 2000).sum()}",
        flush=True
    )

    cat_results = []

    for cat in kept_categories:
        # Subset the data to just one category
        group = analytic[analytic["main_category"] == cat]

        print(f"Processing category: {cat} (n={len(group)})", flush=True)

        try:
            # Run the category-specific regression
            #
            # Here we still include state_avg_stars because within
            # a category there are still multiple states represented
            m = smf.ols(
                "hedonometer_score ~ stars + state_avg_stars",
                data=group
            ).fit()

            # Save the category result
            cat_results.append({
                "category": cat,
                "beta_stars": m.params["stars"],
                "n_reviews": len(group)
            })

        except Exception as e:
            print(f"Category model failed for {cat}: {e}", flush=True)

    # Convert to dataframe
    cat_results = pd.DataFrame(cat_results)

    if not cat_results.empty:
        # Sort from strongest estimated effect to weakest
        cat_results = cat_results.sort_values("beta_stars", ascending=False)

        # Print only top 15 for readability
        print(cat_results.head(15), flush=True)
    else:
        print("No category-level results available.", flush=True)

    # Final message so it is obvious the analysis really finished
    print("\nAnalysis complete.", flush=True)