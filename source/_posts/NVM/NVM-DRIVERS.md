---
title: linux-information
date: 2020-03-29 14:25:19
tags:
- NVM
---

## 中断

- 硬件中断
- 软件中断
- 中断下半部
<!--more-->
## 时钟

### `jiffies`

`jiffies` 记录着cpu自开机以来的时钟中断数`(tick)`。系统一秒钟能产生`HZ`个中断`(timer interrupt)`。`1MHz＝1000，000Hz，1KHz=1000Hz`.

  - 频率是周期的倒数，一般是一秒钟中断产生的次数
      - 假如系统的频率是`200Mhz`,那么一次中断的间隔是`1秒/200,000，000Hz=0.000 000 005秒`.所以理论上系统的精确度是5纳秒
  - `LINUX系统时钟频率`是一个常数HZ来决定的， 通常`HZ＝100`，那么他的精度度就是`10ms`（毫秒）。也就是说每10ms一次中断。所以一般来说Linux的精确度是10毫秒。

    - `Tick`是HZ的倒数，意即timer interrupt每发生一次中断的时间。如HZ为250时，tick为4毫秒(millisecond)

  - 如果需要更高的精度，则需要访问特定寄存器`rdtsl?`。

#### 查看内核设置

- 查看每秒`timer interrupt` 次数

`cat /proc/interrupts | grep timer && sleep 1 && cat /proc/interrupts | grep timer`

#### 类型及溢出

##### 32位`unsigned long  volatile Jiffies` 全局变量

`jiffies` 为Linux核心变数(unsigned long)，在头文件<linux/sched.h>中定义.

它被用来记录系统自开机以来，已经过了多少tick。每发生一次timer interrupt，Jiffies变数会被加一。值得注意的是，Jiffies于系统开机时，并非初始化成零，而是被设为-300*HZ (arch/i386/kernel/time.c)，即代表系统于开机五分钟后，jiffies便会溢位。

因此连续累加一年又四个多月后就会溢出(假定HZ=100，1个jiffies等于1/100秒，jiffies可记录的最大秒数为 (2^32 -1)/100=42949672.95秒，约合497天或1.38年)，即当取值到达最大值时继续加1，就变为了0。

##### 64位`jiffies_64`

64位jiffies 变量。在32位平台上需要加锁访问 `get_jiffies_64()`。要等到此变数溢位可能要好几百万年

##### 溢出处理

通过内置`wrapper`函数。先检查类型，然后转换为`signed long`比较是否小于零。

```c
#define time_after(a,b) \

(typecheck(unsigned long, a) && \

typecheck(unsigned long, b) && \

((long)(b) - (long)(a) < 0))
```

#### 赋值

```c++
#include <linux/jiffies.h>
unsigned long j, stamp_1, stamp_half, stamp_n;

j = jiffies;                      /* read the current value */
stamp_1    = j + HZ;              /* 1 second in the future */
stamp_half = j + HZ/2;            /* half a second */
stamp_n    = j + n * HZ / 1000;   /* n milliseconds */
```

#### 判断

```C++
/**
* The first evaluates true when a, as a snapshot of jiffies, represents a time after b, the second evaluates true when time a is before time b, and the last two compare for "after or equal" and "before or equal."
*/
#include <linux/jiffies.h>
int time_after(unsigned long a, unsigned long b);
int time_before(unsigned long a, unsigned long b);
int time_after_eq(unsigned long a, unsigned long b);
int time_before_eq(unsigned long a, unsigned long b);
```

#### 转换

The code works by converting the values to `signed long`, subtracting them, and comparing the result. If you need to know the difference between two instances of jiffies in a safe way, you can use the same trick: `diff = (long)t2 - (long)t1;`.

`msec = diff * 1000 / HZ;` Get the milliseconds 微秒

```c++
#include <linux/time.h>

unsigned long timespec_to_jiffies(struct timespec *value);
void jiffies_to_timespec(unsigned long jiffies, struct timespec *value);
unsigned long timeval_to_jiffies(struct timeval *value);
void jiffies_to_timeval(unsigned long jiffies, struct timeval *value);
```

- `struct timeval`  seconds + microsconds
- `struct timespec` seconds + nanoseconds

#### 参考链接

[Linux内核中的jiffies及其作用介绍及jiffies等相关函数详解](https://my.oschina.net/u/174242/blog/71851)

## 内核线程

### 操作系统调度算法

CFS

### `task_struct` 进程描述符

### `kthreads`内核线程

## `/proc`文件系统

- read/write,copy_to_usr

[lldch03s08](https://www.oreilly.com/library/view/linux-device-drivers/0596000081/ch03s08.html)

- The return value for read is interpreted by the calling application program as follows:

- If the value equals the count argument passed to the read system call, the requested number of bytes has been transferred. This is the optimal case.

- If the value is positive, but smaller than count, only part of the data has been transferred. This may happen for a number of reasons, depending on the device. Most often, the application program will retry the read. For instance, if you read using the fread function, the library function reissues the system call till completion of the requested data transfer.

- If the value is 0, end-of-file was reached.

- A negative value means there was an error. The value specifies what the error was, according to <linux/errno.h>. These errors look like -EINTR (interrupted system call) or -EFAULT (bad address).

### seqfile
