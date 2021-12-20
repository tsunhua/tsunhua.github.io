---
title: Unicode 字符集及UTF編碼入門
p: it/common/unicode
date: 2021-12-20 21:06:00
tags:
- Unicode
- UTF-8
- UTF-16
- BOM
mathjax: true
---

開始介紹 Unicode 之前，我們先來做一道不定項選擇題。

```css
問題1：請問以下說法正確的是（）

A. 所有中文字符都可用 UTF-8 編碼，並佔用 3 個字節。
B. 字符串可以直接轉成字節數組，字節數組可以直接轉成字符串。
C. 文本的編碼順序跟其書寫順序一致，不一定是按從左到右從上到下順序。
D. 帶 BOM 的文本一定是 UTF-8 編碼，不帶 BOM 的文本不一定是 UTF-8 編碼。
E. Unicode、GBK 和 UTF-8 都是不同的編碼方式。
F. UTF-16 不兼容 ASCII 碼
G. 十進制的數字可以轉成二進制，因此不需要編碼。
```

答案文章末尾揭曉，如果著急想對答案可以先翻到末尾核對；如果想知道為什麼，那就帶著問題繼續往下看吧。

## 字符集

Unicode 是一種國際通用的字符集。

什麼是字符？計算機中的字符分為兩種：打印字符和非打印字符。打印字符包括數字、字母、漢字、假名、標點符號等等，非打印字符又稱之為控制字符，常見的有：回車（'\r'，U+000D）、換行（'\n'，U+000A）等等。

```css
問題2：數字 123 由（）個字符組成？
```

什麼是字符集？字符集就是字符的集合，不同的字符集包含的字符類型和數量可能不一樣。Unicode 是字符集的一種。

字符之所以能被計算機處理，其中最為關鍵的是字符能夠被正確地編碼和解碼。字符的編碼是字符在對應字符集中的序號。此序號是一個整數，稱之為字符碼點 （code point）。不同的字符集可能會對同樣的字符有不同的碼點表示，甚至沒有表示（並不是所有字符在字符集中都有定義）。

<!--more-->

```css
問題3：有一種語言只有五種字符，暫記錄為「金木水火土」，請自定義碼表並說明需要多少個比特位進行編碼。
```

有人說：直接用一個整型來表示用一個字符不就可以了嗎？可以是可以，不過整型大小固定 4 個字節，浪費空間。比如數字 123 使用 ASCII 字符集需要 `1*3=2` 個字節，而使用固定 4 個字節的方式將是 `4*3=12` 字節。

常見的字符集有：

1. US-ASCII（ISO646-US）：美國信息交換標準代碼，1967年首次發表，1986年最後更新，7位，共 128 個字符。
2. ISO-8859-1（ISO-LATIN-1）：1980年發表，8位，共 256 個字符，兼容 US-ASCII。
3. GB2312：國標2312，1980年發表，共 7,445 個字符，兼容 US-ASCII；
4. GBK：國標擴展碼，1995年發表，共 21,886 個字符，兼容 GB2312。
5. GB18030：國標18030，採用可變長編碼，每個字由 1、2 或 4 個字節組成，2000年發表，2005年更新，共 70,244 個字符，兼容 GBK，並實現了 Unicode 2.0 定義的碼位。
6. Unicode：統一碼，1994年發表1.0，2021年發佈14.0版本。

## Unicode

Unicode 碼點，取值範圍為 [U+0000, U+10FFFF]。

```css
問題4：已知 Unicode碼點取值範圍為 [U+0000, U+10FFFF]，請問最多可以表示（）種字符？
```

Unicode 碼點使用平面（Plane）進行歸類，有：

