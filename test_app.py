from re import search
import pytest
from app import create_posts, render_home, render_posts, render_tags
from jinja2 import Environment, FileSystemLoader
import pathlib
from datetime import datetime


# @pytest.fixture
def write_test_content():
    test = (
        pathlib.Path(__file__)
        .parent.joinpath("tests/prototypes/test.md")
        .resolve()
    )
    with open(test, "w+") as f:
        f.write("title: test\n")
        f.write("date: " + f"{datetime.today().strftime('%d-%m-%Y')}\n")
        f.write("tags: test\n")
        f.write("name: test\n")
        f.write("summary: test\n")
        f.write("-------------\n")
        f.write("\n")
        f.write("#test header\n")
        f.write("test content")


# @pytest.fixture
def test_create_posts():
    root = pathlib.Path(__file__).parent.joinpath("tests").resolve()
    write_test_content()
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

    posts, metadata, tags = create_posts(root)
    print(posts)

    assert posts == test_post
    assert metadata == test_metadata
    assert tags == test_tags


def test_render_home():
    root = pathlib.Path(__file__).parent.resolve()
    _, metadata, tags = create_posts(root.joinpath("tests"))
    env = Environment(loader=FileSystemLoader(searchpath="./templates"))
    home_template = env.get_template("home.html")
    render_home(metadata, root.joinpath("tests"), tags, home_template)

    # test_index_content
    with open(root.joinpath("tests/index.html"), "r") as f:
        index_content = f.read()

    test_index_content = """<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n  <link rel="stylesheet" href="../static/main.css">\n  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU" crossorigin="anonymous">\n  <title>Phuoc\'s blog</title>\n</head>\n<body>\n  <br>\n  <div class="container">\n    <div class="row">\n      <div class="col-sm-2">\n        <h1 class="home-page"><a style="text-decoration: none; color: orangered" href="../index.html">Trang chủ</a></h1>\n      </div>\n      <div class="col-sm-10">\n        \n<h1>Tất cả các bài viết</h1><br>\n\n\n  <p>\n  <div class="home-summ">\n    <small class="home-meta">10-10-2021</small>\n    <br>\n    <small class="home-meta right">\n      tags: \n       \n        <a href="tags/test.html" style="text-decoration: none; color: orchid;">test</a>,\n      \n    </small>\n  </div>\n    <h2>\n      <a href="../posts/test.html" style="text-decoration: none; color: orangered">\n        test\n      </a>\n    </h2>\n    <small>\n      test\n    </small>\n  </p>\n\n\n      </div>\n    </div>\n  </div>\n  <br>\n  <div class="footer">\n    <div class="container">\n      \n      <div class="row">\n        <div class="col-sm-4"></div>\n        <div class="col-sm-4 author">\n          <span class="text-muted">Powered by\n            <a style="text-decoration: none; color: orangered" href="https://github.com/tranvietphuoc">Trần Việt Phước</a>\n          </span>\n        </div>\n        <div class="col-sm-4"></div>\n      </div>\n    </div>\n  </div>\n  \n  <script src="../static//script.js" type="text/javascript">\n  </script>\n</body>\n\n</html>"""

    # check file index.html is exists
    assert root.joinpath("tests/index.html").exists() == True
    assert test_index_content == index_content


