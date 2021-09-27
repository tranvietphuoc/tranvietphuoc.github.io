# sizeof của struct

Có khi nào bạn thắc mắc dữ liệu của một struct trong C hay C++ được tổ chức như thế nào không? Vì sao kích thước một struct khi chạy một chương trình đôi khi lại không giống những gì ta đã tính ở ngoài? Bài viết này sẽ đề cập đến các vấn đề trên.

Trước hết, đối vớicác biến có kiểu dữ liệu built-in types thì chúng được tổ chức trên bộ nhớ ra sao? Xét ví dụ:

```c
#include <stdio.h>

int main(){
    int a=10;
    float a=3.14;
    printf("\nAddress of a: %p. Address of b: %p\n",&a,&b);
    return 0;
}
```

Khi biên dịch và chạy đoạn mã trên, kết quả in ra trên máy mình như sau:

<img src="http://i.imgur.com/R3FQ2qj.png">

Như vậy, địa chỉ của b nằm sau a 4 bytes, tức là b nằm kế sau a trên bộ nhớ. Tuy nhiên, kết quả này là ngẫu nhiên. Nói cách khác, a và b có thể nằm kề nhau trên bộ nhớ hoặc nằm rời rạc nhau tùy từng hệ thống. Và hiển nhiên kích thước của a, b cũng có thể tính được (bằng toán tử sizeof).

Giờ ta sẽ xét tới struct. Với chương trình nhỏ sau:

```c
#include <stdio.h>

struct S{
    int x;
    int y;
};

int main(){
    printf("Size of struct S: %d\n",sizeof(S));
    return 0;
}
```

Ở đây bạn có thể nhẩm ở ngoài là x có sizeof là 4, y cũng có sizeof là 4, vậy kích thước của struct S sẽ là 4+4=8. Và khi biên dịch, chạy chương trình trên kết quả cũng là 8.

Nhưng xét ví dụ sau:

```c
#include <stdio.h>

struct Student{
    char id; //1 byte
    int age; //4 bytes
    double gpa; //8 byte;
};

int main(){
    printf("The size of struct Student: %d\n",sizeof(struct Student)); //in ra 16
    return 0;
}
```

Tới đây bạn sẽ nhẩm được kích thước của Student là 1+4+8=13 bytes, nhưng khi chạy chuong trình thì kết quả lại là 16? Nguyên nhân của sự khác biệt này là cách tổ chức bộ nhớ với struct trong C hay struct và class trong C++ gọi là **Struct Alignment**.

Nguyên lý của *struct alignment* như sau:

Đầu tiên compiler sẽ tìm xem trong struct, thành viên nào có kích thước lớn nhất, sau đó cấp phát một block có kích thước tương ứng rồi điền các members vào theo thứ tự khai báo trong struct. Khi nào kết một block, compiler sẽ tiếp tục cấp block mới rồi điền vào, cho đến khi nào cấp hết bộ nhớ cho các thành viên trong struct.

Trở lại chương trình ví dụ trên, compiler sẽ xác định member **gpa** là thành viên có kích thước lớn nhất trong struct (8 bytes).

<img src="http://i.imgur.com/pTbdSaE.png">

Sau đó compiler sẽ đẩy 1 byte của member id vào block.

<img src="http://i.imgur.com/dQfK37L.png">

Lúc này còn 7 bytes trống trong block, compiler sẽ đẩy thành viên tiếp theo vào block, nếu thành viên có kích thước lớn hơn số byte trống còn lại, compiler sẽ cấp thêm block mới. Ở ví dụ trên compiler sẽ padding 3 bytes và đẩy 4 bytes của member age vào 7 bytes trống.

<img src="http://i.imgur.com/H6BpVnD.png">

Vậy là hết block đầu tiên, struct còn lại member gpa chưa cấp bộ nhớ, compiler lúc này sẽ cấp thêm block mới, rồi đẩy 8 bytes của member gpa vào block đó.

<img src="http://i.imgur.com/HHyK1Wa.png">

Xét ví dụ sau:

