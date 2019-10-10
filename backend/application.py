from bson import json_util
from bson.objectid import ObjectId
import csv
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_caching import Cache
from flask_cors import CORS
import json
import numpy as np
import os
from pymongo import MongoClient
import re
from scipy import spatial
import uuid

application = Flask(__name__)
CORS(application)
cache = Cache(application, config={'CACHE_TYPE': 'simple'})
cache.init_app(application)

"""
Lists all existing courses
"""
@application.route("/courses/all", methods=['GET'])
@cache.cached(timeout=50)
def list_all_courses():
    courses_collection = list(t4g_database.courses.find({}))
    return json.dumps(courses_collection, default=json_util.default)

"""
Lists all existing courses
"""
@application.route("/courses/all/<int:limit>", methods=['GET'])
@cache.cached(timeout=50)
def list_courses(limit):
    courses_collection = list(t4g_database.courses.find({}).limit(limit))
    return json.dumps(courses_collection, default=json_util.default), 200

"""
Lists all existing courses with a given title
"""
@application.route("/courses/filter/<title>", methods=['GET'])
@cache.cached(timeout=50)
def find_all_courses(title):
    courses_collection = list(t4g_database.courses.find({ 'title': { '$regex': re.compile(f'.*{title}.*', re.IGNORECASE) }}))
    return json.dumps(courses_collection, default=json_util.default), 200

@application.route("/courses/filter/<title>/<int:limit>", methods=['GET'])
@cache.cached(timeout=50)
def find_courses(title, limit):
    """Lists all existing courses with a given title and a specifc limit
    
    Arguments:
        title {String} -- course title
        limit {int} -- amount of returned courses
    
    Returns:
        JSON -- a given amount of courses matching the given title
    """
    courses_collection = list(t4g_database.courses.find({ 'title': { '$regex': f'.*{title}.*' }}).limit(limit))
    return json.dumps(courses_collection, default=json_util.default), 200

@application.route("/courses/find/<id>", methods=['GET'])
def find_course(id):
    """Finds a specifc course that matches the given id
    
    Arguments:
        id {String} -- course id in the database
    
    Returns:
        JSON -- the matching course
    """
    course = t4g_database.courses.find_one({'_id': ObjectId(id)})
    return json.dumps(course, default=json_util.default), 200

@application.route("/select", methods=['POST'])
def set_option():
    if request.get_json('option_type')['option_type'] == "Berufe":
        # store selected job option and send the session information with generated options
        _uuid = request.get_json('uuid')['uuid']
        option = request.get_json('option')['option']
        session = t4g_database.sessions.find_one({'uuid': uuid.UUID(_uuid).hex})
        session['selected'].append(option)
        session['options'].remove(option)
        for val in session['options']:
            session['options'].remove(val)
            session['not_selected'].append(val)
        session['options'] = _get_options(session['selected'], session['not_selected'])
        t4g_database.sessions.update_one({'uuid': uuid.UUID(_uuid).hex}, {'$set': session})

        # also send results
        return json.dumps(session, default=json_util.default)
    elif request.get_json('option_type')['option_type'] == "Kategorien":
        # store selected categories and send the session with initial options
        _uuid = request.get_json('uuid')['uuid']
        categories = request.get_json('categories')['categories']
        start_jobs_titles = []
        for category in categories:
            job_id = t4g_database.categories.find_one({"category_name": category})['job_id']
            related_job = _load_related_job(job_id)
            start_jobs_titles.append(related_job['title'])
        job_embeddings = [_get_job_embedding(x) for x in start_jobs_titles]
        options = _load_init_options(job_embeddings)
        resp_data = {}
        return resp_data
    else:
        return "Invalid option type, please use either 'Berufe' or 'Kategorien'", 406

@application.route("/init", methods=['GET'])
def init_session():
    resp = {}
    resp['uuid'] = uuid.uuid4().hex
    resp['categories'] = _load_categories()
    t4g_database.sessions.insert_one(resp)
    return json.dumps(resp, default=json_util.default)

def _get_options(selected, not_selected, neighborhood_size = 10, num_pts = 2):
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
    neighbors = np.argpartition(dists, neighborhood_size)[:neighborhood_size]
    rel_neighbors = [x for x in neighbors if x not in selected_indices and x not in not_selected_indices]
    neighbors = list(np.random.choice(rel_neighbors, num_pts, replace=False))
    return [entities[x] for x in neighbors]

def _load_init_options(job_titles):
    if len(job_titles) == 1:
        # suggest two jobs within a rather close distance to the given embedding
        options = _find_close_point(job_titles[0], n_pts=2)
    else:
        if len(job_embeddings) > 2:
            # select two random samples
            job_embeddings = np.random.choice(job_titles, 2, replace=False)

        # suggest one job within a rather close distance each for both of the given embeddings
        for job_title in job_titles:
            option = _find_close_point(job_title)

