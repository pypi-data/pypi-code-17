from collections import defaultdict


def merge_dict(*dicts):
    d = defaultdict(dict)
    for dd in dicts:
        for k, v in dd.items():
            d[k] = v
    return d
