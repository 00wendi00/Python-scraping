#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : thread_test.py
# @Author: Wade Cheung
# @Date  : 2018/6/19
# @Desc  : 1. 启动多进程, multiprocessing   2. 多线程下载网页 threading   3. 使用MongoDB -- 线程安全


import time
import threading
import re
import urllib.request
import urllib.response
import urllib.robotparser
import multiprocessing
from mongo_queue.MongoQueue import MongoQueue
from cache.Downloader import Downloader
from multi_thread.AlexaCallback import AlexaCallback

SLEEP_TIME = 0.5


def threaded_crawler(seed_url, link_regex=None, delay=0, max_depth=-1, max_urls=-1, user_agent='wswp', proxies=None,
                     num_retries=2, scrape_callback=None, cache=None, max_thread=10):
    """Crawl from the given seed URL following links matched by link_regex
    """
    # the queue of URL's that still need to be crawled
    crawl_queue = MongoQueue()
    crawl_queue.clear()
    crawl_queue.push(seed_url)
    # the URL's that have been seen and at what depth
    seen = {seed_url: 0}
    # track how many URL's have been downloaded
    # num_urls = 0
    # rp = get_robots(seed_url)
    D = Downloader(delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries, cache=cache)

    def process_queue():
        while True:
            try:
                url = crawl_queue.pop()
            except KeyError:
                break
            else:
                html = D(url)  # __call__ !!!!!!!!!!!!!!!!
                if scrape_callback:
                    try:
                        links = scrape_callback(url, html) or []
                    except Exception as e:
                        print('Error in callback for :{}:{}'.format(url, e))
                    else:
                        for link in links:
                            crawl_queue.push(normalize(seed_url, link))
                crawl_queue.complete(url)

                # links = []
                # if scrape_callback:
                #     links.extend(scrape_callback(url) or [])
                #     for link in links:
                #         print(link)
                #         crawl_queue.extend(link)
        else:
            print('Finish or Blocked by robots.txt or Error ~ ')

    threads = []
    while threads or crawl_queue:
        # the crawl is still active
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
                print(str(len(threads)) + '--------------------')
        while len(threads) < max_thread and crawl_queue:
            # start some more thread
            thread = threading.Thread(target=process_queue)
            # set daemon so main thread can exit when receives ctrl-c
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
            print(str(len(threads)) + '--------------------')

        # all threads have been processed
        # sleep temporarily so CPU can focus execution elsewhere
        time.sleep(SLEEP_TIME)


def process_crawler(args, **kwargs):
    num_cpus = multiprocessing.cpu_count()
    # pool = multiprocessing.Pool(processes=num_cpus)
    print('-----------------Starting {} processes'.format(num_cpus))
    processes = []
    for i in range(num_cpus):
        p = multiprocessing.Process(target=threaded_crawler, args=[args], kwargs=kwargs)
        # parsed = pool.apply_async(threaded_link_crawler, args, kwargs)
        p.start()
        processes.append(p)
    # wait for processes to complete
    for p in processes:
        p.join()


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = urllib.parse.urldefrag(link)  # remove hash to avoid duplicates
    return urllib.request.urljoin(seed_url, link)


def same_domain(url1, url2):
    """Return True if both URL's belong to same domain
    """
    # return urllib.request.urlparse(url1).netloc == urllib.request.urlparse(url2).netloc
    return urllib.parse.urlparse(url1) == urllib.parse.urlparse(url2)


def get_robots(url):
    """Initialize robots parser for this domain
    """
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(urllib.request.urljoin(url, '/robots.txt'))
    rp.read()
    return rp


def get_links(html):
    """Return a list of links from html
    """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(str(html))


if __name__ == '__main__':
    scrape_callback = AlexaCallback()
    # cache.clear()
    threaded_crawler(scrape_callback.seed_url, scrape_callback=scrape_callback, cache=None, max_thread=60)
