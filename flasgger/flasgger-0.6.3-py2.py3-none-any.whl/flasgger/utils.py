# coding: utf-8

import copy
import inspect
import os
import re
from collections import OrderedDict
from copy import deepcopy
from functools import wraps
from importlib import import_module

import jsonschema
import yaml
from flask import Response, abort, request
from flask.views import MethodView
from jsonschema import ValidationError  # noqa
from six import string_types


def swag_from(specs=None, filetype=None, endpoint=None, methods=None,
              validation=False, schema_id=None, data=None, definition=None):
    """
    Takes a filename.yml, a dictionary or object and loads swagger specs.

    :param specs: a filepath, a dictionary or an object
    :param filetype: yml or yaml (json and py to be implemented)
    :param endpoint: endpoint to build definition name
    :param methods: method to build method based specs
    :param validation: perform validation?
    :param schema_id: Definition id ot name to use for validation
    :param data: data to validate (default is request.json)
    :param definition: alias to schema_id
    """

    def resolve_path(function, filepath):
        if not filepath.startswith('/'):
            if not hasattr(function, 'root_path'):
                function.root_path = get_root_path(function)
            res = os.path.join(function.root_path, filepath)
            return res
        return filepath

    def set_from_filepath(function):
        final_filepath = resolve_path(function, specs)
        function.swag_type = filetype or specs.split('.')[-1]

        if endpoint or methods:
            if not hasattr(function, 'swag_paths'):
                function.swag_paths = {}

        if not endpoint and not methods:
            function.swag_path = final_filepath
        elif endpoint and methods:
            for verb in methods:
                key = "{}_{}".format(endpoint, verb.lower())
                function.swag_paths[key] = final_filepath
        elif endpoint and not methods:
            function.swag_paths[endpoint] = final_filepath
        elif methods and not endpoint:
            for verb in methods:
                function.swag_paths[verb.lower()] = final_filepath

    def set_from_specs_dict(function):
        function.specs_dict = specs

    def decorator(function):

        if isinstance(specs, string_types):
            set_from_filepath(function)
            # function must have or a single swag_path or a list of them
            swag_path = getattr(function, 'swag_path', None)
            swag_paths = getattr(function, 'swag_paths', None)
            validate_args = {
                'filepath': swag_path or swag_paths,
                'root': getattr(function, 'root_path', None)
            }
        if isinstance(specs, dict):
            set_from_specs_dict(function)
            validate_args = {'specs': specs}

        @wraps(function)
        def wrapper(*args, **kwargs):
            if validation is True:
                validate(
                    data,
                    schema_id or definition,
                    **validate_args
                )
            return function(*args, **kwargs)
        return wrapper

    return decorator


def validate(data=None, schema_id=None, filepath=None, root=None,
             definition=None, specs=None):
    """
    This method is available to use YAML swagger definitions file
    or specs (dict or object) to validate data against its jsonschema.

    example:
        validate({"item": 1}, 'item_schema', 'defs.yml', root=__file__)
        validate(request.json, 'User', specs={'definitions': {'User': ...}})

    :param data: data to validate, by defaull is request.json
    :param schema_id: The definition id to use to validate (from specs)
    :param filepath: definition filepath to load specs
    :parm root: root folder (inferred if not provided), unused if path starts
        with `/`
    :param definition: Alias to schema_id (kept for backwards compatibility)
    :param specs: load definitions from dict or object passed here intead of
        a file.
    """
    schema_id = schema_id or definition

    # for backwards compatibility with function signature
    if filepath is None and specs is None:
        abort(Response('Filepath or specs is needed to validate', status=500))

    if data is None:
        data = request.json  # defaults
    elif callable(data):
        # data=lambda: request.json
        data = data()

    if not data:
        abort(Response('No data to validate', status=500))

    # not used anymore but kept to reuse with marshmallow
    endpoint = request.endpoint.lower().replace('.', '_')
    verb = request.method.lower()

    if filepath is not None:
        if not root:
            try:
                frame_info = inspect.stack()[1]
                root = os.path.dirname(os.path.abspath(frame_info[1]))
            except Exception:
                root = None
        else:
            root = os.path.dirname(root)

        if not filepath.startswith('/'):
            final_filepath = os.path.join(root, filepath)
        else:
            final_filepath = filepath
        full_doc = load_from_file(final_filepath)
        yaml_start = full_doc.find('---')
        swag = yaml.load(full_doc[yaml_start if yaml_start >= 0 else 0:])
    else:
        swag = copy.deepcopy(specs)

    params = [
        item for item in swag.get('parameters', [])
        if item.get('schema')
    ]

    definitions = {}
    main_def = {}
    raw_definitions = extract_definitions(
        params, endpoint=endpoint, verb=verb)

    if schema_id is None:
        for param in params:
            if param.get('in') == 'body':
                schema_id = param.get('schema', {}).get('$ref')
                if schema_id:
                    schema_id = schema_id.split('/')[-1]
                    break  # consider only the first

    if schema_id is None:
        # if it is still none use first raw_definition extracted
        if raw_definitions:
            schema_id = raw_definitions[0].get('id')

    for defi in raw_definitions:
        if defi['id'].lower() == schema_id.lower():
            main_def = defi.copy()
        else:
            definitions[defi['id']] = defi

    # support definitions informed in dict
    if schema_id in swag.get('definitions', {}):
        main_def = swag.get('definitions', {}).get(schema_id)

    main_def['definitions'] = definitions

    for key, value in definitions.items():
        if 'id' in value:
            del value['id']

    try:
        jsonschema.validate(data, main_def)
    except ValidationError as e:
        abort(Response(str(e), status=400))


