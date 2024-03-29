title: Bit field in C
date: 27-09-2021
tags: c, struct, bitfield
name: bitfield-c
summary: Bitfield? Nó là gì?

---

# 1. Bit field là gì?

Trong lập trình C hay C++, bạn sẽ gặp một struct có dạng như thế này:

```c
struct Example{
    //.......
    type value: number;
    //.......
};
```

Trong đó:

-   **type** là tên kiểu dữ liệu (có thể là built-in types hay struct, class).
-   **value** là tên biến thành viên.
-   **number** là một số nguyên dương, biểu thị số bit mà **value** dùng trong dãy giá trị của **type**.

Ví dụ, xét struct:

```c
struct foo{
    int a: 2;
};
```

Ở đây, **type** là _int_ (giả sử _int_ được biểu diễn bởi 4 bytes, tức 32 bit), có dãy giá trị từ `-2^31 -- 2^31-1`. Tuy nhiên, **_int a: 2;_** nghĩa là chỉ cần dùng 2 bit trong số 32 bit đó, và dãy giá trị của **a** sẽ từ -2 đến 1 (tức 2^2 giá trị).

**Vậy**, bit field là một khai báo các thành viên của struct với độ rộng rõ ràng theo các bit. Nhưng <u>độ rộng phải nhỏ hơn số bit tối đa đễ biểu diễn kiểu dữ liệu</u>

Công dụng của bit field là tiết kiệm không gian nhớ. Việc này rất hữu dụng khi bạn lập trình cho các hệ thống có ít tài nguyên như hệ thống nhúng.

**Lưu ý** các kiểu dữ liệu dùng trong bit field chỉ thuộc một trong 4 kiểu sau:

-   _unsigned int_ -- Ví dụ: `unsigned int a: 3; //a có giá trị từ 0..7`
-   _signed int_ -- Ví dụ: `signed int a: 3; //a có giá trị từ -4..3`
-   _int_ -- Ví dụ: `int a: 3; //a có giá trị từ -4..3 hoặc từ 0..7`
-   _\_Bool_ (C99) -- Ví dụ: `bool a: 1; //a có giá trị 0..1`

Mở rộng ra, type của các bit field là các kiểu nguyên như _int_, _long_, _short_, _char_, _long long_ có thể kèm theo **signed** hoặc **unsigned**. ~~Đặc biệt là không phải kiểu dấu chấm động như _float_, _double_~~

# 2. Một số ví dụ

Giả gử bạn cho các bit field giá trị vượt quá giá trị tối đa mà bit field có thể lưu trữ thì thế nào? Xét ví dụ:

```c
#include <stdio.h>

struct S{
    unsigned int a: 2; //dãy giá trị từ 0..4
};

int main(){
    S s;
    s.a=4; //gán member a giá trị tối đa có thể chứa
    ++s.a; //tăng member a lên 1
    printf("%d\n",s.a); //in ra 0 -- tương tự như khi bị overflow dữ liệu
    return 0;
}
```

**Vậy**, kích thước của một bit field là bao nhiêu? Xét ví dụ:

```c
#include <stdio.h>

struct S{
    /*cộng tổng số bit mà a,b, chiếm, sau đó so sánh với 8 bit, nếu nhỏ hơn 8 bit thì tính luôn là 1 byte*/
    unsigned char a: 2; //2 bit
    unsigned char b: 1; //1 bit
    // tổng số bit là 3<8 --> sizeof là 1
};

int main(){
    printf("%d\n",sizeof(S)); //in ra 1
    return 0;
}
```

**Kết luận**: Đối với bit field chỉ dùng 1 kiểu dữ liệu, nếu tổng số bit trong bit field nhỏ hơn số bít tối đa để biểu diễn kiểu dữ liệu thì kích thước của bit field là kích thước của kiểu dữ liệu đó, trong ví dụ trên, kiểu _unsigned char_ có kích thước là 1 byte được biểu diễn bởi 8 bit

