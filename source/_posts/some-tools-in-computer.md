---
layout: poster
title: some_tools_in_computer
date: 2019-02-14 12:29:06
tags: [tools]
---

# 龙套角色也精彩

这是学习[操作系统]()时总结的一些编程开发工具，虽然这些并不是实实在在的
生产力开发工具，当在实际应用中，缺少他们却是万万不能的。


<img src="https://i.loli.net/2019/02/14/5c64efab4c2e4.jpg" width="60%" height="60%">
<!--more-->·

## `Linux’s Tools`

### `Make & Makefile`

`GNU make`(简称make)是一种代码维护工具，在大中型项目中，它将根据程序各个模块的更新情况，自动的维护和生成目标代码。

#### makefile的规则。

```makefile
target ... : prerequisites ...
    command
    ...
    ...
```

target也就是一个目标文件，可以是object file，也可以是执行文件。还可以是一个标签（label）。prerequisites就是，要生成那个target所需要的文件或是目标。command也就是make需要执行的命令（任意的shell命令）。 这是一个文件的依赖关系，也就是说，target这一个或多个的目标文件依赖于prerequisites中的文件，其生成规则定义在 command中。如果prerequisites中有一个以上的文件比target文件要新，那么command所定义的命令就会被执行。这就是makefile的规则。也就是makefile中最核心的内容。

#### `参考链接：`

[Isaac Schlueter的Makefile文件教程](https://gist.github.com/isaacs/62a2d1825d04437c6f08)

[Make 命令教程](https://blog.csdn.net/a_ran/article/details/43937041)

[GNU Make手册](https://www.gnu.org/software/make/manual/make.html)

### `dd命令` 

```
bs=<字节数>：将ibs（输入）与欧巴桑（输出）设成指定的字节数；
cbs=<字节数>：转换时，每次只转换指定的字节数；
conv=<关键字>：指定文件转换的方式；
count=<区块数>：仅读取指定的区块数；
ibs=<字节数>：每次读取的字节数；
obs=<字节数>：每次输出的字节数；
of=<文件>：输出到文件；
seek=<区块数>：一开始输出时，跳过指定的区块数；
skip=<区块数>：一开始读取时，跳过指定的区块数；
--help：帮助；
--version：显示版本信息。
```

#### `参考链接` 

[dd参考页](http://man.linuxde.net/dd)