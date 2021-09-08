---
title: Concurrency in Go
date: 2021-09-08 21:41:30
p: it/go/concurrency-in-go.md
tags:
- Go
---



*Concurrency in Go* is an excellent book written by Katherine Cox-Buday. And It is impressive and drive me to learn deeply about Go.

《Go並發編程》是凱瑟琳·考克斯布迪執筆的一本絕好的書籍。此書令我印象深刻，並驅使我深入學習Go。

<!--more-->

Let's get a bird's eye view of this book at first. There are six topics we should care about, including:

1. Troubles we face when using concurrency
2. Go's philosophy on concurrency
3. Go's tools on concurrency
4. Concurrency patterns in Go
5. Concurrency at scale
6. How goroutine works

我們先來總覽此書，有六項我們需要關注的主題，包含：

1. 並發面臨的問題
2. Go的並發哲學
3. Go的並發工具
4. 基於Go的並發模式
5. 大規模並發
6. goroutine如何工作

##Troubles we face when using concurrency (並發面臨的問題)

Concurrency is hard but significant. It is the multicore processors' time, and Moore's Law had come to end. We should improve our program's performance by taking full advantage of multicore. According to Amdahl's Law, the program's potential performance gains from implementing solution to a problem in parallel manner. 

並發難而重要。這是一個多核處理器的時代，摩爾定律已經過時了。我們應該通過充分利用多核心來提升程序的性能。據阿姆達爾定律，程序潛在性能從用並行的方式實現問題的解決方案獲得。



What concurrency troubles us is that it force us to take attention to what we don't need to care before:

1. Race condition
2. Atomicity
3. Memory access synchronization
4. Deadlock, livelock, and starvation

並發困擾我們之處在於其迫使我們關注我們之前無需關心的東西：

1. 競態條件
2. 原子性
3. 內存訪問同步
4. 死鎖、活鎖及餓死



The so-called race condition is the problem occurred  when two or more operations must be executed in order, but the program doesn't guarantee it.

所謂競態條件就是當兩項或多項操作是有序的而程序未能保證其有序執行而引發的錯誤情況。例如：

```go
var data = 0
go func(){
  data++
}()
// maybe sleep a while, so that you can find the problem
// time.Sleep(1*time.Second)
println(data)
```

We cannot guarantee that the write operation to data or the read operation is the first, because they're run in concurrency, so it causes the race condition and the undetermined result.

因對 data 的寫操作和讀操作是並發的，我們無法保證誰先誰後，因而產生競態條件和結果的不確定性。





