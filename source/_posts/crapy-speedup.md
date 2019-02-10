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

## 2. 多进程 `Bug`

ProcessPoolExecutor 的典型用法如下：

```python
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor() as pool:
    ...
    do work in parallel using pool
    ...
```

其原理是，一个 `ProcessPoolExecutor`创建N个独立的Python解释器， N是系统上面可用CPU的个数。你可以通过提供可选参数给 `ProcessPoolExecutor(N)` 来修改 处理器数量。这个处理池会一直运行到with块中最后一个语句执行完成， 然后处理池被关闭。不过，程序会一直等待直到所有提交的工作被处理完成。

被提交到池中的工作必须被定义为一个函数。有两种方法去提交。 如果你想让一个列表推导或一个 map() 操作并行执行的话，可使用 `pool.map()` :

```python
# A function that performs a lot of work


def work(x):
    ...
    return result


# Nonparallel code
results = map(work, data)

# Parallel implementation
with ProcessPoolExecutor() as pool:
    results = pool.map(work, data)
另外，你可以使用 pool.submit() 来手动的提交单个任务：

# Some function
def work(x):
    ...
    return result

with ProcessPoolExecutor() as pool:
    ...
    # Example of submitting work to the pool
    future_result = pool.submit(work, arg)

    # Obtaining the result (blocks until done)
    r = future_result.result()
    ...
```

如果你手动提交一个任务，结果是一个 Future 实例。 要获取最终结果，你需要调用它的 result() 方法。 它会阻塞进程直到结果被返回来。

如果不想阻塞，你还可以使用一个回调函数，例如：

```python
def when_done(r):
    print('Got:', r.result())

with ProcessPoolExecutor() as pool:
     future_result = pool.submit(work, arg)
     future_result.add_done_callback(when_done)
```

回调函数接受一个 Future 实例，被用来获取最终的结果（比如通过调用它的result()方法）。 尽管处理池很容易使用，在设计大程序的时候还是有很多需要注意的地方，如下几点：

这种并行处理技术只适用于那些可以被分解为互相独立部分的问题。
被提交的任务必须是简单函数形式。对于方法、闭包和其他类型的并行执行还不支持。
函数参数和返回值必须兼容pickle，因为要使用到进程间的通信，所有解释器之间的交换数据必须被序列化
被提交的任务函数不应保留状态或有副作用。除了打印日志之类简单的事情，
一旦启动你不能控制子进程的任何行为，因此最好保持简单和纯洁——函数不要去修改环境。

在Unix上进程池通过调用 fork() 系统调用被创建，
它会克隆Python解释器，包括fork时的所有程序状态。 而在Windows上，克隆解释器时不会克隆状态。 实际的fork操作会在第一次调用 pool.map() 或 pool.submit() 后发生。

当你混合使用进程池和多线程的时候要特别小心。
你应该在创建任何线程之前先创建并激活进程池（比如在程序启动的main线程中创建进程池）

### `参考链接`

1. [简单并行编程](https://python3-cookbook.readthedocs.io/zh_CN/latest/c12/p08_perform_simple_parallel_programming.html)

2. [futures入门及内部原理](https://juejin.im/post/5b1e36476fb9a01e4a6e02e4)

3. [廖雪峰-多进程](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431927781401bb47ccf187b24c3b955157bb12c5882d000)

4. [multiprocessing's bug](https://stackoverflow.com/questions/41385708/multiprocessing-example-giving-attributeerror)