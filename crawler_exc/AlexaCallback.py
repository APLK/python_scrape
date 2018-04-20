# encoding:utf-8
'''
@author:lk

@time:2018/4/18 

@desc:

'''
import csv
from io import BytesIO, StringIO
from urllib import parse
from zipfile import ZipFile

from crawler_exc.MongoDBCache import MongoDBCache
from crawler_exc.chapter1 import  crawler


class AlexaCallback:
    '''
    解压zip类,用于解压文件,并读取文件中max_urls条的数据
    '''
    def __init__(self,seed_url,max_urls):
        self.seed_url=seed_url
        self.max_urls=max_urls
    def __call__(self, url, html):
        '''
        :param url: url地址
        :param html:
        :return:
        '''
        if url == self.seed_url and html:
            urls = []
            cache = MongoDBCache()
            with ZipFile(BytesIO(html)) as zf:
                csv_filename = zf.namelist()[0]
                with open(csv_filename, "r", encoding="utf-8") as csvfile:
                    reader = csv.reader(csvfile)
                    for _,url in reader:
                        #在数据库中查找该url是否存在,不存在就添加urls中
                        if not cache.db.webpage.find_one({'_id': 'http://' + url}):
                            urls.append('http://' + url)
                        if len(urls) == self.max_urls:
                            break
            return urls
scrape_callback = AlexaCallback('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip',1000)
cache = MongoDBCache()
crawler(scrape_callback.seed_url, scrape_callback=scrape_callback, cache=cache)

# url='http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
# urlsplit = parse.urlsplit(url)
# path = urlsplit.path
# # 因为windows文件名不识别/结尾的名称,所以需要对这样的文件进行特殊处理
# print('path',path,urlsplit.netloc,urlsplit.netloc)