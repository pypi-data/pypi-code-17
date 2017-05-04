# coding=utf-8


def get_unique_keys(d):
    total_keys = []
    for obj in d:
        for key in obj.keys():
            if key in total_keys:
                continue

            total_keys.append(key)

    return total_keys


def dict_to_csv(d, fields):
    total_keys = fields or sorted(get_unique_keys(d))

    yield total_keys

    def get_row():
        for key in total_keys:
            yield obj.get(key, '')

    if isinstance(d, dict):
        d = [d]

    for obj in d:
        yield list(get_row())
