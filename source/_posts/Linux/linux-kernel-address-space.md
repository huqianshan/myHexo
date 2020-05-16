---
title: linux-kernel-address-space
date: 2019-12-06 10:16:49
tags: [linux]
---

<!-- TOC -->

- [`Linux`内核地址空间](#linux内核地址空间)
- [内核空间分配`api`](#内核空间分配api)
  - [`kmalloc and kzalloc`](#kmalloc-and-kzalloc)
    - [`Description`](#description)
    - [`flags argument`](#flags-argument)
  - [`get_free_page`](#get_free_page)
  - [`vmalloc`](#vmalloc)
    - [`vmalloc Description`](#vmalloc-description)
    - [`说明`](#说明)
  - [`ioremap`](#ioremap)
- [`Linux`的内存管理](#linux的内存管理)
  - [地址类型](#地址类型)
    - [用户虚拟空间地址](#用户虚拟空间地址)
    - [内核地址空间](#内核地址空间)
    - [高端内存和低端内存](#高端内存和低端内存)
  - [内存管理结构](#内存管理结构)
    - [页结构`struct page`](#页结构struct-page)
    - [`kmap`映射](#kmap映射)
    - [页表与`VMA`](#页表与vma)
    - [`vm_area_struct`结构](#vm_area_struct结构)
    - [`struct mm_struct`](#struct-mm_struct)
  - [内存映射](#内存映射)
    - [`mmap`原型](#mmap原型)
  - [建立页表的方法](#建立页表的方法)
    - [使用`remap_pfn_range`一次性建立](#使用remap_pfn_range一次性建立)
    - [使用`nopage_VMA`每次建立一个页表](#使用nopage_vma每次建立一个页表)
  - [地址映射关系](#地址映射关系)
- [参考链接](#参考链接)

<!-- /TOC -->
<!--more-->
![funciton call](https://pic1.zhimg.com/80/v2-c381d93642b716770c6705dac13a30c8_hd.jpg)
![linux_storage.png](https://i.loli.net/2019/12/06/aspKfcHJeBovSWm.png)
![linux_addree_map.png](https://i.loli.net/2019/12/06/el7NgrRHvXcBjs6.png)
![linux_vm_area_struct.png](https://i.loli.net/2019/12/06/9IXsLMrzdEgoqTG.png)

## `Linux`内核地址空间

内存分为三个区段: 1. 用于`DMA`的内存，2. `常规内存`，3.`高端内存`

## 内核空间分配`api`

### `kmalloc and kzalloc`

#### `Description`

> `kmalloc is the normal method of allocating memory for objects smaller than page size in the kernel.`

最常用的内核空间内存分配函数。最终是通过调用`get_free_pages`来实现.`kmalloc()`是基于`slab/slob/slub`分配分配算法上实现的，不少地方将其作为`slab/slob/slub`分配算法的入口，实际上是略有区别的。

最小分配大小 `32/64 Byte` 最大 `128 KB -16`

#### `flags argument`

> GFP_USER - Allocate memory on behalf of user. May
> sleep.
> GFP_KERNEL - Allocate normal kernel ram. May sleep.
> GFP_ATOMIC - Allocation will not sleep. May use emergency pools. For example, use this inside interrupt handlers.
> GFP_HIGHUSER - Allocate pages from high memory.

~~貌似也能从**高端内存**分配~~ **并不能**,是说可能会从高端内存中分配，具体由平台决定

物理内存只能按页面进行分配，不超过`128KB`

### `get_free_page`

参数类似于`kmalloc`.基于`buddy`机制

`alloc_pages`是`Linux`页分配器的核心函数`alloc_pages_node`的简单宏，主要处理了`NUMA`

### `vmalloc`

#### `vmalloc Description`

分配虚拟地址空间的连续区域，尽管可能在物理地址上不是连续的。

访问每个页面需要单独调用`alloc_pages`.通过红黑树管理

#### `说明`

是`Linux`内存分配的基础。 内存分配使用效率不高，如可能，应该直接对页面进行分配。

以上三个函数获得的内存地址均为虚拟地址。但`kmalloc、get_free_pages`地址与物理内存只差基于`PAGE_OFFSET`的偏移。不需要修改页表

`kmalloc()`分配的内存处于`3GB～high_memory`之间，而`vmalloc()`分配的内存在`VMALLOC_START～4GB`之间，也就是非连续内存区。

一般情况下在驱动程序中都是调用`kmalloc()`来给数据结构分配内存，而`vmalloc(`)用在为活动的交换区分配数据结构，为某些I/O驱动程序分配缓冲区，或为模块分配空间

`vmalloc`则不同。且分配得到的地址是不能在处理器之外使用。

正确使用场合： **分配一大堆连续的，只在软件中存在的，用于缓冲的内存区域**

且其不能在原子上下文中使用，因为其内部实现调用了`kmalloc`来获取页表的存储空间，因而可能休眠

### `ioremap`

与`vmalloc`不同的是，`ioremap`并不实际分配内存。其返回的内存地址不能够被直接访问，需要通过特定的接口来操作。

与`vmalloc`相同的是，`ioremap`也是面向页的，会**新建页表**

## `Linux`的内存管理

![linux_storage.png](https://i.loli.net/2019/12/06/aspKfcHJeBovSWm.png)

### 地址类型

#### 用户虚拟空间地址

#### 内核地址空间

- 内核逻辑地址

        与物理地址只差一个偏移量，如`kmalloc`

- 内核虚拟地址

         不必是线性对应一对一。

宏`__pa(),__va()`完成相应的转换

#### 高端内存和低端内存

内核无法直接操作没有映射到内核地址空间的内存。

为了获得更多的地址空间，处理器增添了地址扩展特性。

- 只有内存的低端部分拥有逻辑地址 剩余的部分（高端内存）没有

- 访问高端内存前，内核必须建立明确的虚拟映射

### 内存管理结构

#### 页结构`struct page`

因为高端内存无法使用逻辑地址，且为了保存物理内存信息，对系统中每个物理页，都有一个`page`结构相对应。

- `atomic_t count;`

  >这个页的引用数. 当这个 count 掉到 0, 这页被返回给空闲列表.

- `void *virtual;`
  
  > 这页的内核虚拟地址, 如果它被映射; 否则, NULL. 低内存页一直被映射; 高内存页常常不是. 这个成员不是在所有体系上出现; 它通常只在页的内核虚拟地址无法轻易计算时被编译. 如果你想查看这个成员, 正确的方法是使用 `page_address` 宏.

- `struct page virt_to_page(void kaddr)`
  > 这个宏, 定义在 `<asm/page.h>`, 采用一个内核逻辑地址并返回它的被关联的`struct page`指针. 因为它需要一个逻辑地址, 它不能操作来自 `vmalloc` 的内存或者高端内存

- `struct page *pfn_to_page(int pfn)`
  > 为给定的页帧号返回 `struct page`指针. 如果需要, 它在传递给 `pfn_to_page`之前使用`pfn_valid`来检查一个页帧号的有效性.

- `void page_address(struct page page)`
  > 返回这个页的内核虚拟地址, 如果这样一个地址存在. 对于高端内存, 那个地址仅当这个页已被映射才存在. 这个函数在`<linux/mm.h>` 中定义. 大部分情况下, 你应该使用 `kmap` 而不是 `page_address`

#### `kmap`映射

  `include <linux/highmem.h>`

  `void kmap(struct page page);`

  `void kunmap(struct page *page);`

 - `kmap` 为系统中的**任何页**返回一个**内核虚拟地址**. 对于低端内存页, 它只返回页的逻辑地址; 对于高内存, `kmap` 在内核地址空间的一个专用部分中创建一个特殊的映射. 使用 `kmap` 创建的映射应当一直使用 `kunmap` 来释放;

 - 一个有限数目的这样的映射可用, 因此最好不要在它们上停留太长时间. `kmap` 调用维护一个计数器, 因此如果 2 个或 多个函数都在同一个页上调用 kmap,也是正确的. 还要注意 `kmap` 可能睡眠当没有映射可用时.

 - 如块驱动中`make_request`函数需要对`bvec`中的`page`进行`kmap`映射以得到可以操作的内核虚拟地址

#### 页表与`VMA`

- 页表
  将虚拟地址转化为物理地址

- `VMA`

  虚拟内存区( VMA )用来管理一个进程的地址空间的不同区域的内核数据结构. 一个 VMA 代表一个进程的虚拟内存的一个同类区域: 一个有相同许可标志和被相同对象(如, 一个文件或者交换空间)支持的连续虚拟地址范围. 它松散地对应于一个"段"的概念, 尽管可以更好地描述为"一个有它自己特性的内存对象". 一个进程的内存映射有下列区组成:

  - 给程序的可执行代码(常常称为 text)的一个区.

  - 给数据的多个区, 包括初始化的数据(它有一个明确的被分配的值, 在执行开始), 未初始化数据(BBS),以及程序堆栈.

  - 给每个获得的内存映射的一个区域.

#### `vm_area_struct`结构

![linux_vm_area_struct.png](https://i.loli.net/2019/12/06/9IXsLMrzdEgoqTG.png)

- 当用户空间调用`mmap`完成地址映射时，系统会同时创建一个`vm_area_struct`

- 当驱动设备需要实现`mmap`接口时，会需要对此结构的函数进行操作

- 在`<linux/mm.h>`中定义

#### `struct mm_struct`

- 每个进程都拥有一个`struct mm_struct  <linux/sched.h>`负责整合其他的数据结构.

- 其中包含了：虚拟内存区域链表，页表以及相关内存管理信息，还包括自旋锁以及信号量。

- 通常的方法是使用 `current->mm` 来获得此结构. 注意内存关联结构可在进程之间共享; `Linux` 线程的实现以这种方式工作

### 内存映射

- 内存映射可被实现来提供用户程序对设备内存的直接存取。意味着关联一些用户空间地址到设备内存

- `mmap`限制以`PAGE_SIZE`为单位进行映射。可以极大提升吞吐量

- `mmap`是`file_operations`的结构一部分。

#### `mmap`原型

- `int (*mmap) (struct file *filp, struct vm_area_struct *vma);`

- 为了执行`mmap`只需要为该地址建立页表，并将`vma->vm_ops`替换成一系列新操作。

### 建立页表的方法

#### 使用`remap_pfn_range`一次性建立

`int remap_pfn_range(struct vm_area_struct *vma, unsigned long virt_addr, unsigned long pfn, unsigned long size, pgprot_t prot);`

`int io_remap_page_range(struct vm_area_struct *vma, unsigned long virt_addr, unsigned long phys_addr, unsigned long size, pgprot_t prot);`

负责为一段物理地址建立新的页表。

第一个函数当`pfn`只想实际物理RAM时使用。后者是当指向`I/O`内存时使用。

#### 使用`nopage_VMA`每次建立一个页表

`struct page *(*nopage)(struct vm_area_struct *vma,unsigned long address,int *type)`

### 地址映射关系

- 在进程的`task_struct` 结构中包含一个指向 `mm_struct` 结构的指针，`mm_strcut` 用来描述一个进程的虚拟地址空间。

- 进程的 `mm_struct` 则包含装入的可执行映像信息以及进程的页目录指针`pgd`。该结构还包含有指向 `vm_area_struct` 结构的几个指针，每个`vm_area_struct`代表进程的一个虚拟地址区间。

- `vm_area_struct` 结构含有指向`vm_operations_struct` 结构的一个指针，`vm_operations_struct` 描述了在这个区间的操作。

- `vm_operations` 结构中包含的是函数指针；其中，`open、close` 分别用于虚拟区间的打开、关闭，而`nopage` 用于当虚存页面不在物理内存而引起的“缺页异常”时所应该调用的函数，当`Linux`处理这一缺页异常时（请页机制），就可以为新的虚拟内存区分配实际的物理内存。

![linux_addree_map.png](https://i.loli.net/2019/12/06/el7NgrRHvXcBjs6.png)

## 参考链接

- [`kmalloc`分配物理内存与高端内存映射](https://cloud.tencent.com/developer/article/1380637)

- [高端内存映射之`kmap_atomic`固定映射](https://cloud.tencent.com/developer/article/1381015)

- [高端内存处理](https://tinylab.gitbooks.io/linux-doc/content/zh-cn/vm/highmem.html)

- [虚拟地址转物理地址](http://chinaunix.net/uid-30282771-id-5148360.html)

- [用户态访问物理地址](http://chinaunix.net/uid-30282771-id-5162413.html)

- [`mmap`详解](https://www.cnblogs.com/huxiao-tee/p/4660352.html)

- [Linux内存管理-页框管理-推荐阅读](https://r00tk1ts.github.io/2017/10/20/Linux%E5%86%85%E5%AD%98%E7%AE%A1%E7%90%86-%E9%A1%B5%E6%A1%86%E7%AE%A1%E7%90%86/#)

