# This is my personal blog

![Blog generator tool](https://github.com/tvph/tvph.github.io/actions/workflows/python-app.yml/badge.svg)

* I've created a tool to render from markdown file to static site by `Python` for my self.
* To use this template, you need to clone the repo first. Then run `poetry install` to install virtual environment on your local machine.
* Project structure:
```
    |_ prototypes/       # contains .md file, you will write your posts in here.
    |_ posts/            # contains all html posts file after run ./render
    |_ tags/             # contains all html tags file after run ./render
    |_ templates/        # contains jinja templates for constructing posts, tags html files
    |_ static/           # contains static file like styles or script for your pages
    |_ index.html        # home page of blog
    |_ app.py            # blog generator tool
    |_ test_app.py       # test all functions of blog generator tool
    |_ render            # command for render html files
    |_ requirements.txt  # for create environment for github actions
    |_ poetry.lock
    |_ pyproject.toml

```

* Then write the your posts in `.md` format, edit the metadata and push them into `prototypes` folder. Notice that, the metadata of .md file you need to keep following these formats

```
title: ....
date: ....
tags: ....
name: ....
summary: ....
```

* Finnally. Run `./render` to render `html` files. All `html` files of posts will go to `posts` and `tags` folder.
* To publish your blog. Read [this guide](https://pages.github.com/)
* In addition, you can add a comment plugin your self call [utterances](https://utteranc.es/?installation_id=19767855&setup_action=install). After that, go to
`templates/post.html` and replace the script in `{% block script %}{% endblock %}` with your script.
* Cheers.
