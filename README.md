# Hedonometer Group 8 

datasets are not present in the repo due to large files size.
!(assignemnt-2 avaliable on Kaggle)[https://www.kaggle.com/datasets/yelp-dataset/yelp-dataset/discussion/210898]

---
# 1 The dataset
```mermaid
flowchart TD
    A[Raw Yelp Dataset] --> B[Data Cleaning] 
    B --> C[Remove Duplicates]
    B --> D[Remove Missing Reviews]
    B --> E[Remove Empty Reviews]
    C --> F[Clean Dataset]
    D --> F
    E --> F
    F --> G[Analysis]
```

## 1.1 Loading the dataset

The dataset was loaded as a dataframe using the "pandas" library. The first three lines were skipped, as they contained comments rather than data. What remains are 10222 rows and eight columns. In four of these columns (twitter_rank, google_rank, nyt_rank and lyrics_rank) there are missing values (--). Missing values here mean that a word did not appear in a corpus, either at all or not at a frequency high enough to be given a rank.

## 1.2 Creating the data dictionary 

The first column, "word", contains 10222 words in the form of strings. In the column "happiness_rank", each word is ranked in terms of its percieved positivity or negativity (for example, a "2" in this column denotes the second most positive word overall), here in the form of an integer. The remaining columns contain float values. "Happiness_average" provides the mean score of every word's negativity or positivity across raters. The standard deviation, so to what extent there was disagreement between raters about a word's positivity or negativity, is given in the column "happiness_standard_deviation". There are no missing values in any of the columns listed so far. In the columns "twitter_rank", "google_rank", "nyt_rank" and "lyrics_rank", there are 5222 missing values per column. The columns show the frequency rank of each remaining word in the respective corpus. "Twitter_rank" thus ranks each word that appeared in the Twitter corpus based on how frequently it appeared, with lower values again indicating higher frequency. "Google_rank" does the same for words in the Google corpus, "nyt_rank" for the New York Times corpus, and "lyrics_rank" for a corpus of lyrics.

## 1.3. Sanity checks

The first sanity check implemented is a schema check. All eight columns are defined as expected columns, and the check returns "True" if the dataframe contains all expected columns. This ensures that the right file was loaded, the right delimiter used and that no accidental changes were made to the dataset. Second, there is a value-range check. This returns the lowest and highest values in "happiness_average", and the lowest value in "happiness_standard_deviation". The values for "happiness_average" should be between one and nine, and the standard deviation should not be negative. If the check returns a value outside of what is expected, the column may not have the right dtype, the data may be corrupted or there may be parsing errors.

The ten most positive and negative words by average happiness intuitively make sense. Five out of the ten most positive words are different forms of the root word "laugh", there are two forms of the root word "happy", as well as "joy", "excellent" and "love". Laughter is a natural indicator of happiness, for which joy is practically synonymous, and, together with love, happiness is one of the most positive emotions. "Excellent" is a bit more surprising, as it does not feel like a significantly more positive way of describing something than "marvelous", "perfect", "outstanding", and so on. The ten most negative words pattern around the domains death and violence. Seven of them directly or indirectly relate to death. Six of the words are connected to violence. What stands out is that the root word "terror" appears twice, once as "terrorist" and once as "terrorism". That "terrorist" is considered a more negative word than "rape", and "terrorism" is percieved more negatively than "death" is somewhat surprising. However, in the context of a post-9/11 world that fought a war on terror for 20 years, the strong negative connotations of "terror" again make sense.

# 2. Quantitative exploration: distributions and relationships

## 2.1 Distribution of happiness scores 
Firstly, the distribution is centered around 5 to 6 on average happiness score. The highest concentration of words are clustered approximately around 5.5 to 6. 
We can interpret this according to Dodds et al. (2011) who discuss that the ratings of the word "happiness" are not entirely neutral at 5. Overall, the ratings are slightly more positive.  
The distribution of happiness scores is slightly skewed to the right, which indicates that it is skewed towards happiness. 
In conclusion, most of the scores fall between 5 and 6, with a peak around 5.5. This indicates that many words have happiness scores between 5 and 7. 

## Unexpected Pattern 
One pattern we did not expect was the happiness score above 7 would be less frequent than under 5. 
Additionally, there are more words rated slightly positive than slightly negative. 
We might expect symmetry around 5 because 5 is defined as neutral in the labMT scale (Dodds et al., 2011). However, the histogram shows a structural shift upward. 
This is unexpected because the distribution is uneven as more words are rated positively. 
This further supports the idea that common English words present a tendency towards higher happiness scores instead of true emotional neutrality. 


## 2.2 Disagreement: which words are "contested"? 
To identify contested words, we slected the 15 entries with the highest values in the happiness_standard_deviation column (y-axis). 
These words appear at the top of the scatterplot (highest values on the y-axis), which indicates strong disagreement among respondents about their emotional meaing. 
We have selected 5 of the "most disagreed-about" words to explore the reasons why they are contested: "fucking", "fuckin", "fucked", "pussy", and "whiskey". 
These words have the highest standard deviation values which signifies that they generate the most disagreement about how positive or negative the words are. 

## Analysis
The main characterstic of these words is that they have negative connotations associated with them. For example, the words "fucking", "fuckin", "fucked", and "pussy"  are vulgar and considered highly inappropriate and offensive. Even though such words can be used in daily casual conversations as slang, they still hold very negative meanings. 
Meanwhile, "whiskey" has a neutral meaning and refers to the alcoholic beverage. We can consider how some may associate it with leisure, celebration, or socializing. Therefore, individuals may rate it positively. 
On the other hand, others can associate "whiskey" with negative experiences, alcohol abuse, or simply because they do not like it. Consequently, the word will have a lower happiness score. 
In general, the 5 words are contested because they are problematic, in the way that they can cause issues if they are used to verbally insult or harm someone (except for "whiskey"). The high standard deviation reflects the degree of disagreement of the emotional tone of the words. 
Some respondents perceive these words as strongly negative, while others interpret them as neutral or even positive. This depends on the context and personal experiences. 

## 2.3 Corpus comparison: what counts as "common language" depends on where you look
The four different corpora all represent various contexts and styles of language usage. 
Firstly, Twitter represents informal and real-time communication between users in daily situations. Tweets often contain casual diction such as slang and abbreviations. 
Furthermore, Google Books represents a broad and historical range of language from  books, with more formal and edited words across genres and time periods. 
The New York Times corpus provides formal vocabulary that is based on specific topics and shaped by reporting conventions. 
Lastly, song lyrics form the most creative corpus among the others, in which language is highly expressive. 
We can suggest that these differences emphasize how "common language" varies across corpora and depends on what kind of individuals are represented. 
Language styles, choice of vocabulary, and many other factors influence what is perceived as "common language".


## 3.1 Word Exhibit

Within both the “Very Positive” and “Very Negative” categories, the words that are presented have a universal connotation. The words in “Very Positive” are all synonyms of each other and are typically used in a positive manner. The meanings within the “Very Negative” category have very obvious negative connotations and societal implications, as some of the words engage in human rights abuse. Both categories' words spark an emotional reaction that warrants their respective scores. However, some words found in the “Highly Contested” and “Surprising” categories have iterations of each other or found in both lists; for example, the words “fucking,” “pussy,” and “capitalism.” Unlike the other two categories, the meanings and contexts of these words depend on where they are found and how they are used. Hence, they are found in their respective categories, as different communities may see these words as vulgar or a way to express oneself. 

A happiness score depended on how it was interpreted and evaluated by the Amazon Mechanical Turk. Unfortunately, this would not account for the varied perspectives in the English community and how different speakers might construe the given words. The words captured in the word_exhibit.md encompass both universal meanings and a range of meanings. The Muslim community may approach the word “Islam”  with a sense of reverence, as it is a major world religion. Meanwhile, the far-right Republican Party in the United States may use this word to fearmonger or spread misinformation to the general public. Another instance would befall the word “whiskey,” as the alcoholic community would see the beverage in a negative manner, while others may see it as a way to pass the time. From person to person and community to community, the use of words found in the table triggers a different emotional reaction depending on people’s life experiences and societal connotations. 


## 4.1 Reconstruct the pipeline (data provenance)
> *Hedonometer is a methodological tool proposed by Dodds et al. (2011) for large-scale, text-based measuring of happiness. In a nutshell, this method allows to assess the average happiness expressed in large texts by using happiness score applied to frequently used words.*

The data set already includes the information from labMT lexicon - a word-happiness dictionary used to measure emotional valence. The columns include following variables: words, happiness_rank, happiness_average, happiness_standard_deviation, twitter_rank, google_rank, nyt_rank, lyrics_rank. Based on this information we can reconstruct the pipeline:

---

### 1. Words selection

10,222 words were chosen, as the ones relevant for further evaluation. The selection usually happens based on the frequency of the words used in large corpora. These are a single word tokens, so the list does not include phrases or multiword expressions.

---

### 2. Happiness score assessment

During this step, the chosen words are being assessed by Mechanical Turks, who rate the words on the scale from 1 to 9. This score was used to compute happiness_rank, happiness_average, happiness_standard_deviation.

---

### 3. Corpus frequency analysis

Four corpora were chosen: Twitter, Google Books, New York Times and Song lyrics. After. Then the frequency was checked, how often does each word appear in each media. Based on this, ranks were assigned. So lower is the number, higher is the frequency.


---

### 4. Data merging

The data was merged into one table and missing values were encoded.

---

## 4.2 Consequences and limitations

### 1. Idiomatic expressions

The word selection includes exclusively single word tokens, thus, providing the word, which can appear as a part of idiomatic expression, completely shift the meaning when evaluated alone. For instance, word "kill", sitated on the lowest margine of happiness ranking with a very low score (1.70) is often used in positive slang like "he is killing it" or the word dead with the score 2.34 can be used in a phrase "drop dead", another example would be "break a leg". Single token words selection limits the ability of lexicon to capture idiomatic meaning that is an unseparable part of the language.


---

### 2. Textual positioning

Words are also evaluated outside of the context where they are situated. Through standard deviation we can see the words with highest disagreements amount annoators. For instance the word "pussy" can signify a different meaning depending on the context. This is also the word with the higher standard deviation (i.e. 2.67). The context can significantly shift in the meaning and emotional connotation and it's contextual position would impact the score given by Mechanical Turks.

---

### 3. Corpus heterogeneity

Rhetorics across 4 corpora significantly diverge: twitter - informal, New York Times - institutional, Google Books - broad, Song lyrics - poetic. These are very diverse and non neutral samples. Looking at the numerical indicators that are the same across 4 corpora, assumes that they measure the same thing, while in fact context, emotions, meanings of the words can significantly vary. As a result frequency patterns observed in the data set can indicate differences in rhetorics, rather that emotional language.

---

### 4. Annotator bias

Annotators are also not neutral machines, without culture and personal history. Personal emotional perception can significantly influence the score one assigns to the word. For instance, the words like love, joy appear on the higher end of the scale, with happiness score above 8 and standard devation around 0.9-1.1, which signifies a strong agreement amoung annotators. This can also indicate a shared cultural assumptiom and as a result emotional meanings become generalized. In my opinion, it is essential to provide background information on the people who rate the words, to address the diversity of cultural backgrounds and the possibility to speculate on generasability of the findings.

---

### 5. One-dimensional Likert scale

Likert scale is used to evaluate happiness level. This one-dimensional approach reduces multidimensional nature of qualitatively different emotions into one number, indicating "low happiness". The words from the sample: grief, suicide, anger can evoke very different emotions but still be put in the same category box.

---

## 4.3 Instrumental note

This data set can be well used for control variables for unsupervised semantic labeling. For large-scale quantitative analysis, comparison of relative values and identifying words that generate disagreement (happiness_standard_deviation) this dataset is extremely useful and methodologically transparent.

---

However, I would not use this dataset for generating claims on emotional meaning and discourse. A context deprived word list, does not reflect sarcastic, idiomatic and slang connotations that influence the meaning construction. Words that receive strongly negative (e.g. kill, dead) ratings, can significantly shift emotional function depending on the contextual positioning, idiomatic use and annotators positionality. This instrument reduce complexity to a simplified numerical score. Additionally, the assumption of comparable values derived from heterogeneous corpora risks masking how rhetorics shape emotional expression.

---

This data set is particularly generated for using the method proposed by Dodds et al. (2011). Thus, the limitations are inherent to it, only the change in the method can resolve outlined issues.

---

Although manual word labeling is the cornerstone of this work, it also presents many systematic technical limitations. First, although it is possible to normalize the bias of the average rating of multiple labelers by measuring the baseline value, artifacts remain in the data, which affects the quality of the data. Second, the small number of these labelers is problematic. Because of this, the marginal data of each labeler has too much influence on the final values. Statistical indicators (standard deviation, variance) suffer as a result. Third, this approach does not allow for large-scale research with a large corpus and, for example, cross-linguistic modality.


---
# Analyzing Happiness Scores in the Yelp Open Dataset 
## Introduction 
In this second mini-project, the labMT word list will be the instrument for measuring and analyzing the Yelp dataset. The Yelp corpus contains five files that include metadata about businesses (such as location data, attributes, and categories), users, reviews (which contain full review text, such as user_id and business_id), check-ins for a business, and users’ tips, which are shorter than reviews. For this project, we will use the two files containing business and review data. 
We will ask the following research question: **To what extent does the hedonometer happiness score of Yelp customer reviews correlate with the star ratings assigned to businesses, and do these emotional scores differ across metropolitan regions?** 
Using the hedonometer labMT word list as our framework, each Yelp review will be tokenized, matched, and the happiness scores of the matched words will be averaged to compute a review-level happiness score. The scores serve as both a quantitative measure and a visual representation of the emotional tone expressed by users in the reviews. 
The aim of this project is to compare whether the scores correlate with the star ratings that customers give to businesses. We will explore whether the happiness scores of the hedonometer can predict or provide a correlation with Yelp star ratings. This approach is relevant because it can provide meaningful insight into how customer sentiment, as measured by happiness scores, aligns with typical business reviews. We will have a broader understanding of how the words used in ratings reflect customer satisfaction. Consequently, businesses on Yelp might use such findings to better interpret feedback and improve their services. 
Additionally, this project analyzes the emotional tone in different regions. For example, whether reviews written by users in different urban areas, such as New York or Los Angeles in the U.S., tend to use more positive or negative words in reviews on average. 

## 1. From the Random Sample to the Final Dataset

The LabMT dataset was loaded as a dataframe, and irrelevant columns were disregarded. Two columns remained, “word” and “happiness_score”. Words with happiness scores between 4 and 6 were removed from the LabMT lexicon. This range is considered emotionally neutral in the LabMT framework. Because neutral words are very common, including them would push average review scores toward the midpoint of the scale and weaken the influence of clearly positive or negative words. Removing them follows standard hedonometer practice and produces more informative sentiment scores. Afterwards, 3731 words were left in the LabMT dictionary. 
The cleaned random sample of Yelp reviews was tokenized. A dataframe containing one token per row and the associated review ID was created. The two dataframes were then merged, matching “tokens” with the corresponding word in the LabMT dictionary and attaching the associated happiness score. However, not all tokens could be matched. Many reviews contain informal language, slang or abbreviations (for example, one review begins with “never ‘yelped’ b4” [review id: xlvN59kqb_89HViVW3tApg]). Rows that contained a token but had no happiness score were marked as OOV. Out of a total of 21180467 tokens, 15643779 tokens were not matched, for an overall OOV rate of ~0.7386.
In the next step, a review-level summary was created. All tokens with the same review ID were grouped and summaries for each group computed. The summaries include:
- the average happiness score of all matched tokens in a review, ignoring NaN values
- how many tokens each review contains
- how many of the tokens were matched to a word in the LabMT dataset
- how many tokens were OOV
- the proportion of OOV tokens in each review 
The summary was then merged back onto the cleaned Yelp reviews sample, which contains the full review text, review metadata and business metadata. This was based on the shared column “review_id”. The final dataset was saved as a CSV file. Below is a table showing each column included in the final dataset, along with its Dtype and the number of NaN values in it.
column name NaN Dtype
review_id   0   str
user_id 0   str
business_id 0   str
stars   0   float64
text (review)   0   str
date    0   str
name (business) 0   str
city    0   str
state   0   str
categories  15  str
tokens  0   object
hedonometer_score   15  float64
total_tokens    13  float64
matched_tokens  13  float64
oov_tokens  13  float64
oov_rate    13  float64
The 13 missing values in the columns "total_tokens", "matched_tokens", "oov_tokens", and "oov_rate" are presumably the result of 13 reviews having no text that was recognized as such. During the tokenization process, it was specified that each token must consist of alphabetical letters. Thus, a review that only consists of an emoji would produce no tokens and contribute to the NaN values. Two reviews additionally contained tokens, but were entirely made up of either OOV words or words with a happiness score between 4 and 6. This explains the 15 NaN values in the column “hedonometer_score”. For 15 businesses, metadata on the categories they belong to was missing from the Yelp dataset, resulting in 15 NaN values for “categories”.
