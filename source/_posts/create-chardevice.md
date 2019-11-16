---
title: create-chardevice
date: 2019-11-15 20:16:33
tags: [linux,drivers]
---

## `linux`字符设备驱动设计与实现

### `TDLCD(Test Device For Linux Char Drives)`的设计

- 主要参考`Linux Device Drives`第三章-字符设备驱动程序中的`scull(Simple Chararter Utility for Loading Localities)`
<!--more-->
### `TDLCD`实现步骤

- 字符设备结构定义与初始化
定义设备结构体，并完成结构初始化函数 

- 申请字符设备号
动态申请主、次设备号

- 完成字符设备的注册与消除函数

- 实现驱动方法
  - `llseek`方法
  - `read`方法
  - `write`方法
  - `ioctl`方法
  - `open`方法
  - `release`方法

### 结构设计

#### 模块部分

```c

```

#### 宏定义及头文件

```c
#include <linux/module.h>
#include <linux/init.h>
/*
#define SIZE 0x1000
```

#### 字符设备结构设计

为设备定义一个结构体，包含`cdev`,私有数据及锁等相关信息。

```c
struct tdlcd_dev{
    struct cdev cdev;
    unsigned char mem[SIZE];
}
```

#### `file_operations`结构设计

将自实现的驱动方法函数传递给结构

```c
static const struct file_operations tdlcd_fops={
    .owner=THIS_MODULE,
    .llseek = tdlcd_llseek,
    .read = tdlcd_read,
    .write = tdlcd_write,
    .unlocked_ioctl = tdlcd_ioctl,
    .open = tdlcd_open,
    .release = tdlcd_release,
}
```

#### 字符设备模块的加载与卸载函数

- `static int __init tdlcd_init(void);`
  - init cdev
  - get char device number
  - register devices

- `static void __exit tdlcd_exit(void);`
  - release devices
  - release device number


### `Makefile`

>  

```c
KVERS = $(shell uname -r)

# Kernel modules
obj-m += globalmem.o
obj-m += multi_globalmem.o

# Specify flags for the module compilation.
#EXTRA_CFLAGS=-g -O0

build: kernel_modules

kernel_modules:
        make -C /lib/modules/$(KVERS)/build M=$(CURDIR) modules

clean:
        make -C /lib/modules/$(KVERS)/build M=$(CURDIR) clean

```

### 编译装载结果

![04-char-devices-compiler-insert.jpg](https://i.loli.net/2019/11/15/FEtM5AmhCq1Nl8y.jpg)
