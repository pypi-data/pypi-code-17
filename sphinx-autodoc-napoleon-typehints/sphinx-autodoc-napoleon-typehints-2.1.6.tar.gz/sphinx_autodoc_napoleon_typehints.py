import inspect
import logging
import re

from sphinx.util.inspect import getargspec
from sphinx.ext.autodoc import formatargspec

try:
    from backports.typing import (Any, AnyStr, GenericMeta, TypeVar, Union, get_type_hints)
except ImportError:
    from typing import (Any, AnyStr, TypeVar, GenericMeta, Union, get_type_hints)


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def format_annotation(annotation, obj=None):
    if inspect.isclass(annotation) and annotation.__module__ == 'builtins':
        if annotation.__qualname__ == 'NoneType':
            return '``None``'
        else:
            return ':class:`{}`'.format(annotation.__qualname__)

    annotation_cls = annotation if inspect.isclass(annotation) else type(annotation)
    if annotation_cls.__module__ in ('typing', 'backports.typing'):
        params = None
        prefix = ':class:'
        extra = ''
        class_name = annotation_cls.__qualname__
        if annotation is Any:
            return ':data:`~typing.Any`'
        elif annotation is AnyStr:
            return ':data:`~typing.AnyStr`'
        elif isinstance(annotation, TypeVar):
            return '\\%r' % annotation
        elif class_name in ('Union', '_Union'):
            prefix = ':data:'
            class_name = 'Union'
            if hasattr(annotation, '__union_params__'):
                params = annotation.__union_params__
            else:
                params = annotation.__args__
            if params:
                params = list(params)
                if type(None) in params:
                    params.remove(type(None))
                    class_name = 'Optional'
                    if len(params) > 1:
                        params = [Union[tuple(params)]]
        elif annotation_cls.__qualname__ == 'Tuple' and hasattr(annotation, '__tuple_params__'):
            params = annotation.__tuple_params__
            if annotation.__tuple_use_ellipsis__:
                params += (Ellipsis,)
        elif annotation_cls.__qualname__ == '_ForwardRef':
            try:
                try:
                    global_vars = obj is not None and obj.__globals__ or dict()
                except AttributeError:
                    global_vars = dict()
                # Evaluate the type annotation string and then format it
                actual_type = eval(annotation.__forward_arg__, global_vars)
                return format_annotation(actual_type, obj)
            except Exception:
                return annotation.__forward_arg__
        elif annotation_cls.__qualname__ == 'Callable':
            prefix = ':data:'
            arg_annotations = result_annotation = None
            if hasattr(annotation, '__result__'):
                arg_annotations = annotation.__args__
                result_annotation = annotation.__result__
            elif getattr(annotation, '__args__', None) is not None:
                arg_annotations = annotation.__args__[:-1]
                result_annotation = annotation.__args__[-1]

            if arg_annotations in (Ellipsis, (Ellipsis,)):
                params = [Ellipsis, result_annotation]
            elif arg_annotations is not None:
                params = [
                    '\\[{}]'.format(
                        ', '.join(format_annotation(param, obj) for param in arg_annotations)),
                    result_annotation
                ]
        elif hasattr(annotation, 'type_var'):
            # Type alias
            class_name = annotation.name
            params = (annotation.type_var,)
        elif getattr(annotation, '__args__', None) is not None:
            params = annotation.__args__
        elif hasattr(annotation, '__parameters__'):
            params = annotation.__parameters__

        if params:
            extra = '\\[{}]'.format(', '.join(format_annotation(param, obj) for param in params))

        return '{}`~typing.{}`{}'.format(prefix, class_name, extra)
    elif annotation is Ellipsis:
        return '...'
    elif inspect.isclass(annotation):
        extra = ''
        if isinstance(annotation, GenericMeta):
            extra = '\\[{}]'.format(', '.join(format_annotation(param, obj)
                                              for param in annotation.__parameters__))

        return ':class:`~{}.{}`{}'.format(annotation.__module__, annotation.__qualname__, extra)
    else:
        return str(annotation)


