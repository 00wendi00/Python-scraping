# scraping
Basic knowledge of Scraping


根据<用python写网络爬虫>一书,  对数据抓取的入门知识的练习.
环境:win10 , python3.5.2


以下为文件说明 :

-------------------- base --------------------

crawling1           网络爬虫 -- robots.txt, 网站地图, 网站大小, 使用技术, 所有者; 下载网页,网站地图爬虫.ID遍历爬虫,链接爬虫. 寻找网站所有者

crawling2           数据抓取 . Soup , 补全prettify , 定位find

ScrapeCall          回调类 -- 扩展 : 重写了__init__和__call__方法 --> 将scrape的数据写入csv文件中

test_contrast       正则, soup, Lxml 三种抓取方式进行对比 . 正则和Lxml相当. 基本是soup的6倍.

test_lxml           Lxml.html 的使用

Throttle            推迟调用线程的运行 -- time.sleep()


-------------------- cache --------------------

DiskCache           磁盘缓存 . 将下载的html存入磁盘文件中

Downloader          为链接爬虫添加缓存支持 -- 存入磁盘文件

link_crawler文件    Crawl from the given seed URL following links matched by link_regex

test


-------------------- mongoDB --------------------

MongoCache          基于MongoDB的缓存 . 压缩解压, 索引

test1               -- mongodb, python CRUD , 排序, 多级元素操作

test2               -- mongodb, python 多级元素操作, 查询修改.

test3               测试 MongoCache

test4               抓取网页, 存入MongoDB中


-------------------- multi_thread --------------------

AlexaCallback       回调类 : 读取CSV文件.  下载读取zip文件

link_crawler        串行下载500个页面, 缓存至MongoDB中

test1               测试 link_crawler -- 串行下载500个页面, 缓存至MongoDB中

thread_test         1.多线程下载网页, threading  2.循环创建线程  3.队列的基本操作 -- 线程安全.