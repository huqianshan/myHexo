---
title: pre-for-block-nvm-driver
date: 2019-12-03 15:26:50
tags: [linux,drivers]
---

## `The Block Driver's Tasks`

### `Manaing PM space and providing a block interface`

### `provide protection `

### `assure consistency when lost power`

<!--more-->
## DRAM内存模拟持久化设备的方法

### `dmesg | grep BIOS-e820`

### `sudo su; vi /etc/default/grub`

### `update-grub; reboot`

### `dmesg | grep user;`

### `sudo fdisk -l /dev/pmem0m`



`4KB each page`: transfer physical address to virtual address and make it accessible

upon recive a request the driver computes the physical address of the demanded  PM page.





