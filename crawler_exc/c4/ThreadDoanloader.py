# encoding:utf-8
'''
@author:lk

@time:2018/4/24 

@desc:并发下载

'''
import threading

import time

from crawler_exc.AlexaCallback import AlexaCallback
from crawler_exc.MongoDBCache import MongoDBCache
from crawler_exc.down_loader import DownLoader


def threaded_crawler(seed_url, proxy=None, retries=2,
                     delay=5, scrape_callback=None, cache=None, max_threads=10):
    user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"
    # 在headers中设置agent
    headers = [("User-Agent", user_agent)]
    crawler_queue = [seed_url]
    loader = DownLoader(proxy, headers, None, retries, delay, cache)

    def process_queue():
        while True:
            try:
                url = crawler_queue.pop()
            except IndexError:
                break
            else:
                if url:
                    html = loader(url)
                    links = []
                    if scrape_callback:
                        try:
                            links.extend(scrape_callback(url, html) or [])
                        except Exception as e:
                            print('Error in callback for: {}: {}'.format(url, e))
                        else:
                            for link in links:
                                # add this new link to queue
                                crawler_queue.append(link)

    threads = []
    while threads or crawler_queue:
        for thread in threads:
            if not thread.is_alive():
                print('threads_remove=', thread)
                threads.remove(thread)
        while len(threads) < max_threads and crawler_queue:
            print('threads=', len(threads))
            thread = threading.Thread(target=process_queue)
            thread.setDaemon(True)  # 设置为守护线程
            thread.start()
            threads.append(thread)
        time.sleep(1)


# def main(max_threads):
#     scrape_callback = AlexaCallback('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip',1000)
#     cache = MongoDBCache()
#     # cache.clear()
#     threaded_crawler(scrape_callback.seed_url, scrape_callback=scrape_callback, cache=cache,
#                      max_threads=max_threads)
#
#
# if __name__ == '__main__':
#     main(10)
scrape_callback = AlexaCallback('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip',1000)
cache = MongoDBCache()
cache.clear()
threaded_crawler(scrape_callback.seed_url, scrape_callback=scrape_callback, cache=cache,
                 max_threads=10)