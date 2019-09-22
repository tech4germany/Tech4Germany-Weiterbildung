import requests
from bs4 import BeautifulSoup
import lxml
import re
import boto3
import json

# for pickle
import sys
sys.setrecursionlimit(50000)

last_layers = []
BUCKET_NAME = 't4g-2019-bmas-kursnet-data'

s3 = boto3.resource('s3')

def crawl(targets, parent=None):
    """Crawls and exports all courses under the given target from KursNet
    
    Arguments:
        targets {list<String>} -- KursNet sections
    
    Keyword Arguments:
        parent {[type]} -- [description] (default: {None})
    """
    url = 'https://kursnet-finden.arbeitsagentur.de/kurs/systematiksuche.do?sss='
    
    for item in targets:
        req = requests.get(url + item)
        soup = BeautifulSoup(req.content, 'lxml')
        
        table = soup.find('table', id='systematiksuche_tabelle')
        if not table.find('a', id=re.compile('syNr_[0-9]*')):
            export_courses([parent, item])
            
        else:
            for row in table.find_all('a', id=re.compile('syNr_[0-9]*')):
                crawl([row.text.replace(' ', '+')], parent=item)


def export_courses(layer):
    """Exports all courses under the given layer
    
    Arguments:
        layer {[type]} -- [description]
    """
    url = f'https://kursnet-finden.arbeitsagentur.de/kurs/kursDetail.do?seite=1&sn={layer[1]}&doNext=detail&anzahlSeite=5000000'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'lxml')
    for row in soup.find_all('a', title='Veranstaltungsdetail'):
        export_course([layer[0], layer[1], row['href'].split('vg_id=')[1].split('&anzahl')[0]])


def export_course(course):
    """Exports the given course
    
    Arguments:
        course {[type]} -- [description]
    """
    url = 'https://kursnet-finden.arbeitsagentur.de/kurs/veranstaltungsDetail.do?seite=1&anzahlSeite=5000000&doNext=vgdetail&vg_id='
        
    req = requests.get(url + course[-1])
    soup = BeautifulSoup(req.content, 'lxml')
    content = soup.find('div', id='inhalt')
    title = content.find('h2', id='Titel').text
    course_id = course[-1]
    parent_1 = course[-2]
    parent_2 = course[-3] if len(course) > 2 else ""

    data = {}
    data['meta'] = []

    data['meta'].append({
            'title': course_id,
            'parent_1': parent_1
        })

    s3.Object(BUCKET_NAME, f'data/{course_id}_data.txt').put(Body=json.dumps(data))
    

def main():
    targets = ['B', 'C', 'D']
    crawl(targets)

if __name__ == "__main__":
    main()
