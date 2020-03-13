---
title: python-obeject-oriented
date: 2020-02-10 11:16:49
tags: 
- python
- obejec-oriented
---
<!-- TOC -->

- [`Python` 面向对象编程](#python-面向对象编程)
  - [类`class`提供了一种什么样的编程模式（思维范式）](#类class提供了一种什么样的编程模式思维范式)
  - [相关概念](#相关概念)
  - [高级特性](#高级特性)
    - [类方法的作用](#类方法的作用)
      - [`@staticmethod`和`@classmethod`异同](#staticmethod和classmethod异同)
    - [`__slots__`](#__slots__)
    - [`@property`装饰器](#property装饰器)
    - [多重继承 MixIn](#多重继承-mixin)
    - [定制类](#定制类)
    - [运行期间动态创建类](#运行期间动态创建类)
    - [`metaclass`元类](#metaclass元类)
    - [描述符（`descriptor`）](#描述符descriptor)

<!-- /TOC -->
<!-- more -->
## `Python` 面向对象编程

### 类`class`提供了一种什么样的编程模式（思维范式）

类提供了一种组合数据和功能的方法。

### 相关概念

- 类(Class): 用来描述具有相同属性和方法的对象的集合。它定义了该集合中每个对象所共有的属性和方法。其中的对象被称作类的实例。
  - 实例：也称对象。通过类定义的初始化方法，赋予具体的值，成为一个”有血有肉的实体”。在Python中实例与类是分开的。即`动态语言`（相关属性可能在运行时才创建）
  - 实例化：创建类的实例的过程或操作。
  - 实例变量：定义在实例中的变量，只作用于当前实例。
  - 类变量：类变量是所有实例公有的变量。类变量定义在类中，但在方法体之外。
- 数据成员：类变量、实例变量、方法、类方法、静态方法和属性等的统称。
  - `属性` 为数据变量，由实例直接访问。
  - 可由`dir`查看对象的所有方法与属性,它的输出形式是列表，而`__dict__`是字典
  - `obj.__dict__`查看可写的属性。`__dict__`是用来存储对象属性的一个字典，其键为属性名，值为属性的值。可以用来在`__init__`赋值
- 方法：类中定义的函数。
  - 实例方法： 通过实例调用类函数
  - 静态方法`@staticmethod`：不需要实例化就可以由类执行的方法
  - 类方法`@classmethod`：类方法是将类本身作为对象进行操作的方法，执行类方法时，自动将调用该方法的类赋值给`cls`。
- 面向对象特性
  - 方法重写：如果从父类继承的方法不能满足子类的需求，可以对父类的方法进行改写，这个过程也称override。
  - 封装：将内部实现包裹起来，对外透明，提供api接口进行调用的机制
  - 继承：即一个派生类（derived class）继承父类（base class）的变量和方法。
  - 多态：根据对象类型的不同以不同的方式进行处理。
- 面向对象高级特性
  - 多继承
  - 元类
  - 定制类
  
### 高级特性

#### 类方法的作用

- 通过类名直接调用。

- 在不改变已经写好的类里面的方法的情况下，对输入的数据进行处理 也就是`工厂模式`。所谓的`alternative constructors`,不在外部添加新的修改胶水层，直接在类里添加方法，更符合`OOP`思想

##### `@staticmethod`和`@classmethod`异同

- 参数不同

- 在调用`classmethod`方法时，会将此方法的类传递进去，而不是通常的实例对象。
  - 可以避免类内调用函数时，使用指定`类名.方法名`的硬编码形式。

- [参考StackOverflow问题](https://stackoverflow.com/questions/12179271/meaning-of-classmethod-and-staticmethod-for-beginner)

#### `__slots__`

限制类实例添加属性，只能绑定由`__slots__`指定的属性。但只对当前**类实例**（不是类本身）起作用，继承的子类需要重新指定。

> `Student.set_gender = MethodType(set_gender, Student)`

#### `@property`装饰器

把类的方法当作属性使用。

```python
class Student(object):

    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        self._birth = value

    @property
    def age(self):
        return 2015 - self._birth
```

则`birth`为可读写属性，`age`为只读属性

#### 多重继承 MixIn

在设计类的继承关系时，通常，主线都是单一继承下来的，例如，Ostrich继承自Bird。但是，如果需要“混入”额外的功能，通过多重继承就可以实现，比如，让Ostrich除了继承自Bird外，再同时继承Runnable。这种设计通常称之为MixIn。

MixIn的目的就是给一个类增加多个功能，这样，在设计类的时候，我们优先考虑通过多重继承来组合多个MixIn的功能，而不是设计多层次的复杂的继承关系

#### 定制类

定制类实际上是通过修改一些内置方法，从而使得类展示出不同的功能或接口。

- `__str__` 定义此方法，使得`print(class_name)`返回良好的语句
- `__repr__`返回程序开发者看到的字符串
- `__iter__ __next__()` 迭代方法
- `__getitem__` 类似于列表
- `__getattr__` 重要，常见的动态对象绑定 
- `__call__`只需要定义一个__call__()方法，就可以直接对实例进行调用。对实例进行直接调用就好比对一个函数进行调用一样，所以你完全可以把对象看成函数，把函数看成对象，因为这两者之间本来就没啥根本的区别。
如果你把对象看成函数，那么函数本身其实也可以在运行期动态创建出来，因为类的实例都是运行期创建出来的，这么一来，我们就模糊了对象和函数的界限。

```python
class github(object):
    def __init__(self, url='Get /usr'):
        self.url = url

    def __getattr__(self, attr):
        return github((f"{self.url}/{attr}"))

    def __call__(self, attr):
        return github((f"{self.url}/{attr}"))
#GET /users/:user/repos
# github().users("hu").repos.url
```

```python
#这个例子通过获取属性值的方式去获取字典的键值
class ObjectDict(dict):
    def __init__(self, *args, **kwargs):
        super(ObjectDict, self).__init__(*args, **kwargs)

    def __getattr__(self, name):
        value = self[name]
        if isinstance(value, dict):
            value = ObjectDict(value)
        return value



od = ObjectDict(asf={'a': 1}, d=True)
print(od.asf, od.asf.a)     # {'a': 1} 1
print(od.d)
```

```python
# 批量初始化字典对象
class A():
    def __init__(self,dicts):
        self.__dict__.update(dicts)
        print(self.__dict__)

if __name__ == '__main__':
     dicts={"name":"lisa","age":23,"sex":"women","hobby":"hardstyle"}
     a=A(dicts)
```

#### 运行期间动态创建类

可以通过`type()`函数在运行期创建一个类。

type()函数既可以返回一个对象的类型，又可以创建出新的类型。

要创建一个class对象，type()函数依次传入3个参数：

1. class的名称；
2. 继承的父类集合，注意Python支持多重继承，如果只有一个父类，别忘了tuple的单元素写法；
3. class的方法名称与函数绑定，这里我们把函数fn绑定到方法名hello上。

通过type()函数创建的类和直接写class是完全一样的，因为Python解释器遇到class定义时，仅仅是扫描一下class定义的语法，然后调用type()函数创建出class。

正常情况下，我们都用class Xxx...来定义类，但是，type()函数也允许我们动态创建出类来，也就是说，动态语言本身支持运行期动态创建类，这和静态语言有非常大的不同，要在静态语言运行期创建类，必须构造源代码字符串再调用编译器，或者借助一些工具生成字节码实现，本质上都是动态编译，会非常复杂。

#### `metaclass`元类

- [廖雪峰](https://www.liaoxuefeng.com/wiki/1016959663602400/1017592449371072)
- [元类的一个小栗子](http://rootkiter.com/2017/02/25/Python_ClassBuilder.html)
- [Python 元类 (MetaClass) 小教程](https://lotabout.me/2018/Understanding-Python-MetaClass/)

#### 描述符（`descriptor`）

- [python-how-to-decriptor](https://docs.python.org/zh-cn/3/howto/descriptor.html)
- [面向对象（深入）|python描述器详解](https://zhuanlan.zhihu.com/p/32764345)