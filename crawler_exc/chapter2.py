# encoding:utf-8
'''
@author:lk

@time:2018/4/10 

@desc:正则表达式性能快,使用困难;bs性能慢使用简单;lxml性能快使用简单
如果是下载网页不抽取数据的话建议使用bs;如果只抓取数据,又想避免额外依赖的话
使用正则;lxml是数据抓取的最好选择

'''
import csv
import re

import time
from bs4 import BeautifulSoup
from lxml import etree

from crawler_exc.chapter1 import downloadHtml

FIELDS={'area','population','iso','country',
         'capital','continent','tld','currency_code',
        'currency_name','phone','postal_code_format','postal_code_regex',
        'languages','neighbours'}

def bf_get_square (url):
    '''
    BeautifulSoup获取网页源代码中指定的id和class的text值
    :param url: 地址
    :return:
    '''
    html = downloadHtml(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser').prettify()
        tr = soup.find(attrs={'id': 'places_area__row'})
        print(tr.find(attrs={'class': 'w2p_fw'}).text)

def lxml_square(url):
    '''
    etree获取网页源代码中指定的id和class的text值
    :param url: 地址
    :return:
    '''
    html = downloadHtml(url)
    if html:
        #尽力解析破损的XML
        parser = etree.XMLParser(recover=True)
        tree  = etree.fromstring(html,parser)
        print(tree.cssselect('tr#places_area__row>td.w2p_fw')[0].text)

def re_scraper(html):
    '''
    使用python源生的re表达式匹配td的text内容
    :param html:
    :return:
    '''
    result={}
    for regex in FIELDS:
        result[regex]=re.search(r'<tr id="places_%s__row">.*?<td class="w2p_fw">(.*?)</td>'%regex,html.decode('utf-8')).groups()[0]
    return result

def bs_scraper(html):
    '''
    使用beautifulSoup库匹配td的text内容
    :param html:
    :return:
    '''
    result={}
    soup = BeautifulSoup(html, 'html.parser')
    for regex in FIELDS:
        result[regex]=soup.find('table').find('tr',id='places_%s__row'%regex).find('td',class_='w2p_fw').text
    return result
def lxml_scraper(html):
    '''
    使用lxml.tree库匹配td的text内容
    :param html:
    :return:
    '''
    result={}
    # print('lxml_scraper=',html)
    #尽力解析破损的XML
    if html:
        parser = etree.XMLParser(recover=True)
        tree = etree.fromstring(html,parser)
        # tree=etree.HTML(html,parser)
        for regex in FIELDS:
            #选择父元素为 <table> 元素的所有 id为places_%s__row的<tr> 元素下class为w2p_fw的td标签。
            if tree.cssselect('table>tr#places_%s__row>td.w2p_fw'%regex):
                result[regex]=tree.cssselect('table>tr#places_%s__row>td.w2p_fw'%regex)[0].text
    return result
def scraper_compare(url,test_scraper_count=1000):
    '''
    三种爬虫效率比较
    :param url:
    :param test_scraper_count: 测试爬虫的次数
    :return:
    '''
    html = downloadHtml(url)
    for name,scraper in [('regular',re_scraper),('bs',bs_scraper),('lxml',lxml_scraper)]:
        startTime=time.time()
        for i in range(test_scraper_count):
            #因为regular表达式模块会缓存搜索的结果,为了与其他爬虫的对比公平,需要清除缓存
            if scraper==re_scraper:
                re.purge()
            result = scraper(html)
            assert(result['area']=='199 square kilometres')
        endTime = time.time()
        print('%s,%.2f'%(name,endTime-startTime))

class ScrapeCallback:
    def __init__(self):
        self.writer=csv.writer(open('countries.csv','w'))
        self.field=FIELDS
        self.writer.writerow(self.field)
    def __call__(self, url, html):
        if re.search('/view/',url):
            result = lxml_scraper(html)
            self.writer.writerow(value for name,value in result)


# bf_get_square ('http://example.webscraping.com/places/default/view/American-Samoa-5')
# lxml_square ('http://example.webscraping.com/places/default/view/American-Samoa-5')
# scraper_compare ('http://example.webscraping.com/places/default/view/American-Samoa-5')