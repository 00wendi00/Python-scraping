#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : process_test.py
# @Author: Wade Cheung
# @Date  : 2018/6/19
# @Desc  : 测试process_crawler , 8进程

from mongo_queue import thread_test
from multi_thread.AlexaCallback import AlexaCallback
from mongo.MongoCache import MongoCache


def main(max_threads):
    scrape_callback = AlexaCallback()
    cache = MongoCache()
    thread_test.process_crawler(scrape_callback.seed_url, scrape_callback=scrape_callback, cache=cache,
                                max_threads=max_threads,
                                timeout=10)


if __name__ == '__main__':
    # max_threads = int(sys.argv[1])
    main(8)
