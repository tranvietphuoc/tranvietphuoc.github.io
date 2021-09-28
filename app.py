from jinja2 import Environment, FileSystemLoader
from jinja2.environment import Template
from markdown2 import markdown
from pathlib import Path
from datetime import datetime
import typing as t


# read markdown file then write to a dict
def create_posts(root_path: Path):
    posts = {}

    paths = root_path.joinpath("prototypes").resolve()
    for md_post in paths.iterdir():
        with open(md_post.resolve(), "r") as f:
            posts[md_post.name] = markdown(
                f.read(),
                extras=[
                    "metadata",
                    "fenced-code-blocks",
                    "tables",
                    "strike",
                    "task_list",
                    "code-friendly",
                    "numbering",
                    "footnotes",
                ],
            )

    # return a dict with sorted following date created
    return {
        p: posts[p]
        for p in sorted(
            posts,
            key=lambda p: datetime.strptime(
                posts[p].metadata["date"], "%d-%m-%Y"
            ),
            reverse=True,
        )
    }


# render homepage
def render_home(
    posts_metadata: t.List[dict],
    render_folder: Path,
    tags: t.Set[str],
    template: Template,
):
    """Render home.html file to root folder."""

    home_html = template.render(posts=posts_metadata, tags=tags)
    home_path = render_folder.joinpath("index.html").resolve()
    with open(home_path, "w") as f:
        f.write(home_html)


# render posts
def render_posts(
    posts: t.Dict[str, str],
    tags: t.Set[str],
    render_folder: Path,
    template: Template,
):
    """Render post_metadata['name'].html file to outputs/ folder."""

    for p in posts:
        post_metadata = posts[p].metadata

        post_data = {
            "title": post_metadata["title"],
            "date": post_metadata["date"],
            "tags": post_metadata["tags"],
            "content": posts[p],
        }
        post_html = template.render(post=post_data, tags=tags)

        # render to html files
        post_path = render_folder.joinpath(
            f"{post_metadata['name']}.html"
        ).resolve()
        with open(post_path, "w") as f:
            f.write(post_html)


def render_tags(
    posts_metadata: t.List[dict],
    tags: t.Set[str],
    render_folder: Path,
    template: Template,
):

    # build a dict, contains all metadata follow key is tag
    tags_data = {}
    for t in tags:
        tag = []
        for p in posts_metadata:
            if t in p["tags"]:
                tag.append(p)
                tags_data.update({t: tag})

    # render to html
    for key, value in tags_data.items():
        tag_html = template.render(posts=value, tag=key)

        tag_path = (
            render_folder.joinpath("tags").joinpath(f"{key}.html").resolve()
        )
        with open(tag_path, "w") as f:
            f.write(tag_html)


if __name__ == "__main__":
    # path
    root = Path(__file__).parent.resolve()  # project's path

    posts = create_posts(root)  # get all posts in ./posts/ folder
    # for key, value in posts.items():
    #     print(key, value.metadata)

    # get template environment
    env = Environment(loader=FileSystemLoader(searchpath="./templates"))
    home_template = env.get_template(name="home.html")
    post_template = env.get_template(name="post.html")
    tag_template = env.get_template(name="tags.html")

    posts_metadata = [posts[p].metadata for p in posts]  # all posts metadata

    # convert tags of posts_metadata to list
    for meta in posts_metadata:
        meta["tags"] = meta["tags"].split(",").strip()

    # get posts's tags
    tags = [meta["tags"] for meta in posts_metadata]
    tags = set([i for tag in tags for i in tag])  # is a set

    posts_folder = root.joinpath("posts/").resolve()
    # render all html files
    render_home(
        posts_metadata=posts_metadata,
        render_folder=root.resolve(),
        tags=tags,
        template=home_template,
    )
    render_posts(
        posts=posts,
        tags=tags,
        render_folder=posts_folder,
        template=post_template,
    )
    render_tags(
        posts_metadata=posts_metadata,
        tags=tags,
        render_folder=root.resolve(),
        template=tag_template,
    )
