title: Read/Write trong C
date: 27-09-2020
tags: C
name: read-write
------------------


# Hoạt động của các hàm read()/write() và sự khác nhau với các hàm đọc/ghi trong thư viện stdio.h.

Trước hết mình nói qua về khái niệm file. File là một tập có cấu trúc của dữ liệu. Một physical file (file vật lý) đề cập đến cách lưu trữ file trên phần cứng (ví dụ: trên đĩa, file được lưu trữ thành các blocks được tạo thành từ các tracks và sectors). Một logical file là cách lập trình viên tổ chức cấu trúc file, chứa một đặc tả (description) các bản ghi (record) đặc tính được tìm thấy trong một hoặc nhiều file.

Mọi thiết bị trên hệ thống UNIX đều được xem là file, các file được quản lý bởi kernel thông qua các file descriptor. Khi bạn muốn truy cập thiết bị nào, hệ thống sẽ cấp cho bạn file desciptor của thiết bị đó, bạn sẽ tương tác với thiết bị thông qua file descriptor.

## Hàm read()/write().

Các hàm read(), write() là một lời gọi tới hệ thống nằm trong thư viện unistd.h. Dùng để đọc dữ liệu từ physical file hoặc ghi dữ liệu ra physical file.

Theo sách ~~*The C Programming Language*~~ thì prototype của read() là:

```c
int read(int fd, char* buf, int size);
```

và của write() là:

```c
int write(int fd, char* buf, int size);
```

Trong đó **fd** là *file descriptor*, **buf** là con trỏ tới bộ đệm để chưa dữ liệu đọc được hoặc dữ liệu cần ghi, **size** là số byte cần đọc hoặc ghi.
Số byte đọc/ghi có thể nhỏ hơn size vì nhiều lý do, chẳng hạn nhu bộ nhớ vật lý thiếu không gian lưu trữ, hoặc bị ngắt (interrupt) bởi *signal handler*, etc. Nếu đọc/ghi thành công sẽ trả về số byte đoc/ghi được, nếu lỗi giá trị trả về là -1 kết hợp với biến hệ thống **errno** được set. Chi tiết của hàm [read()](https://linux.die.net/man/2/read), [write()](https://linux.die.net/man/2/write) bạn có thể tham khảo thêm.

read()/write() có thể đọc/ghi bất cứ số bytes nào trong một lần gọi. Giá trị phổ biến nhất là 1, điều này nghĩa là mọt ký tự được đọc/ghi tại 1 thời điểm (unbuffered), và một số nhứ 1024 hay 4096 tương ứng với một khối kích thước trên một thiết bị ngoại vi. Các kích thươc shonw hơn sẽ hiệu quả hơn vì ít lời gọi tới hệ thống được tạo ra hơn. Xét ví dụ đơn giản sau:

```c
#include <unistd.h>

#define BUFSIZE 1024

/* copy input to output */
int main(){
    char buf[BUFSIZE];
    int n;
    while((n=read(0,buf,BUFSIZE))>0)
        write(1,buf,n);
    return 0;
}
```

Chương trình trên đơn giản là đọc dữ liệu từ bạn phím, sau đó in dữ liệu đọc được ra màn hình. Nếu kích thước file không phải là bội của BUFSIZE, một vài lời gọi read sẽ trả về một số bytes nhỏ hơn và sẽ được ghi bởi write, lần gọi kế tiếp read sẽ trả về 0.

Bởi vì read()/write) đọc dữ liệu từ thiết bị ngoại vi hay ghi dữ liệu ra thiết bị đều không qua bộ đệm dữ liệu nên chúng là **unbuffered**.

## Các hàm đọc/ghi file trong thư viện stdio.h

Các hàm đọc/ghi file trong stdio.h ở một mức trừu tượng cao hơn so với các lời gọi hệ thống read()/write()/ Và cấc thao tác đoc/ghi trong stdio.h được thực hiện thông qua một bộ đệm.

Buffer hay bộ đệm alf một vùng nhớ tạm.

Trong stdio.h có một cấu trúc dữ liệu là FILE được định nghĩa như sau (trích ~~*The C Programming Language*~~):

```c
typedef struct _iobuf{
    int cnt;    /* character left*/
    char* ptr;  /* next character position*/
    char* base; /*location of buffer*/
    int flag;   /*mode of file access*/
    int fd;     /*file descriptor*/
} FILE;
```

Tại sao mình lại trích khái niệm FILE lên đây? Phần trước bạn đã biết mọi thao tác đoc/ghi file dùng các lời gọi hệ thống read()/write() đều thông qua file descriptor, nhưng với thao tác đọc/ghi file trong *stdio.h* thì thực hiện thông qua con trỏ FILE. Nói chính xác hơn thì nó vẫn thao tác với file descriptor nhưng ở mức trường tượng cao hơn là *FILE* (đã mô tả ở định nghĩa trên). Bạn có thể lấy file descriptor của một *FILE* * bằng hàm:

```c
int fileno(FILE*);
```

Bài này mình chỉ xét hàm fwrite(), các hàm đọc/ghi khác trong *stdio.h* khá tương tự. fwrite() có prototype là:

```c
size_t fwrite(const void* ptr, size_t size, size_t nobj, FILE* stream);
```

Hàm này ghi **nobj** đối tượng, mỗi đối tượng có kích thước **size** bytes từ mảng được trỏ bởi **ptr** vào postition trong **stream**. Trả về số đối tượng ghi được nếu thành công và một số khác **nobj** nếu không thành công đồng thời set biến hệ thống **errno**. Nếu **size** hoặc **nobj** bằng 0 thì hàm sẽ trả về 0.

Điểm khác biệt nữa là fwrite() ghi dữ liệu từ ptr vào một buffer, khi buffer đầy mới flush dữ liệu lên stream. Trong struct FILE thì buffer là vùng nhớ được trỏ bởi **base**. Tương tự với quá trình ghi, dữ liệu sẽ được đọc vào buffer rồi mới được lưu vào biến.

Khi bạn mở file bằng [fopen()](http://www.cplusplus.com/reference/cstdio/fopen/), một buffer sẽ được tạo ra cho *FILE* stream được mở bởi hàm:

```c
int setvbuf(FILE* stream, char* buf, int mode, size_t size);
```

Hàm này điều khiển bộ đệm của stream, luôn được gọi trước các thao tác đoc/ghi file. **mode** có các giá trị *_IOFBF* nếu full buffering hoặc *_IOFBF* nếu buffering dòng cho các text files, hoặc *_IONBF* nếu không dùng buffer. Nếu **buf** không phải là *NULL* thì nó được dùng như buffer. **size** xác định kích thước của bộ đệm.

## Lợi ích của đọc/ghi file thông qua buffer

Việc dùng bộ đệm với các thao tác đọc/ghi sẽ làm tăng tốc độ. Tuy nhiên việc dùng bộ đệm sẽ gây ra các side effect, chẳng hạn như khi ghi dữ liệu ra file thì dữ liệu vẫn nằm trên bộ đệm cho tới khi đầy mới được đưa ra, trong thời điểm này nếu có các thao tác đọc vào thì dữ liệu sẽ được đưa vào input. Dẫn tới kết quả sai lêch, etc.

Bài viết này kết thúc ở đây!
