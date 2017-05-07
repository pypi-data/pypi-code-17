import sys

from .notebook_finder import NotebookFinder

__VERSION__ = '1.0.0'


sys.meta_path.append(NotebookFinder())
