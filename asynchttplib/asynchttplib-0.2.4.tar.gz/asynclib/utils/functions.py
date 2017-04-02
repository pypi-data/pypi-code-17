from random import randint


def filter_only_keys(dictionary, keys):
    filtered = {}
    for k in keys:
        value = dictionary.get(k)
        if value is not None:
            filtered[k] = value
    return filtered


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def get_from_dict(data, path):
    path = path.split('.')
    if len(path) == 1:
        try:
            return data.get(path[0])
        except AttributeError:
            try:
                return getattr(data, path[0])
            except AttributeError:
                return None
    else:
        try:
            data = data.get(path[0])
        except AttributeError:
            data = getattr(data, path[0])
        return get_from_dict(data, '.'.join(path[1:]))


