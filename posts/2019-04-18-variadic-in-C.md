~~Bài này mình bàn về variadic functions và variadic macros trong C~~

# Variadic functions

Variadic functions tạm dịch là các hàm tham lượng động, là các hàm có các tham số không cố định,nó có thể được gọi với một số các tham số khác nhau, chẳng hạn họ hàm [printf](http://en.cppreference.com/w/c/io/fprintf).

Khai báo một hàm tham lượng động sử dụng một ellipsis (dấu **...**) cho tham số cuối cùng, ví dụ, hàm `int printf(const char* fmt, ...);`. Ví dụ:

```c
int printx(const char* fmt,...); //khai báo
printx("hello world"); //có thể được gọi với một tham số
printx("a=%d b=%d",a,b); //hoặc nhiều tham số

//Nhưng các dạng sau đây sẽ lỗi
// int printy(...,const char* fmt); //Khai báo sai
// int printz(...) //ít nhất phải có một tham số có tên trước ...
```

Tại function call, mỗi tham số là một phần của danh sách đối biến trải qua chuyển đổi đặc biệt không rõ ràng được biết như tham số khuyến mãi mặc định.

Trong thân hàm sử dụng tham lượng động, giá trị của các tham số có thể được truy cập sử dụng [stdarg.h](http://www.cplusplus.com/reference/cstdarg/) header. Ví dụ:

```c
#include <stdio.h>
#include <time.h>
#include <stdarg.h>

void timelog(const char* fmt,...){
    char msg[50];
    strftime(msg, sizeof msg, "%T",localtime(&(time_t){time(NULL)}));
    printf("[%s] ",msg);
    va_list args;
    va_start(args, fmt);
    vprintf(fmt,args);
    va_end(args);
}
int main(){
    timelog("logging %d %d....\n",1,2,3); //xuất dạng [hh:mm:ss] logging 1 2 3...
}
```

Ví dụ, in các giá trị của các kiểu dữ liệu khác nhau:

```c
#include <stdio.h>
#include <stdarg.h>

void m_printf(const char* fmt,...){
    va_list args;
    va_start(args,fmt);

    while(*fmt!='\0'){
        if(*fmt=='d'){
            int i=va_arg(args,int);
            printf("%d\n",i);
        }else if(*fmt=='c'){
            //automatic conversion to integral type
            int c=va_arg(args,int);
            printf("%c\n",c);
        }else if(*fmt=='f'){
            double d=va_arg(args,double);
            printf("%f\n",d);
        }
        ++fmt;
    }
    va_end(args);
}

int main(void)
{
    m_printf("dcff",1,'a',3.14,0);
}
```

# Variadic macro

Variadic macro là một tính năng của vài ngôn ngữ lập trình máy tính, đặc biệt là C preprocessor, theo đó một macro có thể được khai báo để chấp nhận một số đa dạng các tham số. Ví dụ:

```c
#define eprintf(...) fprintf(stderr, __VA_ARGS__)
```

Khi macro được gọi, tất cả các token trong danh sách tham số của nó sau tham số có tên cuối cùng, gồm cả bất kỳ dấu phẩy nào, gọi là *variable argument*. Trình tự này của các token thay thế identifier \_\_VA\_ARGS\_\_ trong thân macro bất cứ khi nào nó xuất hiện, ví dụ:

```c
eprintf("%s:%d: ",in_file, line_no)
// trở thành fprintf(stderr, "%s:%d: ",in_file, line_no)
```

Variable argument là macro mở rộng hoàn toàn trước khi nó được chèn vào macro mở rộng, như một tham số bình thường. Bạn có thể dùng toán tử **#** và **##**  để nối variable argument hoặc paste nó vào token đầu hoặc đuôi với token khác. 

Nếu macro của bạn phức tạp, có thể bạn muốn nhiều tên mô tả cho variable argument hơn \_\_VA\_ARGS\_\_. CPP cho phép điều này, như là phần mở rộng. Bạn có thể viết một tham số ngay trước *'...'*, tên đó được dùng cho variable argument, ví dụ macro eprintf trên có thể được viết:

```c
#define eprintf(args...) fprintf(stderr, args)
```

sử dụng phần mở rộng này. Bạn không thể dùng \_\_VA\_ARGS\_\_ và phần mở rộng này trong một macro giống nhau.

Bạn có thể đặt tên các tham số cũng như các variable arguments trong một variadic macro. Ta có thể định nghĩa *eprintf* như sau:

```c
#define eprintf(fmt,...) fprintf(stderr,fmt,__VA_ARGS__)
```

Dạng này trông có vẻ đặc tả nhiều hơn, nhưng nó lại ít mềm dẻo hơn. Bạn phải cung cấp ít nhất một tham số sau chuỗi định dạng. Trong C chuẩn, bạn không thể bỏ qua dấu phẩy tham số đã đặt tên từ các variable argument. Hơn nữa, nếu bạn để variable argument rỗng, bạn sẽ nhận lỗi cú pháp, bởi vì sẽ có dấu phẩy mở rộng phía sau chuỗi định dạng, chẳng hạn như:

```c
eprintf("success!\n",);
// trở thành fprintf(stderr, "success!\n",);
//sẽ báo lỗi
```

GNU CPP có một cặp extensions để giải quyết vấn đề này. Thứ nhất, bạn được phép để variable argument ngoài một cách trọn vẹn:

```c
eprintf("success!\n")
//trở thành fprintf(stderr,"success!\n",); --> OK
```

Hai là dùng **##**  paste toán tử có một nghĩa đặc biệt khi thế giữa một dấu phẩy và một variable, nếu bạn viết:

```c
#define eprintf(fmt,...) fprintf(stderr, fmt,##__VA_ARGS__)
```

và variable argument được rời ra khi macro eprintf được dùng, sau đó dấu phẩy trước *##* sẽ bị xóa. Nó không xảy ra nếu bạn truyền một tham số rỗng,hoặc nếu trước *##* là bất cứ gì khác dấu phẩy.

```c
eprintf("success!\n")
// trở thành fprintf(stderr, "success!\n");
```

Variadic macro trở thành một phần của ngôn ngữ C chuẩn với C99. 

Bài viết tham khảo từ các nguồn khác nhau!


