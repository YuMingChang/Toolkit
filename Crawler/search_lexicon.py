import re
import requests
from bs4 import BeautifulSoup

print('Search the word from YAHOO Dictionary')
while(True):
    w = input()
    if w == 'q':
        break

    req = requests.get('https://tw.dictionary.search.yahoo.com/search', params={'p': w})
    soup = BeautifulSoup(req.text, 'html.parser')
    flag = soup.find(class_=' w-100p fz-16 va-mid ta-c')
    print('You are searching the URL is: {}'.format(req.url))
    if flag:
        print(flag.text)
        continue

    print(' '.join(s.text for s in soup.findAll('li', class_=re.compile('^d-ib mr-10 va-top'))))
    for tran in soup.findAll('li', class_=re.compile('^lh-22 mh-22 mt-12 mb-12 mr-25')):
        print(tran.text)


    sents = soup.findAll('li', class_=re.compile('^lh-22 mh-22 ml-50 mt-12 mb-12'))
    if sents:
        print('\n釋義：')
        for sent in sents:
            print(sent.text)

    print('- ' * 45)
