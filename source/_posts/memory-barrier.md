---
title: loweer-level-of-code
date: 2019-12-06 20:53:15
tags: [system,c]
---

## 数据一致性
<!-- more -->
<!-- TOC -->

- [数据一致性](#数据一致性)
    - [缓存一致性](#缓存一致性)
    - [顺序一致性](#顺序一致性)
- [内存屏障](#内存屏障)
    - [相关原语以及`x86`指令](#相关原语以及x86指令)
        - [完全内存屏障(`full memory barrier`)](#完全内存屏障full-memory-barrier)
        - [内存读屏障(`read memory barrier`)](#内存读屏障read-memory-barrier)
        - [内存写屏障(`write memory barrier`)](#内存写屏障write-memory-barrier)
        - [实现](#实现)
        - [编译器内存屏障](#编译器内存屏障)
    - [一些参考](#一些参考)
- [多处理器间同步](#多处理器间同步)
- [控制寄存器](#控制寄存器)
    - [`CR0-4`寄存器](#cr0-4寄存器)
- [缓存更新](#缓存更新)
    - [`write through`](#write-through)
    - [`write back`](#write-back)
    - [`dirty-cache`](#dirty-cache)
    - [`clean-cache`](#clean-cache)

<!-- /TOC -->

### 缓存一致性

所谓缓存一致性，就是在多处理器系统中，每个cpu都有自己的L1 cache。很可能两个不同cpu的L1 cache中缓存的是同一片内存的内容，如果一个cpu更改了自己被缓存的内容，它要保证另一个cpu读这块数据时也要读到这个最新的。

不过你不要担心，这个复杂的工作完全是由硬件来完成的，通过实现一种MESI协议，硬件可以轻松的完成缓存一致性的工作。不要说一个读一个写，就是多个同时写都没问题。一个cpu读时总能读入最新的数据，不管它是在自己的cache中，还是在其它cpu的cache中，还是在内存中，这就是缓存一致性。

之前一直认为linux中很多东西是用来保证缓存一致性的，其实不是。缓存一致性绝大部分是靠硬件机制实现的，只有在带lock前缀的指令执行时才与cache有一点关系。（这话说得绝对，但我目前看来就是这样）我们更多的时候是为了保证顺序一致性。

### 顺序一致性

 所谓顺序一致性，说的则是与缓存一致性完全不同的概念，虽然它们都是处理器发展的产物。因为编译器的技术不断发展，它可能为了优化你的代码，而将某些操作的顺序更改执行。
  
 处理器中也早就有了**多发射、乱序执行**的概念。这样的结果，就是实际执行的指令顺序会与编程时代码的执行顺序略有不同。这在单处理器下当然没什么，毕竟只要自己的代码不过问，就没人过问，编译器和处理器就是在保证自己的代码发现不了的情况下打乱执行顺序的。
  
 但多处理器不是这样，可能一个处理器上指令的完成顺序，会对其它处理器上执行的代码造成很大影响。所以就有了顺序一致性的概念，即保证一个处理器上线程的执行顺序，在其它的处理器上的线程看来，都是一样的。这个问题的解决不是光靠处理器或者编译器就能解决的，需要软件的干预。

## 内存屏障

软件干预的方式也非常简单，那就是插入**内存屏障(memory barrier)**。

其实内存屏障这个词，是由搞处理器的人造的，弄得我们很不好理解。内存屏障，很容易让我们串到缓存一致性去，乃至怀疑是否这样做才能让其它cpu看到被修改过的cache，这样想就错了。

所谓内存屏障，从处理器角度来说，是用来串行化读写操作的，从软件角度来讲，就是用来解决顺序一致性问题的。

编译器不是要打乱代码执行顺序吗，处理器不是要乱序执行吗，你插入一个内存屏障，就相当于告诉编译器，屏障前后的指令顺序不能颠倒，告诉处理器，只有等屏障前的指令执行完了，屏障后的指令才能开始执行。

当然，内存屏障能阻挡编译器乱来，但处理器还是有办法。处理器中不是有多发射、乱序执行、顺序完成的概念吗，它在内存屏障时只要保证前面指令的读写操作，一定在后面指令的读写操作完成之前完成，就可以了。

所以内存屏障才会对应有读屏障、写屏障和读写屏障三类。如x86之前保证写操作都是顺序完成的，所以不需要写屏障，但现在也有部分ia32处理器的写操作变成乱序完成，所以也需要写屏障。

其实，除了专门的读写屏障指令，还有很多指令的执行是带有读写屏障功能的，比如带lock前缀的指令。在专门的读写屏障指令出现之前，linux就是靠lock熬过来的。

至于在哪里插入读写屏障，要视软件的需求而定。读写屏障无法完全实现顺序一致性，但多处理器上的线程也不会一直盯着你的执行顺序看，只要保证在它看过来的时候，认为你符合顺序一致性，执行不会出现你代码中没有预料到的情况。所谓预料外的情况，举例而言，你的线程是先给变量a赋值，再给变量b赋值，结果别的处理器上运行的线程看过来，发现b赋值了，a却没有赋值，（注意这种不一致不是由缓存不一致造成的，而是处理器写操作完成的顺序不一致造成的），这时就要在a赋值与b赋值之间，加一个写屏障。

### 相关原语以及`x86`指令

#### 完全内存屏障(`full memory barrier`)

- 保障了早于屏障的内存读写操作的结果提交到内存之后，再执行晚于屏障的读写操作。

- `mfence (asm), void _mm_mfence (void)`

#### 内存读屏障(`read memory barrier`)

- 仅确保了内存读操作

- `lfence (asm), void _mm_lfence (void)`

#### 内存写屏障(`write memory barrier`)

- 仅保证了内存写操作

- `sfence (asm), void _mm_sfence (void)`

#### 实现

常见的`x86/x64`，通常使用`lock`指令前缀加上一个空操作来实现，注意当然不能真的是`nop`指令，但是可以用来实现空操作的指令其实是很多的，比如`Linux`中采用的

    addl $0, 0 (%esp)

#### 编译器内存屏障

编译器会对生成的可执行代码做一定优化，造成乱序执行甚至省略（不执行）。`gcc`编译器在遇到内嵌汇编语句：

    asm volatile("" ::: "memory");
  
将以此作为一条内存屏障，重排序内存操作。即此语句之前的各种编译优化将不会持续到此语句之后。也可用内建的`__sync_synchronize`

`Microsoft Visual C++`的编译器内存屏障为：

    _ReadWriteBarrier() MemoryBarrier()
  
`Intel C++`编译器的内存屏障为：

    __memory_barrier()

### 一些参考

- [乱序的例子](https://blog.csdn.net/zenny_chen/article/details/5980997)

- [从Java角度总结](https://monkeysayhi.github.io/2017/12/28/%E4%B8%80%E6%96%87%E8%A7%A3%E5%86%B3%E5%86%85%E5%AD%98%E5%B1%8F%E9%9A%9C/)

- [不同指令的测试](https://zhuanlan.zhihu.com/p/41872203)

## 多处理器间同步

有了SMP之后，线程就开始同时在多个处理器上运行。只要是线程就有通信和同步的要求。幸好SMP系统是共享内存的，也就是所有处理器看到的内存内容都一样，虽然有独立的L1 cache，但还是由硬件完成了缓存一致性处理的问题。

那不同处理器上的线程要访问同一数据，需要临界区，需要同步。靠什么同步？之前在UP系统中，我们上靠信号量，下靠关中断和读修改写指令。现在在SMP系统中，关中断已经废了，虽然为了同步同一处理器上的线程还是需要的，但只靠它已经不行了。读修改写指令？也不行了。在你指令中读操作完成写操作还没进行时，就可能有另外的处理器进行了读操作或者写操作。缓存一致性协议是先进，但还没有先进到预测这条读操作是哪种指令发出来的。

所以x86又发明了带lock前缀的指令。在此指令执行时，会将所有包含指令中读写地址的cache line失效，并锁定内存总线。这样别的处理器要想对同样的地址或者同一个cache line上的地址读写，既无法从cache中进行（cache中相关line已经失效了），也无法从内存总线上进行（整个内存总线都锁了），终于达到了原子性执行的目的。

当然，从P6处理器开始，如果带lock前缀指令 要访问的地址本来就在cache中，就无需锁内存总线，也能完成原子性操作了（虽然我怀疑这是因为加了多处理器内部公共的L2 cache的缘故）。

因为会锁内存总线，所以带lock前缀指令执行前，也会先将未完成的读写操作完成，也起到内存屏障的功能。

现在多处理器间线程的同步，上用自旋锁，下用这种带了lock前缀的读修改写指令。当然，实际的同步还有加上禁止本处理器任务调度的，有加上任务关中断的，还会在外面加上信号量的外衣。linux中对这种自旋锁的实现，已历经四代发展，变得愈发高效强大。

- [原文链接](https://blog.csdn.net/qb_2008/article/details/6840593)

## 控制寄存器

控制寄存器（CR0～CR3）用于控制和确定处理器的操作模式以及当前执行任务的特性

### `CR0-4`寄存器

- CR0中含有控制处理器操作模式和状态的系统控制标志；

- CR1保留不用；

- CR2含有导致页错误的线性地址；

- CR3中含有页目录表物理内存基地址，因此该寄存器也被称为页目录基地址寄存器PDBR（Page-Directory Base addressRegister）

- [参考](https://blog.csdn.net/epluguo/article/details/9260429)

## 缓存更新

### `write through`

直写式（write through），也叫**直写**，即CPU在向Cache写入数据的同时，也把数据写入主存以保证Cache和主存中相应单元数据的一致性，其特点是简单可靠，但由于CPU每次更新时都要对主存写入，速度必然受影响。

> write throgh:In a write-through cache, data is writen to main memory at the sam e time as the cache is updated.

cache的数据update后，main mem的数据同时update

### `write back`

回写式（write back）即CPU只向Cache写入，并用标记加以注明，直到Cache中被写过的块要被进入的信息块取代时，才一次写入主存。这种方式考虑到写入的往往是中间结果，每次写入主存速度慢而且不必要。其特点是速度快，避免了不必要的冗余写操作，但结构上较复杂。

> write back (also known as copyback):In a write-back cache, data is only written to main memory when it is forced out of the cache on line replacement following a cache miss. Otherwise, writes by the processor only update the cache.

cache的数据update后，main mem的数据不同时update（cache line 被称为dirty）；直到cache数据无效时，才将main mem的数据 update（cache line被称为clean）

### `dirty-cache`

> A cache line in a write-back cache that has been modified while it is in the cache is said to be dirty. A cache line is marked as dirty by setting the dirty bit. If a cache line is dirty, it must be written to memory on a cache miss because the next level of memory contains data that has not been updated. The process of writing dirdy data to main memory is called cache cleaning.

### `clean-cache`

> A cache line that has not been not modified while it is in the cache is said to be clean. To clean a cache is to write dirty cache entries into main memory.If a cache line is clean, it is not wirtten on a cache miss because the next level of memory contains the same data as the cache.
