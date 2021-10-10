import pytest
from app import create_posts, render_home, render_posts, render_tags
from jinja2 import Environment, FileSystemLoader
import pathlib
from datetime import datetime
import tempfile
import os


# @pytest.fixture
def test_write_md_content():
    path = tempfile.mkdtemp()
    prototypes_path = pathlib.Path(path).joinpath("prototypes").resolve()
    prototypes_path.mkdir(mode=511, parents=True, exist_ok=True)
    test_md = prototypes_path.joinpath("test.md").resolve()
    # test = (
    #     pathlib.Path(__file__)
    #     .parent.joinpath("tests/prototypes/test.md")
    #     .resolve()
    # )
    with open(test_md, "w") as f:
        f.write("title: test\n")
        f.write("date: " + f"{datetime.today().strftime('%d-%m-%Y')}\n")
        f.write("tags: test\n")
        f.write("name: test\n")
        f.write("summary: test\n")
        f.write("-------------\n")
        f.write("\n")
        f.write("#test header\n")
        f.write("test content")

    return prototypes_path


def test_create_posts():
    # root = pathlib.Path(__file__).parent.joinpath("tests").resolve()
    path = test_write_md_content()
    # path.parent.parent.resolve()
    test_metadata = [
        {
            "title": "test",
            "date": f"{datetime.today().strftime('%d-%m-%Y')}",
            "tags": ["test"],
            "name": "test",
            "summary": "test",
        }
    ]
    test_post = {"test.md": "<h1>test header</h1>\n\n<p>test content</p>\n"}
    test_tags = {"test"}

    posts, metadata, tags = create_posts(path.parent.resolve())

    assert posts == test_post
    assert metadata == test_metadata
    assert tags == test_tags


def test_render_home():
    path = test_write_md_content()
    # mk tests folder

    _, metadata, tags = create_posts(path.parent.resolve())
    env = Environment(loader=FileSystemLoader(searchpath="./templates"))
    home_template = env.get_template("home.html")

    render_home(metadata, path.parent.resolve(), tags, home_template)

    # test_index_content
    with open(path.parent.joinpath("index.html"), "r") as f:
        index_content = f.read()

    test_index_content = f"""<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n  <link rel="stylesheet" href="../static/main.css">\n  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU" crossorigin="anonymous">\n  <title>Phuoc\'s blog</title>\n</head>\n<body>\n  <br>\n  <div class="container">\n    <div class="row">\n      <div class="col-sm-2">\n        <h1 class="home-page"><a style="text-decoration: none; color: orangered" href="../index.html">Trang chủ</a></h1>\n      </div>\n      <div class="col-sm-10">\n        \n<h1>Tất cả các bài viết</h1><br>\n\n\n  <p>\n  <div class="home-summ">\n    <small class="home-meta">{datetime.today().strftime('%d-%m-%Y')}</small>\n    <br>\n    <small class="home-meta right">\n      tags: \n       \n        <a href="tags/test.html" style="text-decoration: none; color: orchid;">test</a>,\n      \n    </small>\n  </div>\n    <h2>\n      <a href="../posts/test.html" style="text-decoration: none; color: orangered">\n        test\n      </a>\n    </h2>\n    <small>\n      test\n    </small>\n  </p>\n\n\n      </div>\n    </div>\n  </div>\n  <br>\n  <div class="footer">\n    <div class="container">\n      \n      <div class="row">\n        <div class="col-sm-4"></div>\n        <div class="col-sm-4 author">\n          <span class="text-muted">Powered by\n            <a style="text-decoration: none; color: orangered" href="https://github.com/tranvietphuoc">Trần Việt Phước</a>\n          </span>\n        </div>\n        <div class="col-sm-4"></div>\n      </div>\n    </div>\n  </div>\n  \n  <script src="../static//script.js" type="text/javascript">\n  </script>\n</body>\n\n</html>"""

    # check file index.html is exists
    assert path.parent.joinpath("index.html").exists() == True
    assert test_index_content == index_content


