#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : submit_post.py
# @Author: Wade Cheung
# @Date  : 2018/6/20
# @Desc  : 提交表单 :  获取表单, 添加cookie支持, 填表单, 提交, 返回Response.


import urllib.request
import lxml.html
from http.cookiejar import CookieJar

LOGIN_URL = 'http://example.webscraping.com/places/default/user/login?_next=/places/default/index'
LOGIN_EMAIL = 'zhang842876912@gmail.com'
LOGIN_PASSWORD = 'wendi000'


def parse_form(html):
    """提取表单中所有input 标签的详情"""
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get("value")
    return data


if __name__ == '__main__':
    cj = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))  # 添加cookie支持
    html_result = opener.open(LOGIN_URL).read()
    data = parse_form(html_result)  # 获得需要提交的表单详情.
    data['email'] = LOGIN_EMAIL
    data['password'] = LOGIN_PASSWORD
    encoded_data = urllib.parse.urlencode(data)
    request = urllib.request.Request(LOGIN_URL, str.encode(encoded_data))
    response = opener.open(request)
    # 打印http://example.webscraping.com/places/default/index 说明提交成功
    print(str(response.geturl()))
