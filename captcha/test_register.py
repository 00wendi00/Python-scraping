#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_register.py
# @Author: Wade Cheung
# @Date  : 2018/6/21
# @Desc  : 在注册页面中 . 1.抓取注册页面中的图片, 使用Base64解码图像数据--> 二进制
# 2.将图片转换为黑白, 将图片阈值化, 保存图片, image_to_string, 限定字符集, 返回名称和识别的字符
# 3.tesseract-ocr需要下载安装,设环境变量:参考pytesseract书签 .

import base64
import pprint
import string
import urllib.request
import lxml.html
import pytesseract
import random
from io import BytesIO
from PIL import Image
from http.cookiejar import CookieJar
from form_ui import submit_post


def get_captcha(html):
    """抓取注册页面中的图片, 使用Base64解码图像数据--> 二进制 """
    tree = lxml.html.fromstring(html)
    img_data = tree.cssselect('div#recaptcha img')[0].get('src')
    img_data = img_data.partition(',')[-1]
    binary_img_data = base64.b64decode(img_data.encode())
    file_like = BytesIO(binary_img_data)
    # img = Image.open("登录界面.png")
    img = Image.open(file_like)
    return img


def ocr(img):
    """将图片转换为黑白, 将图片阈值化, 保存图片, image_to_string, 限定字符集, 返回名称和识别的字符"""
    rand1 = random.random() * 100000
    # 将图片存放在 D:\data\test_py\pytesseract_image 文件夹中
    img.save(SAVE_PATH + '\\' + str(rand1) + '.png')
    gray = img.convert('L')  # 将图片转换为黑白色
    gray.save(SAVE_PATH + '\\' + str(rand1) + '_gray.png')
    br = gray.point(lambda x: 0 if x < 1 else 255, '1')
    br.save(SAVE_PATH + '\\' + str(rand1) + '_thresholded.png')
    ocrstr = pytesseract.image_to_string(br)  # 调用image_to_string
    ocrstr = str(ocrstr)
    ascii_word = ''.join(c for c in ocrstr if c in string.ascii_letters).lower()  # 此都为小写的ASCII字符, 故将结果限定此字符集
    return str(rand1), ascii_word


SAVE_PATH = 'D:\\data\\test_py\\pytesseract_image'
REGISTER_URL = 'http://example.webscraping.com/places/default/user/register?_next=/places/default/index'
PROCESS_TIMES = 5

if __name__ == '__main__':
    """抓取图片, 转换成文字, 保存和打印结果"""
    result_list = []
    none_list = []
    for i in range(PROCESS_TIMES):
        cj = CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        html_result = opener.open(REGISTER_URL).read().decode()
        form = submit_post.parse_form(html_result)
        pprint.pprint(form)
        namestr, resultstr = ocr(get_captcha(html_result))
        if resultstr:
            result_list.append(resultstr)
            print('结果: ' + resultstr)
        else:
            none_list.append(namestr)

    print(str(len(result_list)))
    print(none_list)
