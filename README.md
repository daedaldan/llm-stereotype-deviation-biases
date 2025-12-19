# Stereotype and Deviation Biases of Large Language Models
This is the data repository for our paper analyzing the stereotype and deviation biases of large language models (LLMs).

## 1. Prompt Engineering
First, we construct implicit and explicit bias prompts representing the following gender, ethnicity and race, and age groups:

**Gender**
* Male
* Female

**Ethnicity and Race**
* Neutral
* White
* Black
* Hispanic
* Asian

**Age**
* Baby Boomers
* Generation X
* Millennials
* Generation Z
* Generation Alpha

These prompts are stored in CSV files that are used for the second stage in the pipeline.

## 2. Generating and Preprocessing Texts
Next, we use the implicit and explicit bias prompts to generate the texts using four different LLMs:
* GPT-4o Mini by OpenAI
* Claude 3.5 Sonnet by Anthropic
* Llama 3.1 70B by Meta
* Command R+ by Cohere

We then perform keyword extraction and sentiment analysis to obtain the following attributes for each text:
* Political Affiliation
* Religion
* Sexual Orientation
* Socioeconomic Status
* Occupation
* Polarity

These generated texts are stored in JSON files that are used in the third stage in the pipeline.

## 3. Pivot Tables, Binomial Tests, Confidence Intervals, and Effect Sizes
Using the LLM-generated texts, we create pivot tables describing how the distributions of different demographic attributes (e.g., religion, politics) in the texts differ based on the input groups (e.g, gender, race, age) represented by the prompts.

We then analyze the LLM outputs by looking at two different types of bias:

* **Stereotype Bias:** when LLMs consistently associate specific traits with a particular demographic group. 

* **Deviation Bias:** the disparity between the demographic distributions extracted from LLM-generated content and real-world demographic distributions. 

To measure the stereotype biases in the texts, we compute the maximum Kullback-Leibler divergence between any pair of demographic groups within each input category (gender, ethnicity and race, or age).

To calculate the deviation biases in the LLM outputs, we perform binomial tests comparing the observed demographic statistics in the texts generated for each input group with their corresponding real-world demographic statistics in the United States. We additionally compute Wilson confidence intervals for each estimated binomial proportion and use Cohen’s h to quantify the effect size of the difference between the observed proportions and their corresponding real-world reference values. The results all deviation bias tests are within the "Cohens_H.csv" file.

## 4. Creating Plots and Percentage Tables
After creating the pivot tables, we can visualize the distributions of demographic attributes for each gender, ethnic, and age group using stacked bar charts for categorical variables (e.g., socioeconomic status) and violinplots for numerical variables (e.g., polarity). During this step, we also create percentage tables describing the distributions.

## 5. Creating LaTeX Tables
Finally, we generate the LaTeX tables used in the research paper from our analysis results. The tables present statistical findings about biases in large language models across different demographic attributes. For example, they allow for comparison of stereotype bias between different demographic groups, explain the statistical significance of the deviation bias measurements, present the occupational distributions in the LLM outputs, and describe the polarity statistics for the model responses.
