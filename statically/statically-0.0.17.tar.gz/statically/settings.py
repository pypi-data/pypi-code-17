import yaml

def read_settings(path):
    with path.open() as file:
        return yaml.load(file)
