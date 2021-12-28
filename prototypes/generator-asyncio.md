title: Từ Generators tới Asyncio
date: 18-11-2021
tags: python
name: generator-asyncio
summary: Generator là gì, Asyncio là gì, chúng liên quan nhau như thế nào?
-----------------------------------------------------------------------



Trong Python, **Generator** là một khái niệm nâng cao nhưng cũng cực kì quan trọng. Generator có thể được define dưới dạng
biểu thức (expression) hoặc hàm (generator function). Chúng hoạt động như một *iterator*.

Để hiểu về generator ta cần hiểu về iterator.

# Iterator

## Định nghĩa

Trong Python, Iterator là một đối tượng có thể lặp qua mỗi phần tử trong nó điển hình là *collections* và *sequences* trong Python.

Iterator cung cấp một cách thức để truy cập các phần tử trong nó, nói cách khác, nó chỉ trả về mỗi phần tử của một collection tuần tự.
Các collections này đều có method `__iter__()` để trả về một đối tượng iterable và `__next__()` để trả về phần tử kế tiếp mỗi khi hàm built-in `next()` được gọi.

Nếu một đối tượng có method `__next()__` đính trong nó, nó là một iterator.

Ví dụ, các đối tượng sau đều là iterator:

```python
for element in [1, 2, 3]:
    print(element, end=' ')
print('\n')

for e in (1, 2, 3):
    print(e, end=' ')
print('\n')

for key in {'one': 1, 'two': 2}:
    print(key, end=' ')
print('\n')

for char in "abc":
    print(char, end=" ")
print('\n')

for line in open('example.txt'):
    print(line, end=' ')
print('\n')
```
kết quả:

```python
1 2 3
1 2 3
one two
a b c
---------------------
FileNotFoundError     Traceback (most recent call last)
....

FileNotFoundError: [Errno 2] No such file or directory: 'example.txt'
```

Đây là những gì chúng ta thấy. Nhưng thực sự đây là những gì diễn ra phía sau câu lệnh `for`:

* `for` gọi hàm `iter()` trên đối tượng được lặp. Hàm này trả về một đối tượng iterable, đối tượng này đã định nghĩa phương thức `__next__()`, nó cho phép
truy cập một phần tử tại 1 thời điểm.

* Khi không còn phần tử nào để duyệt qua nữa, `__next__()` sẽ raise một `StopIteration` Exception để thông báo rằng vòng lặp kết thúc.

* `for` gọi phần tử kế tiếp trong container bằng cách dùng hàm built-in `next()`.

* Các phương thức `__iter()__` và `__next__()` được gọi là iterator protocol.

Xét ví dụ sau:

```python
s = "abc"
it = iter(s)
print(it)   # print <str_iterator object at 0x...>
print(next(it))  # print a
print(next(it))  # print b
print(next(it))  # print c
print(next(it))  # raise StopIteration exception
```

Để nhìn rõ hơn, ta sử dụng module `dis`

```python
import dis

l = [1, 2, 3, 4, 5]
for e in l:
    print(e)

print(dis.dis('for e in l: print(e)'))
```

kết quả hiển thị trên console:

```python
1
2
3
4
5
  1           0 SETUP_LOOP              20 (to 22)
              2 LOAD_NAME                0 (l)
              4 GET_ITER
        >>    6 FOR_ITER                12 (to 20)
              8 STORE_NAME               1 (each)
             10 LOAD_NAME                2 (print)
             12 LOAD_NAME                1 (each)
             14 CALL_FUNCTION            1
             16 POP_TOP
             18 JUMP_ABSOLUTE            6
        >>   20 POP_BLOCK
        >>   22 LOAD_CONST               0 (None)
             24 RETURN_VALUE
None
```

Như bạn có thể thấy, `for` statement gọi `GET_ITER` tương ứng với hàm `iter(l)` được gọi. Vì đó nó tạo một iterator có thể được gọi bằng `FOR_ITER` tương đương với `next()` và sẽ trả về các kết quả.

**Trong Python, ngoài việc chúng ta có thể tạo một iterable object bằng việc dùng iterator protocol** `__iter__()`, **thì ta có thể dùng method** `__getitem__()`


Tóm lại ta có thể kết luận đơn giản như sau:

* Iterable object là một object có thể được duyệt qua bằng các vòng lặp như `for`, `while` hay đằng sau nó là protocol `__next__()`

* Iterator là một iterable object

* Iterator được tạo ra bằng cách gọi phương thức `__iter__()` thông qua hàm built-in `iter()` và được duyệt qua bằng phương thức `__next__()` thông qua hàm built-in `next()`


## Các tính chất của Iterator

* Iterator chỉ có thể được duyệt qua một lần duy nhất.

Xét ví dụ sau:

```python

```


# Generator
