import json
from pymongo import MongoClient

def main():
    connection_string = "mongodb+srv://t4g:bmas@cluster0-4lru4.mongodb.net/test"
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.t4g
    json_data = mongo_db_collection_to_json(t4g_database, 'courses')
    print(json_data)

def mongo_db_collection_to_json(db, collection):
    courses_collection = db[collection].find({})
    data = list()
    for cursor in courses_collection:
        data.append(cursor)
    return data

main()