Còn nếu tổng số bít là lớn hơn số bít tối đa biểu diễn kiểu dữ liệu, xét hai trường hợp:

-   Nếu tổng số bit chia hết cho số bit biểu diễn kiểu dữ liệu thì kích thước của bit field là thương của tổng số bit của member với số bit biểu diễn kiểu dữ liệu đó nhân với kích thước của kiểu dữ liệu.

-   Nếu tổng số bit không chia hết cho số bit của kiểu dữ liệu thì kích thước của bit field là thương của phép chia nguyên giữa tổng số bit member với số bit của kiểu dữ liệu cộng 1 rồi nhân với kích thước của kiểu dữ liệu đó.

Xem ví dụ sau:

```cpp
//giả sử sizeof(unsigned int) là 4
#include <iostream>

struct S{
    unsigned int a: 30;
    unsigned int b: 7;
};

int main(){
    std::cout<<sizeof(S)<<std::endl; //in ra 8 vì 30+7=37>32
    return 0;
}
```

Vậy kích thước bit field sẽ là bao nhiêu nếu nó dùng nhiều kiểu dữ liệu khác nhau? Xét ví du:

```c
#include <stdio.h>

//giả sử unsigned int có sizeof là 4 bytes
struct S{
    unsigned char a: 4; //dùng 4 bit trong 8 bit
    unsigned int b: 30; //dùng 30 trong 32 bit
};

int main(){
    printf("%d\n",sizeof(struct S); in ra 8
    return 0;
}
```

Vì sao lại là 8 bytes? Nguyên tắc cũng giống [data alignment](https://ptv14.github.io/sizeof-struct-and-data-alignment/) Đầu tiên, compiler sẽ tìm ra member có kích thước lớn nhất (ví dụ trên là _unsigned int_) sau đó sẽ xác định số bit tối đa để biểu diễn kiểu dữ liệu của member đó ( ví dụ trên là 32 bit). Và việc so sánh chỉ thực hiện với số này thôi, việc cấp phát, tổ chức bộ nhớ thì y chang như phần **data alignment**. Tổng số bit của các members là 34>32, do đó kết quả sẽ là 8.

Nhiều bit field liền kề được phép đóng gói (packed) cùng nhau, ví du:

```cpp
#include <iostream>

struct S{
    //unsigned được hiểu là unsigned int, giả sử sizeof là 4 bytes
    //compiler cấp 1 block 4 byte (32 bit) rồi điền các bit field vào
    //5 bit biểu diễn giá trị của b1;
    //11 bit: padding, không sử dụng;
    //6 bit biểu diễn  giá trị của b2;
    // 2 bit biểu diễn giá trị của b3;
    //8 bit thừa, không sử dụng
    unsigned b1: 5, : 11, b2: 6, b3: 2;
};

int main(){
    std::cout<<sizeof(S)<<std::endl; //in ra 4
    return 0;
}
```

Ở ví dụ này có một bit field không tên (tức là không có tên trước dấu **:**) chiếm 11 bit, tổng số bit là 24 bit < 32 nên kích thước là 4 byte.

Với các bit field không tên mà khai báo giá trị 0 sau dấu **:** thì compiler sẽ padding vùng nhớ còn lại của block và cấp block mới để đẩy vào các bit field tiếp theo. Ví dụ:

```c
#include <stdio.h>

struct S{
    //giả sử *unsigned* chiến 4 bytes -- 32 bit
    unsigned b1: 5; // 5 bit biểu diễn b1
    unsigned : 0; // padding 27 bit còn lại của block, cấp block mới
    unsigned b2: 6; // điền tiếp 6 bit để biểu diễn b2 vào block mới
    unsigned b3: 15; //điền 15 bit của b3 vào
    //dư 11 bit chưa dùng
};

int main(){
    printf("%d\n",sizeof(struct S)); //in 8
    return 0;
}
```

Trên đây là một số sơ lược về bit field, bài viết mình kết thúc ở đây!
