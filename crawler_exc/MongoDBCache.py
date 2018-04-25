# encoding:utf-8
'''
@author:lk

@time:2018/4/12 

@desc:磁盘缓存

'''
import re
from datetime import timedelta, datetime
from urllib import parse

import os

import zlib

import pickle

from bson import Binary
from pymongo import MongoClient

from crawler_exc.chapter1 import link_crawler


class MongoDBCache:
    '''
    数据库mongodb缓存,用于存储html源代码
    https://github.com/mrvautin/adminMongo   可视化工具
            使用方法:

   1. Navigate to folder & install adminMongo: git clone https://github.com/mrvautin/adminMongo.git && cd adminMongo
    2.Install dependencies: npm install
    3.Start application: npm start or node app
    4.Visit http://127.0.0.1:1234 in your browser

    '''

    def __init__(self, cache_path='cache', max_length=255, expires=timedelta(days=5),client=None):
        self.cache_path = cache_path
        self.max_length = max_length
        self.expires = expires
        #mongodb默认的端口号27017
        if client is None:
            self.client = MongoClient('localhost', 27017)
        self.db = self.client.cache#cache是mongodb的数据库名称
        try:
            #webpage是数据库的表名称
            #mongodb设置expireAfterSeconds属性后表示期望多长时间后自动删除数据库数据,此处设置的5天
            # create_index创建一个名为timestamp的索引,根据此字段的索引值决定数据的更新时间
            self.db.webpage.create_index('timestamp',expireAfterSeconds=expires.total_seconds())
        except Exception as e:
            print(e,'-->请先尝试启动mongodb服务')

    def clear(self):
        self.db.webpage.drop()

    def urt_to_path(self, url):
        '''
        将url转换为合法的系统路径
        :param url:
        :return:
        '''
        # 将url链接分割成不同的几部分
        # 例如http://example.webscraping.com/places/default/view/Anguilla-8分割成:
        # scheme=http,netloc=example.webscraping.com,path=/places/default/view/Anguilla-8
        urlsplit = parse.urlsplit(url)
        path = urlsplit.path
        # 因为windows文件名不识别/结尾的名称,所以需要对这样的文件进行特殊处理
        # print('path=',url,path,urlsplit.netloc,urlsplit.netloc)
        if not path:
            path = urlsplit.netloc+'/index.html'
        elif path.endswith('/'):
            path += '/index.html'
        # 将scheme和netloc及path和query进行拼接
        if not urlsplit.netloc or not urlsplit.query:
            filename=path
        else:
            filename = urlsplit.netloc+ path + urlsplit.netloc
        print(filename)
        # filename文件名中只能包含数字,字母和基本符号,否则就用_替换掉
        filename = re.sub('[^/0-9a-zA-Z\-.,;_]', '_', filename)
        # 将filename以'/'分割后截取255个长度后的列表元素中间插入'/'
        filename = '/'.join(word[:255] for word in filename.split('/'))
        # 拼接成硬盘的绝对路径
        return os.path.join(self.cache_path, filename)

    def __getitem__(self, url):
        '''
        此方法在MongoDBCache属性值发生变化时自动调用
        将文件中的流读取出来并转化为python类型
        :param url: 地址
        :return:
        '''
        # print(url, '__getitem__')
        path = self.urt_to_path(url)
        #在webpage表中找到_id为path的行数据,如果存在就取出字典中为result的key值
        record = self.db.webpage.find_one({'_id': path})
        if record:
            return pickle.loads(zlib.decompress(record['result']))
        else:
            raise KeyError(url+' does not exist')

    def __setitem__(self, url, result):
        '''
        此方法在MongoDBCache属性值发生变化时自动调用
        将result写入文件中
        webpage表中存在三个字段名,_id表示url路径,result表示网页的源代码内容,timestamp表示时间戳
        :param url: 地址
        :param result: 需要写入的数据
        :return:
        '''
        # print(url, 'result')
        path = self.urt_to_path(url)
        timestamp=datetime.utcnow()
        # Binary二进制流对象
        record={'result':Binary(zlib.compress(pickle.dumps((result)))),'timestamp':timestamp}
        #更新或插入一条_id为path,result为result值,timestamp为timestamp值的数据
        self.db.webpage.update({'_id': path}, {'$set': record}, upsert=True)

if __name__ == '__main__':
    link_crawler('http://example.webscraping.com/', '/(index|view)', cache=MongoDBCache())
