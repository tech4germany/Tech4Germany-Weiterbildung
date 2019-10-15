from dotenv import load_dotenv
from nltk.stem.cistem import Cistem
import pandas as pd
from pathlib import Path
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords 
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import os
from pymongo import MongoClient
import re
from sklearn.feature_extraction.text import TfidfVectorizer

def build_corpus():
    env_path = Path('../') / '.env'
    load_dotenv(dotenv_path=env_path)
    connection_string = os.getenv("DATABASE_URL")
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.test
    jobs_collection = t4g_database.jobs
    jobs = jobs_collection.find()
    size = jobs.count()
    stemmer = Cistem()
    corpus = []
    titles = []
    for i, job in enumerate(jobs):
        if i % 1000 == 0: print(f'{i}/{size}')
        indices = []
        title = job['title'].replace(',','')
        titles.append(title)
        text = job['detailed_activities'].strip()
        text = ' '.join(text.split())
        for index in range(len(text)):
            if text[index].isupper() and index > 1 and text[index-1] is not " " and text[index-2] is not " "and not text.endswith(text[index]) and text[index+1] is not " ":
                    indices.append(index)

        for index in reversed(indices):
            text = text[:index] + " " + text[index:]

        text = re.sub('[^A-Za-zä-üÄ-Ü]', ' ', text)
        text = text.lower()
        tokenized_text = word_tokenize(text)
        words = []
        for word in tokenized_text:
            stemmed_word = stemmer.stem(word).strip()
            if stemmed_word not in stopwords.words('german') and word not in stopwords.words('german') and len(stemmed_word) > 2 and stemmed_word not in ['it','3d'] and stemmed_word not in title:
                words.append(stemmed_word)

        corpus.append(' '.join(words))
    return corpus, titles

if __name__ == "__main__":
    corpus, titles = build_corpus()
    vectorizer = TfidfVectorizer(max_features=10000)
    X = vectorizer.fit_transform(corpus)

    with open('job_features.csv', 'w+') as outf:
        for feature_vec, title in zip(X, titles):
            feature_vec = [str(x) for x in feature_vec.toarray().flatten()]
            
            outf.write(f'{title},{",".join(feature_vec)}\n')
    with open('job_feature_map.txt', "w+") as outfeat:
        outfeat.write(" ".join(vectorizer.get_feature_names()))