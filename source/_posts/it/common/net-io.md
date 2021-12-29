---
title: 网络I/O
p: it/common/net-io
date: 2021-12-29 16:30:00
tags:
- net
---

区分几个概念：
同步（synchronous）和异步（asynchronous）是消息通知的机制，是从消息发送方的角度看；
阻塞（blocking）和非阻塞（non-blocking）是线程等待通知的过程，是从接收方的角度看。
多路复用是指单一线程监听多个文件描述符（file descriptor）。
