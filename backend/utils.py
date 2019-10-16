from bson import json_util
from bson.objectid import ObjectId
import csv
import json
import numpy as np
import os
from scipy import spatial
import time

def load_jobs_data(file_name):
    """
    Load entities and embeddings from the given csv file
    
    Arguments:
        file_name {String} -- path to the given csv file
    
    Returns:
        list<String>, list<float> -- two lists including all entities and all embeddings
    """
    embeddings = []
    entities = []
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), file_name), 'r', encoding="utf-8") as infile:
        data = csv.reader(infile, delimiter=',')
        for line in data:
            # a line in the csv file contains the entity followed by the embedding feature vector
            embeddings.append([float(x) for x in line[1:]])
            entities.append(line[0])

    return entities, embeddings


def load_dists(file_path):
    """
    Load a distance matrix from the given csv file
    
    Arguments:
        file_path {String} -- path to the given csv file
    
    Returns:
        list<list<float>> -- a 2d distance matrix indicating the pairwise cosine distances
    """
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), file_path), 'r') as infile:
        data = csv.reader(infile, delimiter=',')
        dist_matrix = []
        for line in data:
            dist_matrix.append([float(x) for x in line])
    return dist_matrix


def load_categories(database):
    """Loads all categories that are stored in the given database
    
    Arguments:
        database {pymongo.database.Database} -- the given database
    
    Returns:
        list<String> -- all stored categories
    """
    category_names = []
    for category_cursor in database.categories.find({}):
        category_names.append(category_cursor['category_name'])
    return category_names

def load_related_job(database, job_id):
    """
    Load a job given a job id
    
    Arguments:
        database {pymongo.database.Database} -- the given database
        job_id {String} -- id of the given job
    
    Returns:
        [JSON] -- the job that matches the given job id in the database
    """
    return database.jobs.find_one({'job_id': job_id})

def load_init_options(database, dist_matrix, entities, selected_ids):
    """
    Load the initial options after select one or more categories
    
    Arguments:
        dist_matrix {list<list<float>>} -- pairwise cosine distance matrix
        entities {list<String>} -- all titles
        selected_titles {list<String>} -- selected titles
    
    Returns:
        list<String> -- two initial titles
    """
    if len(selected_ids) == 1:
        # suggest two jobs within a rather close distance to the given embedding
        option_1 = _find_close_point(dist_matrix, entities, selected_ids[0])
        option_2 = _find_close_point(dist_matrix, entities, selected_ids[0])

        # ensure that we select two different options
        while option_2 == option_1:
            option_2 = _find_close_point(dist_matrix, entities, selected_ids[0])
        options = [entities[option_1], entities[option_2]]

    else:
        if len(selected_ids) > 2:
            # select two random samples
            selected_ids = np.random.choice(selected_ids, 2, replace=False)

        # suggest one job within a rather close distance each for both of the given embeddings
        options = [entities[_find_close_point(dist_matrix, entities, origin)] for origin in selected_ids]

    return options

def _find_close_point(dist_matrix, entities, selected_id, neighborhood_size = 100, skip_range = 1):
    """
    Find a close point relativ to the given job title
    
    Arguments:
        dist_matrix {list<list<float>>} -- pairwise cosine distance matrix
        entities {list<String>} -- all titles
        selected_title {list<String>} -- selected title
    
    Returns:
        String -- one near point
    """
    dists = dist_matrix[entities.index(str(selected_id))]
    neighbors = np.argpartition(dists, neighborhood_size)[skip_range:neighborhood_size]
    return np.random.choice(neighbors, 1)[0]

def get_options(database, entities, embeddings, selected, not_selected, neighborhood_size = 100, num_pts = 2, skip_range = 10, num_jobs = 5):
    """
    Get two k-nearest neighbors of all selected entities
    
    Arguments:
        entities {list<String>} -- all titles
        embeddings {list<list<float>>} -- BoW features
        selected {list<String>} -- all selected titles
        not_selected {list<String>} -- all not selected titles that were shown as options
    
    Keyword Arguments:
        neighborhood_size {int} -- the range within points are suggested (default: {100})
        num_pts {int} -- number of suggested options (default: {2})
        skip_range {int} -- amount of nearest points that are not suggested (default: {10})
        num_jobs {int} -- amount of suggested jobs (default: {10})
    
    Returns:
        list<String>, list<String> -- suggested options and jobs
    """
    print(selected)
    selected_indices = [entities.index(str(x)) for x in selected]
    selected_features = [embeddings[x] for x in selected_indices]
    not_selected_indices = [entities.index(str(x)) for x in not_selected]
    sum_selected = np.zeros(len(selected_features[0]))

    # calculate the averaged point in the embedding space
    for i in range(len(selected_features)):
        for j in range(len(selected_features[i])):
            sum_selected[j] += selected_features[i][j]
    avg_selected = sum_selected / len(selected_features)

    # calculate the distances of all embeddings to the averaged point
    dists = []
    for i in range(len(embeddings)):
        if i % 3 == 0:
            dists.append(spatial.distance.cosine(np.array(embeddings[i]), avg_selected))
        else:
            dists.append(2)

    jobs = [entities[x] for x in np.argpartition(dists, num_jobs)[:num_jobs]]
    try:
        neighbors = np.argpartition(dists, neighborhood_size)[skip_range:neighborhood_size]
        rel_neighbors = [x for x in neighbors if x not in selected_indices and x not in not_selected_indices]
        neighbors = list(np.random.choice(rel_neighbors, num_pts, replace=False))
        options = [entities[x] for x in neighbors]
        return options, jobs
    except: # no more possible options
        return [], jobs

def get_job_infos(database, id):
    """
    Get the information details for a given job title
    
    Arguments:
        database {pymongo.database.Database} -- the given database object
        title {String} -- the job title
    
    Returns:
        String -- [description]
    """
    try:
        job = database.jobs.find_one({"_id": ObjectId(id)})
        return job['title'], job['info'], job['_id']
    except:
        return ""

def get_category_infos(database, title):
    """
    Get the information details for a given job title
    
    Arguments:
        database {pymongo.database.Database} -- the given database object
        title {String} -- the category title
    
    Returns:
        String -- category information 
    """
    try:
        category = database.categories.find_one({"category_name": title})
        return category['info'], category['_id']
    except:
        return ""