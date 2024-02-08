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
- In order to tackle the topic modelling problem, we discussed various models, and we decided to use the LDA model, mainly because it is a probabilistic generative model that assumes each document is composed of a mixture of topics, and each topic is a mixture of words, and it can infer the topic distribution for both documents and words, while other models (Like LSA) can only do so for documents. LDA is slightly slower than other models but it also requires less memory and computational resources.
- The data is vectorized using the TfidfVectorizer from the sklearn library. We chose this method of vectorization because it transforms raw text data into meaningful features (giving important/rare words a higher 'score'), capturing the essence of each document while considering the broader context of the entire corpus.
- We use the Euclidean Distance to calculate the similarity between the user's average topic distribution and the topic distribution of each book in the database. We chose this method because it is the most intuitive one, and it yields better results in this case than other methods like cosine similarity.


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
As we have said before the data is vectorized using the TfidfVectorizer from the sklearn library.
The model is trained using the LDA model from the sklearn library. The number of topics is set to 10
(amount chosen by analyzing the results).
We then represent the doc_topic distribution matrix and we save it as a pickle file so that it can be loaded with each search and the model doesn't have to be trained every time.

> #### TfidfVectorizer
> TfidfVectorizer is a method that transforms text to feature vectors that can be used as input to estimator.
> It is a common method to convert text data to a matrix of token counts. It is important to note that the TfidfVectorizer
> method also normalizes the data.
> 
> The term frequency is the number of times a term appears in a document, and the inverse document frequency is a measure of how much information the word provides, that is, whether the term is common or rare across all documents.
> By using a TF-IDF we use a normalized estimation of the importance of a word in a document.


### Recommending
The user is asked to select the books they have read from the books in the database.
Each row in the doc_topic distribution matrix is then averaged to get the user's topic distribution.
This leaves us with a vector of 10 elements that represents the user's average topic distribution.

We then select the 3 topics with the highest values in that average vector. We have selected three because in this dataset, most books have two predominant topics, but some have 3.

We then calculate the Euclidean distance between the user's average topic distribution and the topic distribution of each book in the database, only taking into consideration the three topics chosen to eliminate information that we don't need.

The books with the lowest distance are then recommended to the user. We only recommend 5 books to the user, but more could potentially be recommended.

> #### Euclidean Distance
> The Euclidean Distance is the distance between two points in space. It is the most common method to calculate the similarity between two vectors.
> Formula: $$\sqrt{\sum_{i=1}^{n} (x_i - y_i)^2}$$. Where x and y are the two vectors and n is the number of elements in the vectors.


## Insufficiencies
- The model is trained on a small dataset and the topics are not always clear.
- Topics are not 'named' so it is difficult to know what the topics are about. We have to physically infer the topics from the words that are most representative of each topic.
- The number of topics is chosen arbitrarily, and it is difficult to know how many topics are truly present in the dataset.
- The use of the Euclidean distance could have its limitations like: let's say there are two vectors with the same distance but in opposite directions. In this case I would arguably recommend the book with the higher values, but the Euclidean distance would not be able to differentiate between the two vectors.

## Images

![Home](https://i.postimg.cc/13q825Jt/Screenshot-2024-02-07-231419.png)

![Selection](https://i.postimg.cc/qMWMW93C/Screenshot-2024-02-06-203104.png)

![Recommendation](https://i.postimg.cc/yYD8QVkH/Screenshot-2024-02-06-203202.png)

![Upload](https://i.postimg.cc/ZKnCG8sX/Screenshot-2024-02-06-203239.png)













  
