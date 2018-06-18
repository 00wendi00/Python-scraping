#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test1.py
# @Author: Wade Cheung
# @Date  : 2018/6/17
# @Desc  : test


import datetime
import cache.link_crawler
from cache.DiskCache import DiskCache
from cache.Downloader import Downloader

download = Downloader()
myCache = DiskCache()

# download = mytest.download('http://example.webscraping.com', {'User_agent': 'wswp'})
# myCache.url_to_path('http://example.webscraping.com')

starttime = datetime.datetime.now()
# cache.link_crawler.link_crawler(seed_url='http://example.webscraping.com/', link_regex='/(index|view)',
#                                 cache=DiskCache())
cache.link_crawler.link_crawler('http://example.webscraping.com/', '/(index|view)', max_depth=2, cache=DiskCache())
endtime = datetime.datetime.now()
print('时长为' + str((endtime - starttime)))


