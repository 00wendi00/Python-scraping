#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : AlexaCallback.py
# @Author: Wade Cheung
# @Date  : 2018/6/19
# @Desc  : 回调类 : 读取CSV文件.  下载读取zip文件

import csv
from zipfile import ZipFile


class AlexaCallback:
    def __init__(self, max_urls=500):
        self.max_urls = max_urls
        self.seed_url = 'https://www.cnblogs.com/'

    def __call__(self, url):
        if url == self.seed_url:
            global urls
            urls = []
            # with ZipFile(StringIO(html)) as zf:
            # with ZipFile('D:\\data\\test_py\\top-1m.csv.zip') as zf:
            # csv_filename = zf.namelist()[0]
            # for _, website in csv.reader(zf.open(csv_filename)):
            with open('D:\\data\\test_py\\top-1m.csv', 'r', encoding='utf-8') as csvfile:
                read = csv.reader(csvfile)
                for row in read:
                    urls.append('http://' + row[1])
                    if len(urls) == self.max_urls:
                        break
        return urls