def test_render_posts():
    root = pathlib.Path(__file__).parent.resolve()
    posts, _, tags = create_posts(root_path=root.joinpath("tests"))
    env = Environment(loader=FileSystemLoader(searchpath="./templates"))
    post_html = env.get_template("post.html")

    render_posts(posts, tags, root.joinpath("tests/posts").resolve(), post_html)

    with open(root.joinpath("tests/posts/test.html"), "r") as f:
        post_content = f.read()

    test_post_content = """<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n  <link rel="stylesheet" href="../static/main.css">\n  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU" crossorigin="anonymous">\n  <title>Phuoc\'s blog</title>\n</head>\n<body>\n  <br>\n  <div class="container">\n    <div class="row">\n      <div class="col-sm-2">\n        <h1 class="home-page"><a style="text-decoration: none; color: orangered" href="../index.html">Trang chủ</a></h1>\n      </div>\n      <div class="col-sm-10">\n        \n<div class="row">\n  <h1><span style="color:lightgrey"># </span>\n    test\n  </h1>\n</div>\n<br>\n\n<div class="row">\n  <div style="display: flex; flex-direction: column;">\n      <small class=\'post-meta\'>Ngày: 10-10-2021</small>\n      <small class="post-meta">Tags: \n        \n          <a href="../tags/test.html" style="text-decoration: none; color: orangered; background-color: lightgray">test</a>,\n        \n      </small>\n    </div>\n</div>\n<br>\n\n<p class="post-content">\n  <h1>test header</h1>\n\n<p>test content</p>\n\n</p>\n\n\n      </div>\n    </div>\n  </div>\n  <br>\n  <div class="footer">\n    <div class="container">\n      \n      <div class="row">\n        <div class="col-sm-4"></div>\n        <div class="col-sm-4 author">\n          <span class="text-muted">Powered by\n            <a style="text-decoration: none; color: orangered" href="https://github.com/tranvietphuoc">Trần Việt Phước</a>\n          </span>\n        </div>\n        <div class="col-sm-4"></div>\n      </div>\n    </div>\n  </div>\n  \n  <script src="https://utteranc.es/client.js"\n        repo="tranvietphuoc/tranvietphuoc.github.io"\n        issue-term="url"\n        label="Comment"\n        theme="github-light"\n        crossorigin="anonymous"\n        async>\n  </script>\n\n  <script src="../static//script.js" type="text/javascript">\n  </script>\n</body>\n\n</html>"""

    assert root.joinpath("tests/posts/test.html").exists() == True
    assert test_post_content == post_content


def test_render_tags():
    root = pathlib.Path(__file__).parent.resolve()
    _, metadata, tags = create_posts(root_path=root.joinpath("tests"))
    env = Environment(loader=FileSystemLoader(searchpath="./templates"))
    tag_html = env.get_template("tags.html")

    render_tags(metadata, tags, root.joinpath("tests/tags"), tag_html)

    with open(root.joinpath("tests/tags/test.html"), "r") as f:
        tag_content = f.read()

    test_tag_content = """<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n  <link rel="stylesheet" href="../static/main.css">\n  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU" crossorigin="anonymous">\n  <title>Phuoc\'s blog</title>\n</head>\n<body>\n  <br>\n  <div class="container">\n    <div class="row">\n      <div class="col-sm-2">\n        <h1 class="home-page"><a style="text-decoration: none; color: orangered" href="../index.html">Trang chủ</a></h1>\n      </div>\n      <div class="col-sm-10">\n        \n<h1>Các bài viết trong tag: <span style="color: lightgray;">TEST</span></h1>\n<br>\n\n\n  <p>\n  <div class="home-summ">\n    <small class="home-meta">10-10-2021</small>\n    <br>\n    <small class="home-meta right">tags: \n      \n      <a href="../tags/test.html" style="text-decoration: none; color: orchid;">\n        test\n      </a>,\n      \n    </small>\n  </div>\n    <h3>\n      <a href="../posts/test.html" style="text-decoration: none; color: orangered">\n        test\n      </a>\n    </h3>\n    <small>\n      test\n    </small>\n  </p>\n\n\n\n      </div>\n    </div>\n  </div>\n  <br>\n  <div class="footer">\n    <div class="container">\n      \n      <div class="row">\n        <div class="col-sm-4"></div>\n        <div class="col-sm-4 author">\n          <span class="text-muted">Powered by\n            <a style="text-decoration: none; color: orangered" href="https://github.com/tranvietphuoc">Trần Việt Phước</a>\n          </span>\n        </div>\n        <div class="col-sm-4"></div>\n      </div>\n    </div>\n  </div>\n  \n  <script src="../static//script.js" type="text/javascript">\n  </script>\n</body>\n\n</html>"""
    print(tag_content.__repr__())
    assert root.joinpath("tests/tags/test.html").exists() == True
    assert test_tag_content == tag_content
