import json
import os
from pymongo import MongoClient
import re
from tqdm import tqdm as tqdm

def import_files(collection, folder):
    files = os.listdir(folder)
    data_files = [input_file for input_file in files if input_file.endswith('_data.txt')]
    for data_file in tqdm(data_files):
        with open(os.path.join(folder, data_file), 'r') as infile:
            # load data
            data = infile.read()
            data = data.replace('\\n', ' ')
            data = data.replace('\\t','')
            data = json.loads(data)

            # export data to database
            collection.insert_one(data)

def main():
    connection_string = "mongodb+srv://t4g:bmas@cluster0-4lru4.mongodb.net/test"
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.t4g
    courses_collection = t4g_database.courses
    import_files(courses_collection, '../scraping/output_2/')

if __name__ == '__main__':
    main()