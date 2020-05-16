---
title: char-device-update
date: 2019-11-20 09:20:12
tags: [drivers]
---
<!-- TOC -->

- [字符设备的改进](#字符设备的改进)
    - [增加并发 解决竞态](#增加并发-解决竞态)
        - [可用技术方案](#可用技术方案)
        - [情况分析](#情况分析)
    - [阻塞操作 `wait-queue`](#阻塞操作-wait-queue)
    - [轮询操作 `select,poll,epoll`](#轮询操作-selectpollepoll)
        - [应用程序中的`select`函数](#应用程序中的select函数)
        - [`poll`函数](#poll函数)
    - [异步通知及异步`IO`](#异步通知及异步io)
    - [异步`I/O`](#异步io)
    - [中断与定时器](#中断与定时器)
        - [[一个基于软中断的秒设备](https://github.com/huqianshan/OperatingSystemAndCompiler/blob/master/drivers/second/second.c)](#一个基于软中断的秒设备httpsgithubcomhuqianshanoperatingsystemandcompilerblobmasterdriverssecondsecondc)
    - [内存映射](#内存映射)

<!-- /TOC -->
## 字符设备的改进

<!--more-->
### 增加并发 解决竞态

#### 可用技术方案

- 屏障

- 中断屏蔽

- 原子操作

- 互斥体 `以进程为竞争单位`

    > 不适用于以下情况
    > - 出现中断或者软中断-->`spin_lock_irq(),spin_lock_irqsave()`
    > - 频繁的切换
    > - 临界区占用时间过短

- 信号量 `教科书经典定义，现在更推荐**互斥体**`

- 自旋锁 `貌似以CPU为竞争资源（默认禁止本地cpu抢占）`
  
  - 顺序锁`seq-lock`

  - 读写锁

  - > 不适用于包含如下情况  
    > - 引起阻塞的代码
    > - 临界区过大
    > - 长时间占用临界区

  - > 注意事项
    > 多核`SMP`情况下，任何一个核拿到了自旋锁，该核上的**抢占**调度就暂时禁止。但仍可能受到**中断**和**底半部`（BH)`**影响。
    > 多核`SMP`编程中，如果进程和其中断进程可能会范围同一临界区，则需要在进程中调用`spin_lock_irq()`,**中断上下文**中调用`spin_lock()`
  
  - > 总结
    > - 即`spin_lock()`可以禁止本地`CPU`的抢占，已及其他`CPU`的竞争
    > - `spin_lock_irq()`可以进一步的禁止本地`CPU`的中断
    > - `spin_lock_irqsave()`进一步增加一个保存中断开启状态，即在关闭本地中断之前禁止中断，如果能够确保没有其他代码禁止本地`CPU`的中断，则可以使用上一个函数。

- `RCU (Read-Copy-Update)`

- 完成量 `Completion`

#### 情况分析

1. 在`tdlcd`中，读写函数中，存在着可能阻塞的系统调用如`copy_from_user`等函数；如果选择自旋锁，在获得锁之后，阻塞在此类函数上，系统切换到调用函数，且也在等待占有这个锁，可能会引发死锁。所以选用`互斥体` 其实更好的选择应该是`信号量semphore`

- [tdlcd+mutex code 链接](https://github.com/huqianshan/OperatingSystemAndCompiler/blob/master/drivers/ch6/tdlcd.c)

### 阻塞操作 `wait-queue`

- [tdlcd+block+sleep code](https://github.com/huqianshan/OperatingSystemAndCompiler/blob/master/drivers/tdlcd/tdlcd_fifo.c)

- ![06-tdlcd-1.5-block.jpg](https://i.loli.net/2019/11/20/FnEsR4JWQU6ITLN.jpg)

### 轮询操作 `select,poll,epoll`

#### 应用程序中的`select`函数

> `int select(int numfds,fd_set *readfds,fd_set *writefds,fd_set *exceptfds,struct timval *timeout)`  
> `numfds`为需要检查的最高文件描述符+1,档任何一个文件描述符变得可写可读时，`select`返回。
> 没有文件描述符满足要求时，`select`进程保持睡眠（阻塞）
> 实际上调用`select`时，每个驱动的`poll`接口被调用，即`select`进程被挂到了每个驱动的等待队列上。
> 一般来说，少量`fd`使用`select`.反之，`epoll`

#### `poll`函数

> `unsigned int (*poll)(struct file *filp),struct poll_table *wait)`

两个参数分别为文件结构体指针，和轮询表指针。

1. 对可能引起设备文件状态变化的等待队列调用`poll_wait(不会引起阻塞)`函数，将对应等待队列加入到轮询表中。 **实际作用是让等待队列唤醒因`select`而睡眠的进程**

2. 返回表示是否能对设备进行无阻塞读写访问的掩码。

- [epoll 测试文件](https://github.com/huqianshan/OperatingSystemAndCompiler/blob/master/drivers/tdlcd/tdlcd_fifo_epoll.c)

### 异步通知及异步`IO`

异步通知:`信号驱动的异步I/O`

- 通过`F_SETDIWB`命令控制设备文件的拥有者

- 通过`F_SETFL`命令设置设备文件以支持`FASYNC`

- 通过`signal`函数连接信号和信号处理函数

![07-tdlcd-async.jpg](https://i.loli.net/2019/11/22/Wdsv39to4IgOTGr.jpg)

[git diff for async](https://github.com/huqianshan/OperatingSystemAndCompiler/commit/01a234b19a7e3167bc738e238a884907d49ca228?diff=split)

### 异步`I/O`

`Linux`常见情况为同步`I/O`,即发出请求之后，应用程序便会阻塞直到请求得到响应。且在等待时不需要占用`CPU`

> 爬虫是不是这样的例子？

异步`I/O`则要么过一段时间来查询之前`I/O`请求完成情况，要么`I/O`请求完成了会自动调用完成绑定的**回调函数**。

实际上阻塞`I/O`是同步的。

`Linux 异步I/O`在内核中得到了实现。

> 对于块设备，`AIO`可以一次性发出大量读写调用，然后通过**通用块层**的调度来实现更好的吸能。用户程序也可以减少过多的同步负载，在业务逻辑层更灵活的进行并发控制和负载均衡。
> 由于相较于用户空间的`glibc`多线程同步实现，减少了线程的负载和潜在的上下文切换。
> `sudo apt-get install libaio-dev`

### 中断与定时器

为了在中断执行时间尽量短和中断处理需完成的工作量大之间找到平衡，`Linux`将中断处理程序分为两个半步：`Top Half  Bottom Half`.

顶半部通常只完成读取状态，登记等工作，且一般不可被中断。

底半部机制主要有`tasklet,工作队列，软中断，线程化irq`

- [ ] 机制未了解
- [x] 待做事项测试

#### [一个基于软中断的秒设备](https://github.com/huqianshan/OperatingSystemAndCompiler/blob/master/drivers/second/second.c)

### 内存映射
