#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test1.py
# @Author: Wade Cheung
# @Date  : 2018/6/19
# @Desc  : 测试 link_crawler -- 串行下载500个页面, 缓存至MongoDB中

from multi_thread.AlexaCallback import AlexaCallback
from multi_thread.link_crawler import link_crawler
from mongo.MongoCache import MongoCache


def main():
    scrape_callback = AlexaCallback()
    cache = MongoCache()
    # cache.clear()
    link_crawler(scrape_callback.seed_url, scrape_callback=scrape_callback, cache=cache)


if __name__ == '__main__':
    main()
