---
title: flask_demo
date: 2020-03-23 21:04:15
tags:
- Python
- Flask
---

## 编写`flask`服务器应用程序

### 连接`非结构化`数据库
<!--more-->
### 生成访问日志

## 配置`gunicore server`

gunicorn是一个python编写的高效的WSGI HTTP服务器，gunicorn使用pre-fork模型（一个master进程管理多个child子进程），使用gunicorn的方法十分简单：

```python
gunicorn --workers=9 server:app --bind 127.0.0.1:8000
```

文档说明使用（2 * cpu核心数量）+1个worker，还要传入一个兼容wsgi app的start up方法

```python
#import multiprocessing
workers = 5   #进程数   # 定义同时开启的处理请求的进程数量，根据网站流量适当调整

threads = 8 #指定每个进程开启的线程数
worker_class = "gevent"   # 采用gevent库，支持异步处理请求，提高吞吐量
bind = "0.0.0.0:80"

backlog = 512
timeout = 30
keepalive=8
daemon=True

loglevel = 'info' #日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'    #设置gunicorn访问日志格式，错误日志无法设置

accesslog='/home/www/flask_blog/logs/guni_access.log'
errorlog='/home/www/flask_blog/logs/guni_error.log'

```

暂停与重启

- `pstree -ap | grep gunicorn` 获取进程树与父进程`PID`

- `kill -HUP ParentPID` 重启`gunicorn`

- `kill -TERM ParentPID` 关闭`gunicorn`

### `gevent`

### `async`

## `Server Proxy: nginx`

## 部署

### `Supervisor` 停用，尚未有`Python3.x`版本

Sueprvisor是Linux上的一个可以监控应用和进程的工具，我们用它来作为守护进程，自动化地启动和停止应用。

## `Docker`

[]()

## 性能测试

### `wrk`

`wrk -c 100 -t 12 -d 5s http://127.0.0.1:8000/todo`

### 参考文献

- [**强烈推荐阅读**](https://zhuanlan.zhihu.com/p/25038203)
