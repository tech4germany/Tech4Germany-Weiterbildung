import requests
from bs4 import BeautifulSoup
import lxml
import re
from tqdm import tqdm as tqdm

# for pickle
import sys
sys.setrecursionlimit(50000)

last_layers = []

def crawl(targets, parent=None):
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
    url = f'https://kursnet-finden.arbeitsagentur.de/kurs/kursDetail.do?seite=1&sn={layer[1]}&doNext=detail&anzahlSeite=5000000'
    try:
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'lxml')
        for row in soup.find_all('a', title='Veranstaltungsdetail'):
            export_course([layer[0], layer[1], row['href'].split('vg_id=')[1].split('&anzahl')[0]])
    except:
        print(f'error at layer {layer}')


def export_course(course):
    url = 'https://kursnet-finden.arbeitsagentur.de/kurs/veranstaltungsDetail.do?seite=1&anzahlSeite=5000000&doNext=vgdetail&vg_id='
        
    try:
        req = requests.get(url + course[-1])
        soup = BeautifulSoup(req.content, 'lxml')
        content = soup.find('div', id='inhalt')
        title = content.find('h2', id='Titel').text
        course_id = course[-1]
        parent_1 = course[-2]
        parent_2 = course[-3] if len(course) > 2 else ""
        with open(f'./output/{course_id}_data.csv', 'w+') as outf:
            outf.write(f'{title}, {course_id}, {parent_1}, {parent_2}, {content}\n')
    
    except:
        print(f'error at course {course}')

def main():
    targets = ['B', 'C', 'D']
    crawl(targets)

if __name__ == "__main__":
    main()
