title: Python GIL
date: 28-09-2021
tags: python, system
name: python-gil
summary: GIL hoạt động ra sao?
----------------------------

# 1. Python Global Intepreter Lock (GIL) là gì?
Nói đơn giản, Python GIL là một [mutex](https://en.wikipedia.org/wiki/Mutual_exclusion) hay **Lock**, nó chỉ cho phép chỉ một [thread](https://realpython.com/intro-to-python-threading/)
điều khiển Python Interpreter tại một thời điểm

Điều này có nghĩa chỉ một *thread* có thể xử lý `Python` bytecode tại một thời điểm, cho đến khi thread đó thực hiện xong.
Với các developer không quan tâm tới lập trình đa luồng thì GIL không có ảnh hưởng gì mấy. Nhưng nó sẽ là một nút cổ chai kinh khủng
đối với hiệu năng đa luồng hoặc các tác vụ đòi hỏi nặng về `CPU-bound`.

**Trong bài này, mình sẽ trình bày cơ chế hoạt động của GIL cũng như những ảnh hưởng của nó đối với một chương trình chạy bằng `Python`**

# 2. Vậy GIL hoạt động ra sao?
Chi tiết, bạn có thể đọc bài của tác giả [David Beazley](https://www.dabeaz.com/python/UnderstandingGIL.pdf). Ở đây mình chỉ tóm tắt sơ bộ về cơ chế hoạt động của GIL

## * Đầu tiên, CPython.
**Xét ví dụ sau**

```python
from threading import Thread
import time

def countdown(n):
    while n > 0:
        n -= 1
start = time.perf_counter()
countdown(100000000)
end = time.perf_counter()
print(f"single {end - start}")

thread_start = time.perf_counter()
t1 = Thread(target=countdown, args=(100_000_000//2,))
t2 = Thread(target=countdown, args=(100_000_00//2),))

t1.start()
t2.start()
t1.join()
t2.join()
thread_end = time.perf_counter()
print(f"thread {thread_end - thread_start}")


```
* hiệu năng trên máy MacPro 4 nhân: chạy tuần tự: 7.8s; threaded (2 threads): 15.4s
* hiệu năng nếu chạy trên 4 threads: 15.7s
* hiệu năng nếu 1 CPU bị disabled: 2 threads: 11.3s; 4 threads: 11.6s (Nhanh hơn ~35% nếu so với chạy threads trên cả 4 nhân)

**Vì sao?**

Như bạn đã biết `CPython` được implemented bằng `C` và `Python`. `CPython` là một *compiler* lẫn *interpreter*. Đầu tiên nó sẽ biên dịch
`Python` code sang dạng `bytecode`, sau đó nó sẽ thông dịch các mã `bytecode` đã được biên dịch sẵn.
Tuy nhiên, không phải `Python` không có khả năng `multithreading`; `GIL` cũng không có nghĩa `CPython` không phù hợp cho các tác vụ đòi hỏi
`CPU-intensive` phân phối trên nhiều `cores`.

Thông thường, `GIL` ít gây ra bottleneck, bởi vì hiếm có ai dùng `Python` cho các tác vụ nặng về CPU. Thay vào đó người ta sẽ dùng `Python` để
gọi các hàm hay các thư viện chuyên biệt được implemented bởi các ngôn ngữ khác như `C/C++`, `Fortran`, `Rust`,... Lúc này, `Python` codes trong thread khác
có thể được thực thi trong khi vẫn gọi hàm từ các thư viện chuyên biệt kể trên.

Lang man cũng nhiều rồi, giờ ta sẽ vào phần chính...

## * Python threads và GIL.
`Python threads`, cũng giống như system threads (`POSIX threads` hay còn gọi là pthreads, và `windows threads`). Các Python threads được quản lý hoàn toàn bởi
hệ điều hành. Quá trình thực thi của các Python thread được thực hiện bởi trình thông dịch Python.

Trong GIL:
1. Thực thi song song (parallel) bị cấm
2. Chỉ cho phép một thread chạy trong interpreter tại một thời điểm
3. Đơn giản hóa các chi tiết ở mức low-level (VD: Quản lý  bộ nhớ, Python interpreter sẽ gọi các extensions được viết trong `C`, etc)

<img src="https://i.imgur.com/bJQ65QH.png" alt="Mô hình thực thi các thread" width=400 height=200/>
    
    * Khi thread chạy, nó sẽ giữ GIL
    * GIL giải phóng với các tác vụ I/O

Với các tác vụ CPU-Bound:
* Các tác vụ CPU-bound sẽ được check mỗi 100 `**ticks**`.
* Có thể thay đổi nó sử dụng `sys.setcheckinterval()` trong module `sys`.

**Vậy `ticks` là giống gì?
Chúng ta sẽ xét ví dụ sau:

```python
def countdown(n):
    while n > 0:
        print(n)
        n -= 1
```

Đây là những gì xảy ra trong `Python Virtual Machine`.
Các số 2, 3, 4 là số dòng trên hàm `countdown` đã định nghĩa ở trên.
Nhân tiện mình giới thiệu luôn module  `dis` dùng để disassembly code trong CPython.
    * *Tick 1* sẽ từ dòng đầu tiên đến lệnh **POP_JUMP_IF_FALSE**
    * *Tick 2* chạy từ lệnh **LOAD_GLOBAL**
    * *Tick 3* sẽ chạy từ lệnh **INPLACE_SUBTRACT**
    * *Tick 4* sẽ từ **JUMP_ABSOLUTE** trở xuống.

```python
>>> import dis
>>> dis.dis(countdown)
  2     >>    0 LOAD_FAST                0 (n)
              2 LOAD_CONST               1 (0)
              4 COMPARE_OP               4 (>)
              6 POP_JUMP_IF_FALSE       26

  3           8 LOAD_GLOBAL              0 (print)
             10 LOAD_FAST                0 (n)
             12 CALL_FUNCTION            1
             14 POP_TOP

  4          16 LOAD_FAST                0 (n)
             18 LOAD_CONST               2 (1)
             20 INPLACE_SUBTRACT
             22 STORE_FAST               0 (n)
             24 JUMP_ABSOLUTE            0
        >>   26 LOAD_CONST               0 (None)
             28 RETURN_VALUE

```

**Check định kỳ (Periodic check)**
* Thread đang chạy hiện tại sẽ:
    * Reset tick counter
    * Chạy signal handlers nếu là thread chính (main thread)
    * Giải phóng GIL (Release)
    * Reacquires GIL

## * Python locks
* Python interpreter chỉ có một loại khóa đơn (single lock type) được sử dụng để build các thread đồng bộ hóa nguyên thủy (thread synchronization primitives)
* Nó không đơn giản là `**mutex**` lock
* Nó là một semaphore nhị phân (Binary semaphore) được dựng từ `pthread mutex` và biến điều kiện (condition variable)
* GIL thực ra là một instance của loại lock này.

## * Thread switching.
Giả sử bạn đang có 2 thread:
* Thread 1 đang chạy
* Thread 2 sẵn sàng chạy (đang chờ GIL)

**Trường hợp 1: đơn giản:**

* Thread 1 đang chạy 1 tác vụ I/O (read/write), nó có thể bị chặn. Vì thế nó releases GIL như hình sau.

<img src="https://i.imgur.com/h6aKNVN.png" alt="I-O" width=400 height=200/>

* Kết quả của việc releases GIL trong một signal operation.

<img src="https://i.imgur.com/Pe7YCxu.png" alt="I-O2" width=400 height=200/>


* Được xử lý bởi thread library và hệ điều hành

**Trường hợp 1: tricky:**

* Thread 1 vẫn đan check.

<img src="https://i.imgur.com/ww6Utdm.png" alt="thread" width=400 height=200/>


* Cả 2 thread đều sẵn sàng chạy
* Các biến điều kiện có 1 hàng chờ nội bộ.

<img src="https://i.imgur.com/svBBNn0.png" alt="cond-var" width=400 height=200/>


* Hệ điều hành có một hàng đợi ưu tiên (`priority queue`) cho threads/processes. HĐH sẽ chạy các threads/processes với mức ưu tiên cao hơn sau khi nhận 1 tín hiệu vào hàng đợi đó.
* thread switching sẽ thực hiện theo hình sau:

<img src="https://i.imgur.com/um90Yzy.png" alt="thread-switching" width=400 height=200 />

Sơ lược và vậy, bạn có thể tìm hiểu sâu hơn trong bài của bác David Beazley.

# 3. GIL đã giải quyết những vấn đề gì?
Python sử dụng reference counting để quản lý bộ nhớ. Phần này mình sẽ trình bài ở bài sau. Tạm hiểu là các đối tượng được tạo trong Python
có một thuộc tính reference count, thuộc tính này giúp interpreter theo dõi số references trỏ tới đối tượng.
Khi thuộc tính này về 0, vùng nhớ được chiếm bởi đối tượng sẽ được giải phóng.

VD:
```python
>>> import sys
>>> a = []
>>> b = a
>>> sys.getrefcount(a)
3
```

* Với GIL. Vấn đề ở đây là cái reference counting ở trên phải được bảo vệ khỏi `race condition` - một cơn ác mộng trong parallel programming, khi 2 hay nhiều threads tăng hay giảm giá trị của nó một cách đồng thời.
Nếu điều này xảy ra, nó có thể gây `leaked memory`, và object đó sẽ không bao giờ được released, hoặc tệ hơn là nó được released trong khi vẫn còn các reference counting khác.
Nó sẽ gây *crashed* chương trình hoặc undefined behavior. Cái này bạn nào code C/C++ làm việc với con trỏ sẽ rõ nó đau đầu ra sao :)

* Vấn đề này có thể được giải quyết bằng việc thêm locks vào tất cả các cấu trúc dữ liệu mà nó được shared giữa các threads. Tuy nhiên, thêm locks
vào những object hay nhóm các object có nghĩa nhiều locks sẽ tồn tại - gây ra một cơn đau đầu khác `**Deadlocks**` (deadlocks có thể chỉ xảy ra nếu có nhiều hơn 1 lock)
Một side effect khác sẽ làm giảm performance bằng việc lặp lại acquisition và release các locks

* Như đã nói sơ qua ở trên. GIL là một khóa đơn trên interpreter, nó thêm một rule thực thi là Python bytecode yêu cầu cung cấp interpreter lock.
Điều này sẽ chống được deadlocks mà không cải thiện được nhiều hiệu suất chương trình.
Nhưng những chương trình đòi hỏi các tác vụ CPU-bound đơn luồng (single threaded) lại hoạt động hiệu quả. Như ví dụ đầu bài.

* GIL mặc dù được sử dụng trong các ngôn ngữ thông dịch khác như Ruby không chỉ giải quyết vấn đề trên. vài ngôn ngữ chống lại yêu cầu của GIL cho các
thread-safe memory management bằng việc dùng các cách tiếp cận khác như garbage collection.
* Mặc khác, vài ngôn ngữ có một sự đền bù cho việc vắng mặt hiệu năng đơn luồng của GIL bằng việc sử dụng các tính năng khác như JIT

# 4. Tại sao GIL được chọn để giải quyết vấn đề?
Chính quyết định chọn GIL là một trong những thứ làm cho Python cực kì phổ biến ngày nay.
Python đã có từ thời máy tính và hệ điều hành còn chưa có khái niệm thread. Python được thiết kế để dễ sử dụng và nhanh chóng để phát triển ứng dụng.
Nhiều extensions đang được viết cho các thư viện `C` đã tồn tại các tính năng cần thiết trong Python. Để chống lại các sự thay đổi không nhất quán,
các C extensions được yêu cầu quản lý bộ nhớ kiểu thread-safe mà GIL đã cung cấp.

GIL giúp tăng hiệu năng với các chương trình đơn luồng, nơi mà chỉ cần 1 lock để quản lý.

Các thư viện `C` mà không phải thread-safe đã trở nên dễ dàng tích hợp. Và các C extensions đã trở thành một trong các lý do Python dễ dàng thích nghi bởi nhiều cộng đồng khác nhau

Cho nên, GIL không phải 1 điểm yếu. Nó là một giải pháp thực tiễn cho các vấn đề khó mà các `CPython` developers đã đối mặt trong quá khứ.

# 5. Tác động đến chương trình multi-threaded

Trở lại với ví dụ đầu bài. Khi chạy single-thread, comment out tất cả dòng code bên dưới, chương trình sẽ in ra `Time taken in seconds - 6.20024037361145`
Sau đó, comment out đoạn code ở trên phần multi-threaded, chương trình sẽ in ra `Time taken in seconds - 6.924342632293701`

Như bạn đã thấy đó, thời gian khá tương đồng ở hai phiên bản. Trong phiên bản multi-threaded, GIL chống lại các CPU-bound threads thực thi song song.

GIL không tác động nhiều trên hiệu năng của các chương trình I/O-bound multi-threaded như khóa được shared giữa các threads trong khi chờ I/O như cách hoạt động của GIL mình đã trình bày ở trên
Đối với các chương trình mà toàn là các CPU-bound threads, eg: chương trình xử lý ảnh,.. sẽ trở thành single threaded do lock. Nhưng cũng sẽ thấy thời gian thực thi tăng.

Sự tăng lên này là kết quả của việc acquire và release tài nguyên liên tục giữa các thread được thêm vào bởi lock.

# 6. Vậy, tại sao GIL vẫn còn tồn tại ở CPython?
Bạn có thể thấy, hầu hết các diễn đàn về Python đều phàn nàn về GIL trong Python. Tuy nhiên các Python developers phải cân nhắc kỹ lưỡng rằng một ngôn ngữ phổ biến như Python nếu có một sự thay đổi lớn
như việc remove GIL ra khỏi interpreter như vậy có gây ra các vấn đề tương thích ngược hay không.

Rõ ràng là GIL không thể bị loại bỏ khỏi CPython, sự cố gắng này của các nhà nghiên cứu và phát triển Python đã được thực hiện nhiều lần trong quá khứ rồi, bởi ai mà không muốn một tính năng tốt hơn phải không :D
tuy nhiên nó đã phá vỡ các C extensions phụ thuộc rất lớn vào giải pháp của GIL cung cấp trước đó.

Dù GIL đã xử lý rất tốt các vấn đề, nhưng vài trong số chúng cũng giảm hiệu năng của các chương trình single-threaded và multi-threaded I/O-bound.

Tác giả của Python cũng đã nói trong bài [It isn't Easy to remove the GIL](https://www.artima.com/weblogs/viewpost.jsp?thread=214235)

Python 3 mà không có GIL thì hiệu năng lại tệ hơn Python 2 trong chương trình single-threaded. Ưu điểm lớn nhất của GIL chính là hiệu năng của chương trình
single-threaded, cho nên GIL vẫn còn được dùng trong Python 3.

Với chương trình vừa có các threads I/O bound lẫn CPU-bound thì Python ép các threads giải phóng GIL <u>sau mỗi khoảng nhất định gọi là tick</u>

# 7. Cách làm việc với GIL.
Nếu bắt buộc phải làm việc multi-threaded trên Python, bạn nên:

* dùng **multiprocessing** thay vì *multithreading*
* dùng một interpreter khác `CPython` như `PyPy`, `JPython`,...
* và chờ... :D

Bài viết này hơi dài và lang mang. Mình xin kết bài ở đây.
Nguồn: [David Beazley,](http://www.dabeaz.com/) và [realpython](https://realpython.com/).
