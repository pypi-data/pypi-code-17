"""staticjam: Markdown + Jinja Site Generator

Only works in Python 3.

Usage:
    staticjam make (blog|pages|both)

"""

from docopt import docopt

from . import __version__
from . import staticjam


def entrypoint():
    """The Python "entrypoint" (main) of this CLI script.

    """

    arguments = docopt(__doc__, version='docopt ' + __version__)
    if arguments['make'] and arguments['pages']:
        staticjam.create_pages()
    elif arguments['make'] and arguments['blog']:
        staticjam.create_blog()
    elif arguments['make'] and arguments['both']:
        staticjam.create_pages()
        staticjam.create_blog()


if __name__ == "__main__":
    entrypoint()
