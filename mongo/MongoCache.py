#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : MongoCache.py
# @Author: Wade Cheung
# @Date  : 2018/6/18
# @Desc  : 基于MongoDB的缓存 . 压缩解压, 索引


import zlib
import pickle
from bson.binary import Binary
from datetime import datetime, timedelta
from pymongo import MongoClient


class MongoCache:
    def __init__(self, client=None, expires=timedelta(days=30)):
        # if a client object is not passed then try
        # connecting to mongodb at the default localhost port
        self.client = MongoClient('localhost', 27017) if client is None else client

        # create connection to store cached webpages,
        # which is the equivalent of a table in a relational database
        self.db = self.client.cache
        # create index to expire cached webpages
        self.db.mywebpage.create_index('timestamp', expireAfterSeconds=expires.total_seconds())

    def __getitem__(self, url):
        """load value at this URL
        """
        record = self.db.mywebpage.find_one({'_id': url})
        if record:
            return pickle.loads(zlib.decompress(record['result']))
        else:
            raise KeyError(url + ' dose not exist')

    def __setitem__(self, url, result):
        """Save value for this URL
        """
        record = {'result': Binary(zlib.compress(pickle.dumps(result))), 'timestamp': datetime.utcnow()}
        self.db.mywebpage.update({'_id': url}, {'$set': record}, upsert=True)
