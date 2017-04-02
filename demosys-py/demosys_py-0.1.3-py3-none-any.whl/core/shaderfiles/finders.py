import functools
import os
from demosys.core import finders
from demosys.conf import settings
from demosys.core.exceptions import ImproperlyConfigured
from demosys.utils.module_loading import import_string

SHADER_DIR = 'shaders'


class FileSystemFinder(finders.FileSystemFinder):
    """Find shaders in ``SHADER_DIRS``"""
    def __init__(self):
        if not hasattr(settings, 'SHADER_DIRS'):
            raise ImproperlyConfigured(
                "Settings module don't define SHADER_DIRS."
                "This is required when using a FileSystemFinder."
            )
        super().__init__(settings.SHADER_DIRS)

    # TODO: Use values from settings to filter shader files
    # def find(self, path):
    #     pass


class EffectDirectoriesFinder(finders.FileSystemFinder):
    """Finds shaders in the registered effects"""
    def __init__(self):
        from demosys.effects.registry import effects
        dirs = list(effects.get_dirs())
        super().__init__(dirs)

    # TODO: Use values from settings to filter shader files
    def find(self, path):
        return self._find(os.path.join(SHADER_DIR, path))


def get_finders():
    for finder in settings.SHADER_FINDERS:
        yield get_finder(finder)


@functools.lru_cache(maxsize=None)
def get_finder(import_path):
    Finder = import_string(import_path)
    if not issubclass(Finder, finders.FileSystemFinder):
        raise ImproperlyConfigured(f'Finder {import_path} is not a subclass of core.finders.FileSystemFinder')
    return Finder()
