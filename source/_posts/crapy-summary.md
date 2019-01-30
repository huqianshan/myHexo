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
- 辅助模块

<!--more-->

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

## 解析链接`urllib.parse`

### 2.1 获取资源格式类型

```python
import re
def get_suffix(name):
    m = re.search(r'\.[^\.]*$', name)
    if m.group(0) and len(m.group(0)) <= 5:
        return m.group(0)
    else:
        return '.jpg'
```

`说明` 当链接url`name`中的最后一个`.`的匹配存在 且小于5个字母，则匹配成功 
        否则默认为`.jpg`

### 2.2 直接获取文件名及后缀名

#### a `split`方法

```python
def get_name_suffix(name):
    return name.split('/')[-1]
```

#### b `os.path`方法

```python
import os
def get_os_name_suffix(name):
    return os.path.basename(name)
```

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

### 3.2 `Cookie`和`timeout`

```python
jar = requests.cookies.RequestsCookieJar()
jar.set('tasty_cookie', 'yum', domain='httpbin.org', path='/cookies')
r = requests.get(url, cookies=jar)
```

`Cookie` 的返回对象为 `RequestsCookieJar`，它的行为和字典类似，但接口更为完整，适合跨域名跨路径使用。你还可以把 `Cookie Jar` 传到 `Requests` 中.

也可以直接生成字典`dict(status='value')` 传递给`requests`

```python
requests.get('http://github.com', timeout=0.001)
```

`说明：`  requests 在经过以 timeout 参数设定的秒数时间之后停止等待响应。基本上所有的生产代码都应该使用这一参数。如果不使用，你的程序可能会永远失去响应：

>timeout 仅对连接过程有效，与响应体的下载无关。 timeout 并不是整个下载响应的时间限制，而是如果服务器在 timeout 秒内没有应答，将会引发一个异常（更精确地说，是在 timeout 秒内没有从基础套接字上接收到任何字节的数据时）If no timeout is specified explicitly, requests do not time out.

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

### 4.2 `Session`会话

```python
session = requests.Session()
session.headers.update({'x-test': 'true'})
```

`说明:`会话对象让你能够跨请求保持某些参数。它也会在同一个 Session 实例发出的所有请求之间保持 cookie， 期间使用 urllib3 的 connection pooling 功能。所以如果你向同一主机发送多个请求，底层的 TCP 连接将会被重用，从而带来显著的性能提升。

任何你传递给请求方法的字典都会与已设置会话层数据合并。方法层的参数覆盖会话的参数。
不过需要注意，就算使用了会话，方法级别`(函数参数)`的参数也不会被跨请求保持。

如果你要手动为会话添加 `cookie`，就使用 [Cookie utility](http://docs.python-requests.org/zh_CN/latest/api.html#api-cookies) 函数 来操纵 `Session.cookies`。

### 4.3 `Ip`代理池

```python
proxies = {
  "http": "http://10.10.1.10:3128",
  "https": "http://10.10.1.10:1080",
}

requests.get("http://example.org", proxies=proxies)
```

## 存储模块

### 5.1 存储文件

```python
def save_image(self, url,rsp_data, word):
    # if directory not exists
    if not os.path.exists("./" + word):
        os.mkdir("./" + word)
    # current existed file number
    self.__counter = len(os.listdir('./' + word)) + 1  
    time.sleep(self.time_sleep)
    # get file name
    name="./"+word+"/"+str(self.__counter)+get_suffix(url)
    with open(name, 'wb') as file:
        file.write(rsp_data) 
    print("图+1,已有" + str(self.__counter) + "张图片")
    return
```

### 5.2 原始套接字响应内容

```python
# must set stream=true
r = requests.get('https://api.github.com/events', stream=True)
with open(filename, 'wb') as fd:
    for chunk in r.iter_content(chunk_size):
        fd.write(chunk)
```

`说明：`  默认情况下，发起请求会同时下载响应头和响应体（就是响应内容）

如果将stream=True 则会推迟响应内容的下载

这里就是：满足某种条件才去下载

```python
if int(r.headers['content-length']) < TOO_LONG:

    content = r.content
```

在请求中把 stream 设为 True，Requests 无法将连接释放回连接池,除非消耗了所有的数据，或者调用了 Response.close。这样会带来连接效率低下的问题。如果在使用 stream=True 的同时还在部分读取请求的 body（或者完全没有读取 body），那么就应该使用 with 语句发送请求，这样可以保证请求一定会被关闭

## 辅助模块

### 6.1 `PIL`和`IO`库

```python
from PIL import Image
from io import BytesIO

i = Image.open(BytesIO(r.content))
```

`说明：` 以请求返回的二进制数据`r.content`创建一张图片，你可以使用如上代码

### 6.2 实时显示下载进度及下载时间

```python
import requests
from contextlib import closing

class ProgressBar(object):
    def __init__(self, title, count=0.0, run_status=None, fin_status=None, total=100.0,    unit='', sep='/', chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.statue)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status, self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)

def download_progress():
    start=time.time()
    with closing(requests.get("https://i.imgur.com/YjVeqM9h.jpg", stream=True)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        progress = ProgressBar("downloading", total=content_size, unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
        # chunk_size = chunk_size < content_size and chunk_size or content_size
        with open('./file.mp3', "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                progress.refresh(count=len(data))
    end=time.time()
    print("time costs {:.3f} secs".format(end-start))

if __name__ == '__main__':
    download_progress()
```

![ba93659578d934af93a9411dd6735931.gif](https://i.loli.net/2019/01/28/5c4f0f52a4f45.gif)

## 参考链接

1. [**request basic**](http://docs.python-requests.org/zh_CN/latest/user/quickstart.html)
2. [**request advanced**](http://docs.python-requests.org/zh_CN/latest/user/advanced.html#advanced)