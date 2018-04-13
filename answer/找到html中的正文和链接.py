# encoding:utf-8
__author__ = 'APLK'
'''
一个HTML文件，找出里面的正文。
一个HTML文件，找出里面的链接。
'''
from bs4 import BeautifulSoup
import urllib.request
import re
def findContent(url,tag,tag_content):
    read = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(read,"html.parser")
    find_all = soup.find_all(tag,tag_content)
    file = open('E:/python_demo/hello/answer/test/result.txt', 'ab+')
    for n in find_all:
        re_compile = re.compile(r'<[^>]+>')
        print(re_compile.sub('',str(n)))
        file.write(re_compile.sub('', str(n)).encode('utf-8'))
        file.write('\n'.encode())
    file.close()

def findLink(url,tag,tag_content):
     read = urllib.request.urlopen(url,timeout = 500).read()
     soup = BeautifulSoup(read,"html.parser")
     find_all = soup.find_all(href=re.compile(tag))
     f = open('E:/python_demo/hello/answer/test/result.txt', 'ab+')
     for n in find_all:
         f.write('\n'.encode())
         f.write(n[tag_content].encode('utf-8'))
         f.write('\n'.encode())
     f.close()

findContent('http://v2ex.com/t/157721#reply10', 'div', 'topic_content')
findLink('http://v2ex.com/t/157721#reply10', 'http', 'href')
findLink('http://v2ex.com/t/157721#reply10', 'http', 'href')