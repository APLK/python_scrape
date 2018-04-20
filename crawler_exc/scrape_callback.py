# encoding:utf-8
'''
@author:lk

@time:2018/4/11 

@desc:

'''
import csv
import re

from crawler_exc.chapter1 import link_crawler
from crawler_exc.chapter2 import lxml_scraper, FIELDS


class ScrapeCallback:
    '''
    实例化ScrapeCallback对象,此类用于将网页数据保存在指定的excel文件中
    '''
    def __init__(self):
        #需要加上newline,否则excel表格每次写入一行都会插入一行空行
        self.openCS = open('countries.csv', 'w', newline='')
        self.writer=csv.writer(self.openCS)
        self.field=FIELDS
        self.writer.writerow(self.field)
    def __call__(self, url, html):
        '''
        包含/view/的链接地址就爬取该地址的网页数据然后写入excel表格中
        :param url: 该网页的地址
        :param html: 该网页的源代码
        :return:
        '''
        if re.search('/view/',url):
            result = lxml_scraper(html)
            if result:
                self.writer.writerow(result.values())

    # def closeFile(self):
    #     '''
    #     close stream
    #     :return:
    #     '''
    #     self.openCS.close()
if __name__ == '__main__':
    link_crawler('http://example.webscraping.com', '/(index|view)', delay=5, retries=2, max_depth=1, user_agent='GoodCrawler',scrape_callback=ScrapeCallback())

