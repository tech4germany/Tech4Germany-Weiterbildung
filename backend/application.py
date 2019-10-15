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

@application.route("/courses/all", methods=['GET'])
@cache.cached(timeout=50)
def list_all_courses():
    """
    List all existing courses
    
    Returns:
        [type] -- [description]
    """
    courses_collection = list(mongo_client.test.courses.find({}))
    return json.dumps(courses_collection, default=json_util.default)

@application.route("/courses/all/<int:limit>", methods=['GET'])
@cache.cached(timeout=50)
def list_courses(limit):
    """
    List all existing courses with a given limit
    
    Arguments:
        limit {int} -- amount of shown courses
    
    Returns:
        JSON -- the first {limit} courses
    """
    courses_collection = list(mongo_client.test.courses.find({}).limit(limit))
    return json.dumps(courses_collection, default=json_util.default)

@application.route("/courses/filter/<title>", methods=['GET'])
@cache.cached(timeout=50)
def find_all_courses_with_title(title):
    """
    List all existing courses matching a given title 
    
    Arguments:
        title {String} -- the search title
    
    Returns:
        JSON -- courses matching a given title
    """
    courses_collection = list(mongo_client.test.courses.find({ 'title': { '$regex': re.compile(f'.*{title}.*', re.IGNORECASE) }}))
    return json.dumps(courses_collection, default=json_util.default)

@application.route("/courses/filter/<title>/<int:limit>", methods=['GET'])
@cache.cached(timeout=50)
def find_courses(title, limit):
    """
    List all existing courses with a given title and a specifc limit
    
    Arguments:
        title {String} -- course title
        limit {int} -- amount of returned courses
    
    Returns:
        JSON -- a given amount of courses matching the given title
    """
    courses_collection = list(mongo_client.test.courses.find({ 'title': { '$regex': f'.*{title}.*' }}).limit(limit))
    return json.dumps(courses_collection, default=json_util.default)

@application.route("/courses/find/<id>", methods=['GET'])
def find_course(id):
    """
    Find a specific course that matches the given id
    
    Arguments:
        id {String} -- course id in the database
    
    Returns:
        JSON -- the matching course
    """
    course = mongo_client.test.courses.find_one({'_id': ObjectId(id)})
    return json.dumps(course, default=json_util.default)

@application.route("/select", methods=['POST'])
def set_option():
    """
    Select an option (either category or job) and generate two new job options
    
    Returns:
        JSON -- a session including two generated options
    """
    _uuid = request.get_json('uuid')['uuid']
    session = mongo_client.test.sessions.find_one({'uuid': uuid.UUID(_uuid).hex})
    if request.get_json('option_type')['option_type'] == "Berufe":
        # store selected job option and send the session information with generated options
        option = request.get_json('options')['options'][0]
        session['selected'].append(option['title'])
        session['options'].remove(option)

        for val in session['options']:
            session['options'].remove(val)
            session['not_selected'].append(val['title'])

        options, session['jobs'] = utils.get_options(job_entities, job_embeddings, session['selected'], session['not_selected'])
        option_objects = []
        for option in options:
            option_object = {}
            option_object['title'] = option
            option_object['info'] = utils.get_job_info(mongo_client.test, option)
            option_objects.append(option_object)
        session['options'] = option_objects
        session['final'] =  0 if len(session['options']) > 0 else 1

        mongo_client.test.sessions.update_one({'uuid': uuid.UUID(_uuid).hex}, {'$set': session})
        return json.dumps(session, default=json_util.default)

    elif request.get_json('option_type')['option_type'] == "Branchen":
        # store selected categories and send the session with initial options
        categories = request.get_json('options')['options']
        start_jobs_titles = []
        for category in categories:
            job_id = mongo_client.test.categories.find_one({"category_name": category['title']})['job_id']
            related_job = utils.load_related_job(mongo_client.test ,job_id)
            start_jobs_titles.append(related_job['title'])

        options = utils.load_init_options(dist_matrix, job_entities, start_jobs_titles)
        option_objects = []
        for option in options:
            option_object = {}
            option_object['title'] = option
            option_object['info'] = utils.get_job_info(mongo_client.test, option)
            option_objects.append(option_object)
        session['options'] = option_objects
        session['option_type'] = "Berufe"
        mongo_client.test.sessions.update_one({'uuid': uuid.UUID(_uuid).hex}, {'$set': session})
        return json.dumps(session, default=json_util.default)
    else:
        return "Invalid option type, please use either 'Berufe' or 'Branchen'", 406

