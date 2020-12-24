---
title: Go 基礎
p: it/go/go-basic.md
tags:
- Go
---

Go 又稱 Golang，是 Google 公司 2009 年發佈的一款開源編程語言，以簡潔而高效的代碼著稱。Go 目前使用 GOPATH 或 Go modules 管理項目中的第三方依賴，且不支持循環依賴。

Go 的基本數據類型有 16 種(不包含別名)，可謂豐富。要注意的是 string 也是基本數據類型，表示一個 UTF-8 字符串，底層是 byte 數組。單個字符使用一個 int32 的別名 rune 表示，其值爲 Unicode 字符碼點。

Go 的變量使用 var 關鍵字聲明，也可以使用短變量聲明；常量則是使用 const 關鍵字聲明。

Go 有 if 條件語句、for 循環語句、switch 選擇語句和 defer 延遲執行語句。Go 的 for 語句兼具其他語言的 while 語句；switch 語句每個 case 條件都支持運算，且默認自動 break；defer 語句可以立即計算參數值，然後在函數 return 前執行。

Go 的可見性跟標識符的首字母是否大寫相關，大寫則是導出的，包外可見；小寫則是非導出的，包外不可見。

Go 有指針，要注意 `&` 是生成指向操作數的指針，而 `*` 是獲取指針指向的底層值。

Go 將一些字段組合成一個結構體(struct) 。結構體支持隱式間接調用，即 p.X 等價於 (*p).X（p 爲結構體指針）。

Go 支持數組，更重要的是支持一種名爲切片(slice) 的動態數組。切片是一個數組片段的描述，包含指向數組的指針、片段的長度和容量。

Go 支持映射(map)。

Go 支持函數(function)的命名返回值、多值返回、作爲值傳遞和閉包。還有一種稱爲方法(method)的特殊函數，其帶有接收者參數，接收者可以是值接收者也可以是指針接收者，指針接收者可以更改接收者的值。

Go 支持將一些方法簽名組成接口(interface)。接口的實現是隱式的，不需要「implements」。一個結構體作爲接收者定義了接口中的所有方法，那麼該結構體就是實現了該接口。因爲隱式的緣故，建議接口方法盡可能少，以便管理。接口是值，可以傳遞。底層值是 nil 的接口，其方法可以被調用；接口本身爲 nil ，則意味著其不保存值也不保存具體類型；空接口(interface{})是包含零個函數的接口，不是爲 nil 接口。

Go 的異常處理很簡單，只有 Error，沒有 throws。

Go 支持 Go 程，一種 Go運行時管理的輕量級線程。Go 程之間可以通過信道(channel) 通信，通過 Mutex 或 RWMutex 共享互斥變量，通過 WaitGroup 等待執行完成。 

Go 中的信道還支持通過 for-range 循環讀取數據，當信道關閉時該循環自動退出。記住，只有發送方可以關閉信道，接收方不能。信道還支持 select 語句，其會**阻塞到某一分支可以執行爲止**，如沒有分支可以執行且設定了default 語句，會一直執行 default 語句。

<!-- more -->

