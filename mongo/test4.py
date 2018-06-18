#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test4.py
# @Author: Wade Cheung
# @Date  : 2018/6/18
# @Desc  : 抓取网页, 存入MongoDB中

from mongo.MongoCache import MongoCache
from datetime import datetime
import cache.link_crawler

starttime = datetime.now()
cache.link_crawler.link_crawler('http://example.webscraping.com/', '/(index|view)', max_depth=2,
                                cache=MongoCache())
endtime = datetime.now()
print('时长为' + str((endtime - starttime)))
