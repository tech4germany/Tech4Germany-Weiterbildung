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

def crawl(targets, data=None):
    """Crawls and exports all courses under the given target from KursNet
    
    Arguments:
        targets {list<String>} -- KursNet sections
        data - wannabe json object
    
    Keyword Arguments:
        parent {[type]} -- [description] (default: {None})
    """
    url = 'https://kursnet-finden.arbeitsagentur.de/kurs/systematiksuche.do?sss='
    
    for item in targets:
        req = requests.get(url + item)
        soup = BeautifulSoup(req.content, 'lxml')

        label = soup.find('table', id='systematiksuche_breadcrumb').find_all('tr')[-1].find_all('td')[-1].text.strip()

        if not data:
            data = {}
            data['parents'] = [{
                item: label
            }]
        else:
            data['parents'][0][item] = label
        
        table = soup.find('table', id='systematiksuche_tabelle')
        if not table.find('a', id=re.compile('syNr_[0-9]*')):
            get_courses_list(item, data)
        else:
            for row in table.find_all('a', id=re.compile('syNr_[0-9]*')):
                crawl([row.text.replace(' ', '+')], data)

        # move one layer up
        del data['parents'][0][item]


def get_courses_list(layer, data):
    """Exports all courses under the given layer
    
    Arguments:
        layer {[type]} -- [description]
    """
    layer_data = data
    course_data = data

    url = f'https://kursnet-finden.arbeitsagentur.de/kurs/kursDetail.do?seite=1&sn={layer}&doNext=detail&anzahlSeite=5000000'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'lxml')
    for row in soup.find_all('a', title='Veranstaltungsdetail'):
        course_data = data
        export_course(row['href'].split('vg_id=')[1].split('&anzahl')[0], course_data)
        course_data = None


def export_course(course, data):
    """Exports the given course
    
    Arguments:
        course {[type]} -- [description]
    """
    url = 'https://kursnet-finden.arbeitsagentur.de/kurs/veranstaltungsDetail.do?seite=1&anzahlSeite=5000000&doNext=vgdetail&vg_id='
        
    req = requests.get(url + course)
    soup = BeautifulSoup(req.content, 'lxml')
    content = soup.find('div', id='inhalt')
    title = content.find('h2', id='Titel').text

    print(course)

    # data = {}
    data['meta'] = []
    data['meta'].append({
            'id': course,
            'title': title
        })

    if any(content.find_all('a', href=re.compile('.*berufenet.arbeitsagentur.de/berufe.*'))):
        data['professions'] = []
        for job in content.find_all('a', href=re.compile('.*berufenet.arbeitsagentur.de/berufe.*')):
            data['professions'].append({
                'title': job.text.strip(),
                'website': job['href']
            })

    sections = ['Veranstaltungsinformationen', 'Veranstaltungsort', 'Kosten/Gebühren/Förderung', 'Dauer und Termine', 'Bildungsanbieter', 'Sonstiges', 'Zugang', 'Veröffentlichungsinformationen']
    for section in sections:
        if content.find('h1', text=section):
            data[section] = []
            div = content.find('h1', text=section).find_next_sibling('div', class_='section')#.find('table')
            if div.find('td', text='Es ist kein Veranstaltungsort zugewiesen'):
                data[section].append({
                    'meta': 'Es ist kein Veranstaltungsort zugewiesen'
                })
            else:
                for row in div.find_all('tr'):
                    if len(row.find_all('td')) == 2:
                        data[section].append({
                            row.find('td').text.strip(): row.find('td').find_next_sibling('td').text.strip()
                        })
                    # adresses (without label)
                    elif len(row.find_all('td')) == 1:
                        # special case 'Postfach' without id
                        if row.find('td', text=re.compile('Postfach.*')):
                            data[section].append({
                                'Postfach': row.find('td').text.strip()
                            })
                        else:
                            data[section].append({
                                row.find('td')['id']: row.find('td').text.strip()
                            })
                    # Veröffentlichungsinformationen
                    elif len(row.find_all('td')) == 3:
                        data[section].append({
                            'Aktualisiert': row.find_all('td')[0].text.split('am: ')[1],
                            'Bildungsanbieter-ID': row.find_all('td')[2].text.split('ID: ')[1]
                        })

    # inhalte
    if content.find('h1', text='Inhalte'):
        data['Inhalte'] = []
        div = content.find('h1', text='Inhalte').find_next_sibling('div', class_='section')
        data['Inhalte'].append({
            'text': div
        })
        for a in div.find_all('a', target='_blank'):
            data['Inhalte'].append({
                a.text.strip() : a['href']
            })
                    
    # rating - Anbieterbewertung
    # besser checken, if data vorhanden ist
    if content.find('h1', text='Anbieterbewertung'):
        data['Anbieterbewertung'] = []
        div = content.find('h1', text='Anbieterbewertung').find_next_sibling('div', class_='section')
        if len(div.find_all('td')) == 1:
            data['Anbieterbewertung'].append({
                'meta': 'Datenlage nicht ausreichend'
            })
        else:
            # check if 'integration in arbeit' exists
            if div.find('td', class_='int-in-arbeit hasdata'):
                score = div.find('td', class_='int-in-arbeit hasdata').find_next_sibling('td').find('div').text
                data['Anbieterbewertung'].append({
                    'Integration in Arbeit_score': score.split(' Punkte')[0].replace(',', '.'),
                    'Integration in Arbeit_n_votes': score.split('(')[1].split(' Teilnehmende')[0]
                })
            
            else:
                data['Anbieterbewertung'].append({
                    'Integration in Arbeit': 'Datenlage nicht ausreichend'
                })
                
            # check if 'Teilnehmerrückmeldungen' exists
            if div.find_all('tr')[2].find_all('span', text=re.compile('.*Sternewert.*')):
                score = div.find_all('tr')[2].find_all('td')[2].text
                data['Anbieterbewertung'].append({
                    'Teilnehmerrückmeldung_score': score.split('Es wurden ')[1].split(' Sterne von möglichen')[0].replace(',', '.'),
                    'Teilnehmerrückmeldung_teilnehmende': score.split('von')[2].split('Teilnehm')[0].strip(),
                    'Teilnehmerrückmeldung_rückmeldungen': score.split('(')[1].split(' Rückmeldungen')[0]
                })
                
                # check if details exist
                if div.find_all('div', class_='_sternedetails_'):
                    for row in div.find('div', class_='_sternedetails_').find_all('tr', class_='popupbottomborder __item_')[1:]:
                        data['Anbieterbewertung'].append({
                           f"sternedetails_{row.find('td', class_='__frage_').text}": row.find('td', class_='__bewertung_').text.split('Sternewert')[1].split('von')[0].strip().replace(',', '.') 
                        })
            else:
                data['Anbieterbewertung'].append({
                    'Teilnehmerrückmeldungen': 'Datenlage nicht ausreichend'
                })


    #print(data)

    s3.Object(BUCKET_NAME, f'data/{course_id}_data.txt').put(Body=json.dumps(data))
    

def main():

    targets = ['B', 'C', 'D']
    crawl(targets)

if __name__ == "__main__":
    main()