def apispec_to_template(app, spec, definitions=None, paths=None):
    """
    Converts apispec object in to flasgger definitions template
    :param app: Current app
    :param spec: apispec.APISpec
    :param definitions: a list of [Schema, ..] or [('Name', Schema), ..]
    :param paths: A list of flask views
    """
    definitions = definitions or []
    paths = paths or []
    spec_dict = spec.to_dict()

    with app.app_context():
        for definition in definitions:
            if isinstance(definition, (tuple, list)):
                name, schema = definition
            else:
                schema = definition
                name = schema.__name__.replace('Schema', '')

            spec.definition(name, schema=schema)

        for path in paths:
            spec.add_path(view=path)

    ret = ordered_dict_to_dict(spec_dict)
    return ret


def ordered_dict_to_dict(d):
    """
    Converts inner OrderedDict to bare dict
    """
    ret = {}
    new_d = deepcopy(d)
    for k, v in new_d.items():
        if isinstance(v, OrderedDict):
            v = dict(v)
        if isinstance(v, dict):
            v = ordered_dict_to_dict(v)
        ret[k] = v
    return ret


def remove_suffix(fpath):  # pragma: no cover
    """Remove all file ending suffixes"""
    return os.path.splitext(fpath)[0]


def is_python_file(fpath):  # pragma: no cover
    """Naive Python module filterer"""
    return ".py" in fpath and "__" not in fpath


def pathify(basenames, examples_dir="examples/"):  # pragma: no cover
    """*nix to python module path"""
    example = examples_dir.replace("/", ".")
    return [example + basename for basename in basenames]


def get_examples(examples_dir="examples/"):  # pragma: no cover
    """All example modules"""
    all_files = os.listdir(examples_dir)
    python_files = [f for f in all_files if is_python_file(f)]
    basenames = [remove_suffix(f) for f in python_files]
    modules = [import_module(module) for module in pathify(basenames)]
    return [
        module for module in modules
        if getattr(module, 'app', None) is not None
    ]


def get_path_from_doc(full_doc):
    """
    If `file:` is provided import the file.
    """
    swag_path = full_doc.replace('file:', '').strip()
    swag_type = swag_path.split('.')[-1]
    return swag_path, swag_type


def json_to_yaml(content):
    """
    TODO: convert json to yaml
    """
    return content


def load_from_file(swag_path, swag_type='yml', root_path=None):
    """
    Load specs from YAML file
    """
    if swag_type not in ('yaml', 'yml'):
        raise AttributeError("Currently only yaml or yml supported")
        # TODO: support JSON
    try:
        with open(swag_path) as yaml_file:
            return yaml_file.read()
    except IOError:
        # not in the same dir, add dirname
        swag_path = os.path.join(
            root_path or os.path.dirname(__file__), swag_path
        )
        with open(swag_path) as yaml_file:
            return yaml_file.read()


def parse_docstring(obj, process_doc, endpoint=None, verb=None):
    """
    Gets swag data for method/view docstring
    """
    first_line, other_lines, swag = None, None, None

    full_doc = None
    swag_path = getattr(obj, 'swag_path', None)
    swag_type = getattr(obj, 'swag_type', 'yml')
    swag_paths = getattr(obj, 'swag_paths', None)
    root_path = get_root_path(obj)

    if swag_path is not None:
        full_doc = load_from_file(swag_path, swag_type)
    elif swag_paths is not None:
        for key in ("{}_{}".format(endpoint, verb), endpoint, verb.lower()):
            if key in swag_paths:
                full_doc = load_from_file(swag_paths[key], swag_type)
                break
        # TODO: handle multiple root_paths
        # to support `import: ` from multiple places
    else:
        full_doc = inspect.getdoc(obj)

    if full_doc:

        if full_doc.startswith('file:'):
            if not hasattr(obj, 'root_path'):
                obj.root_path = root_path
            swag_path, swag_type = get_path_from_doc(full_doc)
            doc_filepath = os.path.join(obj.root_path, swag_path)
            full_doc = load_from_file(doc_filepath, swag_type)

        full_doc = parse_imports(full_doc, root_path)

        line_feed = full_doc.find('\n')
        if line_feed != -1:
            first_line = process_doc(full_doc[:line_feed])
            yaml_sep = full_doc[line_feed + 1:].find('---')
            if yaml_sep != -1:
                other_lines = process_doc(
                    full_doc[line_feed + 1: line_feed + yaml_sep]
                )
                swag = yaml.load(full_doc[line_feed + yaml_sep:])
            else:
                other_lines = process_doc(full_doc[line_feed + 1:])
        else:
            first_line = full_doc

    return first_line, other_lines, swag


