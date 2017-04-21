import re
import json

def camel_to_dashed(camel):
    return re.sub('([a-z])([A-Z])', '\g<1>-\g<2>', camel).lower()


def format_as_text(data, out, sep="\t"):
    """
    Format a data structure as text. This is a rather simple (or possibly oversimplified)
    algorithm for turning json-like data-structures into delimited text.

    :param out:
    :param data:
    :param sep:
    :return:
    """
    if type(data) is list:
        rows = data
    else:
        rows = [data]
    for row in rows:
        print(format_text_row(row, sep), file=out)


def format_text_row(data, sep="\t"):
    """
    Simple object formatting of a single 'row' to be output as plain text.

    A dict will be output as a set of delimited values (no keys are output).

    A list is just a delimited set of its values

    Anything else is just the str() representation of the object.

    :param data:
    :param sep:
    :return:
    """
    if type(data) == dict:
        # Delimited string of dict values sorted by *key* - to give predictable ordering.
        return sep.join([str(v) for k,v in sorted(data.items(), key=lambda i: i[0])])
    elif type(data) == list:
        return sep.join([str(v) for v in data])
    else:
        # Scalar (are there other types to worry about here... e.g. class instance?)
        return str(data)


def format_as_json(data, out):
    print(json.dumps(data, indent=4), file=out)
