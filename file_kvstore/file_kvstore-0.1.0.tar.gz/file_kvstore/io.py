import yaml


def get_dict_from_yaml(filename):
    return yaml.load(_read_file(filename)) or {}


def write_dict_to_yaml(filename, obj):
    for k, v in obj.viewitems():
        obj[k] = _format_value(v)
    _write_file(filename, yaml.dump(obj, default_flow_style=False))


def _format_value(value):
    try:
        value = float(value)
        if value.is_integer():
            value = int(value)
    except ValueError:
        pass
    return value


# Enable easier testing
def _read_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except IOError:
        return ''


def _write_file(filename, yaml_string):
    with open(filename, 'w') as f:
        f.write(yaml_string)
