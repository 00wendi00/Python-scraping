#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : crawling2.py
# @Author: Wade Cheung
# @Date  : 2018/6/15
# @Desc  : 数据抓取 . Soup , 补全prettify , 定位find
import datetime
from bs4 import BeautifulSoup
import urllib.request

class Crawling2:
    def download(url, user_agent='wswp', proxy=None, num_retries=2):
        print('----Downloading : ----', url)
        headers = {'User-agent': user_agent}
        request = urllib.request.Request(url, headers=headers)

        opener = urllib.request.build_opener()
        try:
            html = urllib.request.urlopen(request).read()
        except urllib.request.URLError as e:
            print('Download error : ', e.reason)
            html = None
            if num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    # retry 5xx http errors
                    return Crawling2.download(url, user_agent, proxy)
        return html


html = Crawling2.download('http://example.webscraping.com/places/default/view/United-Kingdom-239')

starttime = datetime.datetime.now()
soup = BeautifulSoup(html, 'html.parser')  # 补全html
soup.prettify()
endtime = datetime.datetime.now()
print((endtime - starttime).microseconds)

tr = soup.find(attrs={'id': 'places_area__row'})
td = tr.find(attrs={'class': 'w2p_fw'})
area = td.text
print(area)