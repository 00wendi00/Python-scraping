#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : thread_test.py
# @Author: Wade Cheung
# @Date  : 2018/6/19
# @Desc  : 1.多线程下载网页, threading  2.循环创建线程  3.队列的基本操作 -- 线程安全.


import queue
import time
import threading
import re
import urllib.request
import urllib.response
import urllib.robotparser
from cache.Downloader import Downloader
from multi_thread.AlexaCallback import AlexaCallback

SLEEP_TIME = 0.5


def threaded_crawler(seed_url, link_regex=None, delay=0, max_depth=-1, max_urls=-1, user_agent='wswp', proxies=None,
                     num_retries=2, scrape_callback=None, cache=None, max_thread=10):
    """Crawl from the given seed URL following links matched by link_regex
    """
    # the queue of URL's that still need to be crawled
    crawl_queue = queue.Queue()
    crawl_queue.put(seed_url)
    # the URL's that have been seen and at what depth
    seen = {seed_url: 0}
    # track how many URL's have been downloaded
    # num_urls = 0
    # rp = get_robots(seed_url)
    D = Downloader(delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries, cache=cache)

    def process_queue():
        while True:
            if crawl_queue.empty():
                break;
            url = crawl_queue.get()  # 若队列为空且 block为true , 则线程暂停. 故必须加上上面的判定.
            depth = seen[url]
            # check url passes robots.txt restrictions
            # if rp.can_fetch(user_agent, str(url)):
            html = D(url)  # __call__ !!!!!!!!!!!!!!!!
            links = []
            if scrape_callback:
                links.extend(scrape_callback(url) or [])
                # if depth != max_depth:
                # can still crawl further
                # if link_regex:
                #     # filter for links matching our regular expression
                #     getlinks = get_links(html)
                #     getlinks = seed_url.join(getlinks)
                #     links.extend(link for link in getlinks if re.match(link_regex, link))
                # links.extend((seed_url + link) for link in get_links(html))

                for link in links:
                    # link = normalize(seed_url, link)
                    # check whether already crawled this link
                    if link not in seen:
                        seen[link] = depth + 1
                        # check link is within same domain
                        # if link.find(seed_url) != -1:
                        print(link)
                        crawl_queue.put(link)

                        # if same_domain(seed_url, link):
                        #     # success! add this new link to queue
                        #     crawl_queue.append(link)
        else:
            print('Finish or Blocked by robots.txt or Error ~ ')

    threads = []
    while threads or not crawl_queue.empty():
        # the crawl is still active
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
                print(str(len(threads)) + '--------------------')
        while len(threads) < max_thread and not crawl_queue.empty():
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
