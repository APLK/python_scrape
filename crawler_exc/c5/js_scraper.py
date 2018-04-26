# encoding:utf-8
'''
@author:lk

@time:2018/4/26 

@desc:

'''
import json
import re
from urllib.request import Request, urlopen

import requests
from lxml import etree


from crawler_exc.down_loader import DownLoader
# def get_results(search,headers=None):
#     url = 'https://api.github.com/search/repositories?q={search}&page=4&per_page=100&sort=stars&order=desc'.format(search=search)
#     req = Request(url)
#     response = urlopen(req).read()
#     result = json.loads(response.decode())
#     return result

loader = DownLoader()
url = 'https://api.github.com/search/repositories?q={search}&page=4&per_page=100&sort=stars&order=desc'.format(search='a')
html = loader(url)
print(html)
print(json.loads(html))
parser = etree.XMLParser(recover=True)
tree = etree.fromstring(html,parser)
print(tree.cssselect('div#results a'))
