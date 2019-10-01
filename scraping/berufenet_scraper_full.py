from dotenv import load_dotenv
from pathlib import Path
import time
import json
import os
from pymongo import MongoClient
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import string
import traceback

env_path = Path('../') / '.env'
load_dotenv(dotenv_path=env_path)
connection_string = os.getenv("DATABASE_URL")
mongo_client = MongoClient(connection_string)
t4g_database = mongo_client.test
jobs_collection = t4g_database.jobs
driver = webdriver.Chrome('./chromedriver')

base_url = 'https://berufenet.arbeitsagentur.de/berufenet/faces/index?path=null/sucheAZ&let='

def crawl_character(character):
    url = base_url + character
    driver.get(url)
    page = 0
    while True:
        for i in range(30):
            for j in range(0, page):
                try:
                    WebDriverWait(driver, 3).until(expected_conditions.presence_of_element_located((By.ID, 'pt1:r1:0:pt1:tbl_suche_az:dc_cl4')))
                    driver.find_element(By.ID, 'pt1:r1:0:pt1:tbl_suche_az:dc_cl4').click()
                    time.sleep(0.5)
                except:
                    print(traceback.format_exc())
                    return
            try:
                WebDriverWait(driver, 3).until(expected_conditions.presence_of_element_located((By.ID, f"pt1:r1:0:pt1:tbl_suche_az:i1:{i}:rl2")))
                driver.find_element(By.ID, f"pt1:r1:0:pt1:tbl_suche_az:i1:{i}:rl2").click()
                WebDriverWait(driver, 3).until(expected_conditions.presence_of_element_located((By.ID, 'b10-0_0_Content_1')))
                data = {}
                data['info']= driver.find_element(By.ID,'b10-0_0_Content_1').text
                data['title'] = driver.find_element_by_css_selector('h1').text
                data['job_id'] = driver.current_url.split('&')[-2].split('=')[-1]
                jobs_collection.insert_one(data)
                print(character, page, i, data)
            except TimeoutException:
                continue
            except Exception:
                continue
            finally:
                driver.get(url)
        page += 1

for character in string.ascii_uppercase[:]:
    crawl_character(character)