def get_root_path(obj):
    """
    Get file path for object and returns its dirname
    """
    try:
        filename = os.path.abspath(obj.__globals__['__file__'])
    except (KeyError, AttributeError):
        if getattr(obj, '__wrapped__', None):
            # decorator package has been used in view
            return get_root_path(obj.__wrapped__)
        filename = inspect.getfile(obj)
    return os.path.dirname(filename)


def parse_definition_docstring(obj, process_doc):
    """
    Gets swag data from docstring for class based definitions
    """
    doc_lines, swag = None, None

    full_doc = None
    swag_path = getattr(obj, 'swag_path', None)
    swag_type = getattr(obj, 'swag_type', 'yml')

    if swag_path is not None:
        full_doc = load_from_file(swag_path, swag_type)
    else:
        full_doc = inspect.getdoc(obj)

    if full_doc:

        if full_doc.startswith('file:'):
            if not hasattr(obj, 'root_path'):
                obj.root_path = get_root_path(obj)
            swag_path, swag_type = get_path_from_doc(full_doc)
            doc_filepath = os.path.join(obj.root_path, swag_path)
            full_doc = load_from_file(doc_filepath, swag_type)

        yaml_sep = full_doc.find('---')
        if yaml_sep != -1:
            doc_lines = process_doc(
                full_doc[:yaml_sep - 1]
            )
            swag = yaml.load(full_doc[yaml_sep:])
        else:
            doc_lines = process_doc(full_doc)

    return doc_lines, swag


def parse_imports(full_doc, root_path=None):
    """
    Supports `import: otherfile.yml` in docstring specs
    """
    regex = re.compile('import: "(.*)"')
    import_prop = regex.search(full_doc)
    if import_prop:
        start = import_prop.start()
        spaces_num = start - full_doc.rfind('\n', 0, start) - 1
        filepath = import_prop.group(1)
        if filepath.startswith('/'):
            imported_doc = load_from_file(filepath)
        else:
            imported_doc = load_from_file(filepath, root_path=root_path)
        indented_imported_doc = imported_doc.replace(
            '\n', '\n' + ' ' * spaces_num
        )
        full_doc = regex.sub(indented_imported_doc, full_doc, count=1)
        return parse_imports(full_doc)
    return full_doc


def extract_definitions(alist, level=None, endpoint=None, verb=None,
                        prefix_ids=False):
    """
    Since we couldn't be bothered to register models elsewhere
    our definitions need to be extracted from the parameters.
    We require an 'id' field for the schema to be correctly
    added to the definitions list.
    """
    endpoint = endpoint or request.endpoint.lower()
    verb = verb or request.method.lower()
    endpoint = endpoint.replace('.', '_')

    def _extract_array_defs(source):
        """
        Extracts definitions identified by `id`
        """
        # extract any definitions that are within arrays
        # this occurs recursively
        ret = []
        items = source.get('items')
        if items is not None and 'schema' in items:
            ret += extract_definitions([items], level + 1, endpoint, verb,
                                       prefix_ids)
        return ret

    # for tracking level of recursion
    if level is None:
        level = 0

    defs = list()
    if alist is not None:
        for item in alist:
            if not getattr(item, 'get'):
                raise RuntimeError('definitions must be a list of dicts')
            schema = item.get("schema")
            if schema is not None:
                schema_id = schema.get("id")
                if schema_id is not None:
                    # add endpoint_verb to schema id to avoid conflicts
                    if prefix_ids:
                        schema['id'] = schema_id = "{}_{}_{}".format(
                            endpoint, verb, schema_id
                        )
                    # ^ api['SWAGGER']['prefix_ids'] = True
                    # ... for backwards compatibility with <= 0.5.14

                    defs.append(schema)
                    ref = {"$ref": "#/definitions/{}".format(schema_id)}
                    # only add the reference as a schema if we are in a
                    # response or
                    # a parameter i.e. at the top level
                    # directly ref if a definition is used within another
                    # definition
                    if level == 0:
                        item['schema'] = ref
                    else:
                        item.update(ref)
                        del item['schema']

                # extract any definitions that are within properties
                # this occurs recursively
                properties = schema.get('properties')
                if properties is not None:
                    defs += extract_definitions(
                        properties.values(), level + 1, endpoint, verb,
                        prefix_ids
                    )

                defs += _extract_array_defs(schema)

            defs += _extract_array_defs(item)

    return defs


def has_valid_dispatch_view_docs(endpoint):
    """
    Return True if dispatch_request is swaggable
    """
    klass = endpoint.__dict__.get('view_class', None)
    return klass and hasattr(klass, 'dispatch_request') \
        and hasattr(endpoint, 'methods') \
        and getattr(klass, 'dispatch_request').__doc__


def is_valid_method_view(endpoint):
    """
    Return True if obj is MethodView
    """
    klass = endpoint.__dict__.get('view_class', None)
    try:
        return issubclass(klass, MethodView)
    except TypeError:
        return False
