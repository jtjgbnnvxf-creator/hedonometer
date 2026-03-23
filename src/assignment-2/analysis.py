import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

DATA_PATH = "data/processed/yelp_hedonometer_scores.csv.gz"
FIG_DIR = "figures"
os.makedirs(FIG_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH, compression="gzip")

print("\n=== SAMPLE AUDIT ===")
print(f"Raw sample size: {len(df)}")



# Summary statistics: stars

x_stars = df["stars"].dropna().to_numpy()
print("\n=== SUMMARY STATISTICS: STARS ===")
print(f"n = {len(x_stars)}")
print(f"min = {np.min(x_stars):.3f}")
print(f"max = {np.max(x_stars):.3f}")
print(f"range = {(np.max(x_stars) - np.min(x_stars)):.3f}")
print(f"mean = {np.mean(x_stars):.3f}")
print(f"median = {np.median(x_stars):.3f}")

#Here we describe the shape of the distribution of star ratings using quantiles (equal sized parts) 
#to avoid assuming normal distribution, we also report the IQR (inter-quartile range) as a measure of spread that is robust to outliers.
#IQR is the difference between the 75th percentile (Q3) and the 25th percentile (Q1)
#gives us an idea of the range of the middle 50% of the data. 
#(takes out outliers or extreme values that could skew the mean and standard deviation)

qs = np.quantile(x_stars, [0.10, 0.25, 0.50, 0.75, 0.90])
print(f"q10 = {qs[0]:.3f}")
print(f"q25 = {qs[1]:.3f}")
print(f"q50 = {qs[2]:.3f}")
print(f"q75 = {qs[3]:.3f}")
print(f"q90 = {qs[4]:.3f}")
print(f"IQR = {(qs[3] - qs[1]):.3f}")
print(f"sample variance = {np.var(x_stars, ddof=1):.3f}")
print(f"sample SD = {np.std(x_stars, ddof=1):.3f}")

#MAD (median absolute deviation) is a measure of variability that is less sensitive to outliers (extremes)
# than the standard deviation.
mad_stars = np.median(np.abs(x_stars - np.median(x_stars)))
print(f"MAD = {mad_stars:.3f}")

#Skewness  measures the assymetry of the distribution. More far from 0 means longer tail on one side
print(f"skewness = {stats.skew(x_stars, bias=False):.3f}")
#Kurtosis measures how havey the tailes are:
# 0 - normal distribution, positive - heavy tails (more outliers), negative - light tails(less outliers)
print(f"excess kurtosis = {stats.kurtosis(x_stars, fisher=True, bias=False):.3f}")


# Summary statistics: hedonometer score
x_happy = df["hedonometer_score"].dropna().to_numpy()

print("\n=== SUMMARY STATISTICS: HEDONOMETER SCORE ===")
print(f"n = {len(x_happy)}")
print(f"min = {np.min(x_happy):.3f}")
print(f"max = {np.max(x_happy):.3f}")
print(f"range = {(np.max(x_happy) - np.min(x_happy)):.3f}")
print(f"mean = {np.mean(x_happy):.3f}")
print(f"median = {np.median(x_happy):.3f}")

qs = np.quantile(x_happy, [0.10, 0.25, 0.50, 0.75, 0.90])
print(f"q10 = {qs[0]:.3f}")
print(f"q25 = {qs[1]:.3f}")
print(f"q50 = {qs[2]:.3f}")
print(f"q75 = {qs[3]:.3f}")
print(f"q90 = {qs[4]:.3f}")
print(f"IQR = {(qs[3] - qs[1]):.3f}")
print(f"sample variance = {np.var(x_happy, ddof=1):.3f}")
print(f"sample SD = {np.std(x_happy, ddof=1):.3f}")

mad_happy = np.median(np.abs(x_happy - np.median(x_happy)))
print(f"MAD = {mad_happy:.3f}")
print(f"skewness = {stats.skew(x_happy, bias=False):.3f}")
print(f"excess kurtosis = {stats.kurtosis(x_happy, fisher=True, bias=False):.3f}")

# Happiness by star rating
#Here we check the average happiness score for each star rating to see if there is a relationship between them.
#The output will show us if higher star ratings tend to have higher happiness scores, 
# which would suggest that the hedonometer is capturing something meaningful about the reviews.
descriptives = df.groupby("stars")["hedonometer_score"].agg(
    mean="mean",
    median="median",
    count="count",
    std="std"
)

print("\n=== HAPPINESS BY STAR RATING ===")
print(descriptives)

# Main association: covariance and Pearson correlation
x = pd.to_numeric(df["hedonometer_score"], errors="coerce")
y = pd.to_numeric(df["stars"], errors="coerce")

xy = pd.concat([x, y], axis=1).dropna()
xy.columns = ["hedonometer_score", "stars"]

x = xy["hedonometer_score"].to_numpy()
y = xy["stars"].to_numpy()

cov_xy = np.cov(x, y, ddof=1)[0, 1]
r = np.corrcoef(x, y)[0, 1]
r_test = stats.pearsonr(x, y)

print("\n=== ASSOCIATION BETWEEN HEDONOMETER SCORE AND STAR RATING ===")
print(f"Sample covariance(hedonometer_score, stars) = {cov_xy:.4f}")
print(f"Pearson correlation r = {r:.4f}")

#Z-score: implementing the standardized effect size (z-score) 
#for the relationship between star ratings and hedonometer scores.
print("\n=== STANDARDIZED EFFECT (Z-SCORES) ===")

# standardize both variables
x_z = (x - np.mean(x)) / np.std(x, ddof=1)   # hedonometer score
y_z = (y - np.mean(y)) / np.std(y, ddof=1)   # star rating

