title: storage classes trong C
date: 27-09-2020
tags: C
name: storage-class
-----------------------

# Các lớp lưu trữ trong C

Trong lập trình C bạn sẽ hay gặp các storage classes còn gọi là các lớp lưu trữ. Điển hình hay gặp là **extern**, **static**, **register** và **auto**.

## extern

Lúc lập trình bạn có thể gặp trường hợp khai báo biến với từ khóa **extern** ở trong 1 hoặc vài file của chương trình, ví dụ:

```c
extern int value;
```

Về ý nghĩa, lớp lưu trữ này thường được sử dụng để tham chiếu tới biến global (biến toàn cục) trong chương trình và báo cho compiler biết rằng biến này đã khai báo và định nghĩa ở một file nào đó của chương trình rồi để tránh việc xung đột trong đặt tên, cũng như giảm bớt số lượng tên biến phải dùng.

**Lưu ý**: không được khởi tạo (initialize) giá trị cho biến có khai báo **extern**. Phạm vi truy cập của biến (scope) được khai báo **extern** là xuyên suốt toàn bộ chương trình, tồn tại tới khi chương trình kết thúc việc thực thi.

Trong một chương trình có nhiều file, một biến global trong một file có thể được truy cập từ một file khác bằng cách sử dụng lớp lưu trữ **extern**.

## static

Lớp lưu trữ **static** được dùng cho cả các biến global và local trong chương trình, ví dụ:

```c
static int value;
```

Các biến static cục bộ (local static variables) chỉ có thể được truy cập trong phạm vi một hàm hoặc một block nơi nó được khai báo, nhưng thời gian tồn tại của  biến static cục bộ là suốt toàn bộ chương trình.

Các biến static toàn cục (global static variables) có phạm vi truy cập tron toàn bộ file nơi nó được khai báo, nhưng không truy cập được ở các file khác trong chương trình.

***Tóm lại***, dù là biến **static** toàn cục hay cục bộ, phạm vi truy cập của chúng đều chỉ giới hạn trong file nơi chúng được khai báo, nhưng tồn tại tới khi chương trình kết thúc.

## register

Khi tiếp xúc với lập trình vi điều khiển - lập trình nhúng, bạn hay gặp từ khóa **register**. Đây là một lớp lưu trữ mà khi khai báo biến với từ khóa **register**, biến sẽ được lưu trong một trong các thanh ghi của CPU. Các thanh ghi được điều khiển trực tiếp bởi CPU, vì vậy dữ liệu trong biến với lớp lưu trữ **register** có thể được truy cập và xử lý với tốc độ nhanh hơn so với biến được lưu trữ trong bộ nhớ chính.

Để chương trình thực thi nahnh hơn thì truy cập thường xuyên thanh ghi là tốt nhất.

Phạm vi truy cập và thời gian tồn tại của biến **register** là cục bộ, tức là tới khi hàm hoặc một khối code nơi nó được khai báo kết thúc. Ví dụ:

```c
register int value;
```

***Tuy nhiên***, trình tối ưu của compiler sẽ lờ đi các biến khai báo **register** nếu như số lượng thanh ghi trong CPU không đủ.

## auto

Khi một biến được khai báo với lớp lưu trữ **auto**, phạm vi truy cập của biến là cục bộ trong hàm hoặc block code nó được khai báo, thời gian tồn tại của biến tới khi hàm hoặc một block code kết thúc. Ví dụ:

```c
auto int value;
```

Đó là một số lớp lưu trữ trong C, mình xin kết bài ở đây!

