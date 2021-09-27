title: preprocessor trong C
date: 27-09-2021
tags: C
name: preprocessor-directives-c
--------------------


~~Bài này mình chỉ nói về Preprocessor Directives trong C, trong C++, khái niệm này cũng tương tự.~~

# Bạn đã nghe qua khái niệm preprocessor directives chưa?

## preprocessor directives 

Tạm dịch là tiền xử lý, là một phần của compiler C/C++, hướng dẫn cho compiler thực hiện một số thao tác sơ bộ (như biên dịch mã có điều kiện, include file,...) trước khi bước vào giai đoạn biên dịch chương trình. Chúng được bắt đầu bằng ký tự **#** và không phải là lệnh trong chương trình, do đó không có dấu **;** khi kết thúc.

Dưới đây là các preprocessor directives bạn sẽ hay gặp.

## #include

Đây là chỉ thị mà code C/C++ bắt buộc phải có, trước khi compile, nếu trình biên dịch bắt gặp chỉ thị *#include* nó sẽ tìm kiếm tập tin theo tên được ghi trong đoạn lệnh *#include*. Nếu tìm thấy nó sẽ chèn nội dung của tập tin đó vào ngay vị trí *#include* xuất hiện, nếu không sẽ báo lỗi.

C hay C++ có vài tính năng như một phần của ngôn ngữ, một số khác như một phần của thư viện chuẩn (*standard library*), là một kho lưu trữ code có sẵn cùng với việc tuân thủ chuẩn của C-compiler. Khi compiler biên dịch chương trình, nó cũng thường liên kết với thư viện chuẩn. Ví du, khi bắt gặp chỉ thị `#include <stdio.h>`, nó sẽ thay thế chỉ thị bằng nội dung của file header *stdio.h*. Và ~~stdio.h~~ là một trong các thư viện chuẩn của C.

Nếu bạn sử dụng chỉ thị *#include* ở dạng `#include <header_name.h>`, compiler sẽ tìm file *header_name.h* trong đường dẫn tới thư mục *include* của trình biên dịch. Nếu bạn sử dụng ở dạng `#include "other.h"` thì compiler sẽ tìm kiếm file *other.h* trong cả thư mục hiện hành và thư mục *include* của compiler.

Ví dụ, trong thư mục đang làm việc có file *add.h* có nội dung như sau:

```c
int add(int a,int b){
    return a+b;
}
```

Và file main.c:

```c
#inlcude <stdio.h>
#include "add.h"

int main(){
    printf("%d + %d = %d\n",2,2,add(2+2));
    return 0;
}
```