| 平面               | 始末字符值              | 用途                                                         |
| ------------------ | ----------------------- | ------------------------------------------------------------ |
| 0號平面（Plane 0） | `U+0000` - `U+FFFF`     | 基本多文種平面（Basic Multilingual Plane，簡稱 BMP），保留 `U+D800` - `U+DFFF`。 |
| 1號平面            | `U+10000` - `U+1FFFF`   | 多文種補充平面（Supplementary Multilingual Plane，簡稱 SMP） |
| 2號平面            | `U+20000` - `U+2FFFF`   | 表意文字補充平面（Supplementary Ideographic Plane，簡稱 SIP） |
| 3號平面            | `U+30000` - `U+3FFFF`   | 表意文字第三平面（Tertiary Ideographic Plane，簡稱 TIP）     |
| 4號平面~13號平面   | `U+40000` - `U+DFFFF`   | （尚未使用）                                                 |
| 14號平面           | `U+E0000` - `U+EFFFF`   | 特別用途補充平面（Supplementary Special-purpose Plane，簡稱 SSP） |
| 15號平面           | `U+F0000` - `U+FFFFF`   | 私人使用區（A區）（Private Use Area-A，簡稱 PUA-A）          |
| 16號平面           | `U+100000` - `U+10FFFF` | 私人使用區（B區）（Private Use Area-B，簡稱 PUA-B）          |

值得注意的是：**Unicode 只定義了碼點，而字符到具體的字節序列的映射由 UTF（Unicode/UCS Transformation Format 統一碼轉化格式） 實現**。

UTF 目前有UTF-8、UTF-16 和 UTF-32。

```css
問題5：Unicode的每個平面最多可以表示（）種字符？BMP除去保留的區域外，共可以表示（）種字符？
```

## UTF-8

UTF-8 是面向字節（8位）的 Unicode 編碼形式，使用一個、兩個、三個字節表示BMP上的字符，使用四個字節表示 BMP 外的字符。兼容 US-ASCII 字符集。

| 碼點位數 | 範圍                   | 字節序列 | Byte 1     | Byte 2     | Byte 3     | Byte 4     |
| -------- | ---------------------- | -------- | ---------- | ---------- | ---------- | ---------- |
| 7        | `U+0000` - `U+007F`    | 1        | `0xxxxxxx` |            |            |            |
| 11       | `U+0080` - `U+07FF`    | 2        | `110xxxxx` | `10xxxxxx` |            |            |
| 16       | `U+0800` - `U+FFFF`    | 3        | `1110xxxx` | `10xxxxxx` | `10xxxxxx` |            |
| 21       | `U+10000` - `U+10FFFF` | 4        | `11110xxx` | `10xxxxxx` | `10xxxxxx` | `10xxxxxx` |

## UTF-16

UTF-16 使用兩個字節來表示基本多語言平面，四個字節來表示輔助平面。

對於英文來說使用 UTF-8 省空間，對於中文來說UTF-16省空間，因為英文用 UTF-8 佔用 1 個字節，用 UTF-16 佔用 2 個字節；中文用 UTF-8 佔用 3 個字節，用 UTF-16 佔用 2 個字節。

| 碼點位數 | 範圍                    | UTF-16 編碼形式（二進制）                        |
| -------- | ----------------------- | ------------------------------------------------ |
| 16       | `U+000000` - `U+00FFFF` | `xxxx xxxx` `xxxx xxxx`                          |
| 20       | `U+010000` - `U+10FFFF` | `1101 10yy` `yyyy yyyy`  `1101 11xx` `xxxx xxxx` |

對於基本多語言平面，其編碼等同於其碼位。

對於輔助平面上的碼，編碼方式為：

1. 減去 0x10000，成二進制形式：yyyy yyyy yyxx xxxx xxxx，共 20 位。
2. 前 10 位為高位，加上 0xD800 作為前導代理(lead surrogates)，值範圍：[0xD800, 0xDBFF]
3. 後 10 位為低位，加上 0xDC00 作為後尾代理(trail surrogates)，值範圍：[0xDC00, 0xDFFF]
4. 可見前導和後尾的值不在同一個區間，最終形成：110110yyyyyyyyyy 110111xxxxxxxxxx

```css
問題6：已知字符A的Unicode碼點為 U+0041，其UTF-8編碼和UTF-16編碼分別是？
```

## UTFs

UTF-16 編碼包含 BE （big endian）和 LE（little endian）版本，大端者，高位字節（MSB，most significant byte）在低地址；小端者，低位字節在低地址。

