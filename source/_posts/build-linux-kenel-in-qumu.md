---
title: build-linux-kenel-in-qumu
date: 2019-11-13 09:54:56
tags: [linux,drivers]
---

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

## 启动带`LCD`的`ARM Linux`内核

![01-arm-linux-qemu-lcd.jpg](https://i.loli.net/2019/11/13/RV1HtyCN2Y3OPsW.jpg)