#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : crawling1.py
# @Author: Wade Cheung
# @Date  : 2018/6/15
# @Desc  :网络爬虫 -- robots.txt, 网站地图, 网站大小, 使用技术, 所有者; 下载网页,网站地图爬虫.ID遍历爬虫,链接爬虫. 寻找网站所有者


# print(whois.whois('www.donghaiair.com/'))

import datetime
import re
import urllib.request
import lxml.html

import giturlparse
import base.ScrapeCall


class Crawling:
    def download(url, user_agent='wswp', proxy=None, num_retries=2):
        print('----Downloading : ----', url)
        headers = {'User-agent': user_agent}
        request = urllib.request.Request(url, headers=headers)

        opener = urllib.request.build_opener()
        if proxy:
            proxy_params = {giturlparse.parse(url).scheme: proxy}
            opener.add_handler(urllib.request.ProxyHandler(proxy_params))
        try:
            html = urllib.request.urlopen(request).read()
        except urllib.request.URLError as e:
            print('Download error : ', e.reason)
            html = None
            if num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    # retry 5xx http errors
                    return Crawling.download(url, user_agent, proxy, num_retries - 1)
        return html

    # print('结果\n' + str(download('http://www.donghaiair.com/').decode()))

    def link_crawler(self,seed_url, link_regex, max_depth=1, scrape_callback=None):
        '''Crawl from given seed Url following links matched by link_regex'''
        seen = {seed_url: 0}
        crawl_queue = [seed_url]
        # keep track which URL's have seen before
        while crawl_queue:
            url = crawl_queue.pop()
            html = Crawling.download(url)
            result_links = [seed_url + i for i in Crawling.get_links(html)]  # 列表综合
            if scrape_callback:
                result_links.extend(scrape_callback(url, html) or [])
            depth = seen[url]
            if depth != max_depth:
                # filter for links matching our regular expression
                for link in result_links:
                    if link not in seen and link not in seen:
                        print(link)
                        seen[link] = depth + 1
                        crawl_queue.append(link)

    def get_links(html):
        '''Return a list of links from html'''
        webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
        return webpage_regex.findall(html.decode())


##回调方法
# def scrape_callback(url, html):
#     if (re.search('/view', url)):
#         tree = lxml.html.fromstring(html)
#         row = [tree.cssselect('table>tr#place_%s_row>td.w2p_fw' % field)[0].text_content() for field in
#                base.test_contrast.FIELDSDS]
#         print(url, row)


starttime = datetime.datetime.now()
craw = Crawling()
craw.link_crawler('http://example.webscraping.com', '/(index|view)', max_depth=2, scrape_callback=base.ScrapeCall.ScrapeCallback())
endtime = datetime.datetime.now()
print((endtime - starttime).microseconds)
# time.clock() , time.time()