| Name                       | UTF-8  | UTF-16  | UTF-16BE   | UTF-16LE      | UTF-32  | UTF-32BE   | UTF-32LE      |
| -------------------------- | ------ | ------- | ---------- | ------------- | ------- | ---------- | ------------- |
| Smallest code point        | 0000   | 0000    | 0000       | 0000          | 0000    | 0000       | 0000          |
| Largest code point         | 10FFFF | 10FFFF  | 10FFFF     | 10FFFF        | 10FFFF  | 10FFFF     | 10FFFF        |
| Code unit size             | 8 bits | 16 bits | 16 bits    | 16 bits       | 32 bits | 32 bits    | 32 bits       |
| Byte order                 | N/A    | \<BOM\>   | big-endian | little-endian | \<BOM\>   | big-endian | little-endian |
| Fewest bytes per character | 1      | 2       | 2          | 2             | 4       | 4          | 4             |
| Most bytes per character   | 4      | 4       | 4          | 4             | 4       | 4          | 4             |

## BOM

BOM，即 Byte Order Mark，字節序標記，用在文本文件的開頭。該標記為字符 U+FEFF，又稱為 ZWNBSP（ZERO WIDTH NO-BREAK SPACE，零寬非換行空格），表示大端字節序；相反的，U+FFFE（Noncharacters，非字符）表示小端字節序。

BOM字符的 UTF-8 編碼為 EF BB BF。UTF-8有 BOM編碼的文件會以 BOM 字符開頭。

UTF-8 不需要 BOM 來指定是小端還是大端字節序，但是可以通過 BOM 來區分是 UTF-8 編碼還是其他編碼。

```css
問題7：請完成下列實操，並說說你對UTF-8編碼、BOM和CRLF的理解

1. 在 Windows 中打開記事本，輸入「好」，然後另存為 UTF-8 編碼的文本文件 a.txt；
2. 使用 vim 打開 a.txt，執行命令 「%!xxd」 可以將文本轉為 16 進制形式；
3. 閱讀並嘗試解讀該 16 進制串；
4. 使用 notepad++ 或 vim 創建一個 b.txt，輸入「好」，按同樣方式獲取並解讀 16 進制串；
5. 在 a.txt 和 b.txt 中增加一個換行，再次獲取並解讀 16 進制串。
```

## 問題答案

**（問題1）**CF。Unicode 採用邏輯序（logical order）編碼文本，比如會對英文從左到右編碼，而對希伯來文從右到左編碼，見：http://www.unicode.org/versions/Unicode3.0.0/ch02.pdf。UTF-16 編碼至少需要 2 個字節，ASCII 碼只需要 1 個字節，不兼容。

**（問題2）**3。很明顯1、2、3分別是3個字符。

**（問題3）**3。計算過程：$2^2<5<2^3$, 可編碼爲：000 金、001 木、010 水、011 火、100 土，剩餘 101、110 和 111 三個碼點。

**（問題4）**1,114,112。計算過程：$16^5+16^4$

**（問題5）**65536，63488。計算過程：$16^4-(16^3-8*16^2)$

**（問題6）**0x41，0x0041。UTF-8表示A佔用1個字節，UTF-16則是佔用2個字節。

**（問題7）**

（1）「好」
Windows記事本：efbb bfe5 a5bb 0a
Vim：e5a5 bb0a
- efbb bf 是 BOM
- e5 a5bb 是「好」的UTF-8 編碼，1110 0101 1010 0101 1011 1101
- 0a 是 LF '\n'，換行符

（2）「好」+換行
Windows記事本：efbb bfe5 a5bb 0d0a
Vim：e5a5 bb0a

- 0d 是 CR '\r' ，回車

結論：
1. Windows記事本中的UTF-8編碼默認是帶BOM的，而Notepad++或Vim編輯器中的UTF-8編碼是無BOM的；
2. Windows記事本中的換行符默認是 CRLF，而Notepad++或Vim編輯器中是Unix風格的 LF。

## 延伸閱讀

- [Unicode碼表](https://unicode-table.com/en/#basic-latin)
- [Unicode 標準14.0.0 -- unicode.org](https://www.unicode.org/versions/Unicode14.0.0/)
- [FAQ：UTF-8, UTF-16, UTF-32 & BOM -- unicode.org](https://www.unicode.org/faq/utf_bom.html)
- [Java的char類型和Unicode](https://kkua.github.io/post/java-char-type-and-unicode/)
- [utf16編碼格式](https://www.cnblogs.com/dragon2012/p/5020259.html)
- [2.5 unicode — Unicode码点、UTF-8/16编码](https://docs.kilvn.com/The-Golang-Standard-Library-by-Example/chapter02/02.5.html)
