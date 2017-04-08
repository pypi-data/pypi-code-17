"""This extension allows to manage local resource path in markdown files.

The first goal of this extension is to transform relative path in markdown
files into absolute path given a required root directory.
Additionaly, this module will track all modified path for futher processing
in a ``resource_path`` attribute of the markdown object.

.. doctest::

   >>> import markdown
   >>> md_content = '''
   ... [a link with relative path](example/code.py)
   ... ![an image with relative path](imgs/funny-404-cat.jpg)
   ... ![this image is considered absolute](/static/my-logo.png)
   ... [this link is a full URL](http://example.org)
   ... '''
   >>> md = markdown.Markdown(
   ...     extensions=['markdown_extra.resource_path'],
   ...     extensions_config={
   ...         'markdown_extra.resource_path': {'root_path': '/blog/post'}})
   >>> html = md.convert(md_content)
   >>> md.resource_path
   [('example/code.py', '/blog/post/example/code.py'),
     ('imgs/funny-404-cat.jpg', '/blog/post/imgs/funny-404-cat.jpg')]
   >>> print(html)
   <p><a href="/blog/post/example/code.py">a link with relative path</a>
   <img alt="an image with relative path" src="/blog/post/imgs/funny-404-cat.jpg" />
   <img alt="this image is considered absolute" src="/static/my-logo.png" />
   <a href="http://example.org">this link is a full URL</a></p>

Path will be transformed only if they are relative.
That means they must not begin with a ``/`` character and must not have
a URL scheme.

As shown in the example above, the root path can be configured with the
``root_path`` keyword.

By default, only the ``a`` and ``img`` tags are processed.
The ``resource_tags`` can be configured to parse additional tags.
The configuration value is a iterable of two element tuples.
The first element is the tag name, the second is the attribute where a tag
may be stored.

.. code:: python

   Markdown(
       extensions=['markdown_extra'],
       extensions_config={
           'markdown_extra': {
               'root_path': '/new/root/path',
               'resource_tags': (('a', 'href'), ('img', 'src')),
           }})

"""

try:
    from urllib.parse import urlparse, urljoin
except ImportError:
    from urlparse import urlparse, urljoin

from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class ResourcePathTreeProcessor(Treeprocessor):
    def __init__(self, md, resource_tags, root_path=None):
        """
        Args:
            md (markdown.Markdow):
            resource_tags (iterable): An iterable of tag definition. A tag
                definition is a (tag, attribute) tuple.
            rout_path (str): root path to convert absolute path resources.
                Can be None no path conversion is needed.
        """
        self.md = md
        self.resource_tags = resource_tags
        self.root_path = root_path
        # make sure the root path ends with a '/'. This is required
        # when using urllib.parse.urljoin
        if self.root_path is not None and not self.root_path.endswith('/'):
            self.root_path = self.root_path + '/'
        super(ResourcePathTreeProcessor, self).__init__(md)

    def run(self, root):
        self.md.resource_path = []

        for tag_name, attr_name in self.resource_tags:
            for tag in root.iter(tag_name):
                path = tag.get(attr_name)
                # do not process this if no tag are given
                if path is None:
                    continue
                parsed = urlparse(path)
                if parsed.scheme or parsed.path.startswith('/'):
                    continue
                if self.root_path is not None:
                    new_path = urljoin(self.root_path, path)
                    tag.set(attr_name, new_path)
                else:
                    new_path = None
                self.md.resource_path.append((path, new_path))


class ResourcePathExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'root_path': ['/blog/post/', "The root path to resolve resources"],
            'resource_tags': [(('a', 'href'), ('img', 'src')),
                              "Tag to process and resource attribute"],
        }
        super(ResourcePathExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add(
            'resource_path',
            ResourcePathTreeProcessor(
                md,
                resource_tags=self.getConfig('resource_tags'),
                root_path=self.getConfig('root_path')),
            '_end')


def makeExtension(**kwargs):
    return ResourcePathExtension(**kwargs)
