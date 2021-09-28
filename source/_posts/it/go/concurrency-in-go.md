---
title: Concurrency in Go
date: 2021-09-08 21:41:30
p: it/go/concurrency-in-go.md
tags:
- Go
- TODO
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

1. 競態
2. 原子性
3. 內存訪問同步
4. 死鎖、活鎖及餓死


The so-called race condition is the problem occurred  when two or more operations must be executed in order, but the program doesn't guarantee it. For Example:

所謂競態就是當兩項或多項操作是有序的而程序未能保證其有序執行而引發的錯誤情況。例如：

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

因對 data 的寫操作和讀操作是並發的，我們無法保證誰先誰後，因而產生競態和結果的不確定性。

Atomicity means that the operation is indivisible and uninterruptible in particular context. 

原子性意味著操作在特定的上下文中是不可分割和不可中斷的。這裏要強調下上下文，因為在進程中爲具備原子性的操作，在操作系統中可能不是；在操作系統中是的，在機器中可能不是；在機器中是的，在整個應用中可能不是。

大部分語句都不具備原子性，比如函數、方法等，又比如 i++（可以分爲取值、增值和賦值三個操作）。

Critical section, the section of program that needs to exclusive access to a shared resource.

臨界區段：需要獨佔訪問共享資源的代碼段。

可以通過內存訪問同步可以解決數據爭用（data race），但無法解決競態（race condition）。如下：

```go
var memoryAccess sync.Mutex
var value int
go func(){
  memoryAccess.Lock()
  value++
  memoryAccess.Unlock()
}()

memoryAccess.Lock()
if value == 0{
  fmt.Printf("the value is %d.\n", value)
}else{
  fmt.Printf("the value is %d.\n", value)
}
memoryAccess.Unlock()
```



死鎖是並發的進程相互等待的情況。

死鎖的四個條件：

1. 互斥：資源是互斥訪問的
2. 等待條件：進程持有一項資源的同時又等待另一項資源
3. 不可搶佔：資源一旦被一個進程持有，其他進程不可搶佔，只能等待持有者釋放
4. 循環等待：進程間相互持有對方所需的資源。

條件1和3是描述資源的屬性，互斥訪問且不可搶佔；條件2和4描述進程的狀況，持有對方需要的資源的同時又在等待對方持有的資源。



活鎖是並發的進程仍在運行，但沒能改變程序的狀態。

餓死是一個並發的進程無法獲取需要的所有資源以進行工作。死鎖及活鎖情況下，所有進程都是同等餓死，沒有工作是可以完成的。

## Go的並發哲學

