#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : MongoQueue.py
# @Author: Wade Cheung
# @Date  : 2018/6/19
# @Desc  : 基于 MongoDB 实现的队列 . 定义了执行过程中的三种状态 : OUTSTANDING, PROCESSING, COMPLETE


from datetime import datetime, timedelta
from pymongo import MongoClient, errors


class MongoQueue:
    OUTSTANDING, PROCESSING, COMPLETE = range(3)

    def __init__(self, clinet=None, timeout=5):
        self.client = MongoClient()
        self.db = self.client.cache
        self.timeout = timeout

    def __nonzero__(self):
        """Returns True if there are more jobs to process
        """
        record = self.db.crawl_queue.find_one({'status': {'$ne': self.COMPLETE}})
        return True if record else False

    def push(self, url):
        try:
            self.db.crawl_queue.insert({'_id': url, 'status': self.OUTSTANDING})
        except errors.DuplicateKeyError as e:
            pass  # already in the queue

    def pop(self):
        """Get an outstanding URL from the queue and set its status to peocessing .
            If the queue is empty a KeyError exception is raised"""
        record = self.db.crawl_queue.find_and_modify(query={'status': self.OUTSTANDING}, update={
            "$set": {'status': self.PROCESSING, 'timestamp': datetime.now()}})
        if record:
            return record['_id']
        else:
            self.repair()
            raise KeyError()

    def complete(self, url):
        self.db.crawl_queue.update({'_id': url}, {'$set': {'status': self.COMPLETE}})

    def repair(self):
        """Release stalled jobs
        """
        record = self.db.crawl_queue.find_and_modify(
            query={
                'timestamp': {'$lt': datetime.now() - timedelta(seconds=self.timeout)},
                'status': {'$ne': self.COMPLETE},
            },
            update={'$set': {'status': self.OUTSTANDING}}
        )
        if record:
            print('Released: ', record['_id'])
