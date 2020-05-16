---
title: build-hello-module-in-linux
date: 2019-11-13 10:49:12
tags: [linux,module]
---

# 编译简单的`linux`内核模块
<!--more-->
## `hello.c`

```c
/*
 * a simple kernel module: hello
 *
 * Copyright (C) 2014 Barry Song  (baohua@kernel.org)
 *
 * Licensed under GPLv2 or later.
 */

#include <linux/init.h>
#include <linux/module.h>

static int __init hello_init(void)
{
	printk(KERN_INFO "Hello World in hjl's linux\n");
	return 0;
}
module_init(hello_init);

static void __exit hello_exit(void)
{
	printk(KERN_INFO "Hello World exit byebye\n ");
}
module_exit(hello_exit);

MODULE_AUTHOR("Hu Jinlei <hjl2016060203025@std.uestc.edu.cn>");
MODULE_LICENSE("GPL v2");
MODULE_DESCRIPTION("A simple Hello World Module");
MODULE_ALIAS("a simplest module");
```

1. 编译
2. `insmod ./hello.ko`加载
3. `rmmod hello`卸载
4. `lsmod`显示加载的模块


![03-arm-linux-module.jpg](https://i.loli.net/2019/11/13/1zoMHxPZeOBiFSr.jpg)

# 在`QEMU`中运行编译的`Linux`内核
<!--more-->
## 内核编译脚本 `build.sh`

```shell
export ARCH=arm
export EXTRADIR=${PWD}/extra
export CROSS_COMPILE=arm-linux-gnueabi-
make LDDD3_vexpress_defconfig
make zImage -j8
make modules -j8
make dtbs
cp arch/arm/boot/zImage extra/
cp arch/arm/boot/dts/*ca9.dtb	extra/
cp .config extra/
```

- 默认的内核配置文件为 `LDDD3_vexpress_defconfig`.上述脚本会将自动编译好的`zImage,dtbs`复制到`extra`目录中

- `extra`目录下的vexpress是一张虚拟的SD卡，作为*根文件系统*的存放介质。它能以`loop`形式被挂载`mount`

    > `sudo mount -o loop,offset=$((2048*512)) extra/vexpress.img extra/img`

## 编译模块的脚本 `module.sh`

```shell
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- modules
sudo mount -o loop,offset=$((2048*512)) extra/vexpress.img extra/img
sudo make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- modules_install INSTALL_MOD_PATH=extra/img
sudo umount extra/img
```

- 它会自动编译内核模块并安装到`vexprees.img`

## 启动带`LCD`的`ARM Linux`内 核

![01-arm-linux-qemu-lcd.jpg](https://i.loli.net/2019/11/13/RV1HtyCN2Y3OPsW.jpg)