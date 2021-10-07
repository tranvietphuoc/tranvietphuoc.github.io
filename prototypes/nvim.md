title: Cá nhân hóa NeoVim
date: 05-10-2021
tags: nvim, editor
name: nvim-preconfig
summary: Mình đã cấu hình NeoVim như thế nào?
-------------------------------------------

# Why NeoVim?

Với giới lập trình viên thì đã không lạ gì về `Vim` editor. Nó là một editor mã nguồn mở, được [Bram Moolenaar](https://en.wikipedia.org/wiki/Vim_(text_editor)) cải tiến từ `Vi` editor trên Unix
Mình biết tới `Vim` từ 2019, sau một hồi lăn tăn chọn lựa giữa `VSCode` và `SublimeText` thì tham khảo trên [reddit](https://www.reddit.com/) mình lại chọn `NeoVim`.

Ủa, sao title là `NeoVim`, xong giới thiệu `Vim`, xong giờ lại về `NeoVim`, bùng binh dữ vậy cha? :D

Thật ra [NeoVim](https://github.com/neovim/neovim) là một `Vim-fork`, nó cũng giống [Vim](https://github.com/vim/vim) thôi, nhưng dễ dàng extensible hơn. Thật ra mình nghe thế chứ cũng chưa viết dc một cái plugin nào trên `NeoVim` cả.

Nói vậy cũng không có nghĩa là Vim ít plugins đâu nhé, cả 1 thế giới trong đó đấy. Bạn có thể làm hàng tá thứ với `VimL` hay còn gọi là `VimScript`.
[Repo này](https://github.com/akrawchyk/awesome-vim) có list 1 danh sách khá đầy đủ các plugins cho `Vim`. Nếu bạn install `Vim` bạn có thể tham khảo.

Còn bạn chọn `NeoVim` giống mình ^^ thì bạn có thể tham khảo [Repo](https://github.com/rockerBOO/awesome-neovim) này nhé!

À, bạn có thể học cách sử dụng `Vim` hay `NeoVim` bằng command `vimtutor` trên terminal nhé. Sau đó là học [VimScript](https://learnvimscriptthehardway.stevelosh.com/),
và [lua for neovim](https://github.com/nanotee/nvim-lua-guide). Ở đây mình không trình bày sâu phần này, hoặc có thể thì ở bài sau.

Dông dài đủ rồi, giờ vào phần chính nè.

# Install NeoVim.

Để dùng `neovim` với đầy đủ các chức năng, đầu tiên bạn phải cài đặt `luajit`, `python`, `nodejs`, `luarocks`.

Sau đó bạn có thể cài `neovim` thông qua các package managers như `apt`, `brew`,... Mình dùng mac nên sẽ dùng `brew` để cài đặt nhé.
```sh
brew install --HEAD luajit
brew install --HEAD neovim
```

Vậy là xong, bạn có thể gõ `nvim` để check.

# Config.

Rồi, giờ là thứ quan trọng nhất nè.

`Vim` cũng như `NeoVim` đều có 1 file để config các settings của mình cho từng môi trường development phù hợp. Với `Vim` thì nó được lưu trong file `.vimrc`
NeoVim thì tất các các config được lưu trong `~/.config/nvim/init.vim` hoặc `~/.config.nvim/init.lua`.

Mình chọn `lua` làm ngôn ngữ để cấu hình cho `nvim` ngoài vì nó dễ mở rộng, như đã chém gió ở trên, mà còn vì để...nhìn cho ngầu :)))

Nói vui thôi, thật ra `lua` là một ngôn ngữ scripting mạnh mẽ, gọn nhẹ và dễ dàng tích hợp vào các ứng dụng cũng như nền tảng khác nhau.
Nên nếu có thời gian thì cũng đáng để học ^^.

Bạn sẽ phải cần cài đặt các chương trình sau trên máy của mình:

* gcc/clang
* libuv
* treesitter
* universal ctags
* python
* pyenv
* gitui
* rust-analyzer
* lua-language-server
* gopls
* clangd
* stylua
* nodejs
* git
* vscode-lldb


Mình đã push sẵn các configs của mình trên [đây](https://github.com/tranvietphuoc/nvim). Bạn có thể cài đặt bằng 1 script `install.sh` hoặc clone project về rồi copy vào thư mục
`~/.config/nvim`. Sau đó mở `nvim` lên và chạy command:
```
:PackerInstall

```
để cài đặt các plugins.
[Packer](https://github.com/wbthomason/packer.nvim) là một trình quản lý plugins cho `nvim` được viết bằng `lua`.

Sau đó chạy comand: 
```
:LSPInstall <lsp>
```
để cài đặt các lsp servers.

Trong các configs trên. Mình sử dụng:
* [nvim-lspconfig](https://github.com/neovim/nvim-lspconfig) để làm LSP client.
* [nvim-lspinstall](https://github.com/kabouzeid/nvim-lspinstall) để cài đặt lsp servers.
* [nvim-dap](https://github.com/mfussenegger/nvim-dap) để làm debuger adapters
* [nvim-cmp](https://github.com/hrsh7th/nvim-cmp) để làm languages auto-completion.
* [toggle-term](https://github.com/akinsho/toggleterm.nvim) để bật/tắt terminal trong vim
* [fugitive](https://github.com/tpope/vim-fugitive) để tích hợp các `git` commands trong editor.
* [nvim-treesitter](https://github.com/nvim-treesitter/nvim-treesitter) để tích hợp `treesitter` vào `nvim` để có syntax highlighting.
* [formatters](https://github.com/mhartington/formatter.nvim) để format code.
* Và các plugins hữu ích khác.

**Các phím tắt mình cũng đã giới thiệu ở phần readme**

Tới đây, bạn có thể sử dụng `neovim` như 1 IDE chính hiệu rồi, nếu không thích cách config của mình, bạn có thể tùy biến theo ý mình.

Thật ra đã có nhiều IDE layer for neovim, nổi tiếng nhất là `LunarVim` và `NVChad`, nhưng với mình, tự config theo ý mình thì thích hơn.

Bài này mình kết ở đây nhé!

