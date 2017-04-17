from collections import defaultdict


def partition(data, min_num):
    """
    This methods divides the entire list to a subset where the content have apears greater than a specified value.


    data contains the list of IDs
    min_num is the threshold used to partition it into sets.

    :param data: list
    :param min_num: integer
    :return: list
    """
    count = defaultdict(int)
    for i in data:
        count[i] += 1
    final_set = []
    for i in count.keys():
        if count[i] > min_num:
            final_set.append(i)
    return final_set


def min_max_normalize(data, min, max):
    r = []
    for i in data:
        value = i - min
        value = value / (max - min)
        r.append(value)
    return r
