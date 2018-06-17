#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_lxml.py
# @Author: Wade Cheung
# @Date  : 2018/6/15
# @Desc  : Lxml.html 的使用
import datetime
import lxml.html
import urllib.request


def download(url, user_agent='wswp', proxy=None, num_retries=2):
    print('----Downloading : ----', url)
    headers = {'User-agent': user_agent}
    request = urllib.request.Request(url, headers=headers)

    opener = urllib.request.build_opener()
    try:
        myhtml = urllib.request.urlopen(request).read()
    except urllib.request.URLError as e:
        print('Download error : ', e.reason)
        myhtml = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # retry 5xx http errors
                return download(url, user_agent, proxy)
    return myhtml


broken_html = download('http://example.webscraping.com/places/default/view/United-Kingdom-239')
starttime = datetime.datetime.now()
tree = lxml.html.fromstring(broken_html)
fixed_html = lxml.html.tostring(tree, pretty_print=True)
endtime = datetime.datetime.now()
print(fixed_html)
print((endtime - starttime).microseconds)


tree = lxml.html.fromstring(broken_html)
td = tree.cssselect('tr#places_area__row > td.w2p_fw')[0]
area = td.text_content()
print(area)




