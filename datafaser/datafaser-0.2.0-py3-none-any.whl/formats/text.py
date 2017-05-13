import numbers


def read(stream):
    return stream.read()


def write(data, stream):
    if isinstance(data, str) or isinstance(data, numbers.Number):
        stream.write(str(data))
    else:
        raise TypeError('Can not write "%s" as text' % type(data))
