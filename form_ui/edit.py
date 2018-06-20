#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : edit.py
# @Author: Wade Cheung
# @Date  : 2018/6/20
# @Desc  : 提交表单 -- 编辑国家人口.


import urllib.request
import urllib.parse
from form_ui import gain_cookie
from form_ui import submit_post

COOKIE_PATH = 'C:\\Users\\wendi\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies'
EDIT_URL = 'http://example.webscraping.com/places/default/edit/Aland-Islands-2'

# 获取cookie , 为登录状态时 , 才能进edit页面
cj = gain_cookie.load_ff_sessions(COOKIE_PATH)
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
http_result = opener.open(EDIT_URL).read()
if http_result:
    data_result = submit_post.parse_form(str(http_result))
    data_result['population'] = str(int(data_result['population']) + 1)
    encoded_data = urllib.parse.urlencode(data_result)
    request = urllib.request.Request(EDIT_URL, str.encode(encoded_data))
    response = opener.open(request)
    print(str(response.geturl()))
