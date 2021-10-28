title: Cài đặt github copilot trên neovim
date: 28-10-2021
tags: neovim, github
name: neovim-copilot
summary: Tìm hiểu copilot trên Neovim
--------------------------------

# Github Copilot?

Nếu thường xuyên code hẳn bạn đã từng nghe tới các extensions hỗ trợ viết code nhanh, chạy bằng AI như `Tabnine` hay `Kites`. Tốc độ code sẽ nhanh hơn đáng kể, nhưng bù lại tài nguyên máy sẽ hao hơn.
Mình đã từng cài cả 2 song lại gỡ cả 2 vì máy mình quá yếu, sài một lát là quạt thổi vù vù :(
Và rồi, gần đây mình nghe tới việc Github tung ra một con trợ lý AI cho việc gõ code, mình rất hào hứng và hy vọng về 1 plugins hỗ trợ viết code nhanh, ít hao tài nguyên.
Kết quả là...ngoài sức tưởng tượng ^^

Thông tin đầy đủ bạn có thể tìm hiểu tại [copilot](https://copilot.github.com/).
Hiện tại chỉ có `Visual Studio Code`, `JetBrains`, và tất nhiên là `Neovim` hỗ trợ extension này.
Vì vẫn đang trong giai đoạn technical preview nên để sử dụng bạn phải đăng ký và sau khoảng 2 tuần `Github` sẽ gửi mail hướng dẫn cài đặt cho từng editors cụ thể.

Sơ qua thì `Github copilot` là "một đôi bạn cùng tiến" trong việc lập trình với bạn.
Nó dựa trên nền tảng `OpenAI Codex` được cung cấp bởi `OpenAI` để train models lấy từ các source codes public trên internet (gồm cả github), từ đó sẽ đưa ra gợi ý phù hợp
giúp bạn code nhanh hơn, gõ ít hơn.

`OpenAI Codex` là một model đa mục đích, hậu duệ của `GPT-3`, nó trains các data gồm cả ngôn ngữ tự nhiên và cả hàng tỉ dòng code được public trên Github.
Nhưng hiện tại model này chỉ hỗ trợ tiếng Anh và các ngôn ngữ phổ biến như `Python`, `Javascript`, `Go`, `Perl`, `PHP`, `Ruby`, `Swift`, `Typescript` và `Shell`.
Theo như giới thiệu thì nó chỉ tốn 14KB bộ nhớ cho Python code, dù sử dụng nhiều bộ nhớ hơn nhưng nó nhanh hơn gấp 3 lần và hỗ trợ nhiều ngôn ngữ tự nhiên hơn so với GPT-3.

Bạn có thể tìm hiểu nhiều hơn về OpenAI Codex [tại đây](https://openai.com/blog/openai-codex/). 


# Cơ chế hoạt động của Copilot?

Đây là hình thể hiện cơ chế hoạt động của `Copilot`:

<img src="https://copilot.github.com/diagram.png" alt="copilot mechanism" width=80% height=auto/><br>


Vì copilot trains các models trên internet và cung cấp các đoạn code gợi ý thông qua các services dưới dạng các API,
nên tài nguyên máy tiêu hao hầu như không có gì nhiều.
So với `Kites` hay `Tabnine`, ngoài việc models được cài đặt local trên máy (tốn dung lượng ổ cứng),
mỗi lần code máy nóng, quạt kêu (ngốn CPU, RAM) làm mình đau xót đến trào nước mắt thì Copilot với mình như một vị cứu tinh vậy.

Nó là một trình tổng hợp mã và đưa ra những gợi ý
code phù hợp với bạn nhất chứ không phải đơn thuần là một search engine, nên sẽ giảm số lần bạn phải tra google,
chỉ cần 1 vài dòng comments, codes. Copilot sẽ **gửi lại cho bạn gợi ý** những dòng code tiếp theo.
**Bạn phải là người quyết định những dòng code nào phù hợp trong context của mình**.


# Cài đặt Copilot.

Sau 2 tuần chờ đợi, Github sẽ gửi cho bạn một mail dẫn tới [trang cài đặt](https://github.com/github/copilot-docs).

Để cài đặt extension này, bạn cần chọn editor tương ứng với 3 loại trên, nếu dùng `Visual Studio Code` hay `JetBrains` bạn chỉ cần cài vào là sử dụng được thì với `Neovim` sẽ hơi mất công một chút.

Với `Neovim`, contributor nổi tiếng trong giới là **tpope** đã viết hẳn 1 plugin cho `Neovim`, để cài đặt bạn copy và paste command sau vào terminal:

```bash
git clone https://github.com/github/copilot.vim.git \
  ~/.config/nvim/pack/github/start/copilot.vim
```

Command này sẽ clone repo về thư mục `~/.config/nvim/pack/`.

Tuy nhiên mình không thích cài trong folder `~/.config/nvim/pack/`,
mình sẽ sử dụng trình quản lý gói `packer` bằng cách thêm `use({'github/copilot.vim'})` vào file `~/.config/nvim/lua/plugins.lua`.
Sau đó restart `Neovim` và chạy command `:PackerInstall` để cài đặt.

Sau khi cài đặt xong, bạn restart lại `Neovim` và paste command này vào để config: `:Copilot setup`.

Và bắt đầu test thôi...


<iframe title="vimeo-player" src="https://player.vimeo.com/video/639997594?h=560476b35c" width="640" height="400" frameborder="0" allowfullscreen></iframe>


It works :D

* Lưu ý 1: ở đây giả sử bạn đã cài `Node` và đang dùng `Neovim` bản prerelease.


* Lưu ý 2: Vì `copilot` sẽ dùng `<Tab>` để complete code, nên bạn cần phải sửa lại keymap của `nvim-cmp` trong file `~/.config/nvim/lua/ext/cmp.lua` một chút để tránh xung đột.
Thay vì dùng `<Tab>`, ta sẽ đổi thành `<S-j>` và `<S-k>` để `select_next_item()` và `select_prev_item()`.


# Đánh giá Github Copilot.

Qua các thống kê về mức độ hiệu quả của người bạn *Github Copilot* của chúng ta, những gợi ý sẽ phù hợp với code context của bạn là 43% cho lần thử đầu tiên, nhưng sau 10 lần thử kế tiếp,
hiệu năng sẽ tăng lên 57%, quá tuyệt phải không nào?

Và vì người anh em này chỉ đang trong giai đoạn technical preview, chưa release chính thức,
nên hi vọng trong tương lai gần mức độ chính xác sẽ tăng lên cao hơn nữa và
hỗ trợ thêm nhiều ngôn ngữ lập trình cũng như ngôn ngữ tự nhiên (có cả tiếng Việt)
cho giới lập trình chúng mình.

Dù trang chủ của `OpenAI Codex` nói hiện tại chỉ hỗ trợ 1 vài ngôn ngữ lập trình phổ biến nhưng mình đã test thử với `Rust` và nó vẫn hoạt động ổn.

Theo mình, sau khi cài đặt xong, chúng ta nên sử dụng Copilot mỗi ngày, nếu có trục trặc gì thì có thể gửi feedback lại. Rất đáng để thử đấy.

Cuối cùng, Github Copilot giảm đáng kể việc code của bạn chứ không phải tự code thay bạn đâu nên là sẽ còn lâu nữa mình mới lo mất việc về tay AI nhé :D.


Cảm ơn bạn đã đọc bài. Mình sẽ kết ở đây.

