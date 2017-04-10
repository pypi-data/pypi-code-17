#!/usr/bin/env python3

"""Configuration class creates unified configuration from /config (by default) dir."""

from os import makedirs

import pickle
import ruamel.yaml as yaml


from . import env
from .env import MODE, ROOTPATH

__all__ = ['Configuration']


class Configuration(object):

    """Configuration creates unified configuration from /config (by default) dir."""

    def __init__(self,
                 root=ROOTPATH,
                 directory='config',
                 cache='caches/Configuration/%s.pickle' % MODE):

        self._config = {}
        self._custom = None
        self.path = ROOTPATH / directory
        self.cache = ROOTPATH / cache

    @property
    def custom(self):
        """Finds best match for custom config file based on host and domain names."""
        if not self._custom:
            names = ['%s-%s.yml' % (ROOTPATH.name, env.hostname()),
                     '%s-%s.yml' % (ROOTPATH.name, 'default'),
                     '%s-%s.yml' % ('default', env.hostname()),
                     'default.yml']
            try:
                self._custom = next(self.path / f for f in names
                                           if (self.path / f).exists())
            except StopIteration:
                raise FileNotFoundError("Custom site config not found. Config directory: %s" %
                                        self.path)
        return self._custom

    @property
    def config(self):
        """Get config."""
        return self._config or self._load_config()


    def _load_config(self):

        """Load config from cache or by parsing all files if necessary."""

        config = {}

        if self.cache and self.cache.exists() and \
           (self.custom.stat().st_mtime < self.cache.stat().st_mtime):
            try:
                config = pickle.load(open(self.cache))
            except Exception:  # pylint: disable=broad-except
                pass
            else:
                # if, for any reason, cached file had __debug directive
                # or the file doesn't belong to config that we want to load
                # we should reload the config anyway
                if '__debug' in config['__meta__'] \
                        or config['__meta__']['hostname'] != env.hostname() \
                        or config['__meta__']['path'] != self.path:
                    config.clear()

        store_config = False

        if not config:
            config = self._parse_config_files(self._get_config_files())
            store_config = True

        if '__meta__' not in config:
            config['__meta__'] = {}

        config['__meta__']['hostname'] = env.hostname()
        config['__meta__']['path'] = self.path

        if store_config and self.cache:
            makedirs(str(self.cache.parent), exist_ok=True)
            with open(str(self.cache), 'wb') as f:
                pickle.dump(config, f)
            with open(str(self.cache.with_suffix('.yml')), 'w') as f:
                yaml.dump(config, f)

        self._config = config
        return config

    def _get_config_files(self):
        """Construct a list of all config files."""
        fileList = []
        modules_dir = self.path / 'modules'
        if modules_dir.is_dir():
            fileList += [f for f in modules_dir.iterdir() if f.is_file() and f.suffix == '.yml']
        fileList.append(self.path / '_automatic.yml')
        fileList.append(self.path / '_common.yml')

        fileList.append(self.custom)

        if (self.path / ('%s_%s.yml' % (env.hostname(), MODE))).is_file():
            fileList.append(self.path / ('%s_%s.yml' % (env.hostname(), MODE)))
        elif (self.path / ('_%s.yml' % (MODE,))).is_file():
            fileList.append(self.path / ('_%s.yml' % (MODE,)))

        return fileList


    def _parse_config_files(self, files):
        """Reads all config files and creates unified configuration.
        Config file format is YAML 1.1 or 1.2 (default).
        """
        config = {}
        fh = None
        for f in files:
            try:
                fh = open(str(f), encoding='utf-8')
                self._deepMerge(config, yaml.load(fh, Loader=yaml.Loader))
            except IOError:
                # ssshhh... silently ignore missing files
                pass
            except (ValueError, yaml.scanner.ScannerError) as e:
                print('Problem with config file: %s' % f)
                raise e
            finally:
                if fh:
                    fh.close()

        return config


    def _deepMerge(self, old, new):
        """Merge two config trees.

        Second config may have special entries:
        __replace: discards old contents and replaces them with a new ones
        __erase: given key is completely removed from final config
        In both cases special keys are dropped.
        Values of special keys are ignored even if they resolve to False.
        """
        if not new:
            return

        for key in new:
            if key in old \
                    and isinstance(old[key], dict) \
                    and isinstance(new[key], dict) \
                    and '__replace' not in new[key] \
                    and '__erase' not in new[key]:
                self._deepMerge(old[key], new[key])
            else:
                if isinstance(new[key], dict) \
                        and '__erase' in new[key] \
                        and key in old:
                    old.pop(key)
                else:
                    old[key] = new[key]

            if key in old and isinstance(old[key], dict):
                if '__replace' in old[key]:
                    old[key].pop('__replace')
                if '__erase' in old[key]:
                    old.pop(key)

    def any(self, *args, **kwargs):
        """Shortcut for finding first existing key path.

        @arg args - one or more lists or tuples of paths
        @arg empty=False - whether or not skip existing but empty keys
        @arg default - fallback value if none found
        """
        empty = 'empty' in kwargs and kwargs['empty']
        for path in args:
            try:
                result = self.get(*path)
                if empty or result:
                    return result
            except KeyError:
                pass
        if 'default' in kwargs:
            return kwargs['default']
        else:
            raise KeyError("No matching config path found. Tried: %s" %
                           ", ".join(["/".join(str(y) for y in x) for x in args]))


    def get(self, *args, **kwargs):
        """Return a value or an complex object from the config.

        Takes arguments that construct the path to the required config
        section and, optionally, a default= parameter.
        """

        current = self.config
        for item in args:
            if item in current:
                current = current[item]
            elif 'default' in kwargs:
                return kwargs['default']
            else:
                raise KeyError("Config path \"/%s\" not found." %
                               '/'.join(str(x) for x in args))
        return current


    def set(self, *args):
        """Allow to temporarily overwrite arbitrary parts of config tree."""

        current = self.config
        for item in args[:-2]:
            if item not in current:
                current[item] = dict()
            current = current[item]
        current[args[-2]] = args[-1]
