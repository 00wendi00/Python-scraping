#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : gain_cookie.py
# @Author: Wade Cheung
# @Date  : 2018/6/20
# @Desc  : 读取Chrome浏览器的Cookie -- 取sqlite中的数据, 将Cookie添加至请求当中, 返回的页面为已登录状态


import lxml.html
import urllib.request
import sqlite3
import os
import sys
import win32crypt
from http.cookiejar import CookieJar
from http.cookiejar import Cookie


def load_ff_sessions(session_filename):
    """使用sqlite3解析Chrome的cookie文件到CookieJar中"""
    cookie_file_path = os.path.join(os.environ['LOCALAPPDATA'], r'Google\Chrome\User Data\Default\Cookies')
    print(cookie_file_path)
    if not os.path.exists(cookie_file_path):
        raise Exception('Cookies file not exist!')
    conn = sqlite3.connect(cookie_file_path)
    sql = 'select host_key,name,encrypted_value,path from cookies where host_key like "%{}%"'.format(
        'example.webscraping.com')
    cj = CookieJar()
    for row in conn.execute(sql):
        print(row[0])
        print(row[1])
        print(row[2])
        print(row[3])
        try:
            ret = win32crypt.CryptUnprotectData(row[2], None, None, None, 0)
        except:
            print('Fail to decrypt chrome cookies')
            sys.exit(-1)

        c = Cookie(
            version=0, name=row[1], value=ret[1].decode(),  # !!!!!!!!!!!!! 此处务必decode ~
            port=None, port_specified=None,
            domain=row[0], domain_specified=None, domain_initial_dot=None,
            path=row[3], path_specified=None,
            secure=None,
            expires=None,
            discard=None,
            comment=None,
            comment_url=None,
            rest=None,
            rfc2109=False
        )
        cj.set_cookie(c)
    return cj


COOKIE_PATH = 'C:\\Users\\wendi\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies'
URL_HOME = 'http://example.webscraping.com'

# 在Chrome中登录之后, 执行代码最终返回 Welcome wade . 不登录的情况下返回Login In
cj_home = load_ff_sessions(COOKIE_PATH)
opener_home = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj_home))
html_re = opener_home.open(URL_HOME).read()
tree = lxml.html.fromstring(html_re.decode())
print(tree.cssselect('ul#navbar li a')[0].text_content())
