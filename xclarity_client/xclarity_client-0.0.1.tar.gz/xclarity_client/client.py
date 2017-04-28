import sys
import traceback


def import_class(import_str):
    mod_str, _sep, class_str = import_str.rpartition('.')
    __import__(mod_str)
    try:
        return getattr(sys.modules[mod_str], class_str)
    except AttributeError:
        raise ImportError('Class %s cannot be found (%s)' %
                          (class_str,
                           traceback.format_exception(*sys.exc_info())))


def Client(version=None, username=None, password=None, url=None):
    version = version.lower().replace('xclarity_', '')
    version_mod_name = 'v%s' % version.replace('.', '_')
    c = import_class("xclarity_client.%s.client.Client" % version_mod_name)
    return c(version=version, username=username, password=password, url=url)
