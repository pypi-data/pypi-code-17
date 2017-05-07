"""The main logic for StaticJaM

"""

import sys
import os
sys.path.append(os.getcwd())
import datetime
import glob
from collections import namedtuple

import jinja2
from bs4 import BeautifulSoup
import markdown


jinja_env = jinja2.Environment(
    loader=jinja2.PackageLoader(
        '_staticjam_source',
        'templates',
    )
)


class Source:
    """A StaticJaM source file.

    A markdown file which becomes a webpage
    (either blog or page) on the static site.
    This is basically an HTML snippet generated
    from markdown and some extra stuff cause
    beautiful soup.

    Attributes:
        path (str): File path to this source file.
        markdown_string (str): Source file contents.
        markdown (markdown.Markdown): Source file contents
            as markdown.Markdown object.
        html_string (str): Source file converted to HTML by
            markdown.Markdown object.
        meta (dict): am i sure of type
        soup (BeautifulSoup): A BeautifulSoup of the HTML
            generated from the source file, which is in
            markdown (ha, ha...).
        title (str): First heading of the post, the
            name. The title is the first h1/heading of the
            soup.

    Note:
        The HTML markdown.markdown() generates is
        not a full HTML page, so for example, this:

          # some title
          some paragraph

        ...becomes this:

          <h1>some title</h1>
          <p>some paragraph</p>

    """

    EXTENSIONS = [
        'markdown.extensions.footnotes',
        'markdown.extensions.meta',
    ]

    def __init__(self, path_to_md):
        self.path = path_to_md
        with open(path_to_md) as f:
            self.markdown_string = f.read()
        self.markdown = markdown.Markdown(
            extensions=self.EXTENSIONS,
        )
        self.html_string = self.markdown.convert(self.markdown_string)
        self.meta = self.markdown.Meta
        self.soup = BeautifulSoup(self.html_string, 'html.parser')
        self.title = self.soup.h1.extract().get_text()


# XXX: shouldn't these be called "articles?" otherwise rename
# all articles to "posts..." tho i like "articles" cause its like
# "zine"... could also change all "blog" to "zine"
class Post(Source):
    """A blog post, created from markdown source (given a file path).

    Constants:
        SUMMARY_CHARACTER_LIMIT (int): --
        TEMPLATE (str): jinja2 template to pull from the jinja2
            environment. This temple is used to render the post.
        MARKDOWN_SOURCE (str): --
        DATE_FORMAT (str): for strftime

    Attributes:
        href (str): Relative path to this article (html). Usable for
            both writing to local directory and as the href attribute
            of a link, in order to link to this post.
        category (str): Derived from the name of the directory
            containing this post.
        summary (str): A string summary (truncated) of the first
            paragraph of the content.
        content (BeautifulSoup): --
        timestamp (str): ---
        timestamp_as_int (int): --

    """

    SUMMARY_CHARACTER_LIMIT = 100
    TEMPLATE = 'blog-article.html'
    MARKDOWN_SOURCE = os.path.join(
        '_staticjam_source',
        'blog'
    )
    DATE_FORMAT = "%a, %d %b %Y"

    def __init__(self, file_path):
        """

        Arguments:
            file_path (str): Path to the markdown source file, which
                is a blog post.

        """

        super().__init__(file_path)
        self.content = self.html_string  # inherited, for backcompat...
        self.category = self.get_category(file_path)
        self.summary = self.summarize(self.soup)
        self.href = self.get_href(self.category, file_path)
        self.timestamp, self.timestamp_as_int = self.get_both_timestamps(file_path)

        if not os.path.exists('blog/' + self.category):
            os.makedirs('blog/' + self.category)

    @classmethod
    def get_category(cls, path_to_file):
        """Return the directory which contains path_to_file.

        Returns:
            str

        """

        directory_path = os.path.dirname(path_to_file)
        category = os.path.basename(directory_path)
        return category

    @classmethod
    def summarize(cls, soup):
        """Take BeautifulSoup and summarize the first paragraph.

        Returns:
            str:

        """

        first_paragraph = soup.find('p').get_text()

        if len(first_paragraph) > cls.SUMMARY_CHARACTER_LIMIT:
            return first_paragraph[:cls.SUMMARY_CHARACTER_LIMIT] + '&hellip;'
        else:
            return first_paragraph

    @staticmethod
    def get_href(category, file_path):
        """Path usable on both web server and for writing
        HTML locally.

        Arguments:
            category (str):
            file_path (str):

        """

        file_name_md = os.path.basename(file_path)
        return os.path.join(
            'blog',
            category,
            os.path.splitext(file_name_md)[0],
            'index.html',
        )

    @classmethod
    def get_both_timestamps(cls, file_path):
        """Returns both the nice string/human-legible timestamp, as
        well as the int version for sorting.

        """

        blog_post_file_name = os.path.basename(file_path)
        timestamp = blog_post_file_name.split('_', 1)[0]
        nice_timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d').strftime(cls.DATE_FORMAT)

        return nice_timestamp, int(timestamp.replace('-', ''))

    def render(self):
        post_template = jinja_env.get_template(self.TEMPLATE)
        return post_template.render(post=self)


def create_blog():
    # Create the blog by first creating all the individual
    # posts, building an index of those posts..
    list_of_all_posts_unsorted = []
    categorized_posts = {}
    search_path = os.path.join(Post.MARKDOWN_SOURCE, '**/*.md')
    for file_path in glob.iglob(search_path, recursive=True):

        # Create the post object and render/output
        post = Post(file_path)
        # create a directory for media belonging to post
        media_directory = os.path.split(os.path.splitext(post.href)[0])[0]
        if not os.path.exists(media_directory):
            os.makedirs(media_directory)

        with open(post.href, 'w', encoding='utf-8') as f:
            f.write(post.render())

        # File by category and add to list of all posts
        list_of_all_posts_unsorted.append(post)
        if post.category not in categorized_posts:
            categorized_posts[post.category] = [post]
        else:
            categorized_posts[post.category].append(post)

    # create the category indexes
    category_template = jinja_env.get_template('category-index.html')
    for category, posts in categorized_posts.items():
        path_to_category_index = os.path.join(
            'blog',
            category,
            'index.html',
        )
        with open(path_to_category_index, 'w', encoding='utf-8') as f:
            f.write(category_template.render(category=category, posts=posts))

    # ... then sort said post list by their creation time
    sorted_list_of_all_posts = sorted(
        list_of_all_posts_unsorted,
        key=lambda x: x.timestamp_as_int,
        reverse=True,
    )

    # .. finally render the blog index
    template = jinja_env.get_template('blog-index.html')  # XXX
    blog_index_path = os.path.join('blog', 'index.html')
    categories_alphabetized = sorted(categorized_posts.keys())
    with open(blog_index_path, 'w', encoding='utf-8') as f:
        f.write(
            template.render(
                posts=sorted_list_of_all_posts,
                categories=categories_alphabetized,
            )
        )


def create_pages():
    search_path = '_staticjam_source/pages/*.md'
    for file_path in glob.iglob(search_path, recursive=False):
        source = Source(file_path)
        meta = source.meta
        soup = source.soup
        article_title = source.title
        # shove it all into the template
        page_template = jinja_env.get_template('page.html')
        page_html = page_template.render(
            body=soup,
            article_title=article_title,
            **meta
        )

        # get HTML output name...
        file_name_md = os.path.basename(file_path)
        output_file_path = os.path.splitext(file_name_md)[0] + '.html'

        # output page content...
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(page_html)
