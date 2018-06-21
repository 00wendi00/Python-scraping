#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_regist.py
# @Author: Wade Cheung
# @Date  : 2018/6/21
# @Desc  : 使用mechanicalsoup获得、填充、提交表单 -- 注册,  使用pytesseract获得图片中的文字

import mechanicalsoup
from captcha import test_register

REGISTER_URL = 'http://example.webscraping.com/places/default/user/register?_next=/places/default/index'
EMAIL = '842876912@qq.com'
PASSWORD = '842876912@qq.com'

br = mechanicalsoup.Browser()
html_result = br.get(REGISTER_URL)
form = html_result.soup.find('form')
# pprint.pprint(form)

namestr, resultstr = test_register.ocr(test_register.get_captcha(str(form)))
print(namestr + ' ==  ' + resultstr)
form.find('input', {'name': 'email'})['value'] = EMAIL
form.find('input', {'name': 'first_name'})['value'] = '0wade0'
form.find('input', {'name': 'last_name'})['value'] = 'Cheung'
form.find('input', {'name': 'password'})['value'] = PASSWORD
form.find('input', {'name': 'password_two'})['value'] = PASSWORD
form.find('input', {'name': 'recaptcha_response_field'})['value'] = resultstr

response = br.submit(form, html_result.url)
print(response.url)
