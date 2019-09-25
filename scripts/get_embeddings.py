import glob
import json
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os
from pymongo import MongoClient
import re
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from tqdm import tqdm as tqdm

def read_embedding_keys(path):
    print('========== Generate keys ==========')
    keys = set()
    with open(path, 'r') as embeddings_data:
        for line in embeddings_data:
            data = line.strip().split(' ')
            keys.add(data[0])
    print('========== Finished generating keys ==========')
    return keys

def generate_embeddings(data_path, relevant_keys):
    print('========== Generate embeddings ==========')
    embeddings = dict()
    with open(data_path, 'r') as embeddings_data:
        for line in embeddings_data:
            data = line.strip().split(' ')
            if data[0] in relevant_keys:
                embeddings[data[0]] = data[1:]
    print('========== Finished generating embeddings ==========')
    return embeddings

def export_embeddings(embeddings, collection):
    print('========== Export embeddings ==========')
    for course in collection.find():
        title = course['meta']['title']
        values = []
        for key in course['parents'].keys():
            values.append(course['parents'][key].split(' ')[0].split('/')[0])
        if len(values) >= 3:
            value = values[-2]
        else:
            value = values[-1]
        value = value.replace(',','')
        value = value.replace('-','').lower()
        if value in embeddings:
            course['repr'] = embeddings[value]
            collection.replace_one({"_id": course["_id"]}, course)
    print('========== Finished exporting embeddings ==========')

def get_relevant_keys(collection, folder, embeddings):
    print('========== Generate relevant keys ==========')
    sum_found = 0
    not_found = set()
    found = set()
    for index, course_cursor in enumerate(collection.find()):
        title = course_cursor['meta']['title']
        values = []
        for key in course_cursor['parents'].keys():
            values.append(course_cursor['parents'][key].split(' ')[0].split('/')[0])
        if len(values) >= 3:
            value = values[-2]
        else:
            value = values[-1]
        value = value.replace(',','')
        value = value.replace('-','').lower()
        if value in embeddings:
            found.add(value)
            sum_found += 1
        else:
            not_found.add(value)
        # print(f'{value}: {value in embeddings} - {sum_found}/{index+1}')
    print(f'Following keys were not found: {not_found}')
    print('========== Finished generating relevant keys ==========')
    return found

def pca_features(embeddings):
    print('========== Fitting T-SNE ==========')
    pca = PCA(n_components=2)
    features = []
    for key in embeddings:
        features.append(embeddings[key])
    tsne_ak_2d = TSNE(perplexity=30, n_components=2, init='pca', n_iter=3500, random_state=32)
    embeddings_ak_2d = tsne_ak_2d.fit_transform(features)
    plt.figure(figsize=(16, 9))
    x = embeddings_ak_2d[:,0]
    y = embeddings_ak_2d[:,1]
    plt.scatter(x, y)
    for i, key in enumerate(embeddings):
        plt.annotate(key, xy=(x[i], y[i]), xytext=(5, 2), 
                     textcoords='offset points', ha='right', va='bottom', size=10)
    plt.legend(loc=4)
    plt.title('Berufsgruppen')
    plt.show()
    print('========== Done Fitting T-SNE ==========')

def main():
    connection_string = "mongodb+srv://t4g:bmas@cluster0-ryhbu.mongodb.net/test?retryWrites=true&w=majority"
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.t4g
    courses_collection = t4g_database.courses
    embedding_keys = read_embedding_keys('../word_embeddings/glove_german.txt')
    relevant_keys = get_relevant_keys(courses_collection, '../scraping/output/', embedding_keys)
    embeddings = generate_embeddings('../word_embeddings/glove_german.txt', relevant_keys)
    pca_features(embeddings)
    # export_embeddings(embeddings, courses_collection)

if __name__ == '__main__':
    main()