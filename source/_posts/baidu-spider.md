---
layout: poster
title: 百度图库爬虫脚本
date: 2018-06-07 20:51:50
tags: [python]
---
## 百度图库关键字爬虫脚本

#### 本章设计了一个基于Python的爬虫模块，可以根据用户自定义的关键词、待爬取图片数量，自动从百度图库中采集并依次保存图片数据。

#### 功能设计与分析

本模块为之后的模型训练提供数据集，属于数据采集部分。本模块的功能应解决以下问题：

1. 目标网站的图片数量足够多，车辆种类涵盖基本种类，且爬取难度不宜过高。 综合分析可知，百度图库能满足以上要求。所以采用百度图库为目标爬取网站。
2. 爬虫模块应能根据不同输入的危险车辆类别，爬取不同种类的车辆图片，所以要求爬虫模块能根据不同的车辆类别名称采集图片
3. 爬虫模块应该能够根据用户指定的数目采集图片，并依次编号分类
<!--more-->
#### Python语言爬虫相关库

> - `OS` 库             用于文件处理
> - `Re`  库             正则表达式库，用于解析网页结构、以及网址后缀前缀
> - `Json` 库           json文本格式库，用于处理返回的网页
> - `Socket` 库       处理网络连接超时问题
> - `Request`库      网络请求库，用于请求网页、存储图片库

![S_2.png](https://i.loli.net/2018/06/07/5b19279936b1f.png)



```python
#/*
#* @Author: hujinlei 
#* @Date: 2018-06-07 20:50:31 
#* @Last Modified by:   hjl 
#* @Last Modified time: 2018-06-07 20:50:31 
#*/
import os
import re
#import urllib
import json
import socket
import urllib.request
import urllib.parse
import urllib.error
# 设置超时
import time

timeout = 8
socket.setdefaulttimeout(timeout)

#!/usr/bin/env python
# -*- coding:utf-8 -*-



class Crawler:
    # 睡眠时长
    __time_sleep = 0.1
    __amount = 0
    __start_amount = 0
    __counter = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    # 获取图片url内容等
    # t 下载图片时间间隔
    def __init__(self, t=0.1):
        self.time_sleep = t

    # 获取后缀名
    def get_suffix(self, name):
        m = re.search(r'\.[^\.]*$', name)
        if m.group(0) and len(m.group(0)) <= 5:
            return m.group(0)
        else:
            return '.jpeg'

    # 获取referrer，用于生成referrer
    def get_referrer(self, url):
        par = urllib.parse.urlparse(url)
        if par.scheme:
            return par.scheme + '://' + par.netloc
        else:
            return par.netloc

        # 保存图片
    def save_image(self, rsp_data, word):
        if not os.path.exists("./" + word):
            os.mkdir("./" + word)
        # 判断名字是否重复，获取图片长度
        self.__counter = len(os.listdir('./' + word)) + 1
        for image_info in rsp_data['imgs']:

            try:
                time.sleep(self.time_sleep)
                suffix = self.get_suffix(image_info['objURL'])
                # 指定UA和referrer，减少403
                refer = self.get_referrer(image_info['objURL'])
                opener = urllib.request.build_opener()
                opener.addheaders = [
                    ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'),
                    ('Referer', refer)
                ]
                urllib.request.install_opener(opener)
                # 保存图片
                urllib.request.urlretrieve(image_info['objURL'], './' + word + '/' + str(self.__counter) + str(suffix))
            except urllib.error.HTTPError as urllib_err:
                print(urllib_err)
                continue
            except Exception as err:
                time.sleep(1)
                print(err)
                print("产生未知错误，放弃保存")
                continue
            else:
                print("图+1,已有" + str(self.__counter) + "张小图")
                self.__counter += 1
        return

    # 开始获取iii
    def get_images(self, word='iron man'):
        search = urllib.parse.quote(word)
        # pn int 图片数
        pn = self.__start_amount
        while pn < self.__amount:
            url = 'http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word=' + search + '&cg=girl&pn=' + str(
                pn) + '&rn=60&itg=0&z=0&fr=&width=&height=&lm=-1&ic=0&s=0&st=-1&gsm=1e0000001e'
            # 设置header防ban
            try:
                time.sleep(self.time_sleep)
                req = urllib.request.Request(url=url, headers=self.headers)
                page = urllib.request.urlopen(req)
                print(page)
                rsp = page.read().decode('unicode_escape')
            except UnicodeDecodeError as e:
                print(e)
                print('-----UnicodeDecodeErrorurl:', url)
            except urllib.error.URLError as e:
                print(e)
                print("-----urlErrorurl:", url)
            except socket.timeout as e:
                print(e)
                print("-----socket timout:", url)
            else:
                # 解析json
                rsp_data = json.loads(rsp)
                self.save_image(rsp_data, word)
                # 读取下一页
                print("下载下一页")
                pn += 60
            finally:
                page.close()
        print("下载任务结束")
        return
    def start(self, word, spider_page_num=1, start_page=1):
        """
        爬虫入口
        :param word: 抓取的关键词
        :param spider_page_num: 需要抓取数据页数 总抓取图片数量为 页数x60
        :param start_page:起始页数
        :return:
        """
        self.__start_amount = (start_page - 1) * 60
        self.__amount = spider_page_num * 60 + self.__start_amount
        self.get_images(word)


if __name__ == '__main__':
    crawler = Crawler(0.05)  # 抓取延迟为 0.05

    # crawler.start('iron', 10, 2)  # 抓取关键词为 “uestc”，总数为 1 页（即总共 1*60=60 张），开始页码为 2
    crawler.start('uestc', 1, 1)  # 抓取关键词为 “uestc”，总数为 10 页（即总共 10*60=600 张），起始抓取的页码为 1
    # crawler.start('capatain', 5)  # 抓取关键词为 “uestc”，总数为 5 页（即总共 5*60=300 张）
```

