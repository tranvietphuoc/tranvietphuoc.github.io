title: Cài đặt github copilot trên neovim
date: 28-10-2021
tags: neovim, github
name: neovim-copilot
--------------------------------

# Github Copilot?

Nếu thường xuyên code hẳn bạn đã từng nghe tới các extensions hỗ trợ viết code nhanh, chạy bằng AI như `Tabnine` hay `Kites`. Tốc độ code sẽ nhanh hơn đáng kể, nhưng bù lại tài nguyên máy sẽ hao hơn.
Mình đã từng cài cả 2 song lại gỡ cả 2 vì máy mình quá yếu, sài một lát là quạt thổi vù vù :(
Và rồi, gần đây mình nghe tới việc Github tung ra một con trợ lý AI cho việc gõ code, mình rất hào hứng và hy vọng về 1 plugins hỗ trợ viết code nhanh, ít hao tài nguyên.
Kết quả là...ngoài sức tưởng tượng ^^

Thông tin đầy đủ bạn có thể tìm hiểu tại [copilot](https://copilot.github.com/).
Hiện tại chỉ có `Visual Studio Code`, `JetBrains`, và tất nhiên là `Neovim` hỗ trợ extension này.
Vì vẫn đang trong giai đoạn technical preview nên để sử dụng bạn phải đăng ký và sau khoảng 1 tuần `Github` sẽ gửi mail hướng dẫn cài đặt cho từng editors cụ thể.

Sơ qua thì `Github copilot` là "một đôi bạn cùng tiến" trong việc lập trình với bạn.
Nó dựa trên nền tảng `OpenAI Codex` được cung cấp bởi `OpenAI` để train models lấy từ các source codes public trên internet (gồm cả github), từ đó sẽ đưa ra gợi ý phù hợp
giúp bạn code nhanh hơn, gõ ít hơn.


# Cơ chế hoạt động của Copilot?

Đây là hình thể hiện cơ chế hoạt động của `Copilot`:

<img src="https://copilot.github.com/diagram.png" alt="copilot mechanism" width=80% height=auto/><br>


Vì copilot trains các models trên internet và cung cấp các đoạn code gợi ý thông qua các services nên tài nguyên máy tiêu hao hầu như không có gì nhiều.
So với `Kites` hay `Tabnine`, ngoài việc models được cài đặt local trên máy (tốn dung lượng ổ cứng), mỗi lần code máy nóng, quạt kêu (ngốn CPU, RAM) đau xót đến trào nước mắt thì Copilot quá tuyệt vời phải không nào?


# Cài đặt Copilot.

Để cài đặt extension này, bạn cần chọn editor tương ứng với 3 loại trên, nếu dùng `Visual Studio Code` hay `JetBrains` bạn chỉ cần cài vào là sử dụng được thì với `Neovim` sẽ hơi mất công một chút.

Contributor nổi tiếng trong giới `Vim` là **tpope** đã viết hẳn 1 plugin cho `Neovim`, để cài đặt bạn copy và paste command sau vào terminal:

```bash
git clone https://github.com/github/copilot.vim.git \
  ~/.config/nvim/pack/github/start/copilot.vim
```

* Lưu ý 1: ở đây giả sử bạn đã cài `Node` và đang dùng `Neovim` bản prerelease.

Sau khi cài đặt xong, bạn mở `neovim` và paste command này vào để config: `:Copilot setup`.

Và bắt đầu test thôi nào...


<iframe title="vimeo-player" src="https://player.vimeo.com/video/639997594?h=560476b35c" width="640" height="400" frameborder="0" allowfullscreen></iframe>


It works :D

* Lưu ý 2: Vì `copilot` sẽ dùng `<Tab>` để complete code, nên bạn cần phải sửa lại keymap của `nvim-cmp` trong file `~/.config/nvim/lua/ext/cmp.lua` một chút để tránh xung đột.
Thay vì dùng `<Tab>`, ta sẽ đổi thành `<S-j>` và `<S-k>` để `select_next_item()` và `select_prev_item()`.

Cảm ơn bạn đã đọc bài. Mình sẽ kết ở đây.

