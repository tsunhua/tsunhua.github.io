---
title: Go调度器
p: it/go/go-scheduler.md
date: 2021-12-27 11:00:00
tags:
- Go
---

现在有三种常见的线程模型，包括：
1. N:1，即 N 个用户线程对应一个系统线程，节省上下文（context switch）切换开销；
2. 1:1，即 1 个用户线程对应一个系统线程，充分利用多个核心（multi-core）；
3. M:N，即 M 个用户线程对应 N 个系统线程，节省上下文开销并充分利用多个核心。

Go的线程调度模型就是 M:N。

<!-- more -->

我们使用三个实体来表示 Go 的线程：
1. 三角框的 M，代表系统线程，在运行时代码中写作 M（Machine）；
2. 圆框的 G，代表 goroutine，包含栈和指令指针等等信息；
3. 方框的 P，代表调度的上下文（context for scheduling），在运行时代码中写作 P（Processor）。

![](https://user-images.githubusercontent.com/11910355/147430806-a7b41eec-5a34-4510-8d9d-2a3d3028a86d.png)

在这种模型中，M 持有 P 来运行 G（M hold P to run G），蓝色的G表示正在运行，灰色的G置于P本地的 runqueue 中等待被调度，P 的数量可以通过 GOMAXPROC 设置（从GO1.5起默认等于CPU核心数）。

为什么不直接将 G 挂在 M 上，而是通过 P 来调度呢？

因为使用P可以灵活高效地管理G，具体如下：

第一，P 可以在 M 阻塞（比如syscall）时，从阻塞的M脱离，挂到其他可用的M上，保证后续的G正常运行。

![](https://www.morsmachine.dk/syscall.jpg)

第二，在阻塞的M解除阻塞状态时，会从其他M抢夺P；如果抢不到，就将G置放到全局的 runqueue中，然后将自己放入线程缓存并休眠。

第三，P 会定时检查全局的 runqueue 中是否有G，有的话拿过来运行。

第四，当 P 运行完本地 runqueue中的任务后，会检察全局的 runqueue 是否有G；如果没有，就从其他P抢夺一半的G过来运行。

![Steal work](https://www.morsmachine.dk/steal.jpg)

参考：[The Go scheduler - Morsing's blog](https://www.morsmachine.dk/go-scheduler)
