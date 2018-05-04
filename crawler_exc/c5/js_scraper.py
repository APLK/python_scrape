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

import lxml

try:
    from PySide.QtGui import QApplication
    from PySide.QtCore import QUrl, QEventLoop, QTimer
    from PySide.QtWebKit import QWebView
except ImportError:
    from PyQt4.QtGui import QApplication
    from PyQt4.QtCore import QUrl, QEventLoop, QTimer
    from PyQt4.QtWebKit import QWebView

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
url = 'http://example.webscraping.com/places/default/search'
# url = 'http://example.webscraping.com/places/default/dynamic'
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

#初始化一个QApplication对象,
app = QApplication([])
#创建一个QWebView对象,用于web文档的容器
webview = QWebView()
# 创建一个QEventLoop对象,用于创建本地时间循环
loop = QEventLoop()
# loadFinished回调连接了QEventLoop的quit方法,可以在网页加载完成之后停止事件循环
webview.loadFinished.connect(loop.quit)
#将要加载的url传给QWebView,PyQt将该url的字符串封装在QUrl对象中
webview.load(QUrl(url))
# 等待网页加载完成,在事件循环启动时调用loop.exec_
loop.exec_()


# 网页加载完成后退出事件循环
# html = webview.page().mainFrame().toHtml()
# # 对加载的网页产生的HTMl进行数据抽取
# parser = etree.XMLParser(recover=True)
# tree = etree.fromstring(html,parser)
# print(tree.cssselect('#result')[0].text)


webview.show()
frame = webview.page().mainFrame()
#找到id为search_term的标签,设置搜索值为.号(表示搜索全部结果)
frame.findFirstElement('#search_term').setAttribute('value','.')
# option:checked 	选择每个被选中的 <option> 元素。此处表示找到id为page_size的标签下的option并选择值为1000
frame.findAllElements('#page_size option')[1].setPlainText('1000')
#找到id为search的第一个标签,设置模拟点击事件
frame.findFirstElement('#search').evaluateJavaScript('this.click()')
# app.exec_()

elements=None
while not elements:
    app.processEvents()
    elements = frame.findAllElements('#results a')
countries = [e.toPlainText().strip() for e in elements]
print(countries)
