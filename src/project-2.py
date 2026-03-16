import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('/Users/danielsitumeang/Desktop/coding-humanities/data/processed/Data_Set_S1.csv')

# --- Histogram ---
df['happiness_average'].hist(bins=20, color='steelblue', edgecolor='black')
plt.title('Distribution of Happiness Scores')
plt.xlabel('Happiness Score')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('happiness_histogram.png')  # saves as image
plt.close() #changed from plt.show() to plt.close() to avoid displaying the plot in interactive environments

# --- Summary statistics ---
col = df['happiness_average']
print(col.describe(percentiles=[0.05, 0.25, 0.75, 0.95]))
print("Mean:        ", col.mean())
print("Median:      ", col.median())
print("Std Dev:     ", col.std())
print("5th pctile:  ", col.quantile(0.05))
print("95th pctile: ", col.quantile(0.95))

# --- 2.2 Scatterplot: average vs standard deviation ---
plt.figure()
plt.scatter(df['happiness_average'], df['happiness_standard_deviation'], 
            alpha=0.3, color='steelblue', edgecolors='none', s=10)
plt.title('Happiness Average vs Standard Deviation')
plt.xlabel('Happiness Average')
plt.ylabel('Standard Deviation')
plt.tight_layout()
plt.savefig('happiness_scatter.png')
plt.close() #changed from plt.show() to plt.close() to avoid displaying the plot in interactive environments

# --- Top 15 most contested words ---
top15 = df.nlargest(15, 'happiness_standard_deviation')[['word', 'happiness_average', 'happiness_standard_deviation']]
print(top15.to_string(index=False))
