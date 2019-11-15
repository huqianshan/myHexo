---
title: create-chardevice
date: 2019-11-15 20:16:33
tags: [linux,drivers]
---

## `linux`字符设备驱动设计与实现

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