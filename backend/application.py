from bson import json_util
from bson.objectid import ObjectId
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_caching import Cache
from flask_cors import CORS
import json
import os
from pathlib import Path
from pymongo import MongoClient
import re

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
    connection_string = f'mongodb+srv://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}@{os.getenv("DATABASE_URL")}'
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.t4g
    courses_collection = list(t4g_database.courses.find({}))
    return json.dumps(courses_collection, default=json_util.default)

"""
Lists all existing courses
"""
@application.route("/courses/all/<int:limit>", methods=['GET'])
@cache.cached(timeout=50)
def list_courses(limit):
    connection_string = f'mongodb+srv://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}@{os.getenv("DATABASE_URL")}'
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.t4g
    courses_collection = list(t4g_database.courses.find({}).limit(limit))
    return json.dumps(courses_collection, default=json_util.default)

"""
Lists all existing courses with a given title
"""
@application.route("/courses/filter/<title>", methods=['GET'])
@cache.cached(timeout=50)
def find_all_courses(title):
    connection_string = f'mongodb+srv://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}@{os.getenv("DATABASE_URL")}'
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.t4g
    courses_collection = list(t4g_database.courses.find({ 'title': { '$regex': re.compile(f'.*{title}.*', re.IGNORECASE) }}))
    return json.dumps(courses_collection, default=json_util.default)

"""
Lists all existing courses with a given title and a specifc limit
"""
@application.route("/courses/filter/<title>/<int:limit>", methods=['GET'])
@cache.cached(timeout=50)
def find_courses(title, limit):
    connection_string = f'mongodb+srv://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}@{os.getenv("DATABASE_URL")}'
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.t4g
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
    connection_string = f'mongodb+srv://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}@{os.getenv("DATABASE_URL")}'
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.t4g
    course = t4g_database.courses.find_one({'_id': ObjectId(id)})
    return json.dumps(course, default=json_util.default)

@application.route("/select", methods=['POST'])
def set_option():
    data = request.json
    uuid = data['uuid']
    option = data['option']
    return jsonify(data)

if __name__ == "__main__":
    env_path = os.path.join(os.path.dirname(__file__), '../.env')
    load_dotenv(dotenv_path=env_path)
    application.run(debug=True, host="0.0.0.0", port=os.getenv("BACKEND_PORT"))