import re

from PIL import Image


class demo3:
    def __init__(self, year=0, month=0, day=0):
        self.year = year
        self.month = month
        self.day = day

    def out_date(self):
        return "year:%d, month:%d, day:%d" % (self.year, self.month, self.day)

    @classmethod
    def pre_out(cls, date_string):
        year, month, day = map(int, date_string.split("-"))
        return cls(year, month, day)


class Date(object):

    def __init__(self, day=0, month=0, year=0):
        self.day = day
        self.month = month
        self.year = year

    @classmethod
    def from_string(cls, date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        date1 = cls(day, month, year)
        return date1

    @staticmethod
    def is_date_valid(date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        return day <= 31 and month <= 12 and year <= 3999


class Student(object):
    __slots__ = ("name")


class github(object):
    def __init__(self, url='Get /usr'):
        self.url = url

    def __getattr__(self, attr):
        return github((f"{self.url}/{attr}"))

    def __call__(self, attr, gg):
        return github((f"{self.url}/{attr}/{gg}"))


class Property:
    def __init__(self, fget):
        self.fget = fget    # 为实例增加方法，这里的方法是未绑定实例的，不会自动传入实例self
        self.fset = None    # 同上，未绑定实例

    def __get__(self, instance, owner):
        if instance is not None:
            return self.fget(instance)  # 调用原方法，传入实例self
        return self

    def __set__(self, instance, value):
        self.fset(instance, value)  # 调用原方法，传入实例self和value

    def setter(self, func):
        self.fset = func  # 更新属性
        return self


class A:
    def __init__(self, data):
        self._data = data

    @Property  # data = Property(data) 描述符实例
    def data(self):
        return self._data

    @data.setter  # data = data.setter(data) 更新属性，并返回描述符实例
    def data(self, value):
        self._data = value


a = A(100)
print(a.data)  # 访问描述符实例，调用__get__()方法
# 100


class A(object):
    def m1(self, n):
        print("self:", self)

    @classmethod
    def m2(cls, n):
        print("cls:", cls)

    @staticmethod
    def m3(n):
        pass


class ObjectDict(dict):
    def __init__(self, *args, **kwargs):
        super(ObjectDict, self).__init__(*args, **kwargs)

    def __getattr__(self, name):
        value = self[name]
        if isinstance(value, dict):
            value = ObjectDict(value)
        return value


class Singleton:
    def __new__(cls):
        if hasattr(cls, 'test'):
            print("has created")
            return cls.test
        Singleton.test = super().__new__(cls)
        return Singleton.test

# %%
def make_avg():
    items=0
    tot=0

    def avger(num):
        nonlocal items,tot
        items+=1
        tot+=num
        return tot/items
    return avger

avg=make_avg()
avg(1)
avg(3)

# %%
import random

SEED = 448

myList = ['list', 'elements', 'go', 'here']
random.seed(SEED)
n=random.sample(myList,2)

print(n)


# %%


# %%


# %%
# %%
pattern=r"IPIP数据：[\d\.]+\-[\d\.]+\s(\w+)\s(\w+)\s(\w+)\s"
t=re.search(pattern,text)
print(t.groups())