def process_signature(app, what: str, name: str, obj, options, signature, return_annotation):
    if callable(obj):
        if what in ('class', 'exception'):
            obj = getattr(obj, '__init__')

        try:
            argspec = getargspec(obj)
        except TypeError:
            return

        if what in ('method', 'class', 'exception') and argspec.args:
            del argspec.args[0]

        return formatargspec(obj, *argspec[:-1]), None


def _process_google_docstrings(type_hints, lines, obj):
    """Process numpy docstrings parameters."""
    for argname, annotation in type_hints.items():
        formatted_annotation = format_annotation(annotation, obj)

        if argname == 'return':
            pass
        else:
            logger.debug('Searching for %s', argname)
            in_args_section = False
            for i, line in enumerate(lines):
                if line == 'Args:':
                    in_args_section = True
                elif in_args_section:
                    if not line.startswith('  '):
                        in_args_section = False
                        break
                    match = re.match('(  +{}) ?: *(.*)'.format(argname), line)
                    if match:
                        lines[i] = match.expand('\\1 ({}): \\2'.format(str(formatted_annotation)))
                        logger.debug('line replaced: %s', lines[i])
                        break


def _check_numpy_section_start(lines, i, section=None):
    """Check if numpy section starts at line `i`"""
    return (
        i > 0 and
        i < len(lines) - 1 and
        lines[i + 1].startswith('---') and
        (section is None or lines[i] == section)
    )


def _process_numpy_docstrings(type_hints, lines, obj):
    """Process numpy docstrings parameters."""
    for argname, annotation in type_hints.items():
        formatted_annotation = format_annotation(annotation, obj)

        if argname == 'return':
            pass
        else:
            logger.debug('Searching for %s', argname)
            in_args_section = False
            for i, line in enumerate(lines):
                if _check_numpy_section_start(lines, i - 1, 'Parameters'):
                    logger.debug('Numpy parameters section ended on line %i', i)
                    in_args_section = True
                elif in_args_section:
                    if _check_numpy_section_start(lines, i):
                        in_args_section = False
                        logger.debug('Numpy parameters section ended on line %i', i)
                        break
                    match = re.match('{}( ?: ?)?'.format(argname), line)
                    if match:
                        lines[i] = argname + ' : ' + formatted_annotation
                        logger.debug('line replaced: %s', lines[i])


def _process_sphinx_docstrings(type_hints, lines, obj):
    for argname, annotation in type_hints.items():
        formatted_annotation = format_annotation(annotation, obj)

        if argname == 'return':
            insert_index = len(lines)
            for i, line in enumerate(lines):
                if line.startswith(':rtype:'):
                    insert_index = None
                    break
                elif (line.startswith(':return:') or line.startswith(':returns:') or
                      line.startswith('')):
                    insert_index = i
                    break

            if insert_index is not None:
                lines.insert(insert_index, ':rtype: {}'.format(formatted_annotation))
        else:
            searchfor = ':param {}:'.format(argname)
            for i, line in enumerate(lines):
                if line.startswith(searchfor):
                    lines.insert(i, ':type {}: {}'.format(argname, formatted_annotation))
                    break


def process_docstring(app, what, name, obj, options, lines):
    if callable(obj):
        if what in ('class', 'exception'):
            obj = getattr(obj, '__init__')

        # Unwrap until we get to the original definition
        while hasattr(obj, '__wrapped__'):
            obj = obj.__wrapped__

        try:
            type_hints = get_type_hints(obj)
        except AttributeError:
            return

        _process_sphinx_docstrings(type_hints, lines, obj)
        _process_google_docstrings(type_hints, lines, obj)
        _process_numpy_docstrings(type_hints, lines, obj)


def setup(app):
    app.connect('autodoc-process-signature', process_signature)
    app.connect('autodoc-process-docstring', process_docstring)
