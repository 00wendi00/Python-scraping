#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_mechanize.py
# @Author: Wade Cheung
# @Date  : 2018/6/20
# @Desc  : 提交表单 :  login page + edit page . 使用mechanical模块, 在3.x版本中, 为mechanicalsoup模块, 详见https://piratefache.ch/python-3-mechanize-and-beautifulsoup/


import mechanicalsoup

LOGIN_URL = 'http://example.webscraping.com/places/default/user/login?_next=/places/default/index'
CURRENT_URL = 'http://example.webscraping.com/places/default/edit/Aland-Islands-2'
LOGIN_EMAIL = 'zhang842876912@gmail.com'
LOGIN_PASSWORD = 'wendi000'


br = mechanicalsoup.Browser()

# login page
login_page = br.get(LOGIN_URL)
login_form = login_page.soup.find('form')
print(login_form)
login_form.find('input', {'name': 'email'})['value'] = LOGIN_EMAIL
login_form.find('input', {'name': 'password'})['value'] = LOGIN_PASSWORD
response = br.submit(login_form, login_page.url)
print(response.url)

# edit page
current_page = br.get(CURRENT_URL)
current_form = current_page.soup.find('form')
population = current_form.find('input', {'name': 'population'})['value']
current_form.find('input', {'name': 'population'})['value'] = str(int(population) + 1)
response1 = br.submit(current_form, current_page.url)
print(response1.url)
