# encoding:utf-8
'''
@author:lk

@time:2018/4/24 

@desc:

'''
from datetime import datetime, timedelta

import multiprocessing
import pymongo
from pymongo import MongoClient, errors


class MongoDb_Queue:
    # 当添加新的ulr时其状态是OUTSTANDING,当url从队列中取出准备下载时状态是PROCESSING
    # 当下载结束后,其状态变为COMPLETE
    OUTSTANDING, PROCESSING, COMPLETE = range(3)

    def __init__(self, client=None, timeout=300):
        print('__init__')
        if client is None:
            self.client = MongoClient('localhost', 27017)
        self.db = self.client.cache  # cache是mongodb的数据库名称
        self.timeout = timeout
        # try:
        #     self.db.crawl_queue.drop()  # 先清空crawl_queue表集合
        # except Exception as e:
        #     print(e, '-->请先尝试启动mongodb服务')

    def clear(self):
        self.db.crawl_queue.drop()

    def __nonzero__(self):
        # $ne表示不等于,查找状态是否存在不等于已完成的记录
        record = self.db.crawl_queue.find_one({'status': {'$ne': self.COMPLETE}})
        return True if record else False

    def push(self, url):
        '''
        插入一条不存在的url到数据库
        :param url:
        :return:
        '''
        try:
            self.db.crawl_queue.insert({'_id': url, 'status': self.OUTSTANDING})
        except errors.DuplicateKeyError as e:
            print('DuplicateKeyError', e)
            pass

    def pop(self):
        '''
        取出一条outstanding状态的数据同时更新他的状态为PROCESSING和时间
        :return:
        '''
        # 找到状态为outstanding的数据并执行status和timestamp属性更新
        record = self.db.crawl_queue.find_and_modify(
            query={'status': self.OUTSTANDING},
            update={'$set': {'status': self.PROCESSING, 'timestamp': datetime.now()}}
        )
        print('record==', record)
        if record:
            return record['_id']
        else:
            # 如果不存在outstanding的状态时
            # 处理url的进程被终止的情况,为了避免丢失这些url,所以需要根据时间间隔判断
            self.repair()
            raise KeyError()

    def peek(self):
        '''
        找到outstanding状态的记录
        :return:
        '''
        record = self.db.crawl_queue.find_one({'status': self.OUTSTANDING})
        if record:
            return record['_id']

    def complete(self, url):
        '''
        设置该url数据的status值为已完成
        :param url: _id对应的url值
        :return:
        '''
        self.db.crawl_queue.find_and_modify(query={'_id': url}, update={
            '$set': {'status': self.COMPLETE}})

    def repair(self):
        '''
        查询timestamp的距离当前的时间间隔是否大于timeout(300s),并且status状态不等于COMPLETE时
        如果大于了就表示处理这个url时间已经超时了,需要重新更新该条url的状态为OUTSTANDING
        :return:
        '''
        # $lt小于的意思.ne表示不等于意思
        record = self.db.crawl_queue.find_and_modify(
            query={'timestamp': {'$lt': datetime.now() - timedelta(seconds=self.timeout)},
                   'status': {'$ne': self.COMPLETE}},
            update={
                '$set': {'status': self.OUTSTANDING}})
        if record:
            print('released:', record['_id'])

            # Each process creates its own instance of MongoClient.
# def func():
#     print('fff')
#     db = pymongo.MongoClient().mydb
#     # Do something with db.
#
# if __name__ == '__main__':
#     proc = multiprocessing.Process(target=func)
#     proc.start()