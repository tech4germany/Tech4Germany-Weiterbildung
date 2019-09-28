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
import uuid

application = Flask(__name__)
CORS(application)
cache = Cache(application,config={'CACHE_TYPE': 'simple'})
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
    return json.dumps(courses_collection, default=json_util.default)

"""
Lists all existing courses with a given title
"""
@application.route("/courses/filter/<title>", methods=['GET'])
@cache.cached(timeout=50)
def find_all_courses(title):
    courses_collection = list(t4g_database.courses.find({ 'title': { '$regex': re.compile(f'.*{title}.*', re.IGNORECASE) }}))
    return json.dumps(courses_collection, default=json_util.default)

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
    return json.dumps(courses_collection, default=json_util.default)

@application.route("/courses/find/<id>", methods=['GET'])
def find_course(id):
    """Finds a specifc course that matches the given id
    
    Arguments:
        id {String} -- course id in the database
    
    Returns:
        JSON -- the matching course
    """
    course = t4g_database.courses.find_one({'_id': ObjectId(id)})
    return json.dumps(course, default=json_util.default)

@application.route("/select", methods=['POST'])
def set_option():
    data = request.json
    uuid = data['uuid']
    option = data['option']
    resp = {}
    return json.dumps(resp, default=json_util.default)

@application.route("/init", methods=['GET'])
def init_session():
    resp = {}
    resp['uuid'] = uuid.uuid4()
    resp['options'] = find_seed_values(cosine_distances, average_distance, entities)
    t4g_database.sessions.insert_one(resp)
    print(resp)
    return json.dumps(resp, default=json_util.default)

def _load_entities():
    entities = []
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/embeddings.csv'), 'r') as embeddings_in:
        data = csv.reader(embeddings_in, delimiter=',')
        for line in data:
            entities.append(line[0])
    return entities

def _load_cosine_distances():
    cosine_distances = []
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/embeddings_dists_cosine.csv'), 'r') as dists_in:
        data = csv.reader(dists_in, delimiter=',')
        for line in data:
            cosine_distances.append([float(x) for x in line])
    return cosine_distances

def _get_unique_distances(distances):
    unique_distances = []
    for i in range(len(distances)):
        for j in range(i+1,len(distances)):
            unique_distances.append(distances[i][j])
    return unique_distances

def _get_average_cosine_distance(unique_distances):
    return sum(unique_distances) / len(unique_distances)

def _find_seed_points(cosine_distance_matrix, average_distance, num_pts):
    seed_pts = np.random.choice(np.arange(len(cosine_distance_matrix[0])), num_pts)
    for index in range(len(seed_pts)-1):
        if cosine_distance_matrix[seed_pts[index]][seed_pts[index+1]] < average_distance:
            return _find_seed_points(cosine_distance_matrix, average_distance, num_pts)
    return seed_pts

def find_seed_values(cosine_distance_matrix, average_distance, entities, num_pts = 2):
    seed_pts = _find_seed_points(cosine_distance_matrix, average_distance, num_pts)
    return [entities[x] for x in seed_pts]

if __name__ == "__main__":
    # load environment variables
    env_path = os.path.join(os.path.dirname(__file__), '../.env')
    load_dotenv(dotenv_path=env_path)

    # connect to database
    connection_string = os.getenv("DATABASE_URL")
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.test

    # load embeddings and entities
    entities = _load_entities()
    cosine_distances = _load_cosine_distances()
    unique_distances = _get_unique_distances(cosine_distances)
    average_distance = _get_average_cosine_distance(unique_distances)

    # start application
    application.run(debug=True, host="0.0.0.0", port=os.getenv("BACKEND_PORT"))