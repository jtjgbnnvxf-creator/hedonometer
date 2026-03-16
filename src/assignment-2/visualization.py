import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns #after consulting with Claude.AI, seaborn was recommended for a boxplot instead of a scatterplot, which shows a less messy visualization of the relationship between happiness score and star rating.

# This function creates the visualization
def visualize_data(score_df):
    print(score_df.columns.tolist())
    print(score_df.head())
    
    #create figure and axis
    fig, ax = plt.subplots(figsize=(9, 6)) # create ax first

    sns.boxplot(
        data=score_df,
        x='stars',
        y='hedonometer_score',
        palette='RdYlGn',
        width=0.5,
        flierprops=dict(marker='o', markerfacecolor='orange', markersize=3, alpha=0.5),
        ax=ax
        )

    ax.set_title('Happiness Score vs. Star Rating', fontsize=14)
    ax.set_xlabel('Star rating', fontsize=12)
    ax.set_ylabel('Happiness score', fontsize=12)
    ax.set_xticklabels(['1 ★', '2 ★', '3 ★', '4 ★', '5 ★'])

    plt.tight_layout()
    plt.savefig('figures/plot1_happiness_vs_stars.png', dpi=150)
    plt.close()

#load dataset
score_df = pd.read_csv('data/processed/yelp_hedonometer_scores.csv.gz', compression='gzip')

print(score_df.columns.tolist())

#run visualization function
visualize_data(score_df)

#table boxplot
import pandas as pd

summary_table = score_df.groupby('stars')['hedonometer_score'].describe()

boxplot_table = summary_table[['min', '25%', '50%', '75%', 'max']]

boxplot_table = boxplot_table.round(2)

print(boxplot_table)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
score_df = pd.read_csv('data/processed/yelp_hedonometer_scores.csv.gz', compression='gzip')

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
score_df = pd.read_csv('data/processed/yelp_hedonometer_scores.csv.gz', compression='gzip')

# Create a summary table for the boxplot (min, Q1, median, Q3, max)
summary_table = score_df.groupby('stars')['hedonometer_score'].describe()
boxplot_table = summary_table[['min', '25%', '50%', '75%', 'max']].round(2).reset_index()

# Create a simple table figure
fig, ax = plt.subplots(figsize=(8, 2))  # short figure height for table only
ax.axis('off')  # hide axes

# Add table to figure
table = ax.table(cellText=boxplot_table.values,
                 colLabels=boxplot_table.columns,
                 cellLoc='center',
                 loc='center')

# Save the figure separately
plt.savefig('figures/simple_table.png', dpi=150, bbox_inches='tight')
plt.show()
plt.close()