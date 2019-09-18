from flask import Flask, render_template
from flask_caching import Cache
from flask_cors import CORS
from bson import json_util
import json
import os
from pymongo import MongoClient

application = Flask(__name__)
CORS(application)
cache = Cache(application,config={'CACHE_TYPE': 'simple'})
cache.init_app(application)

"""
Lists all existing courses
"""
@application.route("/courses")
@cache.cached(timeout=50)
def list_courses():
    connection_string = "mongodb+srv://t4g:bmas@cluster0-4lru4.mongodb.net/test"
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.t4g
    courses_collection = list(t4g_database.courses.find({}))
    return json.dumps(courses_collection, default=json_util.default)


"""
Lists all existing courses with a given title
"""
@application.route("/courses/<title>")
def find_courses(title):
    connection_string = "mongodb+srv://t4g:bmas@cluster0-4lru4.mongodb.net/test"
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.t4g
    courses_collection = list(t4g_database.courses.find({ "title": title }))
    return json.dumps(courses_collection, default=json_util.default)


if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0")