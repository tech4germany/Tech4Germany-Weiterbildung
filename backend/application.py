from flask import Flask, render_template
from flask_caching import Cache
from flask_cors import CORS
from bson import json_util
import json
import os
from pymongo import MongoClient
import re

application = Flask(__name__)
CORS(application)
cache = Cache(application,config={'CACHE_TYPE': 'simple'})
cache.init_app(application)

"""
Lists all existing courses
"""
@application.route("/courses/all")
@cache.cached(timeout=50)
def list_all_courses():
    connection_string = "mongodb+srv://t4g:bmas@cluster0-4lru4.mongodb.net/test"
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.t4g
    courses_collection = list(t4g_database.courses.find({}))
    return json.dumps(courses_collection, default=json_util.default)

"""
Lists all existing courses
"""
@application.route("/courses/all/<int:limit>")
@cache.cached(timeout=50)
def list_courses(limit):
    connection_string = "mongodb+srv://t4g:bmas@cluster0-4lru4.mongodb.net/test"
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.t4g
    courses_collection = list(t4g_database.courses.find({}).limit(limit))
    return json.dumps(courses_collection, default=json_util.default)

"""
Lists all existing courses with a given title
"""
@application.route("/courses/filter/<title>")
def find_all_courses(title):
    connection_string = "mongodb+srv://t4g:bmas@cluster0-4lru4.mongodb.net/test"
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.t4g
    courses_collection = list(t4g_database.courses.find({ 'title': { '$regex': f'.*{title}.*' }}))
    return json.dumps(courses_collection, default=json_util.default)

"""
Lists all existing courses with a given title and a specifc limit
"""
@application.route("/courses/filter/<title>/<int:limit>")
def find_courses(title, limit):
    connection_string = "mongodb+srv://t4g:bmas@cluster0-4lru4.mongodb.net/test"
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.t4g
    courses_collection = list(t4g_database.courses.find({ 'title': { '$regex': f'.*{title}.*' }}).limit(limit))
    return json.dumps(courses_collection, default=json_util.default)


if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0")