import requests
from bs4 import BeautifulSoup
import re
import urllib3
urllib3.disable_warnings()

url = 'https://www.latebird.co/thsr_tickets/search?utf8=✓&thsr_ticket[from_id]={from_id}&thsr_ticket[to_id]={to_id}&thsr_ticket[depart_date]={date}&commit=搜尋'
station_id = [
    ('12', '南港'), ('8', '台北'), ('7', '板橋'),
    ('6', '桃園'), ('5', '新竹'), ('9', '苗栗'),
    ('4', '台中'), ('10', '彰化'), ('11', '雲林'),
    ('3', '嘉義'), ('2', '台南'), ('1', '左營')
]

print('站名與編號：')
for k, v in station_id:
    print('{} : {}'.format(v, k))
from_id = input('起站：')
to_id = input('訖站：')
date = input('乘坐日期2018')
#from_id, to_id, date = 1, 8, '0329'

official_url = 'https://www.latebird.co'
print('URL = {}'.format(url.format(from_id=from_id, to_id=to_id, date='2018'+date)))

req = requests.get(url.format(from_id=from_id, to_id=to_id, date='2018'+date), verify=False)
soup = BeautifulSoup(req.text, 'lxml')

table = soup.find('table', class_='table table-middle-valign')
trs = table.findAll('tr')
if trs:
    l_nums = list()
    print( '- '* 12 + trs[0].text.strip() + ' -' * 12)
    for i in range(2, len(trs)):
        tds = trs[i].findAll('td')
        l_nums.append((tds[0].text.strip(), tds[8].find('a')['href']))
        print('No.{: <2d} 班次{:4s} / {} / {} 剩餘{}張 / ${}'.format(
            i-2,
            tds[0].text.strip().replace('★', ''),
            tds[1].text.strip(),
            tds[2].text.strip(),
            tds[3].text.strip(),
            tds[5].text.strip()
            )
        )
    print('- ' * 32)

    while(True):
        no = input('查詢No.：')
        try:
            no = int(no)
        except ValueError:
            break
        if no < len(l_nums):
            print('您查詢 ({}, {}) 的備註：'.format(l_nums[no][0], official_url + l_nums[no][1]))
            notes = BeautifulSoup(requests.get(official_url + l_nums[no][1], verify=False).text, 'lxml').find('div', class_='col-xs-12 push-xs').text
            print(re.sub(r'\s+備註\s+', '', notes).strip()) 
        else:
            print('No.{} 不在選項內'.format(no))
        print('- ' * 32)
else:
    print('Oops! 沒有您搜尋的班次資訊')

"""
No.0 班次
No.1 起站/迄站
No.2 出發/抵達
No.3 數量
No.4 原票價
No.5 售價
No.6 票種
No.7 取票方式
No.8
"""
