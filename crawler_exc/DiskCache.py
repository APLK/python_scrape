# encoding:utf-8
'''
@author:lk

@time:2018/4/12 

@desc:磁盘缓存

'''
import re
from urllib import parse

import os

import pickle

import zlib

from crawler_exc.chapter1 import link_crawler


class DiskCache:
    '''
    磁盘缓存,用于存储html源代码
    '''
    def __init__(self,cache_path='cache',max_length=255):
        self.cache_path=cache_path
        self.max_length=max_length

    def urt_to_path(self,url):
        '''
        将url转换为合法的系统路径
        :param url:
        :return:
        '''
        #将url链接分割成不同的几部分
        #例如http://example.webscraping.com/places/default/view/Anguilla-8分割成:
        #scheme=http,netloc=example.webscraping.com,path=/places/default/view/Anguilla-8
        urlsplit = parse.urlsplit(url)
        path = urlsplit.path
        #因为windows文件名不识别/结尾的名称,所以需要对这样的文件进行特殊处理
        if not path:
            path+='/index.html'
        elif path.endswith('/'):
            path+='/index.html'
        #将scheme和netloc及path和query进行拼接
        filename=urlsplit.scheme+urlsplit.netloc+path+urlsplit.query
        #filename文件名中只能包含数字,字母和基本符号,否则就用_替换掉
        filename = re.sub('[^/0-9a-zA-Z\-.,;_]', '_', filename)
        #将filename以'/'分割后截取255个长度后的列表元素中间插入'/'
        filename='/'.join(word[:255] for word in filename.split('/'))
        #拼接成硬盘的绝对路径
        return os.path.join(self.cache_path,filename)

    def __getitem__(self, url):
        '''
        此方法在diskcache属性值发生变化时自动调用
        将文件中的流读取出来并转化为python类型
        :param url: 地址
        :return:
        '''
        print(url,'__getitem__')
        path = self.urt_to_path(url)
        if os.path.exists(path):
            with os.open(path,'rb') as fp:
                #将文件流反序列化为python对象,并解压序列化
               return pickle.loads(zlib.decompress(fp.read()))
        else:
            raise KeyError(url+' does not exist')
    def __setitem__(self, url,result):
        '''
        此方法在diskcache属性值发生变化时自动调用
        将result写入文件中
        :param url: 地址
        :param result: 需要写入的数据
        :return:
        '''
        print(url,'result')
        path=self.urt_to_path(url)
        if not os.path.exists(os.path.dirname(path)):#如果文件不存在就创建
            os.makedirs(os.path.dirname(path))
        with open(path,'wb') as fp:
            #将数据序列化压缩为流文件
            fp.write(zlib.compress(pickle.dumps(result)))

        # if not path:
if __name__ == '__main__':
    link_crawler('http://example.webscraping.com/', '/(index|view)', cache=DiskCache())