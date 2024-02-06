# Book Recommending System 

> Authors:
> - [Karen D. Cantero Lopez C411](https://github.com/karendcl)
> - [Luis A. Rodriguez Otero C411](https://github.com/Drackaro)

## Problem Description
The problem is to recommend a series of books of similar
topics to a user based on the books they have read.

## Considerations taken into account

- The corpus is composed of books' summaries and not the actual books because we couldn't find an existing database with the content.
We also consider that a book's main topics must be discussed in a summary of it so the corpus should suffice to make an accurate prediction.
- The books are in English so the model is trained with English books.



## How to run the project
1. Clone the repository
2. Install the required packages
```bash
pip install -r requirements.txt
```
3. Change directory to the `src` folder and run with django
```bash
cd src
```
```bash
python manage.py runserver
```

## Solution implemented
This is a book recommending system that uses the LDA (Latent Dirichlet Allocation) 
model to recommend books to users based on the books they have read and the topics that 
are present in the books.

> #### LDA & Topic Modelling
>Topic modeling is a method for unsupervised classification of documents, similar to 
clustering on numeric data, which finds some natural groups of items (topics) even when 
we’re not sure what we’re looking for. A document typically concerns multiple topics in
different proportions.
>
>LDA is one of the most popular topic modeling techniques. Each document is represented by various words 
and each topic also is represented by various words. LDA finds the topics the documents belong to.

### Preprocessing
The data is preprocessed by removing stop words, punctuation, and numbers. The data is then tokenized and
lemmatized.

### Model
The data is vectorized using the TfidfVectorizer from the sklearn library.
The model is trained using the LDA model from the sklearn library. The number of topics is set to 15
(amount chosen by analyzing the results).
We then represent the doc_topic distribution matrix and we save it as a pickle file so that it can be loaded with each search and the model doesn't have to be trained every time.

> #### TfidfVectorizer
> TfidfVectorizer is a method that transforms text to feature vectors that can be used as input to estimator.
> It is a common method to convert text data to a matrix of token counts. It is important to note that the TfidfVectorizer
> method also normalizes the data.
> Tf-idf stands for term frequency-inverse document frequency, and the vectorizer uses this method to transform the data.
> The term frequency is the number of times a term appears in a document, and the inverse document frequency is a measure of how much information the word provides, that is, whether the term is common or rare across all documents.
> By using a TF-IDF we use a normalized estimation of the importance of a word in a document.


### Recommending
The user is asked to select the books they have read from the books in the database.
Each row in the doc_topic distribution matrix is then averaged to get the user's topic distribution.
This leaves us with a vector of 15 elements that represents the user's average topic distribution.

We then select the 3 topics with the highest values in that average vector. We have selected three because in this dataset, most books have two predominant topics, but some have 3.

We then calculate the cosine similarity between the user's average topic distribution and the topic distribution of each book in the database, only taking into consideration the three topics chosen to eliminate information that we don't need.

The books with the highest cosine similarity are then recommended to the user. We only recommend 5 books to the user, but more could potentially be recommended.

> #### Cosine Similarity
> Cosine similarity is a measure of similarity between two non-zero vectors of an inner product space that measures the cosine of the angle between them. The cosine of 0° is 1, and it is less than 1 for any other angle. It is thus a judgment of orientation and not magnitude: the closer the cosine is to 1, the smaller the angle and the greater the similarity.
> The formula for the cosine similarity is:
> $$\cos(\theta) = \frac{A \cdot B}{||A|| \cdot ||B||} = \frac{\sum_{i=1}^{n} A_i \cdot B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \cdot \sqrt{\sum_{i=1}^{n} B_i^2}} . 
> Where A and B are the vectors and ||A|| and ||B|| are the norms of the vectors.

## Insufficiencies
- The model is trained on a small dataset and the topics are not always clear.
- Topics are not 'named' so it is difficult to know what the topics are about. We have to physically infer the topics from the words that are most representative of each topic.
- The number of topics is chosen arbitrarily and it is difficult to know how many topics are truly present in the dataset.












  
