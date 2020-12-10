---
title: Java 基礎
p: it/java/java-basic.md
tags:
- Java
---

Java 自 95 年誕生至今，已有 25 年的歷史。它是一種半編譯的語言，先將代碼編譯成字節碼，然後在 JVM 中解釋執行。

- 它是一種面向對象的語言，封裝、繼承和多態它都有，類可以多實現但不支持多繼承，而接口可以多繼承。
- 它支持 8 種基本數據類型，同時還提供了其包裝類型，另外還提供了 BigDecimal 精確處理浮點數、提供了 BigInteger 處理大整數。
- 它的方法只有值傳遞，傳遞對象時它是淺拷貝而非深拷貝。類的方法可以被子類重寫，同個類可以有多個同名的重載方法。
- 它支持泛型，一種將類型參數化的技術。不過，也有人稱之爲「僞泛型」，因爲類型會在編譯時被擦除。
- 它支持反射，一種在運行時操作任意對象的方法和屬性的技術，這在框架應用中很常見。
- 它提供了豐富的集合類、迭代器及工具類。
- 它支持多線程，一種在程序進程中同時執行多個任務的技術，同時還有豐富的鎖類型，所有對象的頭信息裏都有一個鎖標識。
- 它支持異常處理，Exception 分編譯時異常和運行時異常，編譯時異常可以被編譯器檢查到，而運行時異常只能在程序運行時發生。
- 它有豐富的 I/O API，派生自 4 個抽象類，InputStream、OutputStream、Reader、Writer，字符流的出現是爲了減少 JVM 進行字符編碼解碼的資源損耗和編解碼錯誤。
- 另外，目前有兩大項目管理工具，Maven 和 Gradle。

<!-- more -->

## Java 入門（基礎概念與常識）

### 歷史

Java 編程語言本名爲 oak（橡樹），因爲商標被註冊了，所以更名爲 Java，而 Java 是印尼的一座島嶼，盛產咖啡豆，有一種咖啡就是以該島命名，Java 編程語言之名因之。使用十六進制編輯器打開 class 文件時會發現前 32 位顯示爲 `CA FE BA BE` ，即 cafe babe （咖啡寶貝）。

```java
$ hexdump Test.class
0000000 ca fe ba be 00 00 00 3b 00 51 0a 00 02 00 03 07
```

- 1994 年完成 1.0 版本。
- 1995 年首次對外發佈，Java 語言誕生。
- 1996 年JDK 1.0 誕生。
- 2004 年 SUN 公司發佈 Java SE 5。
- 2005 年 SUN 公司發佈 Java SE 6。
- 2006 年 SUN 公司推出 OpenJDK 計劃。
- 2014年 Oracle 公司發佈 Java SE 8。
- 2017年 Oracle公司發佈 Java SE 9。
- 2020 年 Oracle 公司發佈 Java SE 15。

### 安裝與卸載JDK

