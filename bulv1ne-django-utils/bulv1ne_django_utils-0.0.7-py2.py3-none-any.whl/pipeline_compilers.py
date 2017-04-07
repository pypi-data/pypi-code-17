from functools import lru_cache

import sass
from django.conf import settings
from django.contrib.staticfiles.finders import get_finders
from django.templatetags.static import static as django_static
from pipeline.compilers import CompilerBase

from .sass_functions.svg_to_data_uri import svg_to_data_uri


def static(path):
    """
    Use the Django builtin static file resolver to return an absolute path
    usable as CSS url() argument. Sass equivalent of the 'static' template
    tag.
    """
    return '"{}"'.format(django_static(path))


def svg_to_data_uri_(file_):
    return svg_to_data_uri(file_, get_include_paths())


OUTPUT_STYLE = getattr(settings, 'LIBSASS_OUTPUT_STYLE', 'nested')
SOURCE_COMMENTS = getattr(settings, 'LIBSASS_SOURCE_COMMENTS', settings.DEBUG)
CUSTOM_FUNCTIONS = getattr(settings, 'LIBSASS_CUSTOM_FUNCTIONS', {
    'static': static,
    'svg_data_uri': svg_to_data_uri_,
})


@lru_cache()
def get_include_paths():
    """
    Generate a list of include paths that libsass should use to find files
    mentioned in @import lines.
    """
    include_paths = []

    # Look for staticfile finders that define 'storages'
    for finder in get_finders():
        try:
            storages = finder.storages
        except AttributeError:
            continue

        for storage in storages.values():
            try:
                include_paths.append(storage.path('.'))
            except NotImplementedError:
                # storages that do not implement 'path' do not store files locally,
                # and thus cannot provide an include path
                pass
    return include_paths


def compile(**kwargs):
    """Perform sass.compile, but with the appropriate include_paths for Django added"""
    INCLUDE_PATHS = get_include_paths()

    kwargs = kwargs.copy()
    kwargs['include_paths'] = (kwargs.get('include_paths') or []) + INCLUDE_PATHS

    custom_functions = CUSTOM_FUNCTIONS.copy()
    custom_functions.update(kwargs.get('custom_functions', {}))
    kwargs['custom_functions'] = custom_functions

    return sass.compile(**kwargs)


class SassCompiler(CompilerBase):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith('.scss')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        force = True
        if not outdated and not force:
            return
        with open(outfile, 'w') as f:
            f.write(
                compile(
                    filename=infile,
                    output_style=OUTPUT_STYLE,
                    source_comments=SOURCE_COMMENTS,
                )
            )
        return outfile