def test_render_posts():
    path = test_write_md_content()

    # create posts folder in temp folder
    path.parent.joinpath("posts").mkdir(mode=511, parents=True, exist_ok=True)

    posts, _, tags = create_posts(root_path=path.parent.resolve())
    env = Environment(loader=FileSystemLoader(searchpath="./templates"))
    post_html = env.get_template("post.html")

    render_posts(
        posts, tags, path.parent.joinpath("posts").resolve(), post_html
    )

    with open(path.parent.joinpath("posts/test.html"), "r") as f:
        post_content = f.read()

    test_post_content = f"""<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n  <link rel="stylesheet" href="../static/main.css">\n  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU" crossorigin="anonymous">\n  <title>Phuoc\'s blog</title>\n</head>\n<body>\n  <br>\n  <div class="container">\n    <div class="row">\n      <div class="col-sm-2">\n        <h1 class="home-page"><a style="text-decoration: none; color: orangered" href="../index.html">Trang chủ</a></h1>\n      </div>\n      <div class="col-sm-10">\n        \n<div class="row">\n  <h1><span style="color:lightgrey"># </span>\n    test\n  </h1>\n</div>\n<br>\n\n<div class="row">\n  <div style="display: flex; flex-direction: column;">\n      <small class=\'post-meta\'>Ngày: {datetime.today().strftime('%d-%m-%Y')}</small>\n      <small class="post-meta">Tags: \n        \n          <a href="../tags/test.html" style="text-decoration: none; color: orangered; background-color: lightgray">test</a>,\n        \n      </small>\n    </div>\n</div>\n<br>\n\n<p class="post-content">\n  <h1>test header</h1>\n\n<p>test content</p>\n\n</p>\n\n\n      </div>\n    </div>\n  </div>\n  <br>\n  <div class="footer">\n    <div class="container">\n      \n      <div class="row">\n        <div class="col-sm-4"></div>\n        <div class="col-sm-4 author">\n          <span class="text-muted">Powered by\n            <a style="text-decoration: none; color: orangered" href="https://github.com/tranvietphuoc">Trần Việt Phước</a>\n          </span>\n        </div>\n        <div class="col-sm-4"></div>\n      </div>\n    </div>\n  </div>\n  \n  <script src="https://utteranc.es/client.js"\n        repo="tranvietphuoc/tranvietphuoc.github.io"\n        issue-term="url"\n        label="Comment"\n        theme="github-light"\n        crossorigin="anonymous"\n        async>\n  </script>\n\n  <script src="../static//script.js" type="text/javascript">\n  </script>\n</body>\n\n</html>"""

    assert path.parent.joinpath("posts/test.html").exists() == True
    assert test_post_content == post_content


def test_render_tags():
    path = test_write_md_content()
    _, metadata, tags = create_posts(root_path=path.parent.resolve())

    # create tags folder in temp folder
    path.parent.joinpath("tags").mkdir(mode=511, parents=True, exist_ok=True)
    env = Environment(loader=FileSystemLoader(searchpath="./templates"))
    tag_html = env.get_template("tags.html")

    render_tags(
        metadata, tags, path.parent.joinpath("tags").resolve(), tag_html
    )

    with open(path.parent.joinpath("tags/test.html"), "r") as f:
        tag_content = f.read()

    test_tag_content = f"""<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n  <link rel="stylesheet" href="../static/main.css">\n  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU" crossorigin="anonymous">\n  <title>Phuoc\'s blog</title>\n</head>\n<body>\n  <br>\n  <div class="container">\n    <div class="row">\n      <div class="col-sm-2">\n        <h1 class="home-page"><a style="text-decoration: none; color: orangered" href="../index.html">Trang chủ</a></h1>\n      </div>\n      <div class="col-sm-10">\n        \n<h1>Các bài viết trong tag: <span style="color: lightgray;">TEST</span></h1>\n<br>\n\n\n  <p>\n  <div class="home-summ">\n    <small class="home-meta">{datetime.today().strftime('%d-%m-%Y')}</small>\n    <br>\n    <small class="home-meta right">tags: \n      \n      <a href="../tags/test.html" style="text-decoration: none; color: orchid;">\n        test\n      </a>,\n      \n    </small>\n  </div>\n    <h3>\n      <a href="../posts/test.html" style="text-decoration: none; color: orangered">\n        test\n      </a>\n    </h3>\n    <small>\n      test\n    </small>\n  </p>\n\n\n\n      </div>\n    </div>\n  </div>\n  <br>\n  <div class="footer">\n    <div class="container">\n      \n      <div class="row">\n        <div class="col-sm-4"></div>\n        <div class="col-sm-4 author">\n          <span class="text-muted">Powered by\n            <a style="text-decoration: none; color: orangered" href="https://github.com/tranvietphuoc">Trần Việt Phước</a>\n          </span>\n        </div>\n        <div class="col-sm-4"></div>\n      </div>\n    </div>\n  </div>\n  \n  <script src="../static//script.js" type="text/javascript">\n  </script>\n</body>\n\n</html>"""
    assert path.parent.joinpath("tags/test.html").exists() == True
    assert test_tag_content == tag_content


def test_close_temp_folder():
    path = test_write_md_content()

    for p in path.parent.iterdir():
        try:
            p.unlink()
        except PermissionError:
            # p.joinpath("test.md").unlink()
            break
