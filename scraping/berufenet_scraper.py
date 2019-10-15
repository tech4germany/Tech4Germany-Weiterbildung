from dotenv import load_dotenv
from pathlib import Path
import time
import json
import os
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

env_path = Path('../') / '.env'
load_dotenv(dotenv_path=env_path)
connection_string = os.getenv("DATABASE_URL")
mongo_client = MongoClient(connection_string)
t4g_database = mongo_client.test
jobs_collection = t4g_database.jobs
driver = webdriver.Chrome('./chromedriver')
page = 9
for j in range(page,14):
    for i in range(30):
        driver.get("https://berufenet.arbeitsagentur.de/berufenet/faces/index?path=null/reglementierteBerufe")
        if j > 2:
            driver.find_element(By.ID, "pt1:r1:0:pt1:tbl_reglementierte_berufe:dc_cl1j_id_2").click()
            time.sleep(3)
            
        if j > 4:
            driver.find_element(By.ID, "pt1:r1:0:pt1:tbl_reglementierte_berufe:dc_cl1j_id_4").click()
            time.sleep(3)

        if j > 6:
            driver.find_element(By.ID, "pt1:r1:0:pt1:tbl_reglementierte_berufe:dc_cl1j_id_6").click()
            time.sleep(3)

        if j > 8:
            driver.find_element(By.ID, "pt1:r1:0:pt1:tbl_reglementierte_berufe:dc_cl1j_id_8").click()
            time.sleep(3)

        if j > 10:
            driver.find_element(By.ID, "pt1:r1:0:pt1:tbl_reglementierte_berufe:dc_cl1j_id_10").click()
            time.sleep(3)

        driver.find_element(By.ID, f"pt1:r1:0:pt1:tbl_reglementierte_berufe:dc_cl1j_id_{j}").click()
        time.sleep(4)
        driver.find_element(By.ID, f"pt1:r1:0:pt1:tbl_reglementierte_berufe:j_id__ctru27pc2:{i}:cf9").click()
        time.sleep(5)
        data = {}
        try:
            data['title'] = driver.find_element_by_css_selector('h1').text
            data['info'] = driver.find_element(By.ID, 'b10-0_0_Content_1').text
            data['job_id'] = driver.current_url.split('=')[-1]
            jobs_collection.insert_one(data)
        except:
            continue
    page += 1    