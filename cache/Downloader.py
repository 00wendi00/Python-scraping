#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : Downloader.py
# @Author: Wade Cheung
# @Date  : 2018/6/17
# @Desc  : 为链接爬虫添加缓存支持 -- 存入磁盘文件


import urllib.request
import giturlparse
import random
from base.Throttle import Throttle
import socket

DEFAULT_AGENT = 'wswp'
DEFAULT_DELAY = 0.3
DEFAULT_RETRIES = 1
DEFAULT_TIMEOUT = 0.8


class Downloader:
    def __init__(self, delay=DEFAULT_DELAY, user_agent=DEFAULT_AGENT, proxies=None, num_retries=DEFAULT_RETRIES,
                 timeout=DEFAULT_TIMEOUT, opener=None, cache=None):
        socket.setdefaulttimeout(timeout)
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.opener = opener
        self.cache = cache

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                # url is not available in cache
                pass
            else:
                if self.num_retries > 0:
                    if result['code'] and 500 <= result['code'] < 600:
                        # server error so ignore result from cache and re-dowmload
                        result = None

        if result is None:
            # result need download
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent': self.user_agent}
            result = self.download(url, headers, proxy, self.num_retries)
            if self.cache:
                # save result to cache
                self.cache[url] = result
        return result['html']

    def download(self, url, headers, proxy=None, num_retries=2, data=None):
        print('----Downloading : ----', url)
        request = urllib.request.Request(str(url), data, headers or {})
        opener = self.opener or urllib.request.build_opener()

        if proxy:
            proxy_params = {giturlparse.parse(url).scheme: proxy}
            opener.add_handler(urllib.request.ProxyHandler(proxy_params))
        try:
            response = opener.open(request)
            html = response.read()
            code = response.code
        except Exception as e:
            print('Download error : ', str(e))
            html = None
            if hasattr(e, 'code'):
                code = e.code
                if num_retries > 0 and 500 <= code < 600:
                    # retry 5xx http errors
                    return self.download(url, headers, proxy, num_retries - 1, data)
            else:
                code = None
        return {'html': html, 'code': code}
