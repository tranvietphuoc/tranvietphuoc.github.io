Trong C/C++, bạn có thể viết một biểu thức tối giản hết mức có thể, chẳng hạn:

```c
int a=4;
int b=0;
a++;
b+=a;
printf("%d %d\n",a,b);
```

Ở đây biểu thức `a++` và `b+=a` tương đương `a=a+1` và `b=b+a`. Đây là điểm mạnh của C/C++, tuy nhiên cũng là điểm yếu vì đôi lúc ta thật sự thấy bối rối về kết quả của nó.

Độ ưu tiên của các toán tử (operator precedence) là một trong những thứ làm ta khá rối khi mới tiếp xúc lập trình.

Bài này mình sẽ bàn về những hành vi không xác định (*undefined behavior*) với một số toán tử trong C/C++.

Thử ví dụ sau, bạn có đoán được kết quả in ra là gì?

```c
int a=1;
printf("%d %d %d\n",++a,a,a++);
```

Có thể bạn sẽ nhẩm kết quả, và khẳng định nó đúng. Vậy thử xét trường hợp sau:

```c
int a=1,b=0;
b=++a + a + a-- + --a + a++;
printf("%d %d\n",a,b);
```

Bắt đầu rối phải không nào? :smile: Thật ra thì bản chất nó là rối như vậy. Nếu bạn thử test trên nhiều compiler, các kết quả thu được sẽ khác nhau, tất cả các kết quả đó đều vô nghĩa, vì chúng là *undefined behavior*, giá trị tính được sẽ tùy thuộc vào cách compiler quy định. Nguyên nhân là các biểu thức trên thay đổi giá trị của một biến quá nhiều lần mà không phân biệt thứ tự trước -  sau (++a trước hay a++ trước? --a trước hay a-- trước?).

Điều này vi phạm một số quy định quan trọng trong trình tự thực thi (*execution sequence*) gọi là [sequence point](https://en.wikipedia.org/wiki/Sequence_point), tất cả các *side-effect* của các tính toán trước đó được đảm bảo là hoàn thành, không ảnh hưởng tới các tính toán theo sau. Nếu các tính toán theo sau bị ảnh hưởng bởi các *side-effect* của các tính toán thực hiện trước thì kết quả là *undefined behavior*

Tuy nhiên xét đoạn code này:

```c
int a=1,b=0;
b=(++a)+(a++) -a
printf("%d %d\n",a,b);
```

Thì kết quả thu được thì lại hoàn toàn xác định, bởi biểu thức trên sử dụng ký pháp Ba Lan (Polish Notation), nên thứ tự tính toán hoàn toàn xác định, do đó, kết quả là duy nhất!

Bài viết này kết thúc ở đây!

