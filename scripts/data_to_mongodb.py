from dotenv import load_dotenv
import glob
import json
import os
from pathlib import Path
from pymongo import MongoClient
import re
from tqdm import tqdm as tqdm

def import_files(collection, folder):
    data_files = [f for f in glob.glob(folder + "**/*_data.txt", recursive=True)]
    for data_file in tqdm(data_files):
        with open(data_file, 'r') as infile:
            # load data
            data = infile.read()
            data = data.replace('\\n', ' ')
            data = data.replace('\\t','')
            data = json.loads(data)

            # export data to database
            collection.insert_one(data)

def main():
    connection_string = f'mongodb+srv://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}@{os.getenv("DATABASE_URL")}'
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.t4g
    courses_collection = t4g_database.courses
    import_files(courses_collection, '../scraping/output/')

if __name__ == '__main__':
    env_path = Path('../') / '.env'
    load_dotenv(dotenv_path=env_path)
    main()