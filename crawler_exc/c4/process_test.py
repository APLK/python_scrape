# encoding:utf-8
'''
@author:lk

@time:2018/4/25 

@desc:

'''
import threading

import time

import multiprocessing

import os

from crawler_exc.AlexaCallback import AlexaCallback
from crawler_exc.MongoDBCache import MongoDBCache
from crawler_exc.c4.MongoDb_Queue import MongoDb_Queue
from crawler_exc.down_loader import DownLoader


def threaded_crawler(seed_url, proxy=None, retries=2,
                     delay=5, scrape_callback=None,  max_threads=10):
    print('Child process {0}Running '.format( os.getpid()))
    # 此处的mongodb都必须单独构建一个对象,不能公用一个
    cache = MongoDBCache()
    cache.clear()
    user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
    # 在headers中设置agent
    headers = [("User-Agent", user_agent)]
    crawler_queue = MongoDb_Queue()
    crawler_queue.clear()
    crawler_queue.push(seed_url)
    loader = DownLoader(proxy, headers, None, retries, delay, cache)

    def process_queue():
        while True:
            try:
                url = crawler_queue.pop()
            except KeyError:
                break
            else:
                if url:
                    html = loader(url)
                    if scrape_callback:
                        links = []
                        try:
                            links.extend(scrape_callback(url, html) or [])
                        except Exception as e:
                            print('Error in callback for: {}: {}'.format(url, e))
                        else:
                            for link in links:
                                # add this new link to queue
                                crawler_queue.push(link)
                    crawler_queue.complete(url)

    threads = []
    startTime=time.time()
    while threads or crawler_queue:
        for thread in threads:
            if not thread.is_alive():
                print('threads_remove=', thread)
                threads.remove(thread)
        while len(threads) < max_threads and crawler_queue.peek():
            print('threads_remove0=', len(threads))
            thread = threading.Thread(target=process_queue)
            thread.setDaemon(True)  # 设置为守护线程,及一个后台运行
            thread.start()
            threads.append(thread)
        if len(threads)==0 and not crawler_queue.peek():
            endTime=time.time()
            print('%s,%.2f'%('threads=',endTime-startTime))#266.67S=4.4445分(min)
            break
        time.sleep(1)
def process_crawler(args, **kwargs):
    # TypeError: can't pickle _thread.lock objects
    num_cpus = multiprocessing.cpu_count() #cpu的核数
    #pool = multiprocessing.Pool(processes=num_cpus)
    print('Starting {} processes'.format(num_cpus))
    processes = []
    for i in range(num_cpus):
        print(num_cpus,i)
        #多进程开启如果调用的mongodb的数据,不能共享一份client,否则TypeError: can't pickle _thread.lock objects
        # 不允许两个进程同时修改一份数据。两个进程没有办法同时修改一份数据
        #参见  http://api.mongodb.com/python/current/faq.html?highlight=pymongo%20mongoclient%20mydb
        p = multiprocessing.Process(target=threaded_crawler, args=[args], kwargs=kwargs)
        #parsed = pool.apply_async(threaded_link_crawler, args, kwargs)
        p.start()
        processes.append(p)
    # wait for processes to complete
    #  <Process(Process-1, started)> 4784
    #  <Process(Process-2, stopped)> 4784
    #  <Process(Process-3, started)> 4784
    #  <Process(Process-4, stopped)> 4784
    for p in processes:
        print('dffff=',p,'processes=',len(processes))
        p.join()
#调用多进程时必须加上__name=='__main__'
# 否则An attempt has been made to start a new process before the current
#  process has finished its bootstrapping phase
if __name__ == '__main__':
    scrape_callback = AlexaCallback('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip', 1000)
    process_crawler(scrape_callback.seed_url, scrape_callback=scrape_callback, max_threads=10)