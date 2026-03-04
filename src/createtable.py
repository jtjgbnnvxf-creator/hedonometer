import pandas as pd
import os
import subprocess
from datetime import datetime

#Load the dataset
df = pd.read_csv("data/processed/Data_Set_S1.csv")

#preview the columns
print(df.columns)

# Category 1: Very Positive
very_positive = df.sort_values(by="happiness_average", ascending=False).head(5)

# Category 2: Very Negative
very_negative = df.sort_values(by="happiness_average", ascending=True).head(5)

# Category 3: Highly Contested
high_std = df.sort_values(by="happiness_standard_deviation", ascending=False).head(5)

# Category 4: Surprising (neutral happiness, but with high disagreement)
surprising = df[(df["happiness_average"].between(4.5, 5.5))].sort_values(by="happiness_standard_deviation", ascending=False).head(5)

# 20 word summary table
summary_table = pd.concat([
    very_positive.assign(category="Very Positive"),
    very_negative.assign(category="Very Negative"),
    high_std.assign(category="Highly Contested"),
    surprising.assign(category="Surprising")
])[["category", "word", "happiness_average", "happiness_standard_deviation"]]

# Save full dataset
df.to_csv("full_output.csv", index=False)

# Print Results
print("Top 5 Very Positive Words:\n", very_positive[["word","happiness_average"]])
print("\nTop 5 Very Negative Words:\n", very_negative[["word", "happiness_average"]])
print("\nTop 5 Highly Contested Words:\n", high_std[["word","happiness_standard_deviation"]])
print("\nSurprising Words:\n", surprising[["word", "happiness_average","happiness_standard_deviation"]])

# Move to existing markdown file
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
md_path = "word_exhibit.md"

with open(md_path, "a") as f:
    f.write(f"# Hedonometer Word Analysis\n\n")
    f.write("##20-Word Summary Table\n\n")
    f.write(summary_table.to_markdown(index=False))
    f.write("\n\n---\n\n")
    f.write(f"\n\n---\n\n")
    f.write("Top 5 Very Positive Words\n")
    f.write(very_positive[["word", "happiness_average"]].to_markdown(index=False))
    f.write("\n\n#### Top 5 Very Negative Words\n")
    f.write(very_negative[["word", "happiness_average"]].to_markdown(index=False))
    f.write("\n\n####  Top 5 Highly Contested Words\n")
    f.write(high_std[["word", "happiness_standard_deviation"]].to_markdown(index=False))
    f.write("\n\n#### Surprising Words (Neutral but Divisive)\n")
    f.write(surprising[["word", "happiness_average", "happiness_standard_deviation"]].to_markdown(index=False))

