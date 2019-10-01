from dotenv import load_dotenv
from pathlib import Path
import os
from pymongo import MongoClient

def get_professions():
    courses = courses_collection.find()
    professions = set()
    counter_found = 0
    counter = 0
    for course in courses:
        counter += 1
        if 'professions' in course:
            counter_found += 1
            print(f"{counter_found}/{counter}")
            for profession in course['professions']:
                professions.add(profession['website'])
    return professions, counter

def main():
    professions, counter = get_professions()
    print(professions)

if __name__ == "__main__":
    env_path = Path('../') / '.env'
    load_dotenv(dotenv_path=env_path)
    connection_string = os.getenv("DATABASE_URL")
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.test
    jobs_collection = t4g_database.jobs
    courses_collection = t4g_database.courses
    main()