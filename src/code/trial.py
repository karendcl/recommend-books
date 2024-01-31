import re

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import string
from nltk.corpus import stopwords
import json
import glob
import os
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')

#load documents from the Docs folder
def load_docs():
    data = []
    for file in glob.glob("Docs/*.txt"):
        with open(file, 'r') as f:
            data.append(f.read())
    return data

def remove_stops(text, stops):
    words = text.split()
    final = ' '.join([word for word in words if word not in stops])
    final = final.translate(str.maketrans('', '', string.punctuation))

    while "  " in final:
        final = final.replace("  ", " ")

    return final

def clean_docs(docs):
    stops = stopwords.words('english')
    cleaned = [remove_stops(doc, stops) for doc in docs]

    #lemmatize the words
    lemmatizer = WordNetLemmatizer()
    for i in range(len(cleaned)):
        words = cleaned[i].split()
        lemmatized = [lemmatizer.lemmatize(word) for word in words]
        cleaned[i] = ' '.join(lemmatized)

    return cleaned


def tf_idf_and_k_means(documents):
    vectorizer = TfidfVectorizer(stop_words='english',
                                 lowercase=True,
                                 ngram_range=(1, 3),
                                 max_features=1000,
                                 max_df=0.9,
                                 smooth_idf=True,
                                 min_df=1)

    vectors = vectorizer.fit_transform(documents)
    feature_names = vectorizer.get_feature_names_out()
    dense = vectors.todense()
    denselist = dense.tolist()

    all_keywords = []
    n_clusters_number = 4

    for description in denselist:
        x = 0
        keywords = []
        for i in description:
            if i > 0:
                keywords.append(feature_names[x])
            x += 1
        all_keywords.append(keywords)

    model = KMeans(n_clusters=n_clusters_number, init='k-means++', max_iter=100, n_init=1)
    model.fit(vectors)

    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()

    # load the results into json file
    with open('results.json', 'w', encoding='utf-8') as f:
        for i in range(n_clusters_number):
            f.write("Cluster %d:" % i)
            for ind in order_centroids[i, :10]:
                f.write(' %s' % terms[ind])
                f.write("\n")
            f.write("\n\n")


from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
def lda_model(documents, num_topics=4):
    tokenizer = RegexpTokenizer(r'\w+')

    tfidf = TfidfVectorizer(tokenizer=tokenizer.tokenize, stop_words='english', lowercase=True, ngram_range=(1,3))
    train_data = tfidf.fit_transform(documents)

    model = LatentDirichletAllocation(n_components=num_topics)
    lda_matrix = model.fit_transform(train_data)
    lda_components = model.components_

    terms = tfidf.get_feature_names_out()

    for topic_idx, topic in enumerate(lda_components):
        zippped = zip(terms, topic)
        sorted_terms = sorted(zippped, key=lambda x:x[1], reverse=True)
        print("Topic %d:" % topic_idx)
        for i in range(10):
            print(sorted_terms[i])
        print("\n")


    #build document-topic matrix
    doc_topic = pd.DataFrame(lda_matrix, columns=["Topic "+str(i) for i in range(num_topics)], index=["Doc "+str(i) for i in range(len(documents))])
    print(doc_topic)

def Amount_of_topics(documents):
    return len(documents)//2 +1

#load the documents
descriptions = load_docs()
cleaned_data = clean_docs(descriptions)
print(cleaned_data)

lda_model(cleaned_data, Amount_of_topics(cleaned_data))

#tf_idf_and_k_means(cleaned_data)


