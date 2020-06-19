---
layout: poster
title: Python的高级烹饪方法
date: 2020-01-31 19:46:38
tags: 
- python
---
<!-- TOC -->

- [`Python`的高级烹饪方法](#python的高级烹饪方法)
  - [给函数添加一个装饰器](#给函数添加一个装饰器)
    - [`需求`](#需求)
    - [`解决方法`](#解决方法)
    - [`说明`](#说明)
    - [定义一个带参数的装饰器](#定义一个带参数的装饰器)
    - [参考链接](#参考链接)
  - [`with`语句和`ContexManager`上下文管理器](#with语句和contexmanager上下文管理器)
    - [上下文管理器 `Context Manager`](#上下文管理器-context-manager)
    - [`with`语法](#with语法)
    - [实例：自定义文件打开类](#实例自定义文件打开类)
    - [内置库`contextlib`](#内置库contextlib)
    - [`pep`参考链接](#pep参考链接)

<!-- /TOC -->

# 1. `Python`的高级烹饪方法

- 装饰器
- `with`语句和`ContexManager`上下文管理器

<!--more-->

## 1.1. 给函数添加一个装饰器

### 1.1.1. `需求`

你想在函数上添加一个包装器，增加额外的操作处理(比如日志、计时等)。

### 1.1.2. `解决方法`

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

### 1.1.3. `说明`

一个装饰器就是一个函数，它接受一个函数作为参数并返回一个新的函数。

下面这样写其实效果是一样的：

```python
def countdown(n):
    pass
countdown = timethis(countdown)
```

强调的是装饰器并不会修改原始函数的参数签名以及返回值。 使用 *args 和 **kwargs 目的就是确保任何参数都能适用。 而返回结果值基本都是调用原始函数 func(*args, **kwargs) 的返回结果，其中func就是原始函数。

刚开始学习装饰器的时候，会使用一些简单的例子来说明，比如上面演示的这个。 不过实际场景使用时，还是有一些细节问题要注意的。 比如上面使用 @wraps(func) 注解是很重要的， 它能保留原始函数的元数据(下一小节会讲到)，新手经常会忽略这个细节。

装饰器本质上是一个Python函数，它可以让其他函数在不需要做任何代码变动的前提下增加额外功能，装饰器的返回值也是一个函数对象。它经常用于有切面需求的场景，比如：插入日志、性能测试、事务处理、缓存、权限校验等场景。装饰器是解决这类问题的绝佳设计，有了装饰器，我们就可以抽离出大量与函数功能本身无关的雷同代码并继续重用。概括的讲，装饰器的作用就是为已经存在的对象添加额外的功能。

### 1.1.4. 定义一个带参数的装饰器

```python
from functools import wraps
import logging

def logged(level, name=None, message=None):
    """
    Add logging to a function. level is the logging
    level, name is the logger name, and message is the
    log message. If name and message aren't specified,
    they default to the function's module and name.
    """
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)
        return wrapper
    return decorate

# Example use
@logged(logging.DEBUG)
def add(x, y):
    return x + y

@logged(logging.CRITICAL, 'example')
def spam():
    print('Spam!')
```

### 1.1.5. 参考链接

- [python-cookbook](https://python3-cookbook.readthedocs.io/zh_CN/latest/c09/p01_put_wrapper_around_function.html)

## 1.2. `with`语句和`ContexManager`上下文管理器

### 1.2.1. 上下文管理器 `Context Manager`

上下文管理器是指在一段代码执行之前执行一段代码，用于一些预处理工作；执行之后再执行一段代码，用于一些清理工作。比如打开文件进行读写，读写完之后需要将文件关闭。又比如在数据库操作中，操作之前需要连接数据库，操作之后需要关闭数据库。在上下文管理协议中，有两个方法`__enter__`和`__exit__`，分别实现上述两个功能

### 1.2.2. `with`语法

```python
with EXPR as VAR:
    BLOCK
```

这里就是一个标准的上下文管理器的使用逻辑，稍微解释一下其中的运行逻辑：

（1）执行EXPR语句，获取上下文管理器（Context Manager）

（2）调用上下文管理器中的__enter__方法，该方法执行一些预处理工作。

（3）这里的as VAR可以省略，如果不省略，则将__enter__方法的返回值赋值给VAR。

（4）执行代码块BLOCK，这里的VAR可以当做普通变量使用。

（5）最后调用上下文管理器中的的__exit__方法。

（6）`__exit__`方法有三个参数：`exc_type, exc_val, exc_tb`。如果代码块BLOCK发生异常并退出，那么分别对应异常的`type、value` 和 `traceback`。否则三个参数全为None。

（7）`__exit__`方法的返回值可以为True或者False。如果为True，那么表示异常被忽视，相当于进行了`try-except`操作；如果为False，则该异常会被重新raise。

### 1.2.3. 实例：自定义文件打开类

```python
# 自定义打开文件操作
class MyOpen(object):

    def __init__(self, file_name):
        """初始化方法"""
        self.file_name = file_name
        self.file_handler = None
        return

    def __enter__(self):
        """enter方法，返回file_handler"""
        print("enter:", self.file_name)
        self.file_handler = open(self.file_name, "r")
        return self.file_handler

    def __exit__(self, exc_type, exc_val, exc_tb):
        """exit方法，关闭文件并返回True"""
        print("exit:", exc_type, exc_val, exc_tb)
        if self.file_handler:
            self.file_handler.close()
        return True

# 使用实例
with MyOpen("python_base.py") as file_in:
    for line in file_in:
        print(line)
        raise ZeroDivisionError
# 代码块中主动引发一个除零异常，但整个程序不会引发异常
```

### 1.2.4. 内置库`contextlib`

Python提供内置的contextlib库，使得上下文管理器更加容易使用。其中包含如下功能：

1. 装饰器contextmanager。该装饰器将一个函数中yield语句之前的代码当做__enter__方法执行，yield语句之后的代码当做__exit__方法执行。同时yield返回值赋值给as后的变量。

```python
@contextlib.contextmanager
def open_func(file_name):
    # __enter__方法
    print('open file:', file_name, 'in __enter__')
    file_handler = open(file_name, 'r')

    yield file_handler

    # __exit__方法
    print('close file:', file_name, 'in __exit__')
    file_handler.close()
    return

with open_func('python_base.py') as file_in:
    for line in file_in:
        print(line)
```

2.`closing`类。该类会自动调用传入对象的`close`方法。使用实例如下：

```python
class MyOpen2(object):
    def __init__(self, file_name):
        """初始化方法"""
        self.file_handler = open(file_name, "r")
        return

    def close(self):
        """关闭文件，会被自动调用"""
        print("call close in MyOpen2")
        if self.file_handler:
            self.file_handler.close()
        return

with contextlib.closing(MyOpen2("python_base.py")) as file_in:
    pass
```

```python
class closing(object):
    """Context to automatically close something at the end of a block."""
    def __init__(self, thing):
        self.thing = thing
    def __enter__(self):
        return self.thing
    def __exit__(self, *exc_info):
        self.thing.close()
```

`closing`类的`__exit__`方法自动调用传入的thing的`close`方法。

### 1.2.5. `pep`参考链接

- [python-dev](https://www.python.org/dev/peps/pep-0343/)
