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

<!-- /TOC -->
## `Linux`内核地址空间

内存分为三个区段: 1. 用于`DMA`的内存，2. `常规内存`，3.`高端内存`

![funciton call](https://pic1.zhimg.com/80/v2-c381d93642b716770c6705dac13a30c8_hd.jpg)

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

与`vmalloc`相同的是，`ioremap`也是面向页的，会修改页表

## `Linux`的内存管理