@application.route("/init", methods=['GET'])
def init_session():
    """
    Initialize a session
    
    Returns:
        JSON -- a generate session containing a UUID and the different categories
    """
    session = {}
    session['uuid'] = uuid.uuid4().hex
    options = utils.load_categories(mongo_client.test)
    option_objects = []
    for option in options:
            option_object = {}
            option_object['title'] = option
            option_object['info'] = utils.get_category_info(mongo_client.test, option)
            option_objects.append(option_object)
    session['options'] = option_objects
    session['option_type'] = "Branchen"
    session['fav_jobs'] = session['fav_courses'] = session['selected'] = session['not_selected'] = []
    mongo_client.test.sessions.insert_one(session)
    return json.dumps(session, default=json_util.default)

@application.route("/like", methods=['POST'])
def like_item():
    """
    Like an item (job or course)
    
    Returns:
        int -- status code
    """
    _uuid = request.get_json('uuid')['uuid']
    title = request.get_json('options')['options']
    session = mongo_client.test.sessions.find_one({"uuid": _uuid})

    # add liked course
    if request.get_json('option_type')['option_type'] == "Kurse":
        session['fav_courses'].append(title['title'])
    
    # add liked job
    elif request.get_json('option_type')['option_type'] == "Berufe":
        session['fav_jobs'].append(title['title'])

    # update session
    mongo_client.test.sessions.update_one({'uuid': uuid.UUID(_uuid).hex}, {'$set': session})
    return 200 if not application.debug else json.dumps(session, default=json_util.default)

@application.route("/unlike", methods=['POST'])
def unlike_item():
    """
    Like an item (job or course)
    
    Returns:
        int -- status code
    """
    _uuid = request.get_json('uuid')['uuid']
    title = request.get_json('options')['options']
    session = mongo_client.test.sessions.find_one({"uuid": _uuid})

    # add liked course
    if request.get_json('option_type')['option_type'] == "Kurse":
        if title in session['fav_courses']:
            session['fav_courses'].remove(title['title'])
    
    # add liked job
    elif request.get_json('option_type')['option_type'] == "Berufe":
        if title in session['fav_jobs']:
            session['fav_jobs'].remove(title['title'])

    # update session
    mongo_client.test.sessions.update_one({'uuid': uuid.UUID(_uuid).hex}, {'$set': session})
    return 200 if not application.debug else json.dumps(session, default=json_util.default)

@application.route("/courses/add", methods=['POST'])
def add_course():
    """
    Add a course
    
    Returns:
        int -- status code
    """
    course = {}
    course['title'] = request.get_json('title')['title']
    course['info'] = request.get_json('info')['info']
    # TODO are additional fields required?

    result = mongo_client.test.courses.insert_one(course)
    return 200 if not application.debug else result

@application.route("/courses/delete", methods=['POST'])
def delete_course():
    """
    Delete a course
    
    Returns:
        JSON -- status code
    """
    # NOTE that deleting only according to the title might not be save
    # TODO use multiple identifers
    result = mongo_client.test.courses.delete_one({"title": request.get_json('title')['title']})
    return 200 if not application.debug else result

if __name__ == "__main__":
    # load environment variables
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path=env_path)

    # connect to database
    connection_string = os.environ.get("DATABASE_URL")
    mongo_client = MongoClient(connection_string)

    # load embeddings and entities
    job_entities, job_embeddings = utils.load_jobs_data('./data/job_embeddings.csv')
    dist_matrix = utils.load_dists('./data/jobs_cosine_distances.csv')

    # start application
    # NOTE not to use debug mode in production
    application.run(debug=True, host="0.0.0.0", port=os.environ.get("BACKEND_PORT"))