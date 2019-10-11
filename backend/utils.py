from bson import json_util
import csv
import json
import numpy as np
import os
from scipy import spatial

def load_jobs_data(file_name):
    embeddings = []
    entities = []
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), file_name), 'r') as infile:
        data = csv.reader(infile, delimiter=',')
        for line in data:
            embeddings.append([float(x) for x in line[1:]])
            entities.append(line[0])
    return entities, embeddings

def load_dists(file_path):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), file_path), 'r') as infile:
        data = csv.reader(infile, delimiter=',')
        dist_matrix = []
        for line in data:
            dist_matrix.append([float(x) for x in line])
    return dist_matrix

def load_categories(database):
    category_names = []
    for category_cursor in database.categories.find({}):
        category_names.append(category_cursor['category_name'])
    return category_names

def load_related_job(database, job_id):
    return database.jobs.find_one({'job_id': job_id})

def load_init_options(dist_matrix, entities, job_titles):
    if len(job_titles) == 1:
        # suggest two jobs within a rather close distance to the given embedding
        option_1 = _find_close_point(dist_matrix, entities, job_titles[0])
        option_2 = _find_close_point(dist_matrix, entities, job_titles[0])
        while option_2 is option_1:
            option_2 = _find_close_point(dist_matrix, entities, job_titles[0])
        options = [entities[option_1], entities[option_2]]
    else:
        if len(job_embeddings) > 2:
            # select two random samples
            job_embeddings = np.random.choice(job_titles, 2, replace=False)

        # suggest one job within a rather close distance each for both of the given embeddings
        options = [_find_close_point(dist_matrix, entities, x) for x in job_titles]

    return options

def _find_close_point(dist_matrix, entities, job_title):
    dists = []
    i = entities.index(job_title)
    dists = dist_matrix[i]
    neighbors = np.argpartition(dists, 30)[1:30]
    return np.random.choice(neighbors, 1)[0]

def get_options(entities, embeddings, selected, not_selected, neighborhood_size = 100, num_pts = 2):
    selected_indices = [entities.index(x) for x in selected]
    selected_features = [embeddings[x] for x in selected_indices]
    not_selected_indices = [entities.index(x) for x in not_selected]
    sum_selected = np.zeros(len(selected_features[0]))
    for i in range(len(selected_features)):
        for j in range(len(selected_features[i])):
            sum_selected[j] += selected_features[i][j]
    avg_selected = sum_selected / len(selected_features)
    dists = []
    for i in range(len(embeddings)):
        dists.append(spatial.distance.cosine(np.array(embeddings[i]), avg_selected))
    jobs = [entities[x] for x in np.argpartition(dists, 10)[:10]]
    try:
        neighbors = np.argpartition(dists, neighborhood_size)[:neighborhood_size]
        rel_neighbors = [x for x in neighbors if x not in selected_indices and x not in not_selected_indices]
        neighbors = list(np.random.choice(rel_neighbors, num_pts, replace=False))
        options = [entities[x] for x in neighbors]
        return options, jobs
    except Exception as e:
        print(e)
        return [], jobs 