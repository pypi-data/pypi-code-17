import os.path
import sys
try:
    from importlib import machinery
    from importlib import import_module as import_module_original
except ImportError:
    # patching for import machinery
    # https://bitbucket.org/ericsnowcurrently/importlib2/issues/8/unable-to-import-importlib2machinery
    import importlib2._fixers as f
    fix_importlib_original = f.fix_importlib

    def fix_importlib(ns):
        if ns["__name__"] == 'importlib2.machinery':

            class _LoaderBasics:
                load_module = object()

            ns["_LoaderBasics"] = _LoaderBasics

            class FileLoader:
                load_module = object()

            ns["FileLoader"] = FileLoader

            class _NamespaceLoader:
                load_module = object()
                module_repr = object()

            ns["_NamespaceLoader"] = _NamespaceLoader
        fix_importlib_original(ns)

    f.fix_importlib = fix_importlib
    from importlib2 import machinery
    from importlib2 import import_module as import_module_original


def expose_all_members(module, globals_=None, _depth=2):
    members = {k: v for k, v in module.__dict__.items() if not k.startswith("_")}
    return expose_members(module, members, globals_=globals_, _depth=_depth)


def expose_members(module, members, globals_=None, _depth=1):
    if globals_ is None:
        frame = sys._getframe(_depth)
        globals_ = frame.f_globals
    globals_.update({k: module.__dict__[k] for k in members})
    return globals_


def import_from_physical_path(path, as_=None, here=None):
    if here is not None:
        here = here if os.path.isdir(here) else os.path.dirname(here)
        here = os.path.normpath(os.path.abspath(here))
        path = os.path.join(here, path)
    module_id = as_ or path.replace("/", "_").rstrip(".py")
    return machinery.SourceFileLoader(module_id, path).load_module()


def import_module(sym, here=None, sep=":"):
    module_path, fn_name = sym.rsplit(sep, 2)
    _, ext = os.path.splitext(module_path)
    if ext == ".py":
        return import_from_physical_path(module_path, here=here)
    else:
        return import_module_original(module_path)


def import_symbol(sym, here=None, sep=":", ns=None):
    if ns is not None and sep not in sym:
        sym = "{}:{}".format(ns, sym)
    module_path, fn_name = sym.rsplit(sep, 2)
    try:
        module = import_module(sym, here=here, sep=sep)
        return getattr(module, fn_name)
    except (ImportError, AttributeError) as e:
        sys.stderr.write("could not import {!r}\n{}\n".format(sym, e))
        raise
