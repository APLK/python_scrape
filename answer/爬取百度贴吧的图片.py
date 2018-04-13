#encoding:utf-8
import urllib.request
import os,time
from threading import Thread
from queue import Queue
from urllib import parse

from bs4 import BeautifulSoup
# https://tieba.baidu.com/p/4752780593

def mkdir(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        print(path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path+' 目录已存在')
        return False

def Schedule(a,b,c):
    '''''
    07
    a:已经下载的数据块
    08
    b:数据块的大小
    09
    c:远程文件的大小
    10
    '''
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    print('%.2f%%' % per)
class DownLoadImg(Thread):
    def __init__(self,que):
        Thread.__init__(self)
        self.que=que
    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            item = self.que.get()
            if item is None:
                break
            directory, link = item
            urllib.request.urlretrieve(link,directory,None)
            # urllib.request.urlretrieve(link,directory,Schedule)
            # time.sleep(3)#防止爬虫被远程关闭,反爬虫
            self.que.task_done()




def getAllImage(url,tag1,tag_content):
    headers = {
                 'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
                                   'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
             'Connection': 'keep-alive'}
    urlopen = urllib.request.Request(url,headers = headers)
    try:
        page = urllib.request.urlopen(urlopen).read()
        page = page.decode('utf-8')
    except os.error.HTTPError as e:
        print(e.code())
        print(e.read().decode('utf-8'))
    # read = urlopen.read()
    # print(read)
    soup = BeautifulSoup(page,"html.parser")
    print(soup)
    find_all = soup.find_all(attrs={'pic_id':tag1})
    print(find_all)
    # 定义要创建的目录
    mkpath="E:/python_demo/hello/answer/test/img1"
    # 调用函数
    mkdir(mkpath)
    queue = Queue()

    # Create 8 worker threads
    for x in find_all:
        src=x['src'].replace('!thumb','')
        print(src)
        join = os.path.join(mkpath, src.split('/')[-1])
        if join.split('.')[-1]=='!thumb':
            break
        else:
            join=join+'.png'
            # httpStr='https:'
        # print(httpStr+x['src'])
        queue.put((join, src))
        # queue.put((join, httpStr+x['src']))
    # Causes the main thread to wait for the queue to finish processing all
    # the tasks
    for x in range(4):
        worker = DownLoadImg(queue)
        # Setting daemon to True will let the main thread exit even though the
        # workers are blocking
        worker.daemon = True
        worker.start()
        # Put the tasks into the queue as a tuple
    queue.join()
# getAllImage('https://huaban.com/','data-baiduimageplus-ignore','data-baiduimageplus-ignore')
getAllImage('http://originoo.com/ws/p.topiclist.php?cGljX2tleXdvcmRzPW5hdHVyYWwgc2NlbmVyeSZtZWRpdW1fdHlwZT1waWM=',"external","lazy")