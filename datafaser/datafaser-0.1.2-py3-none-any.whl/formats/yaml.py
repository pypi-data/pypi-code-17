import yaml


def read(stream):
    return yaml.load(stream)


def write(data, stream):
    yaml.safe_dump(data, stream, default_flow_style=False)
