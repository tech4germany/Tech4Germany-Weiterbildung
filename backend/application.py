from bson import json_util
from bson.objectid import ObjectId
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_caching import Cache
from flask_cors import CORS
import json
import os
from pymongo import MongoClient
import re
import utils
import uuid

application = Flask(__name__)
CORS(application)

# initialize cache for data heavy ressources
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
    return json.dumps(courses_collection, default=json_util.default)

@application.route("/courses/filter/<title>", methods=['GET'])
@cache.cached(timeout=50)
def find_all_courses_with_title(title):
    """Lists all existing courses matching a given title 
    
    Arguments:
        title {String} -- the search title
    
    Returns:
        [type] -- [description]
    """
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
    """Finds a specific course that matches the given id
    
    Arguments:
        id {String} -- course id in the database
    
    Returns:
        JSON -- the matching course
    """
    course = t4g_database.courses.find_one({'_id': ObjectId(id)})
    return json.dumps(course, default=json_util.default)

@application.route("/select", methods=['POST'])
def set_option():
    """[summary]
    
    Returns:
        [type] -- [description]
    """
    _uuid = request.get_json('uuid')['uuid']
    session = t4g_database.sessions.find_one({'uuid': uuid.UUID(_uuid).hex})
    if request.get_json('option_type')['option_type'] == "Berufe":
        # store selected job option and send the session information with generated options
        option = request.get_json('options')['options'][0]
        session['selected'].append(option)
        session['options'].remove(option)

        for val in session['options']:
            session['options'].remove(val)
            session['not_selected'].append(val)

        options, session['jobs'] = utils.get_options(job_entities, job_embeddings, session['selected'], session['not_selected'])
        option_objects = []
        for option in options:
            option_object = {}
            option_object['title'] = option
            option_object['info'] = utils.get_job_info(t4g_database, option)
            option_objects.append(option_object)
        session['options'] = option_objects
        session['final'] =  0 if len(session['options']) > 0 else 1

        t4g_database.sessions.update_one({'uuid': uuid.UUID(_uuid).hex}, {'$set': session})
        return 200 if not application.debug else json.dumps(session, default=json_util.default)

    elif request.get_json('option_type')['option_type'] == "Branchen":
        # store selected categories and send the session with initial options
        categories = request.get_json('options')['options']
        start_jobs_titles = []
        for category in categories:
            job_id = t4g_database.categories.find_one({"category_name": category['title']})['job_id']
            related_job = utils.load_related_job(t4g_database ,job_id)
            start_jobs_titles.append(related_job['title'])

        options = utils.load_init_options(dist_matrix, job_entities, start_jobs_titles)
        option_objects = []
        for option in options:
            option_object = {}
            option_object['title'] = option
            option_object['info'] = utils.get_job_info(t4g_database, option)
            option_objects.append(option_object)
        session['options'] = option_objects
        session['option_type'] = "Berufe"
        t4g_database.sessions.update_one({'uuid': uuid.UUID(_uuid).hex}, {'$set': session})
        return 200 if not application.debug else json.dumps(session, default=json_util.default)
    else:
        return "Invalid option type, please use either 'Berufe' or 'Branchen'", 406

@application.route("/init", methods=['GET'])
def init_session():
    """[summary]
    
    Returns:
        [type] -- [description]
    """
    session = {}
    session['uuid'] = uuid.uuid4().hex
    options = utils.load_categories(t4g_database)
    option_objects = []
    for option in options:
            option_object = {}
            option_object['title'] = option
            option_object['info'] = ""
            option_objects.append(option_object)
    session['options'] = option_objects
    session['option_type'] = "Branchen"
    session['fav_jobs'] = session['fav_courses'] = session['selected'] = session['not_selected'] = []
    t4g_database.sessions.insert_one(session)
    return json.dumps(session, default=json_util.default)

@application.route("/like", methods=['POST'])
def like_item():
    """[summary]
    
    Returns:
        [type] -- [description]
    """
    _uuid = request.get_json('uuid')['uuid']
    title = request.get_json('options')['options']
    print(title)
    session = t4g_database.sessions.find_one({"uuid": _uuid})
    if request.get_json('option_type')['option_type'] == "Kurs":
        session['fav_courses'].append(title)
    elif request.get_json('option_type')['option_type'] == "Beruf":
        session['fav_jobs'].append(title)

    t4g_database.sessions.update_one({'uuid': uuid.UUID(_uuid).hex}, {'$set': session})
    return 200 if not application.debug else json.dumps(session, default=json_util.default)

@application.route("/courses/add", methods=['POST'])
def add_course():
    """[summary]
    
    Returns:
        [type] -- [description]
    """
    course = {}
    course['title'] = request.get_json('title')['title']
    # TODO add all required fields

    result = t4g_database.courses.insert_one(course)
    return 200 if not application.debug else result

@application.route("/courses/delete", methods=['POST'])
def delete_course():
    """[summary]
    
    Returns:
        [type] -- [description]
    """
    # NOTE that deleting only according to the title might not be save
    # TODO use multiple identifers
    result = t4g_database.courses.delete_one({"title": request.get_json('title')['title']})
    return 200 if not application.debug else result

if __name__ == "__main__":
    # load environment variables
    env_path = os.path.join(os.path.dirname(__file__), '../.env')
    load_dotenv(dotenv_path=env_path)

    # connect to database
    connection_string = os.getenv("DATABASE_URL")
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.test

    # load embeddings and entities
    job_entities, job_embeddings = utils.load_jobs_data('../data/job_embeddings.csv')
    dist_matrix = utils.load_dists('../data/jobs_cosine_distances.csv')

    # start application
    application.run(debug=True, host="0.0.0.0", port=os.getenv("BACKEND_PORT"))