import os
os.makedirs("figures", exist_ok=True)
#---review length---
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

DATA_PATH = "data/processed/yelp_hedonometer_scores.csv.gz"

df = pd.read_csv(DATA_PATH, compression="gzip")
df["token_count"] = df["text"].dropna().apply(lambda x: len(x.split()))

##Histogram for distribution of review length to show right skew
fig, ax = plt.subplots()
ax.hist(df['token_count'], bins=50, color='#1f77b4', edgecolor='black', linewidth=0.5)
ax.set_facecolor('#e8e8e8')
ax.set_axisbelow(True)
ax.grid(True, color='white', linewidth=0.8)

mean_val = df['token_count'].mean()
median_val = df['token_count'].median()
plt.axvline(mean_val, color='red', linestyle='dashed', linewidth=1, label=f'Mean: {mean_val:.2f}')
plt.axvline(median_val, color='green', linestyle='dashed', linewidth=1, label=f'Median: {median_val:.2f}')

#legend
plt.legend()

plt.title('Distribution of Review Lengths')
plt.xlabel('Number of Tokens')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('figures/distribution_of_review_lengths.png')  # saves as image
plt.close()

##Bar chart for average tokens per review by star rating
stars = [1, 2, 3, 4, 5]
avg_tokens = [132.372967, 133.463374, 124.087035, 108.245352, 84.760112]

# Create bar chart
plt.figure()
plt.bar(stars, avg_tokens, edgecolor='black')

# Labels and title
plt.title('Average Review Length by Star Rating')
plt.xlabel('Star Rating')
plt.ylabel('Average Number of Tokens')

# Improve x-axis ticks
plt.xticks(stars)

# Layout and save
plt.tight_layout()
plt.savefig('figures/avg_tokens_by_stars.png')
plt.close()

#---Star ratings bar chart---
plt.figure()
# Get counts per star rating
star_counts = df['stars'].value_counts().sort_index()

mean_val   = df['stars'].mean()
median_val = df['stars'].median()

plt.figure()

plt.bar(star_counts.index, star_counts.values, edgecolor='black', width=0.6)

# Add mean and median lines
plt.axvline(mean_val,  color='red', linestyle='dashed', linewidth=1, label=f'Mean: {mean_val:.2f}')
plt.axvline(median_val, color='green', linestyle='dashed',  linewidth=1, label=f'Median: {median_val:.0f}')

plt.title('Distribution of Star Ratings')
plt.xlabel('Star Rating')
plt.ylabel('Frequency')
plt.xticks([1, 2, 3, 4, 5])
plt.legend()

plt.tight_layout()
plt.savefig('figures/star_ratings_bar_chart.png')
plt.close()

#---hedometer score histogram---

# Histogram of hedonometer scores
plt.figure()

df['hedonometer_score'].hist(bins=30, edgecolor='black')

# Add mean and median lines
mean_val = df['hedonometer_score'].mean()
median_val = df['hedonometer_score'].median()

plt.axvline(mean_val, color='red', linestyle='dashed', linewidth=1, label=f'Mean: {mean_val:.3f}')
plt.axvline(median_val, color='green', linestyle='dashed', linewidth=1, label=f'Median: {median_val:.3f}')

# Labels and title
plt.title('Distribution of Hedonometer Scores')
plt.xlabel('Hedonometer Score')
plt.ylabel('Frequency')

# Legend
plt.legend()

# Layout and save
plt.tight_layout()
plt.savefig('figures/hedonometer_histogram.png')
plt.close()

#---happiness by star rating---
stars = [1.0, 2.0, 3.0, 4.0, 5.0]
means = [5.740709, 6.029623, 6.246072, 6.459320, 6.534397]
stds  = [0.431976, 0.383673, 0.349239, 0.332066, 0.354044]
counts = [7708, 3828, 4880, 10663, 22911]

sems = [s / np.sqrt(n) for s, n in zip(stds, counts)]

fig, ax = plt.subplots(figsize=(8, 5))

ax.errorbar(
    stars, means, yerr=stds,   # switched to stds
    fmt='o',
    color='steelblue',
    ecolor='steelblue',
    elinewidth=1.5,
    capsize=5,
    capthick=1.5,
    markersize=7,
    linewidth=2,
    zorder=3
)

ax.set_xlabel('Star Rating', fontsize=12)
ax.set_ylabel('Mean Happiness Score', fontsize=12)
ax.set_title('Happiness Score by Star Rating', fontsize=13)
ax.set_xticks([1, 2, 3, 4, 5])
ax.set_xlim(0.5, 5.5)
ax.set_ylim(5.2, 7.1)                                        # zoomed y-axis
ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.3f')) # three decimal places

ax.set_axisbelow(True)
ax.grid(True, axis='both', color='white', linewidth=0.8)
ax.set_facecolor('#e8e8e8')

plt.tight_layout()
plt.savefig('figures/happiness_by_star.png', dpi=150)
plt.show()