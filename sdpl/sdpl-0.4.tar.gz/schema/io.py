__author__ = 'Bohdan Mushkevych'

from yaml import load as yaml_load, dump, YAMLObject


def load(input_path:str):
    with open(input_path, mode='r', encoding='utf-8') as input_stream:
        return yaml_load(input_stream)


def store(yaml_object:YAMLObject, output_path:str):
    output_path = output_path.strip('\'')
    with open(output_path, 'w', encoding='utf-8') as output_stream:
        dump(yaml_object, output_stream)
