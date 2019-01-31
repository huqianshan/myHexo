---
layout: poster
title: python-advanced
date: 2019-01-31 19:46:38
tags: [python]
---

# `Python`的高级烹饪方法

- 装饰器

![d4f6aa95acfdb33bcf3b9f87a5899396.jpg](https://i.loli.net/2019/01/31/5c52e16861ba4.jpg)

<!--more-->

## 给函数添加一个装饰器

### `需求`

你想在函数上添加一个包装器，增加额外的操作处理(比如日志、计时等)。

### `解决方法`

如果你想使用额外的代码包装一个函数，可以定义一个装饰器函数，例如：

```python
import time
from functools import wraps

def timethis(func):
    '''
    Decorator that reports the execution time.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper
```

### `说明`

一个装饰器就是一个函数，它接受一个函数作为参数并返回一个新的函数。

下面这样写其实效果是一样的：

```python
def countdown(n):
    pass
countdown = timethis(countdown)
```

强调的是装饰器并不会修改原始函数的参数签名以及返回值。 使用 *args 和 **kwargs 目的就是确保任何参数都能适用。 而返回结果值基本都是调用原始函数 func(*args, **kwargs) 的返回结果，其中func就是原始函数。

刚开始学习装饰器的时候，会使用一些简单的例子来说明，比如上面演示的这个。 不过实际场景使用时，还是有一些细节问题要注意的。 比如上面使用 @wraps(func) 注解是很重要的， 它能保留原始函数的元数据(下一小节会讲到)，新手经常会忽略这个细节。

### 参考链接
- [python-cookbook](https://python3-cookbook.readthedocs.io/zh_CN/latest/c09/p01_put_wrapper_around_function.html)