# fit line to z-scores: to check how many standard deviations of increase in star rating (y)
# we get for each standard deviation increase in hedonometer score (x).
# the slope of the line will be the standardized effect size (b_z),
# and the intercept (a_z) should be close to 0 if both variables are standardized.
b_z, a_z = np.polyfit(x_z, y_z, 1)

# R-squared from standardized regression
r_squared = b_z**2

print(f"Standardized slope (b_z) = {b_z:.4f}")
print(f"Standardized intercept (a_z) = {a_z:.4f}")
print(f"R-squared = {r_squared:.4f}")
print(f"Variance explained = {r_squared*100:.2f}%")

# fit line to z-scores: to check how many standard deviations of increase in hedonometer score (y)
# we get for each standard deviation increase in star rating (x). 
# the slope of the line will be the standardized effect size (b_z),
# and the intercept (a_z) should be close to 0 if both variables are standardized.
b_z, a_z = np.polyfit(x_z, y_z, 1)

print(f"Standardized slope (b_z) = {b_z:.4f}")
print(f"Standardized intercept (a_z) = {a_z:.4f}")

print(
    f"A 1 SD increase in hedonometer score is associated with "
    f"a {b_z:.3f} SD increase in star rating."
)

print(f"(This should match Pearson r ≈ {r:.4f})")

# Bootstrap AFTER correlation
# We will use a bootstrap procedure to estimate the sampling distribution of the Pearson correlation coefficient (r) 
# between star ratings and hedonometer scores.
print("\n=== BOOTSTRAP RESULTS ===")

rng = np.random.default_rng(42)
businesses = df["business_id"].dropna().unique()
grouped = {b: g for b, g in df.groupby("business_id")}

r_boot = []
B = 250
# We chose 250 times, for a balance between accuracy and computational time 
# as our sample ios large
for i in range(B):
    sampled_businesses = rng.choice(
        businesses,
        size=len(businesses),
        replace=True
    )

    boot_parts = [grouped[b] for b in sampled_businesses]
    boot_df = pd.concat(boot_parts, ignore_index=True)

    x_b = pd.to_numeric(boot_df["stars"], errors="coerce")
    y_b = pd.to_numeric(boot_df["hedonometer_score"], errors="coerce")

    xy_b = pd.concat([x_b, y_b], axis=1).dropna()
    xy_b.columns = ["stars", "hedonometer_score"]

    x_b = xy_b["stars"].to_numpy()
    y_b = xy_b["hedonometer_score"].to_numpy()

    if len(np.unique(x_b)) < 2 or len(np.unique(y_b)) < 2:
        continue

    r_b = np.corrcoef(x_b, y_b)[0, 1]
    if np.isfinite(r_b):
        r_boot.append(r_b)

r_boot = np.array(r_boot)

if len(r_boot) > 0:
    ci_low = np.quantile(r_boot, 0.025)
    ci_high = np.quantile(r_boot, 0.975)
    boot_mean = np.mean(r_boot)
    boot_se = np.std(r_boot, ddof=1)

    print(f"Bootstrap mean r = {boot_mean:.4f}")
    print(f"Bootstrap SE = {boot_se:.4f}")
    print(f"95% bootstrap CI = [{ci_low:.4f}, {ci_high:.4f}]")
else:
    print("No valid bootstrap estimates were produced.")

#Here we are checking the distribution of the bootstrap estimates of the Pearson r
# to see if it is approximately normal and to visualize the variability in the estimate of r.
    print("\n=== BOOTSTRAP DISTRIBUTION ===")

fig, ax = plt.subplots(figsize=(7,4))

ax.hist(r_boot, bins=30)

ax.set_title("Bootstrap distribution of Pearson correlation")
ax.set_xlabel("Bootstrap Pearson r")
ax.set_ylabel("Frequency")

# confidence interval lines
ci_low = np.quantile(r_boot, 0.025)
ci_high = np.quantile(r_boot, 0.975)

ax.axvline(ci_low, linestyle="--", label="2.5%")
ax.axvline(ci_high, linestyle="--", label="97.5%")

# original r
ax.axvline(r, linestyle="-", label="Observed r")

ax.legend()
plt.savefig(os.path.join(FIG_DIR, "bootstrap_correlation.png"), dpi=300, bbox_inches="tight")
plt.close()


# Scatter plot with fitted line
b, a = np.polyfit(x, y, 1)
xline = np.linspace(x.min(), x.max(), 200)
yline = a + b * xline

fig, ax = plt.subplots(figsize=(7.6, 4.6))
ax.scatter(x, y, s=18, alpha=0.4, label="Reviews")
ax.plot(xline, yline, linewidth=1.5, label="Least-squares line")

ax.set_title("Yelp stars vs hedonometer score")
ax.set_xlabel("Yelp star rating")
ax.set_ylabel("Hedonometer score")
ax.grid(True, alpha=0.25)
ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), title=f"Pearson r = {r:.3f}")

fig.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "stars_vs_happiness.png"), dpi=300, bbox_inches="tight")
plt.close()

# Standardized regression plot (z-scores)
xline_z = np.linspace(x_z.min(), x_z.max(), 200)
yline_z = a_z + b_z * xline_z

fig, ax = plt.subplots(figsize=(7,4.6))
ax.scatter(x_z, y_z, s=18, alpha=0.4, label="Standardized reviews")
ax.plot(xline_z, yline_z, linewidth=1.8, label="Standardized regression")

ax.set_title("Standardized regression: stars vs hedonometer score")
ax.set_xlabel("Star rating (z-score)")
ax.set_ylabel("Hedonometer score (z-score)")
ax.grid(True, alpha=0.25)

ax.legend(title=f"b_z = {b_z:.3f}")

fig.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "standardized_regression.png"), dpi=300, bbox_inches="tight")
plt.close()
print("\nAnalysis complete.")