在 Mac 環境下，從 [Oracle JavaSE 下載地址](https://www.oracle.com/tw/java/technologies/javase-downloads.html) 下載並安裝。安裝完成後執行 `java -version`  可查看安裝的版本，以確認安裝成功。安裝後的Java Home 位置爲 `/Library/Java/JavaVirtualMachines/jdk-9.0.1.jdk/Contents/Home` 。如需卸載該 jdk，可安裝以下 shell 命令，先移除插件後根據查詢到的 jdk 版本移除整個 jdk 文件夾即可。

```bash
sudo rm -fr /Library/Internet\ Plug-Ins/JavaAppletPlugin.plugin
sudo rm -fr /Library/PreferencesPanes/JavaControlPanel.prefpane

ls /Library/Java/JavaVirtualMachines/
输出：jdk-9.0.1.jdk

sudo rm -rf /Library/Java/JavaVirtualMachines/jdk-9.0.1.jdk
```

### Hello World

運行以下代碼，將輸出 `Hello World`。

```java
package hello;

public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}
```

### Java 語言的特點

1. 面向對象（封裝，繼承，多態）
2. 平台無關性（ Java 虛擬機實現平台無關性）
3. 支持多線程
4. 編譯與解釋並存

編譯：生成字節碼(.class文件)，javac 指令。
解釋：解釋字節碼成機器碼，java 指令。

### JVM、JDK 和  JRE

1. JVM，Java Virtual Machine 的縮寫，即 Java 虛擬機，是運行 Java 字節碼的虛擬機（包含解釋器 java），它包含在 JRE 中。不同的操作系統有特定的 JVM 實現，以便 Java 字節碼可以跨平台。
2. JDK，Java Development Kit 的縮寫，即 Java 開發工具集，包含了 JRE 、編譯器（javac）和其他工具（javadoc 和 jdb 等）。
3. JRE，Java Runtime 的縮寫，即 Java 運行時，包含了 JVM、必要的類庫、java 命令和其他基礎構件。

### Java 與 C++ 對比

1. 皆支持面向對象編程（封裝、繼承和多態）。
2. Java 不提供指針來直接訪問內存；C++ 提供。
3. Java 的類不支持多繼承，但接口可以；C++ 的類可以多繼承。
4. Java 有內存垃圾自動回收機制（GC），不需要手動釋放無用內存；C++ 沒有。
5. Java 字符串和字符數組沒有結束符的概念；C/C++ 中字符串和字符數組最後會有一個額外的字符`\0` 來表示結束。

## Java 語法

### 基本類型及其大小

Java 共 8 種數據類型（不包括 void），具體如下表：

![](java_basic/20201202_24328.png)

boolean 值的大小取決於 JVM 實現，Java 虛擬機規範（第8版）規定：單個 boolean佔 4 個字節，而 boolean 數組 1 個字節。

char 值是一個 16 位的 Unicode 字符，最小值是 '\u0000' ，最大值是 '\uffff'，即 0～65535，每個數字對應一個字符。

- 代碼

    ```java
    char a = '中';
    System.out.println((int)a);
    // 輸出 20013
    System.out.println(Integer.toHexString(a));
    // 輸出 4e2d
    System.out.println('\u4e2d');
    // 輸出 中
    ```

byte、short、int、long 類型，採用二進制補碼存儲數據，以便利減法運算。

- 二進制補碼
    - 過程：正數的補碼是其自身；負數的補碼是除符號位外所有二進制位做反碼後加 1 的結果。
    - 原理：假定 X、Y 是两个占1个字节的数。X-Y 等价于 X+(-Y) ，而 -Y 可以看作 0-Y，假定是 0 不足以被减，向上借 1 变为 1 0000 0000，而  1 0000 0000 又等價於 1111 1111 + 1，於是 -Y = 1111 1111 - Y + 1，即 Y 的反碼再 + 1。 見 [https://www.ruanyifeng.com/blog/2009/08/twos_complement.htm](https://www.ruanyifeng.com/blog/2009/08/twos_complement.html)l

long 類型的數據後面一定要加上 L，否則會被認為是整型。

char 類型值使用單引號括起來，String 使用雙引號。

Java 有**自動拆裝箱機制**，裝箱即把基本類型使用其包裝類型包裝起來，拆箱即把包裝類型拆成基本類型。

### 包裝類型及常量池技術

1. Byte、Short、Integer 和 Long 分別默認創建了數值 [-128, 127] 的相應類型的緩存數據。
2. Character 創建了數值在 [0, 127] 的緩存數據。
3. Boolean 直接返回 True 和 False。
4. Float 和 Double 沒有實現常量池技術。

使用常量池技術意味著在緩存範圍內的包裝類型對象是相等的，除非 new 一個對象。使用包裝器的 valueOf 方法默認會先去緩存中取對象，取不到才會 new 一個。

```java
Integer i1 = 33;
Integer i2 = 33;
System.out.println(i1 == i2);// 输出 true
Integer i11 = 333;
Integer i22 = 333;
System.out.println(i11 == i22);// 输出 false
Double i3 = 1.2;
Double i4 = 1.2;
System.out.println(i3 == i4);// 输出 false
```

《阿里巴巴Java開發手冊》規定：

- 【強制】**所有的 POJO 類屬性必須使用包裝數據類型**。
- 【強制】RPC 方法的返回值和參數必須使用包裝數據類型。
- 【推薦】所有的局部變量使用基本數據類型。

### BigDecimal

**（1）使用 BigDecimal 進行浮點數比較和精度取捨**

**（2）使用 BigDecimal(String) 或 BigDecimal.valueOf(double) 構造對象**

```java
float a = 1.0f - 0.9f;
float b = 0.9f - 0.8f;
System.out.println(a);
System.out.println(b);
System.out.println(a == b); // false

BigDecimal a = new BigDecimal("1.0");
BigDecimal b = new BigDecimal("0.9");
BigDecimal c = new BigDecimal("0.8");
System.out.println(a.subtract(b));
System.out.println(b.subtract(c));
System.out.println(a.subtract(b).equals(b.subtract(c))); // true

BigDecimal a = new BigDecimal("1.1252312");
// 取小數點後 2 位，四捨五入
BigDecimal scale = a.setScale(2, RoundingMode.HALF_UP);
System.out.println(scale.toString()); // 1.13
```

### 對象及其大小

基本類型的封裝類型是對象，Java 中的對象由以下部分組成：

1. 對象頭（object header）：由 mark word 和 class pointer 組成。mark word 存儲了對象的 hashcode、GC信息和鎖信息；class pointer 存儲了指向類對象的指針。32 位的 JVM 上對象頭佔 8 個字節，mark word 和 class pointer 各佔一半。64 位的 JVM 默認開啟了壓縮指針選項（-XX+UseCompressedOops）後上對象頭佔用 12 個字節，mark word 佔用 8 個字節，class pointer 佔用 4 個字節。
2. 實例數據（instance data）：
3. 對齊填充（padding）

可使用 `org.openjdk.jol` 工具查看一個對象佔用的字節大小，

- 如下：

    ```java
    public static void main(String[] args){
        System.out.println(VM.current().details());
        System.out.println(ClassLayout.parseClass(Object.class).toPrintable());
        System.out.println(ClassLayout.parseInstance(Integer.valueOf(1)).toPrintable());
    }
    ```

    輸出結果：

    ```bash
    # Running 64-bit HotSpot VM.
    # Using compressed oop with 3-bit shift.
    # Using compressed klass with 3-bit shift.
    # WARNING | Compressed references base/shifts are guessed by the experiment!
    # WARNING | Therefore, computed addresses are just guesses, and ARE NOT RELIABLE.
    # WARNING | Make sure to attach Serviceability Agent to get the reliable addresses.
    # Objects are 8 bytes aligned.
    # Field sizes by type: 4, 1, 1, 2, 2, 4, 4, 8, 8 [bytes]
    # Array element sizes: 4, 1, 1, 2, 2, 4, 4, 8, 8 [bytes]

    java.lang.Object object internals:
     OFFSET  SIZE   TYPE DESCRIPTION                               VALUE
          0    12        (object header)                           N/A
         12     4        (loss due to the next object alignment)
    Instance size: 16 bytes
    Space losses: 0 bytes internal + 4 bytes external = 4 bytes total

    java.lang.Integer object internals:
     OFFSET  SIZE   TYPE DESCRIPTION                               VALUE
          0     4        (object header)                           01 c9 01 4e (00000001 11001001 00000001 01001110) (1308739841)
          4     4        (object header)                           3d 00 00 00 (00111101 00000000 00000000 00000000) (61)
          8     4        (object header)                           48 71 00 00 (01001000 01110001 00000000 00000000) (29000)
         12     4    int Integer.value                             1
    Instance size: 16 bytes
    Space losses: 0 bytes internal + 0 bytes external = 0 bytes total
    ```

結論：在 64 位開啟指針壓縮的環境下，Object 對象佔用 16 個字節，Integer 對象也佔用 16 個字節。

### String、StringBuffer 和 String Builder 的區別

String 類使用 final 修飾字符數組或字節數組來保存字符串，所以 String 對象是不可變的。

```java
public final class String {
	// Java 9 之前
	private final char[] value;
	// Java 9 之後
	private final byte[] value;
}
```

StringBuilder  和 StringBuffer 都繼承自 AbstractStringBuilder，AbstractStringBuilder 使用字符數組來保存字符串，但沒有使用 final 關鍵字修飾，所以這兩者是可變的。

下面從不同角度比較下此三者：

1. 線程安全性：String 對象不可變，線程安全；StringBuffer 對方法加了同步鎖，線程安全；StringBuilder 對方法沒有加同步鎖，線程不安全。
2. 性能：每次對 String 類型進行改變時會生成一個新的 String 對象，然後將指針指向新的 String 對象。StringBuffer 和 StringBuilder 每次對自身進行操作，不生成新對象。同等情況下， StringBuilder 比 StringBuffer 能提升 10%～15% 性能，但要冒線程不安全的風險。

### 注釋

代碼即注釋。先讓標識符見名知意，然後再考慮增加注釋。

### 標識符和關鍵字的區別

標識符是程序、類、變量、方法等取的名字，而關鍵字是具備特殊含義的標識符。常見的關鍵字有：

1. 訪問控制：private、protected、public
2. 類、方法和變量修飾符：abstract、class、extends、final、implements、interface、native、new、static、strictfp、synchronized、transient、volatile
3. 程序控制：break、continue、return、do、while、if、else、for、instanceof、switch、case、default
4. 錯誤處理：try、catch、throw、throws、finally
5. 包相關：import、package
6. 基本類型：boolean、byte、char、double、float、int、short、null、true、false
7. 變量引用：super、this、void
8. 保留字：goto、const

### 自增自減運算符

符號在前先加減再賦值，符號在後先賦值後加減。假定 `a = 1; b = a++` 最後 a 值爲 2，b 值爲 1。

### == 和 equals 的區別

1. 基本數據類型 == 比較的是值，引用數據類型 == 比較的是內存地址。
2. equals 是 Object 類的方法，如無重寫該方法，則默認使用 == 比較對象，即比較內存地址；String 類重寫了 equals 方法使其比較得是值。
3. 整型包裝類都應使用 equals 比較大小。
4. 浮點數之間的等值判斷，基本數據類型不能用==來比較，包裝數據類型不能用 equals 來判斷。
- 重寫 equals 方法通常同時需要重寫 hashcode 方法，爲什麼？

    hashcode 是 Object 類的一個本地方法，其實現時將對象的內存地址轉爲一個 int 值，不同的對象的 hashcode 可能相同。 HashSet 集合進行元素重複校驗時先比較 hashcode ，當 hashcode 一樣時再調用 equals，提高了校驗效率。因此，如果只重寫 equals 方法而不重寫 hashcode 方法，會出現 equals 返回 true，而 hashcode 不等的情況，這樣如果要求 HashSet 去重就會失敗。

    HashSet 基於 HashMap 實現，HashMap 內部有一哈希表，裏面使用 hashcode 進行散列存儲。

### 序列化時如果有些字段不想序列化，怎麼辦？

使用 transient 關鍵字修飾不想序列化的字段。

### continue、break 和 return 的區別

1. continue：跳出當前這一次循環，繼續下一次循環。
2. break：跳出整個循環體，繼續執行循環外的語句。
3. return：跳出所在的方法，結束方法，可以帶一個返回值。

### 泛型、類型擦除和通配符

**泛型的本質是將類型參數化。**Java 的泛型（generics）是 JDK 5 中引入的新特性，還提供了編譯時類型安全檢測機制來檢測非法的類型。但是 Java 的泛型在編譯期間會將泛型信息擦除，即類型擦除，因此也被稱爲**僞泛型**。下面的例子展示了如何在運行期加入非法類型。

```java
List<Integer> list = new ArrayList<>();
list.add(12);
//這裡直接添加會報錯
// list.add("a");
Class<? extends List> clazz = list.getClass();
Method add = clazz.getDeclaredMethod("add", Object.class);
//但是通過反射添加，是可以的
add.invoke(list, "kl");
System.out.println(list);
```

泛型分泛型接口、泛型類和泛型方法。泛型類的具體類型通過實例化時傳入，泛型方法的具體類型通過方法調用時傳入的參數確定。

泛型通配符約定：

1. ？ 表示不確定的 Java 類型，用於泛型方法
2. T（Type）表示確定的一個 Java 類型
3. K V（Key Value）分別表示映射中的鍵、值
4. E（Element）表示集合中的一個元素
5. <? extends A> 上界通配符，表示 A 類型或其子類
6. <? super A> 下界通配符，表示 A 類型或其父類
7. <T extends A> 表示 A 類型或其子類的一種
8. <T extends A & B> 表示 A 類型且B類型的子類的一種
9. ~~<T super A>~~ 

泛型不是協變的，已知 Apple 繼承自 Fruit 的情況下，Plate<Apple> 的引用並不能傳遞給 Plate<Fruit>，但可以傳遞給 Plate<? extends Fruit>。

元素爲 <? extends E> 的集合，只能取出 E，而不能存入 E 及其子類的對象。因爲只能確定該類型是 E 的子類，但具體是哪個子類未知，因此編譯器不允許插入任何 E 或其子類的對象，取出來的時候只能當 E 類型。

```java
public static void main(String[] args) {
  List<? extends A> list = Arrays.asList(new A(), new B());
  list.add(new A()); // 報錯
  list.add(new B()); // 報錯
  A a = list.get(1);
  System.out.println(a.toString());
}

static class A {
}

static class B extends A {
}
```

元素爲 <? super E> 的集合，只能取出 Object，只能存入 E 及其子類的對象。因爲只能確定該類型是 E 的超類，但不知是哪一個超類，所以插入任何 E 及其子類的對象是沒問題的，但是插入 E 的超類就不行了，取出來的時候也只能是 Object，因爲 Object 是一切類的超類。

```java
public static void main(String[] args) {
  List<? super B> list = new ArrayList<>();
  list.add(new A()); // 報錯
  list.add(new B());
  list.add(new C());
  Object object = list.get(1);
  System.out.println(object.toString());
}

static class A {
}
static class B extends A {
}
static class C extends B{
}
```

### 獲取鍵盤輸入數據的常用方法

```java
// 方法一：使用 Scanner，可以快速確定輸入數據的類型，按空格符分割數據
Scanner scanner = new Scanner(System.in);
String s = scanner.nextLine();
System.out.println(s);

// 方法二：使用 BufferedReader 讀取字符序列，高效但需要轉換成其他類型，會拋出 IOException
BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));
String s1 = bufferedReader.readLine();
System.out.println(s1);
```

## 方法（函數）

### 爲什麼 Java 只有值傳遞？

首先要明瞭程序設計語言中的有關函數參數傳遞的兩種方法：

1. 按值調用（call by value）：方法接收調用者提供的參數的值，方法內無法修改實際參數值。
2. 按引用調用（call by reference）：方法接收調用者提供的參數的地址，方法內可以修改實際參數值。

**Java 總是採用按值調用，所有參數值都是一個拷貝，無法修改實際參數值。對於引用類型參數，傳遞的是引用的拷貝，引用的拷貝和引用指向同一個對象，即所謂的淺拷貝**。

```java
public static void main(String[] args) {
  String s1 = "Hello";
  String s2 = "World";
  swap(s1, s2);
  System.out.printf("main s1: %s, s2: %s%n", s1, s2);
}

static void swap(String s1, String s2) {
  String tmp = s1;
  s1 = s2;
  s2 = tmp;
  System.out.printf("swap s1: %s, s2: %s%n", s1, s2);
}
// 運行結果：
// swap s1: World, s2: Hello
// main s1: Hello, s2: World
```

結論：

1. 一個方法不能修改一個基本類型的實參。
2. 一個方法可以改變一個對象類型的實參狀態。
3. 一個方法不能讓對象類型的實參引用一個新對象。

### 深拷貝和淺拷貝有什麼不同？

1. 淺拷貝：對基本類型拷貝其值；對引用類型拷貝其引用。
2. 深拷貝：對基本類型拷貝其值；對引用類型，新建一個對象並拷貝原對象的值。

![](java-basic/Untitled.png)

### 重載和重寫有什麼區別？

1. 重載（overloading）：在一個類中，有多個同名但不同傳入參數的方法，各個重載方法簽名不同。
2. 重寫（overwrite）：子類對父類允許訪問的方法的重新編寫，方法簽名不變，訪問修飾符只能降低不能提高，拋出的異常只能更小，返回值類型也是。

## Java 面向對象

### 面向對象和面向過程

1. 面向過程：不需要實例化對象，內存和 CPU 開銷小，但不容易維護。
2. 面向對象：需要實例化對象，內存和 CPU 開銷大，但易維護、易復用、易擴展。

Java 因爲編譯出的字節碼並不能直接在機器上運行，因而效率上會稍慢。但一些面向過程的腳本語言性能也不一定比 Java 好。

### 構造方法

1. 特點：名字跟類名相同，沒有返回值，不可重寫但可重載。
2. 作用：執行對象的初始化工作，如果類沒有重載任何構造方法，那默認會有不帶參數的構造方法。
3. 子類初始化時一定會調用父類的構造方法，即使子類不顯式調用，也會默認調用父類的無參構造方法。

### 成員變量和局部變量的區別

1. 成員變量：屬於類；可以被 public、private、static 等修飾符修飾；如用 static 修飾則變量屬於類，否則屬於對象存在於堆內存；生命週期隨對象；自動賦予初始化值。
2. 局部變量：屬於代碼塊或方法；只能被 final 修飾；存在於棧內存；生命週期隨代碼塊或方法；不會自動賦予初始化值。

### 對象實例和對象引用的區別

1. 對象實例：存在於堆內存，一個對象實例可以被多個引用指向。
2. 對象引用：存在於棧內存，一個引用指向一個對象實例。

### 面向對象的三大特徵

**（1）封裝**

封裝是將一個對象的狀態信息（即屬性）隱藏在對象內部，一般不允許外界直接訪問，而是提供必要的方法給外界操作。

**（2）繼承**

繼承是使用已有的類創建新類的技術，它提高了代碼復用率和開發效率。關於繼承以下幾點務必明瞭：

1. 子類擁有父類所有的屬性和方法（包括私有的），但父類中的私有屬性和方法子類無法訪問（反射子類也無法訪問），**僅僅擁有**。
2. 子類可以對父類進行擴展，增加新的屬性和方法。
3. 子類可以重寫父類的方法。

**（3）多態**

多態，即一個對象可以擁有多種狀態。具體表現在父類的引用可以指向子類的實例。關於多態以下幾點務必知曉：

1. 對象類型和引用類型之間具有繼承/實現關係。
2. 對象類型不可變，引用類型可變。
3. 方法具有多態性，屬性不具有。父類的引用可以調用子類對象的方法，但不能訪問其屬性。
4. 父類的引用不能調用「只有子類存在但在父類不存在」的方法。
5. 如果子類重寫了父類的方法，真正執行的是子類覆蓋的方法。

### **靜態方法內爲什麼不能調用非靜態成員？**

因爲非靜態成員需要在類實例化成對象後才能被調用，而靜態方法不需要實例化對象就可以被調用。

### 接口和抽象類的區別

1. 方法上：接口的方法默認修飾符是 public，且不能實現（Java 8 開始可以有默認方法和靜態方法，Java 9 開始可以有私有方法和私有靜態方法）；而抽象類可有 public、protected 和 default 修飾符，且可有非抽象的方法。
2. 變量上：接口只能有 static、final 變量；而抽象類沒有限制。
3. 繼承上：一個類可以實現多個接口，接口本身也可以擴展多個接口；但一個類只能繼承一個抽象類。
4. 設計上：接口是對行爲的抽象，是一個行爲規範；抽象類是對類的抽象，是一種模板設計。

## Java 核心技術

### 集合

見 [Java 集合](https://linlshare.github.io/2020/12/02/it/java/java-collection/) 

### 反射機制

**（1）什麼是反射**

Java 的反射機制是在運行時能知道任意一個類的所有屬性和方法，能調用任意一個對象的屬性和方法。

**（2）反射的優缺點**

1. 優點：運行時確定類型，動態加載類，提高代碼靈活度。
2. 缺點：反射性能比直接的 Java 代碼慢，存在安全問題，因爲可以動態操作改變類的屬性。

反射動態加載類的優點即是動態編譯，與之相對的是靜態編譯，靜態編譯是在編譯時就確定了類型。

**（3）反射的應用場景**

反射是框架設計的靈魂。其應用場景有：

1. 模塊化開發；
2. 動態代理設計模式；
3. Spring 框架的 IOC（控制反轉）和 AOP（面向切面編程）；
4. JDBC 連接數據庫等等。

### 異常

**（1）簡介**

Java 的異常歸於同一個 Throwable 類，並分爲兩大類：Error 和 Exception。**Error 通常是 JVM 錯誤，程序無法處理**；**而 Exception 是程序本身可以處理的異常**。Exception 分爲 Checked Exceptions（受檢異常）和 Unchecked Exceptions（不受檢異常）。

![](java-basic/Untitled%201.png)

**Checked Exceptions 又名 Compile Time Exceptions（編譯時異常）**，編譯器可以發現並要求程序處理後才能正常通過編譯，常見的有：

- *IOException*
- *EOFException*
- *MalFormedURLException*
- *IntruptedException*

**Unchecked Exception 又名 Runtime Exceptions（運行時異常）**，編譯器無法檢測出，只有運行時才會發生的異常，常見的有：

- *ArithmaticException*
- *NullPointerException*
- *IndexOutOfBoundsException*
- *ClassCastException*
- *ArrayIndexOutOfBoundsException*
- *NumberFormatException*

**（2）Throwable 類常用方法**

1. `getMessage`：返回異常的簡要描述
2. `toString`：返回異常的詳細信息
3. `getLocalizedMessage`：返回異常的本地化信息（需要子類覆蓋該方法，否則與 `getMessage` 一樣）
4. `printStackTrace`：在控制台打印 Throwable 对象封装的异常信息

**（3）try-catch-finally**

1. try 代碼塊：捕獲異常。其後可接零個或多個 catch 代碼塊，如零個則必須接一個 finally 代碼塊。
2. catch 代碼塊：處理捕獲到的異常。
3. finally 代碼塊：無論是否捕獲或處理異常，finally 代碼塊最終都會被執行。當在 try 代碼塊或 catch 代碼塊中遇到 return 語句時，finally 代碼塊將在方法返回之前被執行。此時如果 finally 中也有 return 語句的話，其返回值將覆蓋 try 或 catch 代碼塊中的返回值。

```java
public static int f(int value) {
  try {
      return value * value;
  } finally {
      if (value == 2) {
          return 0;
      }
  }
}
// f(2) 將返回 0 ，而不是 4.
```

以下情況，finally 代碼塊不會被執行或只部分執行：

1. finally 代碼塊中有異常，代碼會中異常處中止；
2. 在 catch 代碼塊或 finally 塊中調用了 `System.exit` 函數退出程序；
3. 程序所在的線程死亡等等不可預料的系統和硬件問題。

**（4）try-witch-resources**

Java 7 中新增了 ****try-witch-resources 語法糖，適用於實現`java.lang.AutoCloseable` 或者 `java.io.Closeable` 的對象，可以自動關閉申請的資源，然後再執行 catch 或 finally 代碼塊。

```java
// try-catch-finally
Scanner scanner = null;
try {
    scanner = new Scanner(new File("src/main/resources/test.txt"));
    while (scanner.hasNext()) {
        System.out.println(scanner.nextLine());
    }
} catch (IOException e) {
    e.printStackTrace();
} finally {
    if (scanner != null) {
        scanner.close();
    }
}
// try-witch-resources
try (Scanner scanner = new Scanner(new File("src/main/resources/test.txt"))) {
    while (scanner.hasNext()) {
        System.out.println(scanner.nextLine());
    }
} catch (IOException e) {
    e.printStackTrace();
}
```

### 多線程

見 [Java 多線程](https://linlshare.github.io/2020/12/10/it/java/java-concurrent/) 

### 文件與 I/O 流

**（1）Java 中 I/O 流分爲幾種？**

按不同的分類方法有不同的分類：

1. 按流向分：輸入流、輸出流。
2. 按操作單元分：字節流、字符流。
3. 按角色分：節點流、處理流。

Java 中 40 多個 I/O 流相關的類都是從 4 個抽象基類派生：

1. InputStream：字節輸入流
2. Reader：字符輸入流
3. OutputStream：字節輸出流
4. Writer：字符輸出流

![](java-basic/Untitled%202.png)

![](java-basic/Untitled%203.png)

**（2）爲什麼有了字節流還需要字符流？**

不管是文件讀寫還是網絡發送接收，信息的最小存儲單元都是字節，那為什麼 I/O 流操作要分為字節流操作和字符流操作呢？

字符流是由 JVM 將字節流轉換得到的，過程非常耗時，且容易出現亂碼問題。所以 I/O 流提供直接操作字符流的接口，以避免這種轉換。對於文本建議使用字符流，而圖片、音視頻等應使用字節流。

**（3）BIO、NIO、AIO 有什麼區別？**

1. **BIO**（Blocking I/O），同步阻塞 I/O 模式，數據的讀取寫入必須阻塞在一個線程內等待其完成。適用於活動連接數不高（< 單機 1000）的情況，結合線程池一起使用。
2. **NIO**（Non-blocking I/O 或 New I/O），同步非阻塞的 I/O 模型，Java 1.4 中引入，位於 `java.nio` 包，提供 Channel、Selector 和 Buffer 等抽象，支持基於通道面向緩衝的 I/O 操作方法。適用於高負載、高並發的（網絡）應用。
3. **AIO**（Asynchronous I/O），異步非阻塞的 I/O 模型，Java 7 中引入。支持基於事件回調機制的操作方法。

NIO 模型：

![](java-basic/Untitled%204.png)

- NIO 服務端代碼

    ```java
    public class MultiplexerNioServer implements Runnable {

        private Selector selector;
        private volatile boolean stop = false;

        /**
         * 初始化多路复用器 绑定监听端口
         *
         * @param port
         */
        public MultiplexerNioServer(int port) {
            try {
                ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();//获得一个serverChannel
                selector = Selector.open();////创建选择器  获得一个多路复用器
                serverSocketChannel.configureBlocking(false);//设置为非阻塞模式 如果为 true，则此通道将被置于阻塞模式；如果为 false，则此通道将被置于非阻塞模式
                serverSocketChannel.socket().bind(new InetSocketAddress(port), 1024);//绑定一个端口和等待队列长度
                serverSocketChannel.register(selector, SelectionKey.OP_ACCEPT);//把selector注册到channel，关注链接事件
            } catch (IOException e) {
                e.printStackTrace();
                System.exit(1);
            }
        }

        public void stop() {
            this.stop = true; // 优雅停机
        }

        public void run() {
            while (!stop) {
                try {
                    //无论是否有读写事件发生，selector每隔1s被唤醒一次。如果一定时间内没有事件，就需要做些其他的事情，就可以使用带超时的
                    int client = selector.select(1000);
                    System.out.println("1:" + client);
                    // 阻塞,只有当至少一个注册的事件发生的时候才会继续.
                    // int client = selector.select(); 不设置超时时间为线程阻塞，但是IO上支持多个文件描述符就绪
                    if (client == 0) {
                        continue;
                    }
                    System.out.println("2:" + client);
                    Set<SelectionKey> selectionKeys = selector.selectedKeys();
                    Iterator<SelectionKey> it = selectionKeys.iterator();
                    SelectionKey key = null;
                    while (it.hasNext()) {
                        key = it.next();
                        it.remove();
                        try {
                            //处理事件
                            handle(key);
                        } catch (Exception e) {
                            if (key != null) {
                                key.cancel();
                                if (key.channel() != null) {
                                    key.channel().close();
                                }
                            }
                        }
                    }
                } catch (Throwable e) {
                    e.printStackTrace();
                }
            }

            if (selector != null) {
                // selector关闭后会自动释放里面管理的资源
                try {
                    selector.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        public void handle(SelectionKey key) throws IOException {
            if (key.isValid()) {
                //连接事件
                if (key.isAcceptable()) {
                    ServerSocketChannel ssc = (ServerSocketChannel) key.channel();
                    // 通过ServerSocketChannel的accept创建SocketChannel实例
                    // 完成该操作意味着完成TCP三次握手，TCP物理链路正式建立
                    SocketChannel sc = ssc.accept();//3次握手
                    sc.configureBlocking(false);
                    sc.register(selector, SelectionKey.OP_READ);//连接建立后关注读事件
                }

                //读事件
                if (key.isReadable()) {
                    SocketChannel socketChannel = (SocketChannel) key.channel();
                    ByteBuffer readbuffer = ByteBuffer.allocate(1024);//写 0 1024  1024
    //                ByteBuffer readbuffer = ByteBuffer.allocateDirect(1024); //申请直接内存，也就是堆外内存
                    // 读取请求码流，返回读取到的字节数
                    while (true) {
                        int readBytes = socketChannel.read(readbuffer);
                        // 读取到字节，对字节进行编解码
                        if (readBytes > 0) {
                            // 将缓冲区当前的limit设置为position=0，用于后续对缓冲区的读取操作
                            readbuffer.flip();//读写模式反转
                            // 将缓冲区可读字节数组复制到新建的数组中
                            byte[] bytes = new byte[readbuffer.remaining()];
                            readbuffer.get(bytes);
                            String body = new String(bytes, StandardCharsets.UTF_8);
                            System.out.println("input is:" + body);
                            res(socketChannel, body);
                        } else if (readBytes < 0) {
                            // 链路已经关闭 释放资源
                            key.cancel();
                            socketChannel.close();
                        } else {
                            // 没有读到字节忽略
                            return;
                        }
                    }

                }

            }
        }

        private void res(SocketChannel channel, String response) throws IOException {
            if (response != null && response.length() > 0) {
                byte[] bytes = response.getBytes();
                ByteBuffer writeBuffer = ByteBuffer.allocate(bytes.length);
                writeBuffer.put(bytes);
                writeBuffer.flip();
                channel.write(writeBuffer);
                System.out.println("res end");
            }
        }
    }
    ```

- NIO 客戶端代碼

    ```java
    public class NioClientHandler implements Runnable {
        private final String host;
        private final int port;
        private Selector selector;
        private SocketChannel socketChannel;
        private volatile boolean stop;

        public NioClientHandler(String host, int port) {
            this.host = host;
            this.port = port;
            try {
                // 创建选择器
                selector = Selector.open();
                // 打开监听通道
                socketChannel = SocketChannel.open();
                // 如果为 true，则此通道将被置于阻塞模式；如果为 false，则此通道将被置于非阻塞模式
                socketChannel.configureBlocking(false); // 开启非阻塞模式
            } catch (IOException e) {
                e.printStackTrace();
                System.exit(1);
            }
        }

        public void run() {
            try {
                doConnect();
            } catch (IOException e) {
                e.printStackTrace();
                System.exit(1);
            }
            while (!stop) {
                try {
                    int wait = selector.select(1000);
                    if (wait == 0) {
                        continue;
                    }
                    Set<SelectionKey> selectionKeys = selector.selectedKeys();
                    Iterator<SelectionKey> it = selectionKeys.iterator();
                    SelectionKey key = null;

                    while (it.hasNext()) {
                        key = it.next();
                        it.remove();
                        try {
                            handle(key);
                        } catch (Exception e) {
                            if (key != null) {
                                key.cancel();
                                if (key.channel() != null) {
                                    key.channel().close();
                                }
                            }
                        }
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                    System.exit(1);
                }
            }
            if (selector != null) {
                try {
                    selector.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        private void doConnect() throws IOException {
            if (socketChannel.connect(new InetSocketAddress(host, port))) {
                socketChannel.register(selector, SelectionKey.OP_READ);
                doWrite(socketChannel);
            } else {
                socketChannel.register(selector, SelectionKey.OP_CONNECT);
            }
        }

        private void handle(SelectionKey key) throws IOException {
            if (key.isValid()) {
                SocketChannel sc = (SocketChannel) key.channel();
                if (key.isConnectable()) {
                    if (sc.finishConnect()) {
                        sc.register(selector, SelectionKey.OP_READ);
                        doWrite(sc);
                    } else {
                        System.exit(1);
                    }
                }
                if (key.isReadable()) {
                    ByteBuffer readBuffer = ByteBuffer.allocate(1024);
                    int readBytes = sc.read(readBuffer);
                    if (readBytes > 0) {
                        readBuffer.flip();
                        byte[] bytes = new byte[readBuffer.remaining()];
                        readBuffer.get(bytes);
                        String body = new String(bytes, StandardCharsets.UTF_8);
                        System.out.println("res" + body);
                        this.stop = true;
                    } else if (readBytes < 0) {
                        key.cancel();
                        sc.close();
                    }

                }
            }
        }

        private void doWrite(SocketChannel sc) throws IOException {
            // 将消息编码为字节数组
            byte[] request = "Hello".getBytes();
            // 根据数组容量创建ByteBuffer
            ByteBuffer writeBuffer = ByteBuffer.allocate(request.length);
            // 将字节数组复制到缓冲区
            writeBuffer.put(request);
            // flip读写切换操作
            writeBuffer.flip();
            sc.write(writeBuffer);
            if (!writeBuffer.hasRemaining()) {
                System.out.println("写入完成");
            }
        }
    }
    ```

## Java 項目管理和構建

### Maven 项目

**（1）安装**

從 [Maven 官網](https://maven.apache.org/download.cgi)下載 maven 包，解壓並設置環境變量。還可以直接使用 IDEA 的 Maven 插件。

**（2）初始化一個 Maven 項目**

使用以下命令：

```bash
mvn -B archetype:generate -DgroupId=com.mycompany.app -DartifactId=my-app -DarchetypeArtifactId=maven-archetype-quickstart -DarchetypeVersion=1.4
```

或者用 IDEA 直接新建一個 Maven 項目，其結構如下：

![](java-basic/20201114_101407.png)

其中 pom.xml 的內容如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>testmaven</artifactId>
    <version>1.0-SNAPSHOT</version>

    <!--  添加以下屬性，解決編譯報錯  -->
    <properties>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <maven.compiler.encoding>UTF-8</maven.compiler.encoding>
        <java.version>15</java.version>
        <maven.compiler.source>15</maven.compiler.source>
        <maven.compiler.target>15</maven.compiler.target>
    </properties>
    <!-- 新增依賴在下方 -->
    <dependencies>
        <dependency>
            <groupId>org.openjdk.jol</groupId>
            <artifactId>jol-core</artifactId>
            <version>0.14</version>
        </dependency>
    </dependencies>
</project>
```

- 為什麼叫 Maven？

    Maven 來源於意第緒語，爲「行家」的意思。最初是為了簡化 Jakarta Turbine 項目中的構建過程而建立。Maven 使用項目對象模型（POM）和一組插件來構件項目。

- POM 又是指什麼？

    POM（project object model）項目對象模型，maven 使用 `pom.xml` 定義了整個項目的構建、報告和文檔。

**（3）編譯測試打包**

```bash
# 清理 target 中的文件
mvn clean
# 編譯 java 文件成 class 文件，置於 target/classes 文件夾中
mvn compile
# 進行單元測試
mvn test
# 打包成 jar 文件，置於 target 文件夾中
mvn package
# 安裝 jar 包到本地存儲庫（${user.home}/.m2/repository）
mvn install
# 生成自己的 maven 站點
mvn site
```

- SNAPSHOT 是什麼？

    snapshot 簡要的意思，在版本號之後添加 `-SNAPSHOT` 是說明該版本仍處於開發階段，不是最終的發行版本。以 `x.y-SNAPSHOT` 版本為例，發行時會去除 `-SNAPSHOT`  後綴，然後將最新的開發版本升爲`x.(y+1)-SNAPSHOT` 。

- 使用 mvn compile 生成的 jar 包，其內容是怎樣的？

    除了 class 文件外，還有 `META-INF` 文件夾，裏面存放一些清單文件和pom 文件。存放到項目資源文件夾（`main/resources` ）的文件也會被打包到`META-INF` 文件夾中，代碼中可通過`getClass().getResourceAsStream( "/application.properties" )` 調用。

    ```bash
    $ jar tf target/testmaven-1.0-SNAPSHOT.jar 
    META-INF/
    META-INF/MANIFEST.MF
    B.class
    MemoryLayoutTest.class
    A.class
    C.class
    META-INF/maven/
    META-INF/maven/org.example/
    META-INF/maven/org.example/testmaven/
    META-INF/maven/org.example/testmaven/pom.xml
    META-INF/maven/org.example/testmaven/pom.properties
    ```

### Gradle 项目

**（1）安裝**

可從 [gradle 官網](https://www.gradle.org/downloads)下載解壓並配置環境變量的方式安裝。Mac 用戶還可以使用 `brew install gradle` 的方式安裝。或者直接使用 IDEA 項目中的 `gradle-wrapper` ，此時對應的 `gradle` 命令變爲 `gradlew`。

**（2）gradle 命令能做什麼？**

gradle 命令能構建項目， 查看項目依賴、子項目和項目配置等等。

```bash
$ gradle tasks

:tasks

== All tasks runnable from root project

== Build Setup tasks
setupBuild - Initializes a new Gradle build. [incubating]

== Help tasks
dependencies - Displays all dependencies declared in root project 'gs-gradle'.
dependencyInsight - Displays the insight into a specific dependency in root project 'gs-gradle'.
help - Displays a help message
projects - Displays the sub-projects of root project 'gs-gradle'.
properties - Displays the properties of root project 'gs-gradle'.
tasks - Displays the tasks runnable from root project 'gs-gradle'.

To see all tasks and more detail, run with --all.

BUILD SUCCESSFUL

Total time: 3.077 secs
```

**（3）初始化一個 Gradle 項目**

在項目文件夾中新建一個名爲 `build.gradle` 的文件，其內容如下：

```groovy
apply plugin: 'java'
```

隨後新建一個名爲 `settings.gradle` 的文件，其內容可暫時爲空。

在 IDEA 中打開此項目，隨後 IDEA 會自動配置加入 `gradle-wrapper` ，其過程等價於執行以下命令：

```bash
gradle wrapper --gradle-version 6.5
```

**（4）編譯打包**

```bash
# 編譯項目，會默認在 build/classes 中生成類文件，在 build/libs 中生成 jar 包
gradle build
# 或使用 gradle wrapper
./gradlew build

# 清理生成的文件
gradle clean

# 生成 jar 文件
gradle jar

# 運行生成的 jar 文件
gradle run

# 進行單元測試
gradle test
```

**（5）`build.gradle` 中可配置什麼？**

```groovy
// 配置插件，插件提供語法定義
apply plugin: 'java'
apply plugin: 'application'

// 配置入口類
mainClassName = 'hello.HelloWorld'

// 配置依賴倉庫
repositories {
    mavenCentral()
}

// 配置生成的 jar 文件的入口類
jar {
    manifest {
        attributes 'Main-Class': mainClassName
    }
}

// 配置 JDK 兼容性
sourceCompatibility = 1.8
targetCompatibility = 1.8

// 配置依賴
dependencies {
    compile "joda-time:joda-time:2.2"
    testCompile "junit:junit:4.12"
}
```

如需將所有依賴 jar 打進同一個 jar 包，可使用 [shadow 插件](https://github.com/johnrengelman/shadow)或使用 [spring boot 插件](https://spring.io/quickstart)。