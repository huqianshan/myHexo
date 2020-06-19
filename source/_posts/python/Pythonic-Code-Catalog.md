---
title: Pythonic-Code-Catalog
date: 2020-02-10 13:09:50
tags: 
- python
---
<!-- TOC -->

- [`Python`高级用法目录](#python高级用法目录)
  - [`Built-in Objects`语义部分](#built-in-objects语义部分)
    - [双值交换](#双值交换)
    - [容器](#容器)
    - [元组拆包](#元组拆包)
    - [容器的选择](#容器的选择)
      - [数组`array.array`](#数组arrayarray)
      - [内存视图（`memoryview`）](#内存视图memoryview)
  - [函数式编程与高阶函数](#函数式编程与高阶函数)
      - [双向队列以及其他形式的队列](#双向队列以及其他形式的队列)
    - [迭代器](#迭代器)
    - [生成器 `yield`](#生成器-yield)
    - [`lambda map(func, *iterables) fileter`等](#lambda-mapfunc-iterables-fileter等)
  - [语法部分](#语法部分)
    - [上下文管理器](#上下文管理器)
    - [装饰器](#装饰器)
      - [常见的内置装饰器](#常见的内置装饰器)
    - [`getattr`](#getattr)
    - [正则表达式](#正则表达式)
  - [`Objected-Oriented-Programming`](#objected-oriented-programming)

<!-- /TOC -->
<!-- more -->
## `Python`高级用法目录

### `Built-in Objects`语义部分

#### 双值交换

```python
```

```python
a,b=b,a
a,b,c=['a','b','c']
```

#### 容器

切片(slice):

- 切片： `[begin:end:len]` 左开右闭原则；Python 会调用
`seq.__getitem__(slice(start, stop, step))`。

- 多维切片: 如果要得到 `a[i, j]` 的值，Python 会调用 `a.__getitem__((i, j))`。

  - NumPy 中，`...` 用作多维数组切片的快捷方式。如果 x 是四维数组，那
么` x[i, ...]` 就是 `x[i, :, :, :]` 的缩写

容器：

- 容器序列：`list、tuple 和 collections.deque` 这些序列能存放不同类型的
数据

- 扁平序列: `str、bytes、bytearray、memoryview 和 array.array`这类
序列只能容纳一种类型

容器序列存放的是它们所包含的任意类型的对象的引用，而扁平序列
里存放的是值而不是引用

序列

- 可变序列 `list、bytearray、array.array、collections.deque  memoryview`

- 不可变序列 `tuple、str 和 bytes`

  - 序列的`*` 操作问题
![sss](python_1_1_collections_abc.png)

#### 元组拆包

- 元组拆包可以应用到任何可迭代对象上

- 用 `*` 来表示忽略多余的元素 `a,*_,c=s`

  - 用 `*` 运算符把一个可迭代对象拆开作为函数的参数：`t = (20, 8);divmod(*t)`

  - 用 `*` 处理剩下的元素,平行赋值 `a, b, *rest = range(5)`

- 嵌套元组拆包

```python
for name, cc, pop, (latitude, longitude) in metro_areas:
```

#### 容器的选择

##### 数组`array.array`

- 更省空间，字节存储，而非`list`的对象存储

- 数组支持所有跟可变序列有关的操作，包括 `.pop、.insert 和
.extend`。另外，数组还提供从文件读取和存入文件的更快的方法，如
`.frombytes` 和 `.tofile`

- 创建数组需要一个类型码，用来表示在底层的 C 语言应该存放怎样的数据类型。
比如 b 类型码代表的是有符号的字符（signed char），因此 array('b') 创建出的
数组就只能存放一个字节大小的整数，范围从 -128 到 127，这样在序列
很大的时候，我们能节省很多空间。

- array.fromfile 从一个二进制文件里读出 1000 万个
双精度浮点数只需要 0.1 秒，这比从文本文件里读取的速度要快 60
倍，因为后者会使用内置的 float 方法把每一行文字转换成浮点数

- 使用 array.tofile 写入到二进制文件，比以每行一个浮点数的
方式把所有数字写入到文本文件要快 7 倍

- 另外，1000 万个这样的数
在二进制文件里只占用 80 000 000 个字节（每个浮点数占用 8 个字节，
不需要任何额外空间），如果是文本文件的话，我们需要 181 515 739
个字节。

- 另外一个快速序列化数字类型的方法是使用
pickle（https://docs.python.org/3/library/pickle.html)模
块。pickle.dump 处理浮点数组的速度几乎跟 array.tofile 一
样快。不过前者可以处理几乎所有的内置数字类型，包含复数、嵌
套集合，甚至用户自定义的类。

##### 内存视图（`memoryview`）

- `memoryview `是一个内置类，它能让用户在不复制内容的情况下操作同
一个数组的不同切片

- `memoryview.cast` 会把同一块内存里的内容打包
成一个全新的 `memoryview` 对象给你。

### 函数式编程与高阶函数

##### 双向队列以及其他形式的队列

- 双向队列`collections.deque`是一个线程安全、可以快速从两
端添加或者删除元素的数据类型。

#### 迭代器

迭代器是一个表示数据流的对象；这个对象每次只返回一个元素。

`Python` 迭代器必须支持 `__next__()` 方法；这个方法不接受参数，并总是返回数据流中的下一个元素。如果数据流中没有元素，`__next__()` 会抛出 `StopIteration` 异常。

内置的 `iter()` 函数接受任意对象并试图返回一个迭代器来输出对象的内容或元素，并会在对象不支持迭代的时候抛出 `TypeError` 异常。`Python` 有几种内置数据类型支持迭代，最常见的就是列表和字典。如果一个对象能生成迭代器，那么它就会被称作 `iterable`。

```python
for i in iter(obj):
    print(i)

for i in obj:
    print(i)

#可以用 list() 或 tuple() 这样的构造函数把迭代器具体化成列表或元组:
L = [1, 2, 3]
iterator = iter(L)
t = tuple(iterator)
#t (1, 2, 3)
```

生成器表达式背后遵守了迭代器协
议，可以逐个地产出元素，而不是先建立一个完整的列表，然后再把这
个列表传递到某个构造函数里。

- [生成器表达式和列表推导式的参考链接](https://docs.python.org/zh-cn/3/howto/functional.html#generator-expressions-and-list-comprehensions)
- [`doc-python-link`](https://docs.python.org/zh-cn/3/library/stdtypes.html#iterator-types)

#### 生成器 `yield`

生成器是一类用来简化编写迭代器工作的特殊函数。普通的函数计算并返回一个值，而生成器返回一个能返回数据流的迭代器。

毫无疑问，你已经对如何在 Python 和 C 中调用普通函数很熟悉了，这时候函数会获得一个创建局部变量的私有命名空间。当函数到达 return 表达式时，局部变量会被销毁然后把返回给调用者。之后调用同样的函数时会创建一个新的私有命名空间和一组全新的局部变量。但是，如果在退出一个函数时不扔掉局部变量会如何呢？如果稍后你能够从退出函数的地方重新恢复又如何呢？这就是生成器所提供的；他们可以被看成可恢复的函数。

当你调用一个生成器函数，它并不会返回单独的值，而是返回一个支持生成器协议的生成器对象。当执行 yield 表达式时，生成器会输出 i 的值，就像 return 表达式一样。yield 和 return 最大的区别在于，到达 yield 的时候生成器的执行状态会挂起并保留局部变量。在下一次调用生成器 __next__() 方法的时候，函数会恢复执行。

**Python 会忽略代码里 []、{} 和 () 中的换行**，因此如果你的代码里
有多行的列表、列表推导、生成器表达式、字典这一类的，可以省
略不太好看的续行符 \

#### `lambda map(func, *iterables) fileter`等

`lambda`：能嵌入到其他表达式当中的匿名函数（闭包）。

```python
map(lambda x: x*x, [y for y in range(10)] )
```

`map`它可以将一个函数映射到一个可枚举类型上面。也就是将函数 f 依次套用在 a 的每一个元素上面。

“你会发现自己如果能将「遍历列表，给遇到的每个元素都做某种运算」的过程从一个循环里抽象出来成为一个函数 map，然后用 lambda 表达式将这种运算作为参数传给 map 的话，考虑事情的思维层级会高出一些来，需要顾及的细节也少了一点。”

也就是将一个循环过程用一行map函数实现，并将lambda函数作为一个参数传递进去。

1. Python 之中，类似能用到 lambda 表达式的「高级」函数还有 `reduce`、`filter` 等高级函数。

2. 这种能够接受一个函数作为参数的函数叫做「高阶函数」（higher-order function），是来自函数式编程（functional programming）的思想。

- 它的第一个重要意义是可以在表达式当中直接定义一个函数，而不需要将定义函数和表达式分开，这样有助于将逻辑用更紧凑的方式表达出来。

- 它的第二个重要意义是引入了闭包。基本上来说常见的支持lambda表达式的语言里，不存在不支持闭包的lambda表达式；从函数式编程的角度来说，支持闭包也是很重要的。闭包是指将当前作用域中的变量通过值或者引用的方式封装到lambda表达式当中，成为表达式的一部分，它使你的lambda表达式从一个普通的函数变成了一个带隐藏参数的函数。

- 它的第三个重要意义（如果有的话）是允许函数作为一个对象来进行传递。某些语言由于历史原因，只有匿名函数可以作为对象传递，而具名函数不可以，比如PHP。
  
- [参考连接](https://www.zhihu.com/question/20125256)

### 语法部分

#### 上下文管理器

参见 [`with`语句和`ContexManager`上下文管理器](https://huqianshan.github.io/articles/python%2Fpython-advanced#with%E8%AF%AD%E5%8F%A5%E5%92%8Ccontexmanager%E4%B8%8A%E4%B8%8B%E6%96%87%E7%AE%A1%E7%90%86%E5%99%A8)

#### 装饰器

参见 [装饰器](https://huqianshan.github.io/articles/python%2Fpython-advanced#%E7%BB%99%E5%87%BD%E6%95%B0%E6%B7%BB%E5%8A%A0%E4%B8%80%E4%B8%AA%E8%A3%85%E9%A5%B0%E5%99%A8)

##### 常见的内置装饰器

- `@unique`装饰器可以帮助我们检查保证没有重复值。

#### `getattr`

`getattr()` 函数用于返回一个对象属性值。`getattr(object, name[, default])`

- object -- 对象。
- name -- 字符串，对象属性。
- default -- 默认返回值，如果不提供该参数，在没有对应属性时，将触发 AttributeError。

#### 正则表达式

- [正则表达式参考链接](https://docs.python.org/zh-cn/3/howto/regex.html#using-regular-expressions)

### `Objected-Oriented-Programming`

- [`Python`面向对象编程](https://huqianshan.github.io/articles/python%2Fpython-obeject-oriented)

