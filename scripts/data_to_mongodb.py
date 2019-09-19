import csv
import json
import os
from pymongo import MongoClient
from tqdm import tqdm as tqdm

def import_files(collection, folder):
    files = os.listdir(folder)
    csv_files = [input_file for input_file in files if input_file.endswith('_data.csv')]
    for csv_file in tqdm(csv_files):
        with open(os.path.join(folder, csv_file), 'r') as csvfile:
            course_reader = csv.reader(csvfile, delimiter=',')
            for row in course_reader:
                if len(row) > 1:
                    title = row[0].strip()
                    course_id = row[1].strip()
                    parent_1 = row[2].replace('+', ' ').strip()
                    parent_2 = row[3].replace('+', ' ').strip()
                    collection.insert_one({'title': title, 'parent_1': parent_1, 'parent_2': parent_2})
                    break

def main():
    connection_string = "mongodb+srv://t4g:bmas@cluster0-4lru4.mongodb.net/test"
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.t4g
    courses_collection = t4g_database.courses
    import_files(courses_collection, '../scraping/output/')

if __name__ == '__main__'
    main()