#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : Throttle.py
# @Author: Wade Cheung
# @Date  : 2018/6/17
# @Desc  : 推迟调用线程的运行 -- time.sleep()

import urllib.request
import datetime
import time


class Throttle:
    """Throttle downloading by sleeping between requests to same domain
        """

    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}

    def wait(self, url):
        """Delay if have accessed this domain recently
                """
        domain = urllib.request.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.datetime.now()
