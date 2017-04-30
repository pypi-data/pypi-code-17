from markdown import Markdown
from markdown.extensions.codehilite import makeExtension as CodeHilite
from markdown.extensions.meta import makeExtension as MetaData
from pyembed.markdown import PyEmbedMarkdown
from mdx_gfm import GithubFlavoredMarkdownExtension as Github
from markdown.extensions.wikilinks import WikiLinkExtension
from markdown.extensions.toc import TocExtension


def join_settings(settings, metadata):
    config = {}

    for key, value in settings.items():
        if key in metadata.keys():
            config[key] = metadata[key][0]
        else:
            config[key] = settings[key]

    return config


def compile(content, settings):
    extensions = [Github(), CodeHilite(), PyEmbedMarkdown(), MetaData(),
                  TocExtension(),
                 WikiLinkExtension(base_url=settings['url'], end_url='.html')]
    md = Markdown(extensions=extensions)

    markdown = md.convert(content)
    return markdown, join_settings(settings, md.Meta)
