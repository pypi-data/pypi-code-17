"""
extract markdown-like comments from a file and convert them to markdown.

 Extract markdown-like comments from (source code) file, convert them
 to valid markdown and run pandoc on it.
 Since the comment characters for different languages differ,
 this program can be adjusted to use the comment character used in your
 file by command line arguments.
"""

from .main import excerpt
from .ui import excerpts