```c
struct foo{
    char p;        //1 byte
    struct foo1{
        char* ptr;  // 4 hoặc 8 bytes -- giả sử là 8 bytes(hệ thống 64 bit)
        short x;    //2 bytes
    } inner; 
    /*compiler sẽ xác định inner.ptr là member có kích thước lớn nhất, sau đó sẽ cấp 1 block bằng 8 bytes, đẩy 1 byte của member p vào block, padding 7 bytes. Vì 7 bytes không đủ để cấp cho member tiếp theo nên compiler sẽ cấp block mới rồi điền inner.ptr (8 bytes) vào, tiếp tục cấp thêm block mới rồi điền inner.x (2 bytes) vào. Lúc này đã cấp xong bộ nhớ cho các member, còn dư 6 bytes trống, padding 6 bytes này. Vậy kích thước của struct foo là 8+8+8=24 bytes*/
};
```

Xét ví dụ:

```c
#include <stdio.h>

struct foo{
};

int main(){
    printf("The size of struct foo is: %d\n",sizeof(struct foo)); // in 1
    return 0;
}
```

**Kết luận** : Vậy, với struct rông (không có member) thì compiler sẽ cấp cho struct đó 1 byte.

**Lưu ý** : *Địa chỉ của một struct sẽ là địa chỉ của member đầu tiên của struct*.

Ở các ví dụ sau, bạn hãy tính xem kích thước của các struct sau đây là bao nhiêu nhé!

```c
struct foo1{
    char* p;
    char c;
    int n;
};
```

```c
struct foo2{
    short x;
    double a;
    char p;
};
```

Trở lại các ví dụ trên, bạn có thắc mắc tại sao lại phải padding không?

# Data alignment

Như bạn đã biết, bộ nhớ máy tính là một dãy các ô nhớ liên tiếp nhau mỗi ô nhớ có kích thước 1 byte. Tuy nhiên khi chương trình chạy, các vi xử lý hiện nay sẽ không đọc từng ô nhớ một mà là một nhóm các ô nhớ là bội của 2, 4 hoặc 8 (tức là đọc 2, 4, hoặc 8 bytes liên tiếp). Mục đích của việc này là tăng hiệu suất đọc/ghi của hệ thống.

Việc lưu trữ các kiểu dữ liệu cơ bản trên C hay C++ trên các hệ thống x86 hay ARM không thường bắt đầu bằng các bytes địa chỉ tùy ý trong bộ nhớ. Ngoại trừ kiểu *char* là có thể được lưu trữ ở bất kì ô nhớ có địa chỉ nào, các kiểu dữ liệu khác đều có *alignment requirement* (yêu cầu liên kết dữ liệu) riêng. *short* được lưu ở ô nhớ nào có địa chỉ chẵn, *int* - 4 bytes hoặc *float* - 4 bytes được lưu ở ô nhớ nào có địa chỉ là bội số của 4, *long* - 8 bytes hoặc *double* - 8 bytes được lưu ở ô nhớ có địa chỉ là bội của 8. Nguyên tắc trên được áp dụng cho kiểu dữ liệu có dấu (*signed*) hoặc không dấu (*unsigned*).

Ta gọi các kiểu dữ liệu cơ bản trong C trên hệ thống x86 hay ARM là **self-alignment** . Các con trỏ cũng là **self-alignment** (về cơ bản, con trỏ cũng được xem là kiểu dữ liêu).

Tới đây có lẽ bạn đã hiểu vì sao phải padding ở các ví dụ ở phần trên rồi. Tác dụng của nó là truy cập bộ nhớ nhanh hơn vì nó tạo điều kiện sinh ra việc nạp (fetch) và đặt các chỉ thị đơn (single-instruction) của kiểu dữ liệu. Nếu không có hạn chế của alignment, code có thể kết thúc việc phải truy cập 2 hay nhiều từ máy (machine word).

Một số vi xử lý cũ bắt buộc chương trình C của bạn vi phạm các nguyên tắc alignment (chẳng hạn việc ép kiểu địa chỉ lẻ sang một con trỏ *int* và cố sử dụng nó). Việc này không chỉ làm code thực thi thậm lại mà còn gây các chỉ thị sai.

**Lưu ý** một từ máy có kích thước tùy thuộc vào hệ thông của bạn:

* Hệ thống 16 bit: 1 word = 2 bytes (16 bit)
* Hệ thống 32 bit: 1 word = 4 bytes (32 bit)
* Hệ thống 64 bit: 1 word = 8 bytes (64 bit)

**Kết luận**: ~~Mục đích của việc padding dữ liệu là để các khối dữ liệu luôn rơi vào vị trí các bytes địa chỉ chẵn nhằm tăng tốc độ đọc của CPU với bộ nhớ~~.



