import requests
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import csv

url = 'https://wiki.52poke.com/zh-hant/%E5%AE%9D%E5%8F%AF%E6%A2%A6%E5%88%97%E8%A1%A8%EF%BC%88%E6%8C%89%E5%85%A8%E5%9B%BD%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%EF%BC%89'
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')

villages = [
    'roundy eplist s-关都',
    'roundy eplist s-城都',
    'roundy eplist s-豐緣',
    'roundy eplist s-神奧',
    'roundy eplist s-合眾',
    'roundy eplist s-卡洛斯',
    'roundy eplist s-阿羅拉',
]
s = '1221231'

f = open('poke.txt', 'w', encoding = 'utf8')

for n, village in enumerate(villages):
    table = soup.find('table', village)
    for tr in table.find_all('tr'):
        td = tr.find_all('td')
        if len(td) > 6:
            f.write("{} {}{}".format(td[int(s[n])].text, td[int(s[n])+2].text, td[int(s[n])+4].text).replace('\n', ''))
            f.write("\n")
f.close()
