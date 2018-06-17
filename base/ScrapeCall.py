#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : ScrapeCall.py
# @Author: Wade Cheung
# @Date  : 2018/6/17
# @Desc  : 回调类 -- 扩展 : 重写了__init__和__call__方法 --> 将scrape的数据写入csv文件中

import csv
import re
import lxml.html


class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('D:\\data\\test_py\\countries.csv', 'w'))
        self.fields = {'area', 'population', 'iso', 'country', 'capital', 'continent', 'tld', 'currency_code',
                       'currency_name',
                       'phone', 'postal_code_format', 'postal_code_regex', 'languages', 'neighbours'}

        self.writer.writerow(self.fields)

    def __call__(self, url, html):
        if re.search('/view/', url):
            tree = lxml.html.fromstring(html)
            row = []
            for field in self.fields:
                if tree.cssselect('table>tr#places_{}__row>td.w2p_fw'.format(field)):
                    row.append(tree.cssselect('table>tr#places_{}__row>td.w2p_fw'.format(field))[0].text_content())
                    self.writer.writerow(row)
