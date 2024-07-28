---
title: Python 程序如何做到高效且穩健？
date: 2024-07-28 10:49:00
tags:
- Python
---

Python 幾乎是每個程序員都會使用的語言，但大多數人都將 Python 視為腳本語言，在需要的時候運行一下，進行數據處理或抓取等。大部分情況下都是一次性的工作（Job），很少有人會將其作爲長期運行的後端服務。這是爲何？

Python 是一門解釋型的語言，其依賴於 Python解釋器（或直譯器，官方的且最流行的是 CPython解釋器）來加載源代碼然後解釋運行。解釋運行使得 Python可以在終端中直接運行 `python` 即可開始一邊寫代碼一邊看運行結果，對用戶相當友好，但與之同時也帶來了無可避免的性能問題，從而難以成為後端服務的主流。主流如 Java、Go 都是編譯型的語言，意味著源代碼需要先編譯成二進制文件（在Java中是字節碼），然後直接在運行時（在Java中是JVM）中運行，且在編譯成二進制文件的過程中通常會進行若干優化，使得運行的程序更加高效。

<!-- more -->

還有一個更爲嚴重的問題是：Python 中的解釋器 CPython 中的全局解釋鎖問題（GIL）導致單個 Python進程裏同時只有一個線程（或執行緒）在執行，限制了任務並行處理的能力，無法充分利用 CPU 的多核能力。因而，在 Python中使用多線程（multithread）進行 CPU密集型操作往往比單線程來得慢。通常，Python用戶會採用多進程（multiprocess）來處理 CPU密集型操作，從而避開此問題。可期待的是，尚在預發佈狀態的 [Python3.13](https://docs.python.org/zh-cn/3.14/whatsnew/3.13.html)計劃實現 [PEP 703](https://peps.python.org/pep-0703/)以移除 GIL限制，或能解決此問題。

此外，Python有著割裂的異步編程生態，常常讓新手不知所措。進程、線程、[綠程](https://greenlet.readthedocs.io/en/latest/)（greenlet）、[協程](https://docs.python.org/zh-cn/3/library/asyncio-task.html)（coroutine），令人眼花瞭亂。進程和線程自然不需要多講了。綠程和協程呢？它們是 Python中異步編程的兩種方式，綠程需要使用第三方庫 [gevent](https://www.gevent.org/)並在進行猴子補丁（Monkey patching）後方可正常使用；協程使用 asyncio 及 async/await原語，asyncio在 3.4版本後已進入官方庫，async/await原語在3.5版本後被引入。

asyncio 的引入使得第三方庫逐漸出現割裂，同步和異步各成生態。比如連接 MySQL的庫分 pymysql 還有 aiomysql，pymysql 用於MySQL的同步調用，aiomysql 用於 MySQL的異步調用。此種割裂是其他編程語言罕見的。不經讓人發出疑問：是什麼造成了這種割裂？

數年的 Go開發經驗，自然使得我將 Go中的協程（goroutine）和 Python中協程（coroutine）進行比較。Go中的代碼都是運行在 goroutine 中的，默認是主協程，可以通過在函數調用前添加 `go` 關鍵字從而將函數置於新的協程之中運行。所有協程交由運行時統一管理，在多個線程中進行調度。Go用戶並不需要關心函數在哪個線程之上運行，以及何時運行，也無法操縱 goroutine。Go運行時將 M 個協程調度到 N 個線程（M:N調度），並在協程阻塞時掛起，使得線程可以運行下一個協程。線程交由運行時，因而也無需頻繁創建和銷毀線程，而 goroutine 是佔用的內存空間較少，創建goroutine 是廉價操作，這大大提高了程序運行效率。

Go 可謂大道至簡，將複雜留給自己，簡單留給用戶，只需一個 `go`，不用關心進程和線程。反觀 Python，在並發或並行執行上就有多進程、多線程和多協程，共三套方案。每套方案都有各自的用途和侷限，用戶常常在其中迷失，同時也增加了程序維護和調錯的複雜度。

Python 把線程對象和協程對象交給了用戶，且 M個協程是綁定於 1 個線程之上的（M:1調度），無法被調度到其他線程上。

由此我們可以初步得出 Python 同、異步生態割裂的原因：
1. Python 是解釋型語言，沒有運行時管理，無法隱藏進程、線程的複雜，無法實現 M:N 調度。
2. Python 中官方的 CPython解釋器有 GIL 限制，即使實現了 M:N 調度也無法實現並行處理。

未來，Python 程序要更高效且穩健地運行，我認爲勢必要實現以下幾點：
1. 移除 GIL限制，釋放多線程並行能力。可喜的是，這點已經在 Python3.13預發佈版本中實現。
2. 如果要實現極致的性能，那麼最好是隱藏進程、線程和協程的概念及操作，將線程和協程交由運行時管理。這還有助於弭合 Python中同、異步編程的鴻溝。已知目前有第三方庫 [PyInstaller](https://pyinstaller.org/en/stable/index.html) 可以實現將 Python文件編譯成一個二進制文件，並有部分優化字節碼能力。
3. 強化依賴包的管理。如果無法達到依賴的嚴格統一，那麼將會給團隊協作造成麻煩，而且排查線上問題的複雜度將上升。目前有第三方庫 [poetry](https://python-poetry.org/docs/) 可以做到這點。

回到當前的狀況，在目前普遍使用的是 3.9 左右版本的情況下，我們應該如何做到高效而穩健呢？

1. 引入 `poetry` 庫，強化依賴包的管理，保證依賴的嚴格統一，這是程序在各個環境下正確運行的關鍵。也可採用統一的 Docker基礎鏡像的方式保證在 Docker環境下的依賴統一。
2. 對於 CPU密集型的任務，應選用進程池（採用 [multiprocessing.pool](https://docs.python.org/zh-cn/3/library/multiprocessing.html#multiprocessing.pool.Pool) 或 [ProcessPoolExecutor](https://docs.python.org/zh-cn/3/library/concurrent.futures.html)）進行處理，而不是線程池。
3. 對於 IO密集型的任務，可以使用線程池，但推薦選用協程或綠程。原因是創建線程的過程不比創建協程的過程高效；而且線程則由系統管理，會產生系統調用，而協程由用戶管理，管理效率較高。
4. 當決定採用協程進行異步編程時，應審視舊有代碼中是否有耗時的同步調用，如有應盡量換成異步，以避免阻塞事件循環。如難以換成異步，應再次審視任務是 CPU密集型還是 IO密集型，如是 CPU密集型應將任務置於進程池中執行；如是 IO密集型則應置於線程池。（ `await loop.run_in_executor()`）