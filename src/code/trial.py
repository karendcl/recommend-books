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


directory = os.getcwd()
directory = os.path.join(directory, 'code')
def load_docs() -> list:
    """
    Load the documents from the /Docs folder.
    The documents are expected to be in .txt format

    Returns:
        list: the list of documents
    """
    data = []
    global directory

    dir = os.path.join(directory, 'Docs', '*.txt')


    #for file, replace with the cleaned text
    for file in glob.glob(dir):
        print(file)
        with open(file, 'r') as f:
            data1 = f.read( )
            processed = clean_text(data1)
            data.append(processed)

    return data

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
    final = ' '.join([word for word in words if word not in stops])
    final = final.translate(str.maketrans('', '', string.punctuation))

    #remove extra spaces
    while "  " in final:
        final = final.replace("  ", " ")

    return final

def clean_text(text : string) -> string:
    """ Clean the text by removing stop words and lemmatizing the words

    Parameters:
        text (str): the text to be cleaned

    Returns:
        str: the cleaned text
    """
    stops = stopwords.words('english')
    cleaned = remove_stops(text, stops)

    #lemmatize the words
    lemmatizer = WordNetLemmatizer()
    words = cleaned.split()
    lemmatized = [lemmatizer.lemmatize(word) for word in words]
    cleaned = ' '.join(lemmatized)

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

    #print the topics
    for i, topic in enumerate(lda_components):
        print(f"Top words for topic {i}\n")
        print([terms[i] for i in topic.argsort()[-10:]])
        print("\n")

    #save lda model to file to be retrained later
    with open(os.path.join(directory,'lda_model.pkl'), 'wb') as f:
        pickle.dump(model, f)

    #save the count vectorizer to file to be retrained later
    with open(os.path.join(directory,'count_vectorizer.pkl'), 'wb') as f:
        pickle.dump(count_vectorizer, f)

    with open(os.path.join(directory, 'lda_matrix.pkl'), 'wb') as f:
        pickle.dump(lda_matrix, f)

    #build document-topic matrix
    doc_topic = pd.DataFrame(lda_matrix, columns=["Topic "+str(i) for i in range(num_topics)], index=["Doc "+str(i) for i in range(len(documents))])
    print(doc_topic)


def Amount_of_topics(documents):
    """
    Calculate the amount of topics to be used in the LDA model

    Parameters:
        documents (list): the list of documents

    Returns:
        int: the amount of topics to be used
    """
    return len(documents)//2 + 1


def Add_New_Document(text, title):
    """
    Fits the new document to the data without retraining it.
    Saves the new document to the Docs folder

    Parameters:
        alldocs (list): the list of all documents
        text (str): the text of the new document
        title (str): the title of the new document

    Returns:
        None

    """

    cleaned_text = [clean_text(text)]

    dir1 = os.path.join(directory, 'Docs', '*.txt')

    #count how many documents there are
    count = 0
    for file in glob.glob(dir1):
        count += 1

    dir = os.path.join(directory, 'Docs', f'{title}.txt')

    #create a file in directory
    with open(dir, 'w') as f:
        #encode the cleaned text to utf-8
        f.write(cleaned_text[0])

    #see if the quantity of documents changed
    new_count = 0
    for file in glob.glob(dir1):
        new_count += 1

    if new_count > count:
        with open(os.path.join(directory,'lda_model.pkl'), 'rb') as f:
            model = pickle.load(f)

        with open(os.path.join(directory,'count_vectorizer.pkl'), 'rb') as f:
            count_vectorizer = pickle.load(f)

        new_data = count_vectorizer.transform(cleaned_text)

        old_matrix = model.components_

        lda_matrix = model.partial_fit(new_data)

        new_data = new_data.reshape(1, -1)
        topic_dist = lda_matrix.transform(new_data)


        #save the new model and count vectorizer
        with open(os.path.join(directory,'lda_model.pkl'), 'wb') as f:
            pickle.dump(lda_matrix, f)

        with open(os.path.join(directory,'count_vectorizer.pkl'), 'wb') as f:
            pickle.dump(count_vectorizer, f)

        with open(os.path.join(directory,'lda_matrix.pkl'), 'wb') as f:
            pickle.dump(topic_dist, f)

        # insert the new document into the document-topic matrix
        doc_topic = pd.DataFrame(lda_matrix, columns=["Topic " + str(i) for i in range(len(old_matrix))],
                                     index=["Doc " + str(i) for i in range(new_count)])
        return doc_topic
    else:
        return "Document Already Exists"


def Load_First_Time():
    """
    Load the documents for the first time and train the LDA model

    Returns:
        list: the list of documents
    """
    descriptions = load_docs()
    print(descriptions)
    lda_model(descriptions, Amount_of_topics(descriptions))
    return descriptions

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

    #load model
    with open(os.path.join(directory,'lda_matrix.pkl'), 'rb') as f:
        model = pickle.load(f)

    count = len(model)

    mask = [True if i in docs_read else False for i in range(count)]

    print(mask)

    docs_read = model[mask]

    docs_not_read_ind = [i for i in range(count) if mask[i] == False]

    #get avg of docs read
    avg_read = np.mean(docs_read, axis=0)

    #order the docs not read by similarity to the avg of docs read
    def similarity(x):
        return np.dot(avg_read, x)/(np.linalg.norm(avg_read)*np.linalg.norm(x))

    dict = {}
    for i in docs_not_read_ind:
        dict[i] = similarity(model[i])

    docs_not_read = sorted(dict.items(), key=lambda x: x[1], reverse=True)


    #return indices of the most similar docs
    return [i[0] for i in docs_not_read]


