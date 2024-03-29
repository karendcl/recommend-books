import re

import numpy as np
import pandas as pd
import string
from nltk.corpus import stopwords
import glob
from nltk.stem import WordNetLemmatizer
import pickle
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import os
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


directory = os.getcwd()
directory = os.path.join(directory, 'code')

def remove_stops(text : string, stops :list) -> string:
    """ Remove stop words and extra spaces from the text
    
    Parameters:
        text (str): the text to be cleaned
        stops (list): the list of stop words to be removed
        
    Returns:
        str: the cleaned text
    """
    #remove stop words
    words = text.split()
    final = ' '.join([word for word in words if (word not in stops
                      and word not in string.punctuation)])

    return final

def remove_nums(text : string) -> string:
    """ Remove numbers from the text

    Parameters:
        text (str): the text to be cleaned

    Returns:
        str: the cleaned text
    """
    txt = text.split()
    for i in txt:
        try:
            int(i)
            txt.remove(i)
        except:
            pass
    return ' '.join(txt)

def clean_text(text : string) -> string:
    """ Clean the text by removing stop words and lemmatizing the words

    Parameters:
        text (str): the text to be cleaned

    Returns:
        str: the cleaned text
    """
    #tokenize
    text = text.lower()

    stops = stopwords.words('english')
    cleaned = remove_stops(text, stops)

    #lemmatize the words
    lemmatizer = WordNetLemmatizer()
    words = cleaned.split()
    lemmatized = [lemmatizer.lemmatize(word) for word in words]
    cleaned = ' '.join(lemmatized)
    cleaned = remove_nums(cleaned)

    return cleaned


def lda_model(documents, num_topics=4):
    """ Perform Latent Dirichlet Allocation on the documents
    Save the model and the count vectorizer to be used later with new data

Parameters:
    documents (list): the list of documents to be analyzed
    num_topics (int): the number of topics to be found

Returns:
    None

    """
    tokenizer = RegexpTokenizer(r'\w+')

    count_vectorizer = TfidfVectorizer(tokenizer=tokenizer.tokenize, stop_words='english', lowercase=True, ngram_range=(1,3))

    train_data = count_vectorizer.fit_transform(documents)

    model = LatentDirichletAllocation(n_components=num_topics, learning_method='online')
    lda_matrix = model.fit_transform(train_data)

    lda_components = model.components_
    terms = count_vectorizer.get_feature_names_out()

    #create json file with the topics
    with open(os.path.join(directory, 'topics.json'), 'w') as f:
        f.write("{\n")
        for i, topic in enumerate(lda_components):
            f.write(f'"{i}": {{"topic": {i}, "words": {str([terms[i] for i in topic.argsort()[-10:]])}}}')
            if i != num_topics-1:
                f.write(",\n")
        f.write("\n}")

    with open(os.path.join(directory, 'lda_matrix.pkl'), 'wb') as f:
        pickle.dump(lda_matrix, f)

    #build document-topic matrix
    doc_topic = pd.DataFrame(lda_matrix, columns=["Topic "+str(i) for i in range(num_topics)], index=["Doc "+str(i) for i in range(len(documents))])

    #save doc_topic as json
    doc_topic.to_json(os.path.join(directory, 'doc_topic.json'))



def Amount_of_topics():
    """
    Calculate the amount of topics to be used in the LDA model

    Parameters:
        documents (list): the list of documents

    Returns:
        int: the amount of topics to be used
    """
    return 270


def update(texts):
    """
    Fits the new document to the data without retraining it.
    Saves the new document to the Docs folder

    Parameters:
        texts (list): all documents

    Returns:
        None

    """

    #clean data
    texts = [clean_text(i) for i in texts]
    lda_model(texts, Amount_of_topics())
    print(f'Entropy: {enthropy_model()}')

def determine_topics(vector):
    """
    Determine the most relevant topics in a vector

    Parameters:
        vector (list): the vector to be analyzed

    Returns:
        list: the indices of the most relevant topics
    """
    tops = np.argsort(vector)[::-1]

    for i in range(len(tops)):
        if vector[tops[i]] < 0.05:
            return tops[:i]

    return tops



def make_suggestion(docs_read):
    """
    Make a suggestion of the most similar documents to the ones read

    Parameters:
        docs_read (list): the list of indices of the documents read

    Returns:
        list: the list of indices of the most similar documents ordered by similarity


    """

    #map docs_read to the correct indices (0 to n-1)
    docs_read = [i-1 for i in docs_read]

    print(docs_read)

    #load model
    with open(os.path.join(directory,'lda_matrix.pkl'), 'rb') as f:
        model = pickle.load(f)

    count = len(model)

    mask = [True if i in docs_read else False for i in range(count)]

    docs_read = model[mask]

    docs_not_read_ind = [i for i in range(count) if mask[i] == False]

    #get avg of docs read
    avg_read = np.mean(docs_read, axis=0)

    #determine the most relevant topics
    topics = determine_topics(avg_read)

    #reduce the model to the most relevant topics
    model = model[:, topics]
    avg_read = avg_read[topics]
    print(avg_read)

    #order the docs not read by similarity to the avg of docs read
    def similarity(x):
        #eucledean distance
        return np.linalg.norm(avg_read - x)

    dict = {}

    for i in docs_not_read_ind:
        dict[i] = similarity(model[i])

    docs_not_read = sorted(dict.items(), key=lambda x: x[1])

    #return indices of the most similar docs
    return [i[0] for i in docs_not_read][:5] , [100 - i[1] * 100 for i in docs_not_read][:5]


def enthropy_model():

    with open(os.path.join(directory, 'lda_matrix.pkl'), 'rb') as f:
        model = pickle.load(f)

    #calculate the entropy of each topic
    entropy = -np.sum(model * np.log(model), axis=0)

    #calculate the average entropy
    avg_entropy = np.mean(entropy)

    return avg_entropy






