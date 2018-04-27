# encoding:utf-8
'''
@author:lk

@time:2018/4/26 

@desc:

'''
import csv
import json
import re
import string
from urllib.request import Request, urlopen

try:
    from PySide.QtGui import *
    from PySide.QtCore import *
    from PySide.QtWebKit import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
    from PyQt4.QtWebKit import *

import requests
import time
from lxml import etree


from crawler_exc.down_loader import DownLoader

FIELDS={'id','pretty_link','country',}
def get_results(url,search='',page=0,pageSize=10,headers=None):
    '''
    根据搜索的关键字loader网页
    :param search:
    :param headers:
    :return:
    '''
    # url = 'https://api.github.com/search/repositories?q={search}&page=4&per_page=100&sort=stars&order=desc'.format(search=search)

    loader = DownLoader(headers=headers)
    html = loader(url)
    return html
def get_all_results(headers=None):
    countries=set()
    for search in string.ascii_lowercase:
        page=0
        while True:
            time.sleep(1)
            html = get_results(search, page,pageSize=10,headers=headers)
            try:
                ajax=json.loads(html)
            except ValueError as e:
                print('ValueError',e)
                ajax=None
            else:
                for record in ajax['records']:
                    countries.add(record['country'])
            page+=1
            if ajax is None or page>=ajax['num_pages']:
                break
    open('countries.txt','w').write('\n'.join(sorted(countries)))
def write_csv(headers=None):
    html = get_results('.', page=0,pageSize=1000,headers=headers)
    try:
        ajax=json.loads(html)
    except ValueError as e:
        print('ValueError',e)
        ajax=None
    writer = csv.writer(open('countries_c5.csv', 'w',newline=''))
    writer.writerow(FIELDS)
    for record in ajax['records']:
        writer.writerow([record[field] for field in FIELDS] )

# url = 'http://example.webscraping.com/places/ajax/search.json?&search_term={search}&page_size={pageSize}&page={page}'.format(search=search,pageSize=pageSize,page=page)
url = 'http://example.webscraping.com/places/default/dynamic'
user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
# 在headers中设置agent
headers = [("User-Agent", user_agent)]
# print(write_csv(headers=headers))
# print(get_all_results(headers=headers))
# print(get_results('a',headers=headers))
# print(json.loads(html))
# parser = etree.XMLParser(recover=True)
# tree = etree.fromstring(html,parser)
# print(tree.cssselect('div#results a'))

# html = get_results(url, headers=headers)
# parser = etree.XMLParser(recover=True)
# tree = etree.fromstring(html,parser)
# print(tree.cssselect('#result')[0].text)

app = QApplication([])

