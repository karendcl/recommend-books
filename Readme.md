# Book Recommending System 

> Authors:
> - [Karen D. Cantero Lopez C411](https://github.com/karendcl)
> - [Luis A. Rodriguez Otero C411](https://github.com/Drackaro)

## Porblem Description
The problem is to recommend a series of books of similar
topics to a user based on the books they have read.

## Considerations taken into account


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

### Recommending
The user is asked to select the books they have read from the books in the database.
Each row in the doc_topic distribution matrix is then averaged to get the user's topic distribution.
This leaves us with a vector of 15 elements that represents the user's average topic distribution.

We then select the 3 topics with the highest values in that average vector. We have selected three because in this dataset, most books have two predominant topics, but some have 3.

We then calculate the cosine similarity between the user's average topic distribution and the topic distribution of each book in the database, only taking into consideration the three topics chosen to eliminate information that we don't need.

The books with the highest cosine similarity are then recommended to the user. We only recommend 5 books to the user, but more could potentially be recommended.

> #### Cosine Similarity
> Cosine similarity is a measure of similarity between two non-zero vectors of an inner product space that measures the cosine of the angle between them. The cosine of 0° is 1, and it is less than 1 for any other angle. It is thus a judgment of orientation and not magnitude: the closer the cosine is to 1, the smaller the angle and the greater the similarity.

##

## Insuficiencies
- The model is trained on a small dataset and the topics are not always clear.
- Topics are not 'named' so it is difficult to know what the topics are about. We have to physically infer the topics from the words that are most representative of each topic.
- The number of topics is chosen arbitrarily and it is difficult to know how many topics are truly present in the dataset.












  
