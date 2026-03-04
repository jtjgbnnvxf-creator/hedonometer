### 2.1 Distribution of Happiness Scores

### Histogram Interpretation
The distribution of happiness scores is slightly skewed to the right.
Most scores fall between [5] and [6], with a peak around [5.5].

### Unexpected Pattern
One pattern I did not expect was the happiness score above 7 would be less frequent than under five

### 2.2 Disagreement: which words are “contested”?
----
### 5 "mostdisagreed-about" words
----
### Qualitative intrerpretation -> quatitative patterns
----

## 4.1 Reconstruct the pipeline

> *Hedonometer is a methodological tool proposed by Dods et al. (2021) for large-scale, text-based measuring of happiness. In a nutshell, this method allows to assess the average happiness expressed in large texts by using happiness score applied to frequently used words.*

The data set already includes the information from labMT lexicon - a word-happiness dictionary used to measure emotional valence. The columns include following variables: words, happiness_rank, happiness_average, happiness_standard_deviation, twitter_rank, google_rank, nyt_rank, lyrics_rank. Based on this information we can reconstruct the pipeline:

---

### 1. Words selection

10,222 words were chosen, as the ones relevant for further evaluation. The selection usually happens based on the frequency of the words used in large corpora. These are a single word tokens, so the list does not include phrases or multiword expressions.

---

### 2. Happiness score assessment

During this step, the chosen words are being assessed by mechanical turks, who rate the words on the scale from 1 to 9. This score was used to compute happiness_rank, happiness_average, happiness_standard_deviation.

---

### 3. Corpus frequency analysis

Four corpora were chosen: Twitter, Google Books, New York Times and Song lyrics. After. Then the frequency was checked, how often does each word appear in each media. Based on this, ranks were assigned. So lower is the number, higher is the frequency.

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/8/8a/Sentiment_analysis_diagram.png" width="600"/>
</p>

---

### 4. Data merging

The data was merged into one table and missing values were encoded.

---

## 4.2 Consequences and limitations

### 1. Context deprivation

The word selection includes exclusively single word tokens, thus, providing the words stripped from the context, sarcasm and slang. Thus, words, especially ones on the margins (e.g. nsmallest/nlargest), can be significantly simplified, which impacts its rating. For instance, word kill is often used in positive slang like "he is killing it" or the word dead "drop dead" or phrases "break a leg". This word selection is deprived from contextual meaning in discourse.

---

### 2. Evaluation outside context

Words are also evaluated outside of the context where they are situated. The context can significantly shift the meaning and emotional connotation, the same example with kill and dead, if given in a phrase or located in the context, would impact the score given by Mechanical Turks.

---

### 3. Corpus heterogeneity

Rhetorics across 4 corpora significantly diverge: twitter - informal, New York Times - institutional, Google Books - broad, Song lyrics - poetic. These are very diverse and non neutral samples. Looking at the numerical indicators that are the same across 4 corpora, assumes that they measure the same thing, while in fact context, emotions, meanings of the words can significantly vary.

---

### 4. Annotator bias

Annotators are also not neutral machines, without culture and personal history. Personal emotional perception can significantly influence the score one assigns to the word. Another word that appears on extreme end of the scale is love, the data does not provide any information, whether the annotators interpret it different. Thus, emotional meanings become generalized. In my opinion, it is essential to provide background information on the people who rate the words, to address the diversity of cultural backgrounds.

---

### 5. One-dimensional Likert scale

Likert scale is used to evaluate happiness level. This one-dimensional approach reduces multidimensional nature of qualitatively different emotions into one number, indicating "low happiness". The words from the sample: grief, suicide, anger can evoke very different emotions but still be put in the same category box.

---

## 4.3 Instrumental note

This data set can be well used for control variables for unsupervised semantic labeling (NLP/related methods). For large-scale quantitative analysis, comparison of relative values and identifying words that generate disagreement (happiness_standard_deviation) this dataset is extremely useful and methodologically transparent.

---

However, I would not use this dataset for generating claims on emotional meaning and discourse. A context deprived word list, strip sarcastic, idiomatic and slang connotations that influence the meaning construction. Words that receive strongly negative (e.g. kill, dead) ratings, can significantly shift emotional function depending on the contextual positioning. This instrument reduced complexity to a simplified numerical score. Additionally, the assumption of comparable values derived from heterogeneous corpora risks masking how rhetorics shape emotional expression.

---

This data set is particularly generated for using the method proposed by Dods et al. (2021). Thus, the limitations are inherent to it, only the change in the method can resolve outlined issues.

---

Although manual word labeling is the cornerstone of this work, it presents many systematic technical limitations as well. First, although it is possible to normalize the bias of the average rating of multiple labelers by measuring the baseline value, artifacts remain in the data, which affects the quality of the data. Second, the small number of these labelers is problematic. Because of this, the marginal data of each labeler has too much influence on the final values. Statistical indicators (standard deviation, variance) suffer as a result. Third, this approach does not allow for large-scale research with a large corpus and, for example, cross-linguistic modality.

---

## Future Direction

Therefore, using a different method, like Natural Language Processing (NLP) would allow to resolve these issues. The use of automated extraction of semantic characteristics will help to avoid outlined issues.

---