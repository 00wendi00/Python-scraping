#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test1.py
# @Author: Wade Cheung
# @Date  : 2018/6/18
# @Desc  : mongodb, python CRUD , 排序, 多级元素操作


from pymongo import MongoClient

client = MongoClient('localhost', 27017)
url = 'http://example.webscraping.com/places/default/view/United-Kingdom-239'
html = '===='
db = client.cache
# 插入一条 , 插入多条数据
post_id1 = db.webpage.insert({'url': url, 'html': html})
post_id2 = db.webpage.insert([{'url': url, 'html': html}, {'url': 'www.baidu.com', 'html': 'www.baidu.com~~~'}])
print(post_id1)
print(post_id2)

# 查询数据, 查询不到则返回None
print(db.webpage.find({'url': url}))  # 返回内存之地
print(db.webpage.find_one({'url': url}))

# mongodb的条件操作符
#    (>)  大于 - $gt
#    (<)  小于 - $lt
#    (>=)  大于等于 - $gte
#    (<= )  小于等于 - $lte


print('--查看全部--')
# 查询全部
for i in db.webpage.find():
    print(i)

print('--排序--')
# 排序 : 在MongoDB中使用sort()方法对数据进行排序，sort()方法可以通过参数指定排序的字段，并使用 1 和 -1 来指定排序的方式，其中 1 为升序，-1为降序。
for i in db.webpage.find().sort([("url", -1)]):
    print(i)

# 更新数据
db.webpage.update({'url': url}, {'$set': {"html": 'update后的Html============='}}, True, False)

# 语法
# db.webpage.update(
#    <query>,    #查询条件
#    <update>,    #update的对象和一些更新的操作符
#    {
#      upsert: <boolean>,    #如果不存在update的记录，是否插入
#      multi: <boolean>,        #可选，mongodb 默认是false, 只更新找到的第一条记录 . True有多条记录则不更新
#      writeConcern: <document>    #可选，抛出异常的级别。
#    }
# )

# 删除某条件下的记录, 删除某id 的记录, 删除所有记录
db.webpage.remove({'url': 'www.baidu.com'})
id = db.webpage.find_one({'url': 'http://example.webscraping.com/places/default/view/United-Kingdom-239'})
db.webpage.remove(id)
db.webpage.remove()

print('--查看数据--')
# 查询全部
for i in db.webpage.find():
    print(i)


