import argparse
import sys
from .plugemin import render

__all__ = [
    "main",
]
def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--template",
                        help="the jinja2 template to use")
    parser.add_argument("-p", "--input-plugin",
                        help="The plugin to use to parse the input data")
    parser.add_argument("-d", "--data",
                        help="The data to use to render templates",
                        default=sys.stdin)
    return parser.parse_args()


def main(argv=None):
    """A command line interface to plugemin. This can be used independently
    of the Python API.
    """
    argv = sys.argv[1:] if argv is None else argv
    args = parse_args(argv)

    _template = args.template
    input_plugin = args.input_plugin
    data = args.data

    if not _template:
        raise ValueError("Must Specify template to use")
    if not input_plugin:
        input_plugin = None

    for result in render(_template, data, input_plugin=input_plugin):
        print(result)


if __name__ == "__main__":
    main()
