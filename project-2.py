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
plt.show()

# --- Summary statistics ---
col = df['happiness_average']
print(col.describe(percentiles=[0.05, 0.25, 0.75, 0.95]))
print("Mean:        ", col.mean())
print("Median:      ", col.median())
print("Std Dev:     ", col.std())
print("5th pctile:  ", col.quantile(0.05))
print("95th pctile: ", col.quantile(0.95))