---
layout: poster
title: crapy-speedup
date: 2019-01-30 19:46:13
tags: [python]
---

# (二) 让爬虫飞起来(`crapy-speedup`)

- 多线程 `multithreading`$\to$`threading`库
- 多进程 `multiprocess`
- 协程 `gevent`
- 异步 `asyio`

![tumblr_mvl7699VoR1rqg00io8_r1_250.gif](https://i.loli.net/2019/01/30/5c518f78e69c3.gif)
<!--more-->

`关键词:` `同步` `锁` 

## 1. 多线程 `multithreading`

Python中的线程会在一个单独的系统级线程中执行（比如说一个 POSIX 线程或者一个 Windows 线程），这些线程将由操作系统来全权管理。

### 线程的启动与停止

可以通过继承`Thread`类来实现线程操作

```python
from threading import Thread

def run_time(func):
    def wrapper(*args, **kw):
        start = time.time()
        func(*args, **kw)
        end = time.time()
        print('running {:.3f}'.format(end-start),' s')
    return wrapper

class CountdownThread(Thread):
    def __init__(self, n):
        super().__init__()
        # do your own inititation
        self.__thread_num = n

    def do_something(self):
        pass

    def run(self):
        threads=[]
        print("threads num is ",self.__thread_num)
        for _ in range(self.__thread_num):
            th=Thread(target=self.do_something,args=(,))
            th.start()
            threads.append(th)
        for th in threads:
            th.join(20)
        print("下载任务结束")

%%prun
if __name__ == '__main__':
    crawler = Crawler(55)  # 抓取线程数为 55
    crawler.run()
```

如果线程执行一些像I/O这样的阻塞操作，那么通过轮询来终止线程将使得线程之间的协调变得非常棘手。比如，如果一个线程一直阻塞在一个I/O操作上，它就永远无法返回，也就无法检查自己是否已经被结束了。要正确处理这些问题，你需要利用超时循环来小心操作线程。 例子如下：

```python
class IOTask:
    def terminate(self):
        self._running = False

    def run(self, sock):
        # sock is a socket
        sock.settimeout(5)        # Set timeout period
        while self._running:
            # Perform a blocking I/O operation w/ timeout
            try:
                data = sock.recv(8192)
                break
            except socket.timeout:
                continue
            # Continued processing
            ...
        # Terminated
        return
```

`参考链接：` [并发编程](https://python3-cookbook.readthedocs.io/zh_CN/latest/c12/p01_start_stop_thread.html)