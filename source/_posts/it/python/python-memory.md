---
title: Python 程序內存管理及OOM問題分析
date: 2024-08-03 22:38:00
tags:
	- Python
	- 代碼家
---

## 內存管理

Python 採用以引用計數法為主，以標記-清除算法和分代收集為輔的內存管理策略。

標記-清除算法會從根節點出發標記所有「活動對象」，然後再將沒有標記到的對象標記為「非活動對象」進行回收。因此該算法可以用來解決循環引用導致的內存洩漏問題。

分代收集算法會將內存對象分到三個世代中，每個代觸發回收時只回收當前代，並將存活的對象轉移到下一代，對象所在世代越久遠的越不可能是垃圾，觸發回收的頻率越低。因此該算法通過空間換時間的方式提高了垃圾回收效率。

## OOM 問題分析

當進程中有大量線程在等待執行，或者有大對象未被及時釋放時，會造成系統內存資源緊張，甚至 OOM（內存溢出），從而服務進程被 kill。

<!--more-->

這時候，我們就需要進行內存分析了。有一款工具叫 [memray](https://bloomberg.github.io/memray/getting_started.html) ，可以用來收集和分析 Python 進程的內部內存使用情況。下面逐步簡要介紹下如何使用使用該工具。

### 安裝 `memray`

在 Python 進程所在的（虛擬）環境和進行綁定進程的環境中都需要安裝，命令如下：

```python
# 如果使用容器運行服務，建議將下面兩個步驟寫入 Dockerfile 中
pip3 install memray
# 確保安裝了 gdb 或 lldb，memray工具需要
yum install -y gdb
```

需要確保 Python 進程在安裝了該工具之後重啓。

### 綁定 Python進程

使用 `memray attach` 命令綁定到 Python進程，進行內存數據收集，命令如下：

```python
# 抓取10分鐘的內存數據到文件 attach_file.bin中
python3 -m memray attach --aggregate --duration 600 -o attach_file.bin <進程ID>
```

`memray attach` 的可選參數有：

```bash
options:
  -h, --help            show this help message and exit
  -o FILE, --output FILE
                        Capture allocations into the given file instead of starting a live tracking session
  -f, --force           If the output file already exists, overwrite it
  --aggregate           Write aggregated stats to the output file instead of all allocations
  --native              Track native (C/C++) stack frames as well
  --follow-fork         Record allocations in child processes forked from the tracked script
  --trace-python-allocators
                        Record allocations made by the pymalloc allocator
  --compress-on-exit    Compress the resulting file using lz4 after tracking completes
  --no-compress         Do not compress the resulting file using lz4
  --duration DURATION   Duration to track for (in seconds)
  --method {auto,gdb,lldb}
                        Method to use for injecting commands into the remote process
  -v, --verbose         Print verbose debugging information.
```

### 進行分析

使用 `memray summary` 可以生成匯總表格進行分析，還可以使用 `memray flamegraph` 生成火焰圖，命令如下：

```bash
# 生成匯總表格
python3 -m memray summary attach_file.bin
# 生成火焰圖，HTML文件
python3 -m memray flamegraph attach_file.bin
```

## 一些建議

對象會佔用內存，而內存是有限資源，因此正確管理對象的生命週期相當重要。在本人的編程經驗中，對於對象的管理，我認為有兩個點是需要特別注意的：

### 及時回收大對象

大對象如果得不到及時回收，很容易累積並引發 OOM，因此及時回收大對象尤為重要。Python 中使用以下語句主動銷毀不再使用的大對象，並主動觸發 GC。

```python
# 銷毀對象，會自動調用對象的 __del__ 方法，然後解除對象v對相關數據的引用
del v
# 主動觸發GC
gc.collect()
```

### 使用池化技術

對於進程、線程、網路連接等佔用內存且需要頻繁使用的對象，應該使用池化技術，也就是進程池、線程池或連接池。這樣做既可以避免對象重複創建和銷毀以提升程序執行效率，還可以避免忘記銷毀對象，或者同時創建過多的對象，從而導致內存溢出的情況。

Python 中可以使用  `ProcessPoolExecutor` 創建進程池，使用 `ThreadPoolExecutor` 創建線程池；而連接池就很多了，對於 HTTP 請求，常用的 `requests` 和 `httpx` 都有其連接池的設定，在此就不一一介紹了，使用到的時候可以自行搜索下。

### 避免集合多次擴容

在循環中將對象 append 集合中是值得留意的操作，因爲這樣很容易導致集合多次擴容，影響效率且容易導致多次重新分配內存，產生過多的臨時對象，引發 GC壓力，甚至 OOM。建議在循環之前就確定好集合的容量，避免集合多次擴容。

Python 中可以使用列表推導式或 Numpy庫創建固定大小的列表，如下：

```python
# 創建一個容量為 10 且設置爲 0 的列表
list_a = [ 0 for _ range(10) ]

# 使用 numpy 創建一個同樣的列表
import numpy as np
list_b = np.zeros(10)
```
