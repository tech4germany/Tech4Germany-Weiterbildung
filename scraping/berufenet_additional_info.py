from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathlib import Path
import json
import os
from pymongo import MongoClient
import requests

def main():
    env_path = Path('../') / '.env'
    load_dotenv(dotenv_path=env_path)
    connection_string = os.getenv("DATABASE_URL")
    mongo_client = MongoClient(connection_string)
    t4g_database = mongo_client.test
    jobs_collection = t4g_database.jobs
    base_url = 'https://berufenet.arbeitsagentur.de/berufenet/faces/index?path=null/sucheAZ/kurzbeschreibung&dkz='
    count = jobs_collection.count()
    for index, job in enumerate(jobs_collection.find()):
        job_id = job['job_id']
        url = base_url + job_id
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'lxml')
        job['job_type'] = soup.find_all("div", class_="header-secondary-text")[-1].text.strip()
        detail_url = 'https://berufenet.arbeitsagentur.de/berufenet/faces/index?path=null/sucheAZ/kurzbeschreibung/taetigkeitsinhalte&dkz=' + job_id
        req = requests.get(detail_url)
        soup = BeautifulSoup(req.content, 'lxml')
        job['detailed_activities'] = soup.find_all("div", id="b11-0_0_Content_1")[-1].text.strip()
        jobs_collection.replace_one({"_id": job["_id"]}, job)
        print(f'{index}/{count}')

if __name__ == '__main__':
    main()