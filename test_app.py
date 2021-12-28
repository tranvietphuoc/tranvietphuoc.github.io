import pytest
from app import create_posts, render_home, render_posts, render_tags
from jinja2 import Environment, FileSystemLoader
import pathlib
from datetime import datetime
import tempfile
import shutil


@pytest.fixture
def test_setup():

    # write md contents

    path = tempfile.mkdtemp()
    prototypes_path = pathlib.Path(path).joinpath("prototypes").resolve()
    prototypes_path.mkdir(mode=511, parents=True, exist_ok=True)
    test_md = prototypes_path.joinpath("test.md").resolve()

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

    yield test_md

    # tear down
    shutil.rmtree(test_md.parent.parent.resolve())  # rm all files in mkdtemp


def test_create_posts(test_setup):

    path = test_setup

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

    posts, metadata, tags = create_posts(path.parent.parent.resolve())

    assert posts == test_post
    assert metadata == test_metadata
    assert tags == test_tags


def test_render_home(test_setup):
    path = test_setup

    # mk tests folder

    _, metadata, tags = create_posts(path.parent.parent.resolve())
    env = Environment(loader=FileSystemLoader(searchpath="./templates"))
    home_template = env.get_template("home.html")

    render_home(metadata, path.parent.parent.resolve(), tags, home_template)

    # test_index_content
    with open(path.parent.parent.joinpath("index.html"), "r") as f:
        index_content = f.read()

    test_index_content = f""""""  # check file index.html is exists
    print(repr(index_content))
    # assert path.parent.parent.joinpath("index.html").exists() == True
    # assert test_index_content == index_content


def test_render_posts(test_setup):
    path = test_setup

    # create posts folder in temp folder
    path.parent.parent.joinpath("posts").mkdir(
        mode=511, parents=True, exist_ok=True
    )

    posts, _, tags = create_posts(root_path=path.parent.parent.resolve())
    env = Environment(loader=FileSystemLoader(searchpath="./templates"))
    post_html = env.get_template("post.html")

    render_posts(
        posts, tags, path.parent.parent.joinpath("posts").resolve(), post_html
    )

    with open(path.parent.parent.joinpath("posts/test.html"), "r") as f:
        post_content = f.read()

    test_post_content = f""""""

    print(repr(post_content))
    # assert path.parent.parent.joinpath("posts/test.html").exists() == True
    # assert test_post_content == post_content


def test_render_tags(test_setup):
    path = test_setup

    _, metadata, tags = create_posts(root_path=path.parent.parent.resolve())

    # create tags folder in temp folder
    path.parent.parent.joinpath("tags").mkdir(
        mode=511, parents=True, exist_ok=True
    )
    env = Environment(loader=FileSystemLoader(searchpath="./templates"))
    tag_html = env.get_template("tags.html")

    render_tags(
        metadata, tags, path.parent.parent.joinpath("tags").resolve(), tag_html
    )

    with open(path.parent.parent.joinpath("tags/test.html"), "r") as f:
        tag_content = f.read()

    test_tag_content = f""""""
    print(repr(tag_content))
    # assert path.parent.parent.joinpath("tags/test.html").exists() == True
    # assert test_tag_content == tag_content
