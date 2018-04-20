# encoding:utf-8
'''
@author:lk

@time:2018/4/12 

@desc:

'''
import random
import socket
import urllib
from datetime import datetime
import urllib.request
import time

import os

from crawler_exc.TqdmUpToProgress import TqdmUpToProgress

DEFAULT_TIMEOUT = 60000*5
class DownLoader:
    '''
    爬虫下载器类
    用于限速爬取网页并存储爬取过的缓存网页
    '''
    def __init__(self,proxy=None,headers=None, user_agent='wswp1', retries=2, delay=5,cache=None, timeout=DEFAULT_TIMEOUT):
        '''
        初始化:param seed_url: 需要爬虫的入口链接
        :param proxy: ip代理
        :param user_agent: 用户代理
        :param retries: 访问失败后的重连最大次数
        :param delay: 限制访问的时间间隔
        :param cache: 缓存
        '''
        socket.setdefaulttimeout(timeout)
        self.proxy=proxy
        self.user_agent=user_agent
        self.retries=retries
        self.headers=headers
        self.delay=delay
        self.cache=cache
        self.speedLimit=SpeedLimit(delay)

    def __call__(self, url):
        result=None
        if self.cache:#存在缓存时
            try:
                result = self.cache[url]
            except KeyError:
                pass
            else:
                pass
                #if self.retries>0 and 500<=result['code']<600:
                #    result=None
        if result is None:#没有缓存就需要去调用download爬取
            self.speedLimit.wait(url)
            #随机从代理池中取出一个代理ip进行爬取
            proxyIP = random.chocie(self.proxy) if self.proxy else None
            # with TqdmUpToProgress(unit='B', unit_scale=True, miniters=1,
            #                       desc=self.seed_url.split('/')[-1]) as zf:  # desc取最后一个元素作为文件名
            #     urllib.request.urlretrieve(self.seed_url, filename=self.seed_url.split('/')[-1],
            #                                reporthook=zf.update_to, data=None)
            result=self.download(url,proxyIP,self.headers,self.retries)
            # print('result=',dict(result))
            if self.cache:#如果需要缓存则存储该缓存url信息
                self.cache[url]=result
        return result['html']

    def downloadZIPTOLocal(self,  url):
        '''
        带下载进度条的远程数据下载到本地
        :param url:
        :return:
        '''
        desc=url.split('/')[-1]
        if not desc or not os.path.isfile(desc):
            with TqdmUpToProgress(unit='B', unit_scale=True, miniters=1,
                  desc=desc) as t:  # desc取最后一个元素作为文件名
                #urlretrieve函数是将远程数据直接保存到本地,open函数表示远程url的类文件对象，
                # 然后像本地文件一样操作这个类文件对象来获取远程数据
                urllib.request.urlretrieve(url, filename=desc,
                                   reporthook=t.update_to, data=None)

    def download(self,  url, proxyIP, headers, retries):
        '''
        下载网页源代码
        :param url: 网页地址
        :param proxyIP: 代理ip
        :param headers: 头部信息
        :param retries: 重复爬取数
        :return:
        '''
        build_opener = urllib.request.build_opener()
        if proxyIP:  # 使用代理
            proxy_handler = urllib.request.ProxyHandler(proxies=proxyIP)
            build_opener.add_handler(proxy_handler)
            urllib.request.install_opener(build_opener)
        try:
            if headers:
                build_opener.addheaders(headers)
            opener_open = build_opener.open(url)
            html = opener_open.read()
            code = opener_open.code
        except urllib.request.URLError as e:
            print('error_:', e.reason)
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if retries > 0 and 500 <= code <= 600:
                    # 如果服务器端错误,并且未超过重试的次数,则递归调用
                    return self.download(url, headers, proxyIP, retries - 1)
            else:
                code=None
        except socket.timeout as e:#爬虫超时会造成假死状态,所以这里需要捕捉异常
            print(type(e))
            html = ''
            code=None
            if retries > 0:
                # 如果服务器端错误,并且未超过重试的次数,则递归调用
                return self.download(url, headers, proxyIP, retries - 1)
        return {'html':html,'code':code}

class SpeedLimit:
    '''
    限制爬虫频繁访问网址
    '''

    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        '''
        休眠
        :param url:
        :return:
        '''
        # netloc取的是网络的host and port地址
        domain = urllib.request.urlparse(url).netloc
        last_seen = self.domains.get(domain)
        # print('domain=',domain,last_seen)
        # 如果距离上次访问的时间间隔小于delay就休眠距离上次的时间然后才继续
        if self.delay > 0 and last_seen is not None:
            dt = self.delay - (datetime.now().second - last_seen.second)
            print('dt=', dt)
            if dt > 0:
                time.sleep(dt)
        self.domains[domain] = datetime.now()

# eg_link='http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
# loader = DownLoader()
# print(loader(eg_link))