Các thư viện C chuẩn, bạn có thể tham khảo tại [đây](http://en.cppreference.com/w/c/header).

## #pragma

Chỉ thị *#pragma* là phương thức đặc biệt của C standard cho việc cung cấp các thông tin bổ sung cho compiler, nhiều hơn những gì được truyền đạt trong ngôn ngữ đang dùng. Nó dùng để kiểm soát hành vi thực hiện cụ thể, như là disable warning của compiler hoặc thay đổi các alignment requirement. 

Chuẩn ISO C++ không yêu cầu các compiler hỗ trợ bất cứ pragma nào, tuy nhiên, một vài non-standard pragma được hỗ trợ bởi nhiều implementations.

* **#pragma STDC**

Chuẩn ISO C yêu cầu các C compilers hỗ trợ 3 dạng pragmas dưới đây:

1. **#pragma STDC FENV_ACCESS** *arg*
2. **#pragma STDC FP_CONTRACT** *arg*
3. **#pragma STDC CX_LIMITED** *arg*

Trong đó *arg* có thể là **ON**, **OF** hoặc **DEFAULT**.

Hành vi của chương trình là không xác định nếu bất cứ cái nào trong 3 pragma ở trên xuất hiện trong bất cứ ngữ cảnh nào khác ngoài tất cả các khai báo external hoặc đứng trước các khai báo explicit và các câu lệnh trong một khối lệnh.

* **#pragma once**

*#pragma once* là một pragma không chuẩn, được hỗ trợ bởi đại đa số các compiler hiện đại. Nếu nó xuất hiện ở đầu file, nó sẽ đảm bảo tránh việc include trùng lặp.

Cách tiếp cận chuẩn thay thế cho *#pragma once* để chống lại việc include nhiều header giống nhau là sử dụng ~~include guards~~:

```c
#ifndef FILENAME_H  //if not define FILENAME_H
#define FILENAME_H  //then define FILENAME_H
// contents of the header
#endif /* FLENAME_H */ //end
```

Ngoài ra các bạn còn có thể gặp các dạng *#pragma* sau:

* #pragma warning
* #pragma error

Ví dụ, `#pragma warning (disable : 4101)` sẽ bỏ qua warning 4101.

Còn nhiều thứ hay ho về **#pragma** nữa bạn có thể tìm hiểu thêm trên mạng


## macro definitions (#define, #undef)

Macro là một đoạn code được tượng trưng bởi 1 cái tên, tên này thường được viết hoa, khi compiler bắt gặp tên đã được **#define**, nó sẽ thay thế tên bằng đoạn code được định nghĩa. 

Để định nghĩa một macro, bạn sử dụng **#define**, ví dụ:

```c
#define MAX 100 //MAX lúc này là 100

int arr[MAX] //tương đương int arr[100]
```

**#define** cũng dùng để định nghĩa một function macro, ví dụ:

```c
#include <stdio.h>

#define GETMAX(a,b) ((a)>(b)?(a):(b)) //định nghĩa GETMAX(a,b)

int main(){
    int x=5,y=3;
    printf("Max number: %d\n",GETMAX(5,3)); // in ra 5
    return 0;
}
```

Cũng có thể sử dụng **#define** để định nghĩa 1 đoạn code gồm nhiều dòng với ký tự *backslash* **\**, ví dụ:

```c
#include <stdio.h>

#define ERROR() fprintf(stderr,"An error has occurred\n");\
                exit(1)

int main(){
    int a;
    if(!scanf("%d",&a))
        ERROR();
    return 0;
}
```

Định nghĩa function macro chấp nhận 2 toán tử đặc biệt là **#** và **##** trong replacement sequence. Ví dụ:

```c
#define str(x) #x  //thay thế str(x) bởi x
printf("%s",str(ptv)); //in chuỗi ptv
```

hoặc:

```c
#define condition(a,b) a##b //thay thế condition(a,b) bằng chuỗi ab
condition(i,f)(1<2)       //tương đương if(1<2){...{
   printf("true");
}
```

Một ví dụ vui về chỉ thị **#define** với toán tử và **##**:

```c
#include <stdio.h>

#define ptv(H,O,W,A,R,E,U) W##O##R##E
#define FUNNY ptv(i,a,m,f,i,n,e) //thay FUNNY bằng main 

//chương trình không có hàm main :smile:
int FUNNY(){
   printf("Are you happy?\n");
   return 0;
}
```

Bạn cũng có thể bỏ định nghĩa một macro bằng chỉ thị **#undef**, ví dụ:

```c
#define SIZE 100 
int table1[SIZE]; //tương đương int table1[100];
#undef SIZE     // bỏ định nghĩa SIZE
#define SIZE 200 //định nghĩa lại SIZE
int table2[SIZE]; //tương đương int table2[200];
```

## Conditonal inclusions(#ifdef, #ifndef, #if, #endif, #else, #elif)

Mình sẽ chia làm 2 nhóm: 

Nhóm **#if,#else, #elif, #endif**, các chỉ thị này là conditional directives, nó cũng khá tương đồng với các conditional operators trong C. Cú pháp:

```
#if constant-expression-1
    <section-1>
#elif constant-expression-2
    <newline-section-2>
.
.
.
#elif constant-expresion-n
    <newline section-n>
#else
    <newline section>
#endif
```

Nếu *constant-expression-1* đúng thì *<section-1>* được thực hiện, Nếu *constant-expression-2* đúng thì *<newline section-2>* được thực hiện,....

Ví dụ:

```c
#if MAX>100
    printf("Mã nguồn ứng với MAX>100");
#elif MAX<100
    printf("Mã nguồn ứng với MAX<100");
#else
    printf("Mã nguồn ứng với MAX==100");
#endif
```

Nhóm **#ifdef** và **#ifndef** cho phép bạn kiểm tra một *identifier* đã được định nghĩa hay chưa. Nếu chưa được định nghĩa hoặc đã gỡ bỏ định nghĩa thì:

* **#ifdef** *identifier* tương đương với **#if** *0*
* **#ifndef** *identifier* tương đương với **#if** *1*

Nếu identifier đã được định nghĩa rồi và có hiệu lực thì:

* **#ifdef** *identifier* tương đương với **#if** *1*
* **#ifndef** *identifier* tương đương với **#if** *0*

Ví dụ sau bạn sẽ rất hay gặp:

```c
/* Đoạn code dùng định nghĩa header file */
#ifndef HEADER_H
#define HEADER_H
/* ... */
#endif
```
Nếu bạn đã thử debug chương trình bằng việc chèn thêm các dòng lệnh in ra trạng thái của tiến trình thì conditional directives cực kỳ hữu dụng. (Trong trường hợp chương trình của bạn không thể debug bằng **gdb**, chẳng hạn như các chương trình về giao thức truyền thông mạng)

## Line control (#line)

**#line** dùng để chỉ định line numbers trong một chương trình đối với việc tham chiếu chéo (cross-reference) và báo lỗi (erro reporting). Cú pháp:

```c
#line number "filename"
```

*number* là số thứ tự dòng mới sẽ được gán cho dòng code kế tiếp, các số thứ tự của các dòng kế tiếp sẽ tăng từng đơn vị một. *"filename"* là một tham số tùy chọn, cho phép định nghĩa lại tên file sẽ được show ra. Ví dụ:

```c
#line 20 "assigning variable"
int a?;
```

Đoạn code này sẽ sinh ra một lỗi sẽ được show như một lỗi trong file "assigning variable", dòng 20.

## Error directives(#error)

Chỉ thị này hủy bỏ việc compile khi nó được tìm thấy, sinh ra compilation error. Ví dụ:

```c
#ifndef __cplusplus
#error A C++ compiler is required!
#endif
```

Ví dụ này hủy bỏ việc biên dịch nếu tên macro *__cplusplus* không được định nghĩa. 

## Predefined macro names

Các tên macro điển hình dưới đây luôn luôn đã được định nghĩa.

| Macro            | Value                                            |
| ----------------:|:------------------------------------------------:|
|  \_\_LINE\_\_      |  Giá trị số nguyên tượng trung cho dòng hiện tại của file mã nguồn đang được biên dịch           |
|  \_\_FILE\_\_        |  Một string literal chứa tên giả của file nguồn đang được biên dịch.                            |   
|  \_\_DATE\_\_        |  Một string literal định dạng "Mmm dd yyyy" chứa ngày quá trình biên dịch bắt đầu.               |
|  \_\_TIME\_\_        |  Một string literal dạng "hh:mm:ss" chứa thời quá trình biên dịch bắt đầu.                    |
|  \_\_cplusplus   |  Một giá trị nguyên. Phụ thuộc vào version của chuẩn được hỗ trợ bởi compiler: * 199711L: ISO C++ 1998/2003  * 201103L: ISO C++ 2011                 |
| \_\_STDC\_\_       |  Hằng số 1. Nó được định rằng identifier này được định nghĩa là 1 chỉ trong chuẩn thực thi phù hợp.   |

Còn một số macros khác, các bạn có thể tìm hiểu thêm trên mạng.
 
Bài viết này mình tham khảo từ nhiều nguồn khác nhau! Bạn có thể dùng google-sama để tìm hiểu nhiều hơn :smile: Tới đây mình xin kết bài!

