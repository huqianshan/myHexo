---
title: copy-virtual-ubuntu
date: 2019-11-13 18:47:21
tags: [linux,vmware,network]
---
<!-- TOC -->

- [解决复制的虚拟机无法识别网卡`eth0`](#解决复制的虚拟机无法识别网卡eth0)
    - [背景](#背景)
    - [原因](#原因)
    - [解决办法](#解决办法)
    - [参考链接](#参考链接)

<!-- /TOC -->
# 解决复制的虚拟机无法识别网卡`eth0`

## 背景

最近在学习Linux程序设计及驱动相关知识，买了宝华老师的书，但是在把baohua_linux复制到本地之后，从虚拟机进入ifconfig，只有lo网络，没有其他网卡，虚拟机的网络适配器设置为NAT模式。
<!--more-->
## 原因

1. `UUID`为机器标识码，保证对同一时空的所有机器唯一。虚拟机同样会有一个UUID，而且这个UUID是唯一的。

2. 虚拟机的`UUID`一般和虚拟机配置文件的位置和物理主机有关。

3. 虚拟机移动时不需要改变`UUID`.复制时`UUID`对应的`Mac`地址改变。导致eth0设备装载的配置与默认不一致。

4. 同时，`70-persistent-net.rules文件`中记录了`MAC`以及`eth0`

## 解决办法

- 生成`70-persistent-net.rules文件`

  - 如果系统中已有`/etc/udev/rules.d/70-persistent-net.rules`,删除，重启会自动生成
  - 如没有，手动生成

    - `export MATCHADDR=”00:f1:f3:1a:f0:05”`

    - `export INTERFACE=eth0`

    - `sudo /lib/udev/write_net_rules`
- 查看系统的网卡 `lspci | grep Eth*` 

  - 显示为`Ethernet controller: Advanced Micro Devices, Inc. [AMD] 79c970 [PCnet32 LANCE] (rev 10)`
  - 打开VMware 虚拟机配置 (.vmx)，在其中添加一行ethernet0.virtualDev = “e1000”


## 参考链接

- [本文直接参考](https://blog.csdn.net/five0918/article/details/72782531)

- [手动生成`eth0`以及`mac`配置文件](https://blog.csdn.net/gw85047034/article/details/50978490)

- [虚拟机移动后`uuid`不匹配问题](https://blog.51cto.com/bfe99/900977)