以下內容多來自[《Go 指南》](https://tour.go-zh.org/)，內容有所改動。

## 歷史

Go 又稱 Golang，是 Google 公司開發的一款靜態強類型、編譯型、並發型，並具有垃圾回收功能的編程語言。

1. 2007.9.21 罗伯特·格瑞史莫(Robert Griesemer)、罗勃·派克(Rob Pike)和肯·汤普逊(Ken Thompson) 開始設計 Go。
2. 2009.11 Google 發佈 Go 語言。
3. 2012.3 Go 1.0 發佈。
4. 2018.8 Go 1.11 發佈，預支持 modules 進行依賴管理。

## 入門

### 安裝

按照[官方教程](https://golang.org/doc/install)安裝即可。

### Hello World

直接在系統 Home 目錄，新建一一個 hello.go 文件，寫入代碼如下：

```go
package main //程序從 main 包的 main 函數開始運行
import "fmt" //導入 fmt 包

func main() { //main函數
    fmt.Println("Hello, World!") //打印日誌
}
```

然後執行 `go run hello.go` 即可。

### GOPATH

當項目未啟用 Go modules 時，Go 使用 `GOPATH` 環境變量解析 import 語句。`GOPATH` 的值默認爲 `$HOME/go` ， `GOPATH` 目錄結構如下：

```go
GOPATH=/home/user/go

src/
    foo/
        bar/               (go code in package bar)
            x.go
        quux/              (go code in package main)
            y.go
bin/
    quux                   (installed command)
pkg/
    linux_amd64/
        foo/
            bar.a          (installed package object)
```

- src：存放依賴的源代碼
- bin：存放安裝的命令
- pkg：存法安裝的包對象

啟用 Go modules 後雖然不通過 `GOPATH` 解析 import 語句，但下載的源代碼和安裝的命令都會存在`GOPATH`目錄下。

### Vendor

Vendor 就是使用本地依賴包的模式，Go 1.5 作爲實驗特性，Go 1.6 正式支持，Go 1.14 正式終結。命名爲 vender(小商販) 是一種比喻，並將 GOPATH 隱喻爲有固定地址的商舖。啟用 Vendor 模式很簡單，在項目中創建一個名爲 vendor 的文件夾然後拷貝依賴的源代碼進入其中即可。比如有如下的項目使用了 Vendor：

```go
$GOPATH
|	src/
|	|	github.com/constabulary/example-gsftp/
|	|	|	cmd/
|	|	|	|	gsftp/
|	|	|	|	|	main.go
|	|	|	vendor/
|	|	|	|	github.com/pkg/sftp/
|	|	|	|	golang.org/x/crypto/ssh/
|	|	|	|	|	agent/
```

在文件 `github.com/constabulary/example-gsftp/cmd/gsftp/main.go` 中應這樣 import 依賴（不需要加入 vendor 前綴）：

```go
import (
	...
	"golang.org/x/crypto/ssh"
	"golang.org/x/crypto/ssh/agent"
	"github.com/pkg/sftp"
)
```

這種方式顯然會帶來代碼膨脹，特別是N個庫同時用 Vendor 模式依賴一個通用庫時，那麼該通用庫的代碼將會出現N次。

### Go modules

Go 官方推出的依賴管理系統，在 Go 1.11 和 1.12中已經有初步支持，但默認關閉；從 1.13 開始默認啟用，1.14 開始可用於生產。

**（1）使用 Go modules**

使用 Go modules 很簡單，只需要在項目根路徑(不可以在 `$GOPATH/src` 裏面)執行 `go mod init example.com/m` 即可初始化一個名爲 `example.com/m` 的模塊，之後會在項目根路徑生成一個名爲 `go.mod` 的依賴文件，其內容結構如下：

```go
module example.com/hello //模塊名

go 1.12 //使用的 Go 版本

require rsc.io/quote v1.5.2 //依賴項
```

此外，Go modules 還生成和維護著一個名爲 `go.sum` 的文件，該文件包含了期望的指定模塊版本的內容的加密哈希。

爲保證依賴的一致性，需要同時將 `go.mod` 和 `go.sum` 加入版本管理。

**（2）更新依賴**

更新小版本很簡單，一個 `go get` 命令就完了。更新大版本比更新小版本複雜，因爲大版本通常會帶來 API 的變化，Go 要求更改大版本號後，模塊名也要加上版本號。例如原本是 `rsc.io/quote` 的依賴，升級到 v3 後依賴要改成 `rsc.io/quote/v3` ，因此代碼中的 import 語句要改成 `rsc.io/quote/v3` ，然後清理掉舊版本的依賴，有點麻煩。

```bash
# 列出當前項目的模塊和依賴項
go list -m all
# 直接更新到最新的小版本
go get rsc.io/sampler
# 列出所有小版本
go list -m -versions rsc.io/sampler
# 更新到指定版本
go get rsc.io/sampler@v1.3.1

# 查看模塊的所有版本
go list -m rsc.io/q...
# 清除未使用的依賴
go mod tidy
```

### 循環依賴

Go 不支持循環依賴，Go設計者Rob Pike認爲如果出現兩個包循環依賴，那麼是你的設計問題。

筆者就出現過一次循環依賴，場景是：封裝了一個打印日誌的庫A和一個解析配置的庫B，庫A需要通過庫B配置，庫B需要用庫A打印日誌。最後選擇在庫B使用原始的日誌打印。

## 語法

### 數據類型

**（1）基本類型**

```go
bool

string

int  int8  int16  int32  int64
uint uint8 uint16 uint32 uint64 uintptr

byte // uint8 的别名

rune // int32 的別名
    // 表示一個 Unicode 碼點

float32 float64

complex64 complex128
```

其中 int, uint 和 uintptr 在 32 位系統上通常為 32 位寬，在 64 位系統上則為 64 位寬。

string 表示一個 UTF-8 類型的字符串，底層是一個字節數組。

rune 表示一個 Unicode 碼點，是 int32 的別名。讀取 string 中的每個字符，只需要將 string 轉爲 rune 數組即可

Java 中的 char 類型，每個字符對應一個 Unicode 碼點，可以表示BMP範圍內（即[U+0000, U+FFFF]之間）的Unicode字符。String 是 UTF-8 類型。

**（2）零值**

没有明确初始值的变量声明会被赋予它们的 **零值**。

零值是：

- 数值类型为 `0`，
- 布尔类型为 `false`，
- 字符串为 `""`（空字符串）。

**（3）類型轉換**

數值之間可以通過表達式 T(v) 將值 v 轉換為類型 T，如：

```go
i := 42
f := float64(i)
u := uint(f)
```

**（4）类型推导**

在聲明一個變量而不指定其類型時（即使用不帶類型的 := 語法或 var = 表達式語法），變量的類型由右值推導得出。

```go
i := 42           // int
f := 3.142        // float64
g := 0.867 + 0.5i // complex128
```

### 變量

**（1）聲明語句**

```go
// var 開頭，逗號(,)分割變量名，最後寫數據類型 
var c, python, java bool
```

**（2）賦值語句**

```go
var c, python, java = true,false,"no"
```

或直接使用**短變量聲明**，注意短變量聲明只能在函數內使用，因爲函數外的每個語句要求必須以關鍵字開始。

```go
c, python, java := true,false,"no"
```

### 常量

常量聲明使用 const 關鍵字。常量可以是字符、字符串、布尔值或数值。常量不能用 `:=` 语法声明。

```go
const Pi = 3.14
```

`iota` 可以用來創建順序遞增的常量。

```go
const (
	Low = iota //0
	Medium     //1
	High       //2
)
```

### 風格

1. 每行程序結束後不需要撰寫分號（;）。
2. 大括號（{）不能夠換行放置。
3. if判斷式和for循環不需要以小括號包覆起來。
4. 使用 tab 做排版

### 流程控制

**（1）if-else**

不需要小括號，可以使用簡短語句。

```go
_,ok := sendMsg();
if ok {
  // do something
}else{
  // do other thing
}
// 等價於以下簡短語句
if _,ok := sendMsg(); ok {
  // do something
}else{
  // do other thing
}
```

**（2）for**

Go 中的 for 語句，還包含了其他語言的 while 的功能。特別的不用括號包裹。

```go
// 功能：遍歷 10 次
for i:=0;i<10;i++{
}
// 功能：類似於其他語言 while 的功能
var i = 0
for i<10{
}
// 功能：無限循環，類似於其他語言中的 while(true)
for{
}
// 功能：for range 循環，返回當前元素的下標及副本
// 可通過 _ 忽略其中的某個值
pow := []int{1, 2, 4, 8}
for i, v := range pow {
	fmt.Printf("%d,%d\n", i, v)
}
for _,v := range pow {
	fmt.Printf("%d\n", v)
}
for i := range pow {
	fmt.Printf("%d\n", i)
}
```

**（3）switch**

Go 中的 switch 語句是自動 break 的。如果不想要break，需要在 case 後面協商 fallthrough。

Go 中的 switch 的 case 無需為常量，且取值不必為整數。

```go
// 功能：選擇顏色
switch color {
    case Red:
    // do something
    case Green:
    // do something
    default:
    // do something
}
// 功能：替代 if-then-else，更整齊
result := request()
switch {
    case result > 0:
    case result <0:
    default:
}
// 或者
switch result := request(); {
    case result > 0:
    case result <0:
    default:
}
```

**（4）defer**

defer 語句會將函數推遲到外層函數返回之後執行。

推遲調用的函數其參數會立即求值，但直到外層函數返回前該函數都不會被調用。

推遲的函數調用會被壓入一個棧中。當外層函數返回時，被推遲的函數會按照後進先出的順序調用。

```go
func main() {
	defer fmt.Println("world")

	fmt.Println("hello")
}
```

defer 並不是免費的。defer 底層會調用 `runtime.deferproc` 去設置要延遲調用的函數，調用 `runtime.deferreturn` 會依次執行先前延遲調用的函數。參考：https://medium.com/i0exception/runtime-overhead-of-using-defer-in-go-7140d5c40e32

### 可見性

- 導出：大寫字母開頭的標識符，包外可訪問。
- 未導出：非大寫字母開頭的標識符，包外不可訪問。

### 指針

Go 擁有指針。指針保存了值的內存地址。

- 類型 `*T` 是指向 `T` 類型值的指針。其零值為 `nil`。
- `&` 操作符會**生成一個指向其操作數的指針**。（注意：把`&` 理解爲取地址符號是錯誤的）
- `*` 操作符**表示指針指向的底層值**。（注意：把`*` 理解爲取值符號是錯誤的）

```go
func main() {
	i, j := 42, 2701

	p := &i         // 指向 i
	fmt.Println(*p) // 通過指針讀取 i 的值
	*p = 21         // 通過指針設置 i 的值
	fmt.Println(i)  // 查看 i 的值

	p = &j         // 重定向到 j
	*p = *p / 37   // 通過指針對 j 進行除法運算
	fmt.Println(j) // 查看 j 的值
}
```

### 結構體

一個結構體（struct）就是一組字段（field）。外界使用點號來訪問結構體字段。

結構體字段可以通過結構體指針來訪問。如果我們有一個指向結構體的指針 p，那麼可以通過 `(*p).X` 來訪問其字段 X。不過這麼寫太囉嗦了，所以語言也允許我們使用**隱式間接引用**，直接寫 `p.X` 就可以。

```go
type Vertex struct {
	X, Y int
}

func main() {
  v := Vertex{1, 2}
	v.X = 4
	fmt.Println(v.X)
  
  p := &v
	p.X = 1e9
	fmt.Println(v)

	v2 = Vertex{X: 1}  // Y:0 被隱式地賦予
	v3 = Vertex{}      // X:0 Y:0
	p  = &Vertex{1, 2} // 創建一個 *Vertex 類型的結構體（指針）
}
```

### 數組

類型 [n]T 表示擁有 n 個 T 類型的值的數組。

表达式

```go
var a [10]int
```

會將變量 `a` 聲明為擁有 10 個整數的數組。

### 切片

**（1）定義**

類型 []T 表示一個元素類型為 T 的切片。T 可以是任何類型，包括切片本身。

切片通過兩個下標來界定，即一個上界和一個下界，二者以冒號分隔：

```go
a[low : high]
```

它會選擇一個半開區間，包括第一個元素，但排除最後一個元素。

切片下界的默認值爲 0，上界則是其底層數組的長度。

對於數組 `var a [10]int` 來說，以下切片是等價的：

```go
a[0:10]
a[:10]
a[0:]
a[:]
```

**（2）切片的本質**

一個切片是一個數組片段的描述，包含指向數組的指針、片段的長度和容量，其結構如下：

![](go-basic/Untitled.png)

![](go-basic/Untitled%201.png)

切片的長度就是它所包含的元素個數。
切片的容量是從它的第一個元素開始數，到其底層數組元素末尾的個數。
切片 s 的長度和容量可通過表達式 `len(s)` 和 `cap(s)` 來獲取。

更改切片的元素會修改其底層數組中對應的元素。與它共享底層數組的切片都會觀測到這些修改。

```go
func main() {
	names := [4]string{
		"John",
		"Paul",
		"George",
		"Ringo",
	}
	fmt.Println(names)

	a := names[0:2]
	b := names[1:3]
	fmt.Println(a, b)

	b[0] = "XXX"
	fmt.Println(a, b)
	fmt.Println(names)
}
```

注意：切片的零值爲 nil，其長度和容量爲 0 且沒有底層數組。

**（3）通過 make 創建切片**

```go
a := make([]int, 5)  // len(a)=5
b := make([]int, 0, 5) // len(b)=0, cap(b)=5
```

**（4）通過 append 追加元素**

```go
func append(s []T, vs ...T) []T
```

`append` 的第一個參數 `s` 是一個元素類型為 `T` 的切片，其餘類型為 `T`的值將會追加到該切片的末尾。

`append` 的結果是一個包含原切片所有元素加上新添加元素的切片。

當 `s` 的底層數組太小，不足以容納所有給定的值時，它就會分配一個更大的數組。返回的切片會指向這個新分配的數組。

當引用一個原始數組時，GC不會釋放該數組的空間，即使只用到其中一小部分數據。因此函數返回切片的時候要特別注意，最好拷貝需要數據到新的切片再返回。

```go
// 使用 copy 函數
func CopyDigits(filename string) []byte {
    b, _ := ioutil.ReadFile(filename)
    b = digitRegexp.Find(b)
    c := make([]byte, len(b))
    copy(c, b)
    return c
}
// 或使用 append 函數
func CopyDigits(filename string) []byte {
    b, _ := ioutil.ReadFile(filename)
    b = digitRegexp.Find(b)
    var c []byte
    return append(c, b...)
}
```

### 映射

映射將鍵映射到值。

映射的零值為 `nil` 。`nil` 映射既沒有鍵，也不能添加鍵。

`make` 函數會返回給定類型的映射，並將其初始化備用。

```go
type Vertex struct {
	Lat, Long float64
}

var m = map[string]Vertex{
	"Bell Labs": {40.68433, -74.39967},
	"Google":    {37.42202, -122.08408},
}
```

 常用操作：

1. 插入或修改元素：`m[key] = elem`
2. 獲取元素：`elem = m[key]`
3. 通過雙賦值檢測某個鍵是否存在：`elem, ok := m[key]`
4. 刪除元素：`delete(m, key)`

### 函數(function)

**（1）概述**

函數可以沒有參數或接受多個參數。當連續兩個或多個函數的已命名形參類型相同時，除最後一個類型以外，其它都可以省略。

```go
func add(x, y int) int {
	return x + y
}

func main() {
	fmt.Println(add(42, 13))
}
```

**（2）命名返回值**

Go 的返回值可被命名，它們會被視作**定義在函數頂部的變量**。返回值的名稱應當具有一定的意義，它可以作為文檔使用。沒有參數的 `return` 語句返回已命名的返回值。也就是 `直接` 返回。直接返回語句應當僅用在下面這樣的短函數中。在長的函數中它們會影響代碼的可讀性。

```go
func split(sum int) (x, y int) {
	x = sum * 4 / 9
	y = sum - x
	return
}

func main() {
	fmt.Println(split(17))
}
```

**（3）多值返回**

函數可以返回任意數量的返回值。

```go
func swap(x, y string) (string, string) {
	return y, x
}

func main() {
	a, b := swap("hello", "world")
	fmt.Println(a, b)
}
```

**（4）函數值**

函數也是值，可以作爲函數的參數或返回值。

```go
func compute(fn func(float64, float64) float64) float64 {
	return fn(3, 4)
}
fmt.Println(compute(math.Pow))
```

**（5）閉包(closure)**

閉包是指一個函數引用了其函數體之外的變量，該函數可以訪問並賦予其引用的變量的值。換句話說就是該函數跟函數體之外的變量綑綁在一起了。每次調用閉包中的函數可以改變閉包中變量的值。例如斐波那契閉包：

```go
func fibonacci() func() int {
	x,y := 0,1
	return func() int {
		res := x
		x,y = y,x+y
		return res
	}
}

func main() {
	f := fibonacci()
	for i := 0; i < 10; i++ {
		fmt.Println(f())
	}
}
```

### 方法(method)

方法就是一類帶特殊的**接收者參數**的函數。方法接收者在它自己的參數列表內，**位於 func 關鍵字和方法名之間**。

```go
type Vertex struct {
	X, Y float64
}
// 這就是方法
func (v Vertex) Abs() float64 {
	return math.Sqrt(v.X*v.X + v.Y*v.Y)
}

func main() {
	v := Vertex{3, 4}
	fmt.Println(v.Abs())
}
```

值得注意的是：接收者的類型定義和方法聲明必須在同一包內；不能爲內建類型聲明方法。

接收者除了是**值接收者**外，還支持**指針接收者**，使用 `*T` (不能是 `*int` 之類的) 的文法即可。指針接收者可以修改接收者指向的值。如下：

```go
type Vertex struct {
	X, Y float64
}

func (v Vertex) Abs() float64 {
	return math.Sqrt(v.X*v.X + v.Y*v.Y)
}

func (v *Vertex) Scale(f float64) {
	v.X = v.X * f
	v.Y = v.Y * f
}

func main() {
	v := Vertex{3, 4}
	v.Scale(10) // 此時 Go 會解釋爲 (&v).Scale(10)，這就是指針重定向
	fmt.Println(v.Abs())
}
```

使用指針接收者的好處：

1. 方法能夠修改其接收者指向的值。
2. 避免在每次調用方法時複製該值。該值佔用的空間越大，則越顯得高效。

注意：一個結構體採用值接收者的方式實現了接口的方法，則隱含著採用指針接收者的方式實現了接口的方法。（接收者是指針類型的方法，很可能在方法中會對接收者的屬性進行更改操作，從而影響接收者；而對於接收者是值類型的方法，在方法中不會對接收者本身產生影響）

### 接口

**（1）定義**

接口類型是**由一組方法簽名定義的集合**。接口類型的變量可以保存**任何**實現了這些方法的值。

**（2）隱式實現**

類型通過實現一個接口的所有方法來實現該接口。既然無需專門顯式聲明，也就沒有「implements」關鍵字。

```go
type Animal interface {
	eat()
}

type John struct{}

func (j *John) eat() {
	fmt.Println("eat...")
}

type Person interface {
	eat()
	talk()
}

func (j *John) talk() {
	fmt.Println("talk...")
}

func main() {
	var a Animal = &John{}
	a.eat()
	var b Person = &John{}
	b.eat()
	b.talk()
}
```

**（4）接口值**

接口也是值，可以作爲函數的參數或返回值。在內部，接口值可以看做包含值和具體類型的元組：`(value, type)` 。接口值保存了一個具體底層類型的具體值。接口值調用方法時會執行其底層類型的同名方法。

```go
// Animal、John 見上面的代碼
j := John{}
describe(j)

func describe(i Animal){
	fmt.Printf("(%v, %T)\n", i, i)
}
```

**（5）底層值爲 nil 的接口值**

即便接口內的具體值為 nil，方法仍然會被 nil 接收者調用。

```go
// 改造上面的代碼
func (j *John) talk() {
	if j == nil {
		fmt.Println("j is <nil>")
		return
	}
	fmt.Println("talk...")
}

func main() {
	var x Person
	var y John
	x = &y
	describe(x)
	x.talk() // 正常調用
}
```

判斷接口的底層值是否爲 nil 的方法：

```go
// 接上
println( x == nil || reflect.ValueOf(x).IsNil())
```

**（6）nil 接口值**

nil 接口值既不保存值也不保存具體類型。

為 nil 接口調用方法會產生運行時錯誤，因為接口的元組內並未包含能夠指明該調用哪個 **具體** 方法的類型。

```go
type I interface {
	M()
}

func main() {
	var i I
	describe(i)
	i.M() // 此處拋出 panic: runtime error: invalid memory address or nil pointer dereference
}

func describe(i I) {
	fmt.Printf("(%v, %T)\n", i, i) // (<nil>, <nil>)
}
```

**（7）空接口**

指定了**零個方法**的接口值被稱為空接口，即 `interface{}` 。空接口可保存任何類型的值。（因為每個類型都至少實現了零個方法。）空接口被用來處理未知類型的值。例如，`fmt.Print` 可接受類型為 `interface{}` 的任意數量的參數。

```go
func main() {
	var i interface{}
	describe(i)

	i = 42 // 保存 int值
	describe(i)

	i = "hello" // 保存 string值
	describe(i)
}

func describe(i interface{}) {
	fmt.Printf("(%v, %T)\n", i, i)
}
```

**（8）類型斷言**

類型斷言提供了訪問**接口值底層具體值**的方式。

```go
// 判斷接口i的底層值類型是否爲T，如是返回其底層值和true，否則返回T類型的零值和false
t, ok := i.(T)
```

```go
var i interface{} = "hello"
s, ok := i.(string)
fmt.Println(s, ok)
f, ok := i.(int)
fmt.Println(f, ok)
// 支持類型選擇
func do(i interface{}) {
	switch v := i.(type) {
	case int:
		fmt.Printf("Twice %v is %v\n", v, v*2)
	case string:
		fmt.Printf("%q is %v bytes long\n", v, len(v))
	default:
		fmt.Printf("I don't know about type %T!\n", v)
	}
}
```

### 異常處理

Go 程序使用 `error` 值來表示錯誤狀態。

```go
type error interface {
    Error() string
}
```

通常函數會返回一個 `error` 值，調用的它的代碼應當判斷這個錯誤是否等於 `nil` 來進行錯誤處理。`error` 為 nil 時表示成功；非 nil 的 `error` 表示失敗。

```go
if i, err := strconv.Atoi("42"); err == nil {
    fmt.Println("Converted integer:", i)
}
```

### Go 程(goroutine)

**（1）定義**

**Go 程（goroutine）是由 Go 運行時管理的輕量級線程**。

```go
// x,y,z 的求值發生在當前 Go 程中，f 的執行則是在新的 Go 程中
go f(x, y, z)
```

（**2）信道**

**信道是帶有類型的管道**，你可以通過它用**信道操作符** `<-` (箭頭就是數據流的方向)來發送或者接收值。

默認情況下，發送和接收操作在另一端準備好之前都會阻塞。這使得 Go 程可以在沒有顯式的鎖或競態變量的情況下進行同步。

```go
// 創建信道
ch := make(chan int)
// 將 v 發送至信道 ch。
ch <- v
// 從 ch 接收值並賦予 v。
v := <-ch
```

**信道可以是帶緩衝，**將緩衝長度作為第二個參數提供給 `make` 來初始化一個帶緩衝的信道。

```go
ch := make(chan int, 100)
```

**僅當信道的緩衝區填滿後，向其發送數據時才會阻塞。當緩衝區為空時，接受方會阻塞。**

**（3）range 和 close**

有且僅有發送者可以通過 close 方法關閉一個信道。接收者讀取值的時候可以通過 `v, ok := <-ch`  的 ok 值判斷是否信道關閉了。更簡單的是使用 for-range 不斷從信道接收值，直到信道關閉，循環自動退出。

```go
func fibonacci(n int, c chan int) {
	x, y := 0, 1
	for i := 0; i < n; i++ {
		c <- x
		x, y = y, x+y
	}
	close(c)
}

func main() {
	c := make(chan int, 10)
	go fibonacci(cap(c), c)
	for i := range c {
		fmt.Println(i)
	}
}
```

**（4）select**

select 語句使一個 Go 程可以等待多個通信操作。select 會阻塞到某個分支可以繼續執行為止，這時就會執行該分支。當多個分支都準備好時會隨機選擇一個執行。當 select 中的其它分支都沒有準備好時，default 分支就會執行。

```go
func fibonacci(c, quit chan int) {
	x, y := 0, 1
	for {
		select {
		case c <- x:
			x, y = y, x+y
		case <-quit:
			fmt.Println("quit")
			return
    default:
      // 當 c 和 quit 阻塞時會執行到此處
		}
	}
}

func main() {
	c := make(chan int)
	quit := make(chan int)
	go func() {
		for i := 0; i < 10; i++ {
			fmt.Println(<-c)
		}
		quit <- 0
	}()
	fibonacci(c, quit)
}
```

- 練習：等價二叉查找樹

    函數 tree.New(k) 用於構造一個隨機結構的已排序二叉查找樹，它保存了值 k, 2k, 3k, ..., 10k。

    Walk 步進 tree t 將所有的值從 tree 發送到 channel ch。

    用 Walk 實現 Same 函數來檢測 t1 和 t2 是否存儲了相同的值。

    ```go
    package main

    import "golang.org/x/tour/tree"

    func Walk(t *tree.Tree, ch chan int){
    	if t.Left != nil{
    		Walk(t.Left, ch)
    	}
    	ch <- t.Value
    	if t.Right != nil{
    		Walk(t.Right, ch)
    	}
    }

    // Same 检测树 t1 和 t2 是否含有相同的值。
    func Same(t1, t2 *tree.Tree) bool{
    	ch1,ch2 := make(chan int),make(chan int)
    	go func(){
    		Walk(t1, ch1)
    		close(ch1)
    	}()
    	go func(){
    		Walk(t2, ch2)
    		close(ch2)
    	}()
    	for i := range ch1{
    		if i != <-ch2 {
    			return false
    		}
    	}
    	return true
    }

    func main() {
    	println(Same(tree.New(1),tree.New(1)))
    }
    ```

**（5）sync.Mutex**

互斥鎖可以保證每次只有一個 Go 程訪問一個共享變量。

Go 標準庫中的 **Mutex** 就是一個互斥鎖，可以創建為其他結構體的字段；零值為解鎖狀態。Mutex類型的鎖和線程無關，可以由不同的線程加鎖和解鎖。在代碼前調用 Lock 方法，並在代碼後調用 Unlock 方法來保證一段代碼互斥執行。

```go
type SafeCounter struct {
	v   map[string]int
	mux sync.Mutex
}

func (c *SafeCounter) Increase(key string) {
	c.mux.Lock()
	c.v[key]++
	c.mux.Unlock()
}

func (c *SafeCounter) Value(key string) int {
	c.mux.Lock()
	defer c.mux.Unlock()
	return c.v[key]
}

func main() {
	c := SafeCounter{v: make(map[string]int)}
	for i := 0; i < 1000; i++ {
		go c.Increase("somekey")
	}

	time.Sleep(time.Second)
	fmt.Println(c.Value("somekey"))
}
```

爲了提升讀寫性能，常用 **RWMutex** 代替 **Mutex。**RWMutex是讀寫互斥鎖。該鎖可以被同時多個讀取者持有或唯一個寫入者持有。RWMutex可以創建為其他結構體的字段；零值為解鎖狀態。RWMutex類型的鎖也和線程無關，可以由不同的線程加讀取鎖/寫入和解讀取鎖/寫入鎖。

下面的代碼效果不明顯，因爲讀的次數不多。

```go
type SafeCounter struct {
	v   map[string]int
	mux sync.RWMutex
}

func (c *SafeCounter) Increase(key string) {
	c.mux.Lock()
	c.v[key]++
	c.mux.Unlock()
}

func (c *SafeCounter) Value(key string) int {
	c.mux.RLock()
	defer c.mux.RUnlock()
	return c.v[key]
}

func main() {
	now := time.Now()
	c := SafeCounter{v: make(map[string]int)}
	for i := 0; i < 1000; i++ {
		go c.Increase("somekey")
	}
	time.Sleep(time.Second)
	fmt.Println(c.Value("somekey"))
	print(time.Now().Sub(now))
}
```

**（6）WaitGroup**

WaitGroup 可以等待一組 Go 程結束。通過調用 Add 方法設定要等待的 Go 程數量。然後各個 Go 程通過調用 Done 方法結束等待。

```go
type SafeCounter struct {
	v   map[string]int
	mux sync.RWMutex
}

func (c *SafeCounter) Increase(key string, wg *sync.WaitGroup) {
	c.mux.Lock()
	c.v[key]++
	wg.Done()
	c.mux.Unlock()
}

func (c *SafeCounter) Value(key string) int {
	c.mux.RLock()
	defer c.mux.RUnlock()
	return c.v[key]
}

func main() {
	wg := sync.WaitGroup{}
	wg.Add(1000)
	c := SafeCounter{v: make(map[string]int)}
	for i := 0; i < 1000; i++ {
		go c.Increase("somekey", &wg)
	}
	wg.Wait()
	fmt.Println(c.Value("somekey"))
}
```