---
title: block-devices
date: 2019-11-23 14:47:42
tags: [drivers]
---

## 块驱动设备

### 与字符驱动设备相比

- 性能要求更高

- 请求处理更加复杂（调度策略）

- 存在着缓冲区，且以固定大小读写，支持随机读写

### 访问存储介质的架构

- 虚拟文件系统

- 磁盘文件系统 原始块设备

- 块`I/O`调度层

- 块设备驱动

<!--more-->
### 块设备驱动结构

#### `block_device_operation`结构体

#### `gendisk`结构体

#### `bio、request、request_queue`

一个`bio`结构体实例对应上层对块的`I/O`请求。内部包含了开始扇区，数据方向，数据放入的页等相关信息。

`bio_vec`用来描述与`bio`请求对应的所有的内存。向量描述为`[page,offset,len]`,即片段

一个请求`request`是多个`bio`调整优化之后的合并操作。

#### `I/O`调度器

- `Noop I/O`调度器，即简单的`FIFO`队列，进行基本的合并，适合`Flash`的存储器。

- `Anticipatory I/O`调度器，试图推迟满足请求，以完成对请求的排序。对读临近区的请求在延时的几个微秒中一并执行。已被删除

- `Deadline I/O`调度器，尽可能的把每次请求的延迟降至最低。适合读取比较多的场合。

- `CFQ I/O`为所有任务分配均匀的`I/O`带宽。

### 测试步骤

> 接下来即可进行测试
>
> - `ll /dev | grep sbull`
> - 分区：`fdisk /dev/sbull`
> - 格式化，指定文件系统：`mkfs.ext4 /dev/sbull`
> - 挂载：`mount /dev/sbull /mnt`
> - 查看磁盘物理分区信息：`cat /proc/partitions`
> - 查看磁盘分区占用情况：`df -ahT`

### `API`的更改

由于内核代码的不断修改，许多函数的接口都已经发生变化。编译起来报错不断。一个个慢慢goolge修改。参考了以下资料链接。

- [`2.6`内核的更改](https://lwn.net/Articles/333620/)
- [`ldd`的`git`仓库](https://github.com/duxing2007/ldd3-examples-3.x/tree/origin/linux-4.9.y)
- [关于`sbull`在2.6内核版本下的测试](https://blog.csdn.net/liuqiang55888/article/details/102573174)
- [`ldd`在线中文版本](http://www.embeddedlinux.org.cn/ldd3/)

### `__bio_kmap_atomic` 被删除

- [`bio_kmap_atomic`](https://source.puri.sm/Librem5/linux-nitrogen6/commit/d004a5e7d4dd6335ce6e2044af42f5e0fbebb51d)

>This helper doesn't buy us much over calling kmap_atomic directly.
In fact in the only caller it does a bit of useless work as the
caller already has the bvec at hand, and said caller would even
buggy for a multi-segment bio due to the use of this helper. 

> So just remove it.
Signed-off-by: default avatarChristoph Hellwig <hch@lst.de>
Signed-off-by: default avatarJens Axboe <axboe@kernel.dk>

### `struct request`中 `cmd_type`被删除

- [链接及示例](https://lkml.org/lkml/2017/1/31/562)

> From	Christoph Hellwig <>
  Subject	[PATCH 08/10] block: introduce blk_rq_is_passthrough
  Date	Tue, 31 Jan 2017 16:57:29 +0100

> This can be used to check for fs vs non-fs requests and basically
removes all knowledge of BLOCK_PC specific from the block layer,
as well as preparing for removing the cmd_type field in struct request.

> Signed-off-by: Christoph Hellwig <hch@lst.de>

### [`end_bio`的参数变为一个](https://www.kernel.org/doc/htmldocs/filesystems/API-bio-endio.html)

### [构造函数必须强制类型转换](https://www.kernel.org/doc/htmldocs/kernel-api/API-blk-queue-make-request.html)

### `样例块驱动代码`

- [`Test Device For Linux Block Drivers`](https://github.com/huqianshan/OperatingSystemAndCompiler/commit/ed07917c8e8902f8d1721dd93ce1513fb87e3b27)
