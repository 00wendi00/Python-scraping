#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test1.py
# @Author: Wade Cheung
# @Date  : 2018/6/19
# @Desc  : 对Ajax接口的爬取. 存入countries.txt文件中.

# 缺少渲染动态网页. PySide, Selenium


import demjson
import lxml.html
import json
import string
from cache.Downloader import Downloader

D = Downloader()
# return all result
result = D('http://example.webscraping.com/places/ajax/search.json?&page_size=10&page=0&search_term=.')
if result:
    json_obj = demjson.decode(result)
    print(str(json_obj['num_pages']))

html = D('http://example.webscraping.com/places/default/search')
tree = lxml.html.fromstring(format(html))
print(tree.cssselect('div#results a'))

template_url = 'http://example.webscraping.com/places/ajax/search.json?&page={}&page_size=10&search_term={}'
countries = set()
for letter in string.ascii_lowercase:
    page = 0
    while True:
        html_result = D(template_url.format(page, letter))
        if html_result:
            try:
                ajax = json.loads(html_result.decode())
            except ValueError as e:
                print(e)
                ajax = None
            else:
                for record in ajax['records']:
                    countries.add(record['country'])
            page += 1
            if ajax is None or page >= ajax['num_pages']:
                break

open('countries.txt', 'w').write('\n'.join(sorted(countries)))
