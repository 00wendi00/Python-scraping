#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test3.py
# @Author: Wade Cheung
# @Date  : 2018/6/18
# @Desc  : 测试 MongoCache


import time
from datetime import timedelta
from mongo.MongoCache import MongoCache

cache = MongoCache(expires=timedelta())  # MongoDb每分钟检查过期记录
result = {'html': '......'}
cache['qwer'] = result
print(cache['qwer'])

time.sleep(60)  # MongoDb每分钟检查过期记录
print(cache['qwer'])
