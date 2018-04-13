# encoding:utf-8
'''
@author:lk

@time:2018/4/8 

@desc:

'''
import queue
import re
import urllib.request, urllib.parse, urllib.robotparser

import itertools

import time

from datetime import datetime

from bs4 import BeautifulSoup
from flask import json

from crawler_exc.down_loader import DownLoader


def downloadHtml(url, headers=None, proxy=None, num_retries=2):
    '''
    解析该网址的源代码
    :param url: 网址
    :param proxy: ip代理
    :param user_agent: 用户代理
    :param retries: 请求失败的最大次数
    :return: 返回网页源代码
    '''
    print('start scrape:%s     ...' % url)
    # 设置urllib.request的代理
    # request = urllib.request.Request(url, headers)
    build_opener = urllib.request.build_opener()
    if proxy:  # 使用代理
        proxy_handler = urllib.request.ProxyHandler(proxies=proxy)
        build_opener.add_handler(proxy_handler)
        urllib.request.install_opener(build_opener)
    try:
        html = build_opener.open(url,
                                 data=bytes(json.dumps(headers).encode(encoding='UTF-8'))).read()
    except urllib.request.URLError as e:
        print('error:', e.reason)
        html = ''
        if hasattr(e, 'code'):
            code = e.code
            if num_retries > 0 and 500 <= code <= 600:
                # 如果服务器端错误,并且未超过重试的次数,则递归调用
                downloadHtml(url, headers, proxy, num_retries - 1)
    return html


def parseHtml(prefix, url, link_regex=None):
    '''
    解析html源代码中
    :param prefix: 前缀
    :param url: 地址
    :param link_regex:匹配规则
    :return:
    '''
    html = downloadHtml(url)
    links = BeautifulSoup(html, 'html.parser')
    # http://example.webscraping.com/places/default/view/Albania-3
    for link in links.find_all(href=re.compile(link_regex)):
        downloadHtml(prefix + link['href'])  # 查a标签的href值


def autoDownCount(prefix):
    '''
    根据页码索引递增爬取
    :param prefix: 前缀
    :return:
    '''
    max_error = 5
    min_error = 1
    for page in itertools.count(1):
        html = downloadHtml(prefix % page)
        if html is None:
            min_error += 1
            if min_error >= max_error:
                break
        else:
            min_error = 0


def get_links(html):
    re_compile = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return re_compile.findall(html)


def link_crawler(seed_url, link_regex=None, proxy=None, user_agent='wswp1', retries=2, headers=None,
                 max_depth=2, max_urls=-1, delay=5, scrape_callback=None,cache=None):
    '''
    爬虫入口.
    :param seed_url: 需要爬虫的入口链接
    :param link_regex: 超链接的匹配规则
    :param proxy: ip代理
    :param user_agent: 用户代理
    :param retries: 访问失败后的重连最大次数
    :param headers:头部参数
    :param max_depth: 爬虫的最大页面深度
    :param max_urls: 最大的链接下载数
    :param delay: 限制访问的时间间隔
    :param scrape_callback: 数据写入excel回调类
    :return:
    '''
    parser = get_robot(seed_url)
    crawler_list = queue.deque([seed_url])
    num_urls = 0
    seen = {seed_url: 0}
    loader = DownLoader(proxy,headers, user_agent, retries, delay, cache)
    # print(crawler_list)
    while crawler_list:
        url = crawler_list.pop()
        # 该user_agent是否支持爬虫
        # print(url,parser.can_fetch(user_agent, send_url))
        if parser.can_fetch(user_agent, seed_url):
            html = loader(url)
            # print('html0='+html.decode('utf-8'))
            depth = seen[url]
            links = []
            # 如果需要抓取html标签中的数据,调用lxml获取对应的属性值,并存储在excel表格中
            if scrape_callback:
                scrape_callback(url, html)  # 实例化对象scrape_callback会自动调用类中的__call__方法
            # 没超过最大页面深度
            if depth != max_depth:
                # 超链接的匹配规则并且html存在时
                if link_regex and html:
                    links.extend(link for link in get_links(html.decode('utf-8')) if
                                 re.search(link_regex, link))
                for link in links:
                    urljoin = normalize(link, seed_url)
                    print(urljoin)
                    if urljoin not in seen:
                        seen[urljoin] = depth + 1
                        if same_domain(seed_url, urljoin):
                            crawler_list.append(urljoin)
            num_urls += 1
            if num_urls == max_urls:
                scrape_callback.closeFile()
                break
        else:
            print('bad agent:', user_agent)
            scrape_callback.closeFile()
            break


def same_domain(url1, url2):
    '''
    比对host地址是否一致
    :param url1:
    :param url2:
    :return: True则一致
    '''
    return urllib.parse.urlparse(url1).netloc == urllib.parse.urlparse(url2).netloc


def normalize(link, send_url):
    '''
    以#分割url然后取前面的与send_url进行拼接
    :param link:
    :param link_regex:
    :param send_url:
    :return: 拼接好的url
    '''
    urldefrag, _ = urllib.parse.urldefrag(link)
    urljoin = urllib.parse.urljoin(send_url, urldefrag)
    return urljoin


def get_robot(url):
    '''
    构造一个parser对象,用于判断user_agent是否能够正常访问
    :param url: 地址
    :return:
    '''
    parser = urllib.robotparser.RobotFileParser()
    parser.set_url(urllib.parse.urljoin(url, '/robots.txt'))
    parser.read()
    return parser


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

# autoDownCount('http://example.webscraping.com/places/default/view/-%d')
# link_crawler('http://example.webscraping.com', '/(index|view)', 'GoodCrawler', max_depth=1)
# link_crawler('http://example.webscraping.com', '/(index|view)', delay=2, retries=1, user_agent='BadCrawler')
