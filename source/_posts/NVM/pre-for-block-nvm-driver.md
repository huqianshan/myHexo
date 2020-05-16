---
title: pre-for-block-nvm-driver
date: 2019-12-03 15:26:50
tags: 
- [linux,drivers]
- NVM
---

## `The Block Driver's Tasks`

### `Manaing PM space and providing a block interface`

### `provide protection`

### `assure consistency when lost power`

<!--more-->
## DRAM内存模拟持久化设备的方法

### `dmesg | grep BIOS-e820`

- [`dmesg`](https://blog.csdn.net/bytxl/article/details/8846587) 命令显示linux内核的环形缓冲区信息，我们可以从中获得诸如系统架构、cpu、挂载的硬件，RAM等多个运行级别的大量的系统信 息。当计算机启动时，系统内核（操作系统的核心部分）将会被加载到内存中。在加载的过程中会显示很多的信息，在这些信息中我们可以看到内核检测硬件设备。

- [`e820`](https://blog.csdn.net/RichardYSteven/article/details/69350893): BIOS像x86架构（包括x86_64）上的操作系统引导程序提供物理内存信息的功能。当请求BIOS中断号15H，并且置操作码AX=E820H的时候，BIOS就会向调用者报告可用的物理地址区间等信息，e820由此得名。
  - Usable：已经被映射到物理内存的物理地址。
  - Reserved：这些区间是没有被映射到任何地方，不能当作RAM来使用，但是kernel可以决定将这些区间映射到其他地方，比如PCI设备。通过检查/proc/iomem这个虚拟文件，就可以知道这些reserved的空间，是如何进一步分配给不同的设备来使用了。
  - ACPI data：映射到用来存放ACPI数据的RAM空间，操作系统应该将ACPI Table读入到这个区间内。
  - ACPI NVS：映射到用来存放ACPI数据的非易失性存储空间，操作系统不能使用。
  - Unusable：表示检测到发生错误的物理内存。这个在上面例子里没有，因为比较少见。

### `sudo su; vi /etc/default/grub`

`GRUB_CMDLINE_LINUX="memmap=4G!4G"`

最后一段内存起始为`0x1 0000 0000 = 4G`，结束为`0x 2 bfff ffff = 10G`

![ss](..\..\pics\nvm-pre-e820.png)

设置起始地址为`0x1 0000 0000 = 4G`,长度亦为4G.

### `update-grub; reboot`

> After the host has been rebooted, a new `/dev/pmem{N}` device should exist, one for each memmap region specified in the GRUB config. These can be shown using **`ls /dev/pmem*`**.
> Naming convention starts at /dev/pmem0 and increments for each device. The `/dev/pmem{N}` devices can be used to create a DAX filesystem.

### `dmesg | grep user;`

![nvm-pre-map](source\pics\nvm-pre-usr-map.png)

此时此段内存应被标记为`persistent`.

### mount file system

> Create and mount a filesystem using /dev/pmem device(s), then verify the dax flag is set for the mount point to confirm the DAX feature is enabled. The following shows how to create and mount an EXT4 or XFS filesystem.

```bash
sudo mkfs -V -t ext4 -c /dev/pmem0
sudo mkdir /pmem
sudo mount -v -o dax /dev/pmem0 /pmem
sudo mount -v | grep /pmem
> /dev/pmem0 on /pmem type ext4 (rw,relatime,seclabel,dax,data=ordered)
```

#### `mkfs`

Linux mkfs命令用于在特定的分区上建立 linux 文件系统.

- device ： 预备检查的硬盘分区，例如：/dev/sda1
- -V : 详细显示模式
- -t : 给定档案系统的型式，Linux 的预设值为 ext2
- -c : 在制做档案系统前，检查该partition 是否有坏轨
- -l bad_blocks_file : 将有坏轨的block资料加到bad_blocks_file 里面
- block : 给定 block 的大小

![mkfs-pmem0](source\pics\nvm-pre-mkfs.png)

#### `mount`

`mount` 用于加载文件系统到指定的加载点。此命令的最常用于挂载cdrom，使我们可以访问cdrom中的数据，因为你将光盘插入cdrom中，Linux并不会自动挂载，必须使用Linux mount命令来手动完成挂载

- -V：显示程序版本；
- -l：显示已加载的文件系统列表；
- -h：显示帮助信息并退出；
- -v：冗长模式，输出指令执行的详细信息；
- -n：加载没有写入文件“/etc/mtab”中的文件系统；
- -r：将文件系统加载为只读模式；
- -a：加载文件“/etc/fstab”中描述的所有文件系统。

#### `fdisk`

`fdisk` 用于观察硬盘实体使用情况，也可对硬盘分区。它采用传统的问答式界面，而非类似DOS fdisk的cfdisk互动式操作界面，因此在使用上较为不便，但功能却丝毫不打折扣。

- -b<分区大小>：指定每个分区的大小；
- -l：列出指定的外围设备的分区表状况；
- -s<分区编号>：将指定的分区大小输出到标准输出上，单位为区块；
- -u：搭配"-l"参数列表，会用分区数目取代柱面数目，来表示每个分区的起始地址；
- -v：显示版本信息。

```bash
fdisk -l /dev/pmem0
Disk /dev/pmem0: 4 GiB, 4294967296 bytes, 8388608 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
```

分区是将一个硬盘驱动器分成若干个逻辑驱动器，分区是把硬盘连续的区块当做一个独立的磁硬使用。分区表是一个硬盘分区的索引,分区的信息都会写进分区表

#### `df`

`df`命令用于显示目前在Linux系统上的文件系统的磁盘使用情况统计。

#### `lsblk`

`lsblk`命令用于列出所有可用块设备的信息，而且还能显示他们之间的依赖关系，但是它不会列出RAM盘的信息。块设备有硬盘，闪存盘，cd-ROM等等。

### Show Capacity

- `sudo fdisk -l /dev/pmem0`

- `sudo lsblk /dev/pmem0`

- `df`

## Ref

[Using-the-memmap-kernel-option](https://docs.pmem.io/getting-started-guide/creating-development-environments/linux-environments/linux-memmap)
