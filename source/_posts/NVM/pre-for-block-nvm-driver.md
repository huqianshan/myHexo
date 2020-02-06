---
title: pre-for-block-nvm-driver
date: 2019-12-03 15:26:50
tags: [linux,drivers]
---

## `The Block Driver's Tasks`

### `Manaing PM space and providing a block interface`

### `provide protection`

### `assure consistency when lost power`

<!--more-->
## DRAM内存模拟持久化设备的方法

### `dmesg | grep BIOS-e820`

### `sudo su; vi /etc/default/grub`

`GRUB_CMDLINE_LINUX="memmap=4G!12G"`

begin 12 GB to 16 GB

### `update-grub; reboot`

> After the host has been rebooted, a new `/dev/pmem{N}` device should exist, one for each memmap region specified in the GRUB config. These can be shown using `ls /dev/pmem*`. Naming convention starts at /dev/pmem0 and increments for each device. The `/dev/pmem{N}` devices can be used to create a DAX filesystem.

### `dmesg | grep user;`

### mount file system

> Create and mount a filesystem using /dev/pmem device(s), then verify the dax flag is set for the mount point to confirm the DAX feature is enabled. The following shows how to create and mount an EXT4 or XFS filesystem.

```bash
sudo mkfs.ext4 /dev/pmem0
sudo mkdir /pmem
sudo mount -o dax /dev/pmem0 /pmem
sudo mount -v | grep /pmem
> /dev/pmem0 on /pmem type ext4 (rw,relatime,seclabel,dax,data=ordered)
```

### Show Capacity

- `sudo fdisk -l /dev/pmem0`

- `sudo lsblk /dev/pmem0`

## Ref

[Using-the-memmap-kernel-option](https://docs.pmem.io/getting-started-guide/creating-development-environments/linux-environments/linux-memmap)
