import horetu
from . import parse, dump

def main():
    horetu.cli({
        'import': parse.parse,
        'export': dump.dump,
        'format': dump.format,
    }, name='bguo')
