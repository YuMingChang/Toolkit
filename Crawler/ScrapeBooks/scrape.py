# -*- coding: utf8 -*-
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

HTML_PARSER = 'html.parser'
ROOT_URL = 'http://www.books.com.tw/'
RANK_URL = 'http://www.books.com.tw/web/sys_saletopb/books/19?attribute=30'
RANK_BEGIN, RANK_LIMIT = 0, 100
RE = re.compile('已追蹤作者|  ')
LIST_EN = ['author', 'publisher', 'pulication_date',
           'language', 'price', 'discount', 'deadline', 'content']
LIST_ZHTW = ['作者', '出版社', '出版日期', '語言', '定價', '優惠價', '優惠期限', '內容大綱']
SAVE_CONTENT = True


def get_books_link():
    rank_req = requests.get(RANK_URL)
    if rank_req.status_code == requests.codes.ok:
        soup = BeautifulSoup(rank_req.content, HTML_PARSER)
        rankshop_link = []
        for link in soup.find_all('li', {'class': 'item'}):
            rankshop_link.append(link.a['href'])
        parse_book(rankshop_link[RANK_BEGIN:RANK_LIMIT])


def parse_book(rankshop_link):
    dt = datetime.today()
    filename = 'TopBook{y}{m:02d}.md'.format(y=dt.year, m=dt.month)
    f = open(filename, 'w', encoding='utf-8')

    if not SAVE_CONTENT:
        del LIST_EN[-1]
        del LIST_ZHTW[-1]

    for number, link in enumerate(rankshop_link, 1):
        req = requests.get(link)
        if req.status_code == requests.codes.ok:
            book_dict = {}
            soup = BeautifulSoup(req.content, HTML_PARSER)

            def SaveValues(eleTags, isTitleImg):
                if isTitleImg:
                    book_dict['title'] = eleTags.find('h1', {'itemprop': 'name'}).text
                    book_dict['image'] = eleTags.find('img', {'class': 'cover M201106_0_getTakelook_P00a400020052_image_wrap'})['src']
                else:
                    for tag in eleTags.find('ul').find_all('li'):
                        for item in LIST_ZHTW:
                            index = LIST_ZHTW.index(item)
                            text = tag.text
                            if re.search(item, text):
                                try:
                                    text = RE.sub('', text)
                                    text_begin = text.find(LIST_ZHTW[index])
                                    text_end = text.find('\n', text.find(LIST_ZHTW[index]))
                                    book_dict[LIST_EN[index]] = text[
                                        text_begin: text_end if text_end != -1 else None]
                                except:
                                    pass
                            elif LIST_EN[index] == 'content' and SAVE_CONTENT:
                                book_dict[LIST_EN[index]] = soup.find('div', {'class': 'bd'}).text.lstrip()
            # print (book_dict)
            SaveValues(soup.find('div', {'class': 'mod type02_p01_wrap clearfix'}), True)
            SaveValues(soup.find('div', {'class': 'type02_p003 clearfix'}), False)
            SaveValues(soup.find('div', {'class': 'cnt_prod002 clearfix'}), False)
            write_md(f, book_dict, number)

    f.close()
    print('\a')     # Notice Program End.


def write_md(f, book_dict, number):
    try:
        f.write('##No.{no} {title}\n'.format(no=number, title=book_dict['title']))
        f.write('![img]({img})\n\n'.format(img=book_dict['image']))
        for index, item in enumerate(LIST_EN):
            if item in book_dict:
                if LIST_EN[index] == 'content' and SAVE_CONTENT:
                    f.write('\t* {item}：\n\t\t'.format(item=LIST_ZHTW[index]))
                    f.write(book_dict[LIST_EN[index]].replace('\u3000\u3000', '\t\t'))
                else:
                    f.write('\t* {item}\n'.format(item=book_dict[LIST_EN[index]]))
            else:
                print ("No.{no} {title}'s {item} is None.".format(
                    no=number, title=book_dict['title'], item=item))
    except:
        pass


if __name__ == '__main__':
    get_books_link()
