---
layout: poster
title: auto-google-translation
date: 2019-02-15 09:57:53
tags: [python,script]
---

# 字幕也疯狂

`观曲千首 不如操琴一曲` 试着做一个勤劳的字幕组小员工~

<img src="https://img1.doubanio.com/view/subject/l/public/s28051018.jpg" width="100" height="100%">

<!--more-->

```python
import pathlib
import gevent
from gevent.pool import Pool
from googletrans import Translator

global sou_file
global des_file
count = 0
global translator
translator = Translator(service_urls=['translate.google.cn'])

def tran_sub(line):
    global des_file
    global count
    global translator
    count += 1
    print("count,%d" % count)
    line = line.decode('utf-8')
    if line.startswith('Dialogue') and 'student speaking' not in line:
        des_file.write(line.encode('utf-8'))
        head_str,english_str = tuple(line.rsplit(',,', 1))
        chinese_str = translator.translate(english_str, dest='zh-CN').text
        print(chinese_str)
        c_line = ',,'.join([head_str,chinese_str+'\n']).replace('English', 'Chinese').replace('您', '你').encode('utf-8')
        des_file.write(c_line)
    else:
        des_file.write(line.encode('utf-8'))

def main():
    sou_path = u"/Users/eugene/workspace/translationCSAPP/subtitle/English/"
    des_path = u"/Users/eugene/workspace/translationCSAPP/subtitle/Chinese_English/"

    filename = u"Lecture 23  Concurrent Programming.ass"

    global sou_file
    global des_file
    sou_file = open(sou_path+filename, 'rb')
    des_file = open(des_path+filename, 'wb+')
    # pool = Pool(10)
    # pool.map(tran_sub, sou_file)
    threads = [gevent.spawn(tran_sub, line) for line in sou_file.readlines()]
    gevent.joinall(threads)
    sou_file.close()
    des_file.close()

if __name__ == '__main__':
    main()


# for line in lines:
#      if line.startswith('Dialogue:'):
#         parts = line.rsplit(',,', 1)
#         line = ',,'.join([parts[0], parts[1].lstrip().capitalize()])
#     f.write(line)
```

`说明：需要安装第三方库googletrans`

[第一个字幕作品](https://github.com/EugeneLiu/translationCSAPP)
[Bili链接](https://www.bilibili.com/video/av31289365)