def _find_close_point(job_titles, n_pts=1):
    dists = []
    for job_title in job_titles:
        i = entities.index(job_title)
        dists = dist_matrix[i]
        neighbors = np.argpartition(dists, 30)[1:30]
        print(i, neighbors)

# def _load_entities():
#     entities = []
#     with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/embeddings.csv'), 'r') as embeddings_in:
#         data = csv.reader(embeddings_in, delimiter=',')
#         for line in data:
#             entities.append(line[0])
#     return entities

# def _load_embeddings():
#     embeddings = []
#     with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/embeddings.csv'), 'r') as infile:
#         data = csv.reader(infile, delimiter=',')
#         for line in data:
#             embedding = [float(x) for x in line[1:]]
#             embeddings.append(embedding)
#     return embeddings

# def _load_cosine_distances():
#     cosine_distances = []
#     with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/embeddings_dists_cosine.csv'), 'r') as dists_in:
#         data = csv.reader(dists_in, delimiter=',')
#         for line in data:
#             cosine_distances.append([float(x) for x in line])
#     print("Done")
#     return cosine_distances

# def _get_unique_distances(distances):
#     """Gets all unique distances from a n x n distance matrix where i != j
    
#     Arguments:
#         distances {list<list<float>>} -- an n x n distance matrix describing all pairwise distances between points i and j
    
#     Returns:
#         list<float> -- all unique distance with i != j
#     """
#     unique_distances = []
#     for i in range(len(distances)):
#         for j in range(i+1,len(distances)):
#             unique_distances.append(distances[i][j])
#     return unique_distances

# def _get_average_cosine_distance(unique_distances):
#     return sum(unique_distances) / len(unique_distances)

# def _find_seed_points(cosine_distance_matrix, average_distance, num_pts):
#     seed_pts = np.random.choice(np.arange(len(cosine_distance_matrix[0])), num_pts)
#     for index in range(len(seed_pts)-1):
#         if cosine_distance_matrix[seed_pts[index]][seed_pts[index+1]] < average_distance:
#             return _find_seed_points(cosine_distance_matrix, average_distance, num_pts)
#     return seed_pts

# def _find_seed_values(cosine_distance_matrix, average_distance, entities, num_pts = 2):
#     seed_pts = _find_seed_points(cosine_distance_matrix, average_distance, num_pts)
#     return [entities[x] for x in seed_pts]

def _load_categories():
    categories = list(t4g_database.categories.find({}))
    return json.dumps(categories, default=json_util.default)

def _load_related_job(job_id):
    return t4g_database.jobs.find_one({'job_id': job_id})

def _load_jobs_data(file_name):
    embeddings = dict()
    entities = []
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), file_name), 'r') as infile:
        data = csv.reader(infile, delimiter=',')
        for line in data:
            embeddings[line[0]] = [float(x) for x in line[1:]]
            entities.append(line[0])
    return entities, embeddings

# def _load_job_entities(file_name):
#     with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), file_name), 'r') as infile:
#         data = csv.reader(infile, delimiter=',')
#         entities = [line[0] for line in data]
#     return entities

def _get_job_embedding(job):
    return job_embeddings[job]

# def _load_dists(job_embeddings):
#     print("Load jobs embeddings.")
#     dist_matrix = []
#     with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "../data/jobs_cosine_distances.csv"), 'a+') as outfile:
#         for key_i in job_embeddings:
#             dists = []
#             for key_j in job_embeddings:
#                 dists.append(spatial.distance.cosine(job_embeddings[key_i], job_embeddings[key_j]))
#             outfile.write(f'{",".join([str(x) for x in dists])}\n')
#             dist_matrix.append(dists)
#     print("Done.")
#     return dist_matrix

def _load_dists(file_path):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), file_path), r) as in_file:
        data = csv.reader(infile, delimiter=',')
        dist_matrix [float(y) for x in data for y in x]
    return dist_matrix

if __name__ == "__main__":
    # load environment variables
    env_path = os.path.join(os.path.dirname(__file__), '../.env')
    load_dotenv(dotenv_path=env_path)

    # connect to database
    connection_string = os.getenv("DATABASE_URL")
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.test

    # load embeddings and entities
    job_entities, job_embeddings = _load_jobs_data('../data/job_embeddings.csv')
    dist_matrix = _load_dists(job_embeddings)

    # start application
    application.run(debug=True, host="0.0.0.0", port=os.getenv("BACKEND_PORT"))