#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test2.py
# @Author: Wade Cheung
# @Date  : 2018/6/18
# @Desc  : mongodb, python 多级元素操作, 查询修改.


from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.cache
my_set = db.myset
dic = {"name": "zhangsan",
       "age": 18,
       "contact": {
           "email": "1234567@qq.com",
           "iphone": "11223344"}
       }
my_set.insert(dic)

for i in my_set.find({"contact.iphone": "11223344"}):
    print(i)

result = my_set.find_one({"contact.iphone": '11223344'})
print(result["contact"]["email"])

result = my_set.update({"contact.iphone": "11223344"}, {"$set": {"contact.email": "6666666666@qq.com"}})
result1 = my_set.find_one({"contact.iphone": "11223344"})
print(result1["contact"]["email"])

my_set.remove()
