---
layout: poster
title: crapy-summary
date: 2019-01-28 20:18:15
tags:
---

# 爬虫模块化总结 （一）

- 读取链接部分
- 解析链接
- 参数配置
- 爬虫框架
- 存储模块

## 读取链接

### 1.1 从文档从直接读取目标url

  ```python
 def txt_to_dic(name):
    filename=name
    dic=[]
    with open(filename,'r',encoding='utf-8') as file:
            for line in file:
                line=line.strip('\n')
                dic.append(line)
    print('%s Txt loads fine'%(name))
    print("url has %s "%(len(dic)))
    return dic
  ```

  `说明:`  输入 `name`文件名; 输出 `dic` 以列表形式的url;

## 参数配置

### 3.1 配置随机`user_agenet`

  ```python
  import random
  def get_user_agent():
    user_agent = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        ]
    return random.choice(user_agent)
  ```

## 爬虫框架

### 4.1 `class` 类框架

```python
class Crawler:
    __time_sleep = 0.1     # 睡眠时长
    __amount = 0           # 爬取数量
    __start_amount = 0     # 开始数目
    __counter = 0          # 当前计数
    __headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    # 默认初始化
    def __init__(self, t=0.1):
        self.time_sleep = t

    # 保存图片
    def save_image(self, rsp_data, word):
        return

    # 开始获取图片
    # word 存储url的文件名 不含后缀名
    def get_images(self, word='urls_drawings'):
        # 得到资源的url
        image_lists=[]
        image_lists=txt_to_dic(word+'.txt')
        # 从指定数目开始
        pn = self.__start_amount
        while self.__counter < self.__amount:
            url=image_lists[pn]
            # 设置header防ban
            try:
                time.sleep(self.time_sleep)
                headers={'User-Agent': get_user_agent()}
                ir = requests.get(url,headers=headers)
                ir.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(e)
                print('-----HTTPError:', url)
            except requests.exceptions.ConnectionError as e:
                print(e)
                print("-----Connection error:", url)
            except requests.exceptions.ProxyError as e:
                print(e)
                print("-----proxy error:", url)
            except requests.exceptions.InvalidURL as e:
                print(e)
                print("-----Url invalid:",url)
            except requests.exceptions.ConnectTimeout as e:
                print(e)
                print("-----ConnectTimeOut:",e)
            else:
                # 没有错误时下载图片
                # flag ： 此处待改进 检测到`502`错误应该重试3次
                if ir.status_code == requests.codes.ok:
                    self.save_image(ir.content, word)
            finally:
                ir.close()
                if self.__counter==self.__amount-1:
                    print(url)
                pn += 1
        print("下载任务结束")
        return
    def start(self, word, spider_page_num=100,start_amout=0):
        """
        爬虫入口
        :param word: 抓取的分类关键词
        :param spider_page_num: 需要抓取抓取图片数量
        :return:
        """
        self.__start_amount = start_amout
        self.__amount = spider_page_num
        self.get_images(word)


if __name__ == '__main__':
    crawler = Crawler(0.05)  # 抓取延迟为 0.05

    crawler.start('urls_drawings',1000,102)
```

