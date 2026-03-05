import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("Data_Set_S1.csv", 
                 sep="\t",
                 skiprows=3,
                 na_values=["-"], 
                 encoding="utf-8"
                 )

corpora = ["twitter", "google", "nyt", "lyrics"]

# Count how many labMT words appear in each corpus top 5000 ---------- 
# "appear in top 5000" = rank exists AND rank <= 5000
top5000_sets = {}

for c in corpora: 
    col = f"{c}_rank"
    present_top5000 = df.loc[df[col].notna() & (df[col] <= 5000), "labMT_word"]
    top5000_sets[c] = set(present_top5000)

counts_present = {c: len(top5000_sets[c]) for c in corpora}

print("Number of labMT words in top 5000 for each corpus")
for c in corpora: 
    print(f"{c}: {counts_present[c]}")

# ---------- Overlap table ----------
# Pairwise overlaps (Twitter & NYT, etc.)
overlap = pd.DataFrame (index-corpora, columns = corpora, dtype=int)

for a in corpora: 
    for b in corpora: 
        overlap.loc[a,b] = len(top5000_sets[a] & top5000_sets[b])

print("\n--- Pairwise overlaps (top 5000 sets) ---")
print(overlap)

# How many words appear in all 4 corporas? 
all_four = set.intersection(*(top5000_sets[c] for c in corpora))
print("\nWords in all 4 corpora (top 5000):", len(all_four))

# ---------- Bar chart of "how many words are present"
plt.figure()
plt.bar(counts_present.keys(), counts_present.values())
plt.title("How many labMT words in each corpus top 5000?")
plt.xlabel("Corpus")
plt.ylabel("Count of words (rank <= 5000)")
plt.tight_layout()
plt.savefig("top5000_presence_bar.png")
plt.close()