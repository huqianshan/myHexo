---
title: block-drivers-devices
date: 2019-11-23 14:47:42
tags: 
- [drivers]
---

## 块驱动设备

<!--more-->
### 与字符驱动设备对比

- 性能要求更高

- 请求处理更加复杂（调度策略）

- 存在着缓冲区，且以固定大小读写，支持随机读写

![09-block-char-diff.jpg](https://i.loli.net/2019/12/09/K1YP6L9MEX5fdDz.jpg)

### 访问存储介质的架构

- 虚拟文件系统

- 磁盘文件系统 原始块设备

- 块`I/O`调度层

- 块设备驱动

- 硬件存储器

![linux-drivers-block.png](https://i.loli.net/2019/12/09/ONAi6r13GSMpzcJ.png)

#### `I/O`调度器

- `Noop I/O`调度器，即简单的`FIFO`队列，进行基本的合并，适合`Flash`的存储器。

- `Anticipatory I/O`调度器，试图推迟满足请求，以完成对请求的排序。对读临近区的请求在延时的几个微秒中一并执行。已被删除

- `Deadline I/O`调度器，尽可能的把每次请求的延迟降至最低。适合读取比较多的场合。

- `CFQ I/O`为所有任务分配均匀的`I/O`带宽。

- 改变内核调度算法

    - 内核传参改变调度算法 `kernel elevator=deadline`

    - 使用如下命令改变内核调度算法 `echo SCHEDULER > /sys/block/DEVICE/queue/scheduler`

### 设备文件与普通文件的区别

- 概念上
    - `普通文件`: 文本，可执行程序、媒体文件等常规文件
    - `设备文件`: 就是I/O设备。如挂载在内核`/dev`上的设备，也能通过文件系统读写。
        - 类unix操作系统都是基于文件概念的，文件是由字节序列而构成的信息载体。那么就可以把`设备文件`当作`可读写的I/O设备`。
        - 设备文件通常分为`字符设备`、`块设备`、`网络设备`
- 寻址空间上
    - 普通文件: 内核虚拟地址空间，普通文件比块设备文件多一层文件系统的地址转换机构。
    - 设备文件：物理寻址空间

### 存储结构的划分

- `PAGE`

    页：内存映射的最小单位

- `Segment`

    段：在`PAGE`中被操作的单位,由若干个块组成

- `BLOCK`

    块：逻辑上进行数据存储的最小单位。

    逻辑块的大小是在格式化的时候确定的, 一个 `Block` 最多仅能容纳一个文件（即不存在多个文件同一个`Block`的情况.
    - **`Block`是`VFS`和文件系统传送数据的基本单位**
        - Linux内核要求 `Block_Size = Sector_Size *`$$2^n$$，并且`Block_Size <= 内存的Page_Size(页大小）`
        - block对应磁盘上的一个或多个相邻的扇区，而`VFS`将其看成是一个单一的数据单元.
    - 块设备的`block`
        - 块设备的block的大小不是唯一的，创建一个磁盘文件系统时，管理员可以选择合适的扇区的大小，同一个磁盘的几个分区可以使用不同的块大小。
        - 块设备文件的每次读或写操作是一种"原始"访问，**因为它绕过了磁盘文件系统**，内核通过使用最大的块`(4096)`执行该操作。

- `Sector`
    扇区：硬件`I/O`设备存储数据的基本单位

    这个Sector就是`512byte`，和实际物理存储介质设备上的概念不一样。如果实际的设备的sector不是512byte，而是4096byte(eg SSD)，那么只需要将多个内核sector对应一个ssd sector即可

### 块设备驱动核心结构

#### `block_device`

#### `gendisk`

- **一个物理磁盘或分区在内核中的描述**

#### `hd_struct`

- **描述一个具体的磁盘分区**

#### `block_device_operations`

- **描述磁盘的操作方法集**

#### `request_queue`

- **表示针对一个gendisk对象的所有请求的队列，是相应gendisk对象的一个域**

#### `request`

- **表示经过IO调度之后的针对一个gendisk(磁盘)的一个"请求"，是request_queue的一个节点。多个request构成了一个request_queue**

#### `bio`

- **表示应用程序对一个gendisk(磁盘)原始的访问请求，一个bio由多个bio_vec，多个bio经过IO调度和合并之后可以形成一个request。**

#### `bio_vec`

- **描述的应用层准备读写一个gendisk(磁盘)时需要使用的内存页page的一部分，即上文中的"段"，多个bio_vec和bio_iter形成一个bio**

#### `bio_iter`

- **描述一个bio_vec中的一个sector信息**

![linux-block-function.png](https://i.loli.net/2019/12/09/EjkW3cKgAMmPF2I.png)

![linux-partion-block.png](https://i.loli.net/2019/12/09/4T6GABRen37JdFh.png)

![10-bio.jpg](https://i.loli.net/2019/12/09/zvDykq1gF7oQJP4.jpg)

### 块设备核心方法

- `set_capacity()`设置`gendisk`对应的磁盘的物理参数

- `blk_init_queue()`分配+初始化+绑定一个有IO调度的gendisk的`requst_queue`，处理函数是`void (request_fn_proc) (struct request_queue *q);`类型

- `blk_alloc_queue()` 分配+初始化一个没有IO调度的gendisk的`request_queue`

- `blk_queue_make_request()`绑定处理函数到一个没有IO调度的`request_queue`，处理函数函数是`void (make_request_fn) (struct request_queue q, struct bio bio);`类型

- `__rq_for_each_bio()`遍历一个`request`中的所有的`bio`

- `bio_for_each_segment()`遍历一个`bio`中所有的`segment`

- `rq_for_each_segment()`遍历一个`request`中的所有的`bio`中的所有的`segment`

    最后三个遍历算法都是用在request_queue绑定的处理函数中，这个函数负责对上层请求的处理。

### 3.16版本源代码

#### `block_device`原型

```c
struct block_device {
    dev_t            bd_dev; /* 对应底层设备的设备号 */
    int            bd_openers; /* 该设备同时被多少进程打开 */
    struct inode *        bd_inode;    /* 块设备的inod，可利用bd_dev通过bdget获得 */
    struct super_block *    bd_super; /* 文件系统的超级块信息 */
    struct mutex        bd_mutex;    /* open/close mutex */
    struct list_head    bd_inodes; 
    void *            bd_claiming;
    void *            bd_holder;
    int            bd_holders;
    bool            bd_write_holder;
#ifdef CONFIG_SYSFS
    struct list_head    bd_holder_disks;
#endif
    /* 首先block_device既可以是gendisk的抽象，又可以是hd_struct(分区)的抽象
     * 当作为分区的抽象时，bd_contains指向了该分区所属的gendisk对应的block_device
     * 当作为gendisk的抽象时，bd_contains指向自身的block_device
     */
    struct block_device *    bd_contains;
    unsigned        bd_block_size; /* 块的大小 */
    struct hd_struct *    bd_part; /* 指向分区指针，对于gendisk，指向内置的分区0 */
    /* number of times partitions within this device have been opened. */
    unsigned        bd_part_count; /* 该设备的所有分区同时被打开的次数 */
    int            bd_invalidated; /* 置1表示内存中的分区信息无效，下次打开设备时需要重新扫描分区表 */
    struct gendisk *    bd_disk; /* 通用磁盘抽象，当该block_device作为分区抽象时，指向该分区所属的gendisk，当作为gendisk的抽象时，指向自身 */
    struct list_head    bd_list;
    /*
     * Private data. You must have bd_claim'ed the block_device
     * to use this. NOTE: bd_claim allows an owner to claim
     * the same device multiple times, the owner must take special
     * care to not mess up bd_private for that case.
     */
    unsigned long        bd_private;

    /* The counter of freeze processes */
    int            bd_fsfreeze_count;
    /* Mutex for freeze */
    struct mutex        bd_fsfreeze_mutex;
};
```

block_device是伪文件系统bdevfs中对块设备或设备分区的抽象，它唯一的对应于一个设备号（对分区来说，主设备号相同，次设备号不同）。
    它的详细内容如上（include/linux/fs.h）

#### `gendisk`原型

```c
165 struct gendisk {
169         int major;                      /* major number of driver */
170         int first_minor;
171         int minors;
174         char disk_name[DISK_NAME_LEN];  /* name of major driver */
175         char *(*devnode)(struct gendisk *gd, umode_t *mode);
177         unsigned int events;            /* supported events */
178         unsigned int async_events;      /* async events, subset of all */
185         struct disk_part_tbl __rcu *part_tbl;
186         struct hd_struct part0;
188         const struct block_device_operations *fops;
189         struct request_queue *queue;
190         void *private_data;
192         int flags;
193         struct device *driverfs_dev;  // FIXME: remove
194         struct kobject *slave_dir;
196         struct timer_rand_state *random;
197         atomic_t sync_io;               /* RAID */
198         struct disk_events *ev;
200         struct blk_integrity *integrity;
202         int node_id;
203 };
```

```txt
struct gendisk
--169-->驱动的主设备号
--170-->第一个次设备号
--171-->次设备号的数量，即允许的最大分区的数量，1表示不允许分区
--174-->设备名称
--185-->分区表数组首地址
--186-->第一个分区,相当于part_tbl->part[0]
--188-->操作方法集指针
--189-->请求对象指针
--190-->私有数据指针
--193-->表示这是一个设备
```

> 同样是面向对象的设计方法，Linux内核使用gendisk对象描述一个系统的中的块设备，类似于Windows系统中的磁盘分区和物理磁盘的关系，OS眼中的磁盘都是逻辑磁盘，也就是一个磁盘分区，一个物理磁盘可以对应多个磁盘分区，在Linux中，这个gendisk就是用来描述一个逻辑磁盘，也就是一个磁盘分区

```c
struct gendisk *alloc_disk(int minors);

//注册gendisk类型对象到内核
void add_disk(struct gendisk *disk);

//从内核注销gendisk对象
void del_gendisk(struct gendisk *gp);
```

#### `hd_struct`磁盘分区描述 

 `hd_struct`用于描述一个具体的磁盘分区，其详细内容如下`（include/linux/genhd.h）`

```c
struct hd_struct {
    sector_t start_sect; /* 该分区的起始扇区号 */
    sector_t nr_sects; /* 该分区的扇区个数，也就是分区容量 */
    sector_t alignment_offset;
    unsigned int discard_alignment;
    struct device __dev;
    struct kobject *holder_dir;
    int policy, partno; /* 该分区的分区号 */
    struct partition_meta_info *info;
#ifdef CONFIG_FAIL_MAKE_REQUEST
    int make_it_fail;
#endif
    unsigned long stamp;
    atomic_t in_flight[2];
#ifdef    CONFIG_SMP
    struct disk_stats __percpu *dkstats;
#else
    struct disk_stats dkstats;
#endif
    atomic_t ref;
    struct rcu_head rcu_head;
};
```

#### `block_device_operations`原型

```c
//include/linux/blkdev.h
1558 struct block_device_operations {
1559         int (*open) (struct block_device *, fmode_t);
1560         void (*release) (struct gendisk *, fmode_t);
1561         int (*ioctl) (struct block_device *, fmode_t, unsigned, unsigned long);
1562         int (*compat_ioctl) (struct block_device *, fmode_t, unsigned, unsigned long);
1563         int (*direct_access) (struct block_device *, sector_t,
1564                                                 void **, unsigned long *);
1565         unsigned int (*check_events) (struct gendisk *disk,
1566                                       unsigned int clearing);
1568         int (*media_changed) (struct gendisk *);
1569         void (*unlock_native_capacity) (struct gendisk *);
1570         int (*revalidate_disk) (struct gendisk *);
1571         int (*getgeo)(struct block_device *, struct hd_geometry *);
1573         void (*swap_slot_free_notify) (struct block_device *, unsigned long);
1574         struct module *owner;
1575 };
```

```txt
struct block_device_operations
--1559-->当应用层打开一个块设备的时候被回调
--1560-->当应用层关闭一个块设备的时候被回调
--1562-->相当于file_operations里的compat_ioctl，不过块设备的ioctl包含大量的标准操作，所以在这个接口实现的操作很少
--1567-->在移动块设备中测试介质是否改变的方法，已经过时，同样的功能被check_event()实现
--1571-->即get geometry，获取驱动器的几何信息，获取到的信息会被填充在一个hd_geometry结构中
--1574-->模块所属，通常填THIS_MODULE
```

#### `request_queue`原型

每一个gendisk对象都有一个request_queue对象，前文说过，块设备有两种访问接口，一种是/dev下，一种是通过文件系统，后者经过IO调度在这个gendisk->request_queue上增加请求，最终回调与request_queue绑定的处理函数，将这些请求向下变成具体的硬件操作.

从驱动模型的角度来说, 块设备主要分为两类需要IO调度的和不需要IO调度的, 前者包括磁盘, 光盘等, 后者包括Flash, SD卡等, 为了保证模型的统一性 , Linux中对这两种使用同样的模型但是通过不同的API来完成上述的初始化和绑定

```c
294 struct request_queue {
 298         struct list_head        queue_head;
 300         struct elevator_queue   *elevator;
 472 };
```

```txt
struct request_queue
--298-->请求队列的链表头
--300-->请求队列使用的IO调度算法, 通过内核启动参数来选择: kernel elevator=deadline
request_queue_t和gendisk一样需要使用内核API来分配并初始化,里面大量的成员不要直接操作, 此外, 请求队列如果要正常工作还需要绑定到一个处理函数中, 当请求队列不为空时, 处理函数会被回调, 这就是块设备驱动中处理请求的核心部
```

#### `request`原型

```c
 struct request {
  98         struct list_head queuelist;
 104         struct request_queue *q;
 117         struct bio *bio;
 118         struct bio *biotail;
 119
 120         struct hlist_node hash; /* merge hash */
 126         union {
 127                 struct rb_node rb_node; /* sort/lookup */
 128                 void *completion_data;
 129         };
 137         union {
 138                 struct {
 139                         struct io_cq            *icq;
 140                         void                    *priv[2];
 141                 } elv;
 142
 143                 struct {
 144                         unsigned int            seq;
 145                         struct list_head        list;
 146                         rq_end_io_fn            *saved_end_io;
 147                 } flush;
 148         };
 149
 150         struct gendisk *rq_disk;
 151         struct hd_struct *part;
 199 };
```

```txt
struct request
--98-->将这个request挂接到链表的节点
--104-->这个request从属的request_queue
--117-->组成这个request的bio链表的头指针
--118-->组成这个request的bio链表的尾指针
--120-->内核hash表头指针
```

#### `bio`原型

bio用来描述单一的I/O请求，它记录了一次I/O操作所必需的相关信息，如用于I/O操作的数据缓存位置，，I/O操作的块设备起始扇区，是读操作还是写操作等等

```c

 46 struct bio {
 47         struct bio              *bi_next;       /* request queue link */
 48         struct block_device     *bi_bdev;
 49         unsigned long           bi_flags;       /* status, command, etc */
 50         unsigned long           bi_rw;          /* bottom bits READ/WRITE,
 51                                                  * top bits priority
 52                                                  */
 54         struct bvec_iter        bi_iter;
 59         unsigned int            bi_phys_segments;
 65         unsigned int            bi_seg_front_size;
 66         unsigned int            bi_seg_back_size;
 68         atomic_t                bi_remaining;
 70         bio_end_io_t            *bi_end_io;
 72         void                    *bi_private;
 85         unsigned short          bi_vcnt;        /* how many bio_vec's */
 91         unsigned short          bi_max_vecs;    /* max bvl_vecs we can hold */
104         struct bio_vec          bi_inline_vecs[0];
105 };
```

```txt
struct bio
--47-->指向链表中下一个bio的指针bi_next
--50-->bi_rw低位表示读写READ/WRITE, 高位表示优先级
--90-->bio对象包含bio_vec对象的数目
--91-->这个bio能承载的最大的io_vec的数目
--95-->该bio描述的第一个io_vec
--104-->表示这个bio包含的bio_vec变量的数组，即这个bio对应的某一个page中的一"段"内存
```

#### `bio_vec bio_iter`

```c
 25 struct bio_vec {
 26         struct page     *bv_page;
 27         unsigned int    bv_len;
 28         unsigned int    bv_offset;
 29 };  
 31 struct bvec_iter {
 32         sector_t                bi_sector;      /* device address in 512 bytess  ectors */
 34         unsigned int            bi_size;        /* residual I/O count */
 35 
 36         unsigned int            bi_idx;         /* current index into bvl_ve
 37 
 38         unsigned int            bi_bvec_done;   /* number of bytes completed
 39                                                    current bvec */
 40 };
```

```txt  
struct bio_vec
--26-->描述的page
--27-->描述的长度
--28-->描述的起始地址偏移量
```

#### 遍历函数

```c
 738 #define __rq_for_each_bio(_bio, rq)     \
 739         if ((rq->bio))                  \
 740                 for (_bio = (rq)->bio; _bio; _bio =_bio->bi_next)

242 #define bio_for_each_segment(bvl, bio, iter)
243         __bio_for_each_segment(bvl, bio, iter, (bio)->bi_iter)

 #define rq_for_each_segment(bvl, _rq, _iter)                    \
 743         __rq_for_each_bio(_iter.bio, _rq)                       \
 744                 bio_for_each_segment(bvl, _iter.bio, _iter.iter)
```

### 测试步骤

源代码可参考[`sbull`一个ramdisk块设备实现](https://github.com/duxing2007/ldd3-examples-3.x/tree/master/sbull)

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

#### `__bio_kmap_atomic` 被删除

- [`bio_kmap_atomic`](https://source.puri.sm/Librem5/linux-nitrogen6/commit/d004a5e7d4dd6335ce6e2044af42f5e0fbebb51d)

>This helper doesn't buy us much over calling kmap_atomic directly.
In fact in the only caller it does a bit of useless work as the
caller already has the bvec at hand, and said caller would even
buggy for a multi-segment bio due to the use of this helper.

> So just remove it.
Signed-off-by: default avatarChristoph Hellwig <hch@lst.de>
Signed-off-by: default avatarJens Axboe <axboe@kernel.dk>

#### `struct request`中 `cmd_type`被删除

- [链接及示例](https://lkml.org/lkml/2017/1/31/562)

> From Christoph Hellwig <>
  Subject [PATCH 08/10] block: introduce blk_rq_is_passthrough
  Dat Tue, 31 Jan 2017 16:57:29 +0100

> This can be used to check for fs vs non-fs requests and basically
removes all knowledge of BLOCK_PC specific from the block layer,
as well as preparing for removing the cmd_type field in struct request.

> Signed-off-by: Christoph Hellwig <hch@lst.de>

- [`end_bio`的参数变为一个](https://www.kernel.org/doc/htmldocs/filesystems/API-bio-endio.html)

- [构造函数必须强制类型转换](https://www.kernel.org/doc/htmldocs/kernel-api/API-blk-queue-make-request.html)

#### `bio_rw` has been removed

changed to `bio_datadir()`

```c
/*
 * Return the data direction, READ or WRITE.
 */
#define bio_data_dir(bio) \
	(op_is_write(bio_op(bio)) ? WRITE : READ)
```

[get rid of bio_rw and READA](https://patchwork.kernel.org/patch/9173331/)

#### `blk_queue_bounce_limit(BLK_BOUNCE_ANY)`

has been set to default

[BLK_BOUNCE_ANY is the defauly now, so the call is superflous.](https://www.redhat.com/archives/dm-devel/2017-June/msg00173.html)

#### `blk_queue_ordered()` changed

deprecate barrier and replace blk_queue_ordered() with blk_queue_flush()

[replaced with simpler blk_queue_flush().](https://lore.kernel.org/patchwork/patch/213145/)

but `blk_queue_flush` is also removed

[Updateto use the newer `blk_queue_write_cache()`](https://patchwork.kernel.org/patch/8814411/)

#### `struct bio` changed some values

- `struct block_device bio->bi_bdev` changed to `bio->gendisk`
  - [ref 1](https://github.com/torvalds/linux/commit/74d46992e0d9dee7f1f376de0d56d31614c8a17a#diff-c6085c3d2f71f3ff1bbf7b9799ad96a1)

  - [ref 2 bi_bdev field was replaced with the gendis](https://patchwork.kernel.org/patch/9918641/)

- sector of `bio` has moved to `struct bio_iter`

- and the definetion of bio has moved to `blk_types.h`

### `样例块驱动代码`

- [`Test Device For Linux Block Drivers`](https://github.com/huqianshan/OperatingSystemAndCompiler/commit/ed07917c8e8902f8d1721dd93ce1513fb87e3b27)

- [`RAMDISK`](https://www.cnblogs.com/cslunatic/p/3678613.html)

### 参考链接

- [块设备驱动模型](https://www.cnblogs.com/xiaojiang1025/p/6500557.html)

- [如何学习Linux设备驱动](https://www.cnblogs.com/cslunatic/archive/2013/04/08/3006808.html)
