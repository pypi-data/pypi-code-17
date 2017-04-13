
def _flatten(input_obj, key_prefix):
    new_dict = {}
    if type(input_obj) is dict:
        for key, value in input_obj.items():
            if type(value) is dict or type(value) is list or \
                    type(value) is tuple:
                        new_dict.update(
                            _flatten(input_obj[key], key_prefix + key + "_"))
            else:
                new_dict[key_prefix + key] = value
    elif type(input_obj) is list or type(input_obj) is tuple:
        for nr, item in enumerate(input_obj):
            new_dict.update(_flatten(item, key_prefix + str(nr) + "_"))
    else:
        new_dict[key_prefix[:-1]] = input_obj

    return new_dict


def flatten(input_object):
    """Flatten any object into one-level dict representation.

    Args:
        input_object: Python object (list, dict, tuple, int, string, ...)

    Returns:
        dict: Flattened object in dict representation.

    Examples:
        >>> a = {"f": ["a", "b"], "b": {"x": [1, 2, 3]}, "i": 1}
        >>> flatten(a)
        {
            'f_0': 'a',
            'f_1': 'b',
            'b_x_0': 1,
            'b_x_1': 2,
            'b_x_2': 3,
            'i': 1
         }
    """
    return _flatten(input_object, key_prefix="")


if __name__ == "__main__":
    d = {
        "a": 2,
        "b": 3,
        "c": {
            "e": 5,
            "f": 6
        },
        "d": [1, 2, 3, 2, 1],
        "e": [9, 8, 7, [1, 2], {"a": "b"}],
        "x": [[[[[{
            "foo": "bar"
        }]], [{
            "bar": "foo"
        }]]]],
        "g": [{
            "x": [1, 2, 3]
        }, {
            "y": "ahoj"
        }, {
            "z": 42
        }]
    }

    d_expected = {
        "a": 2,
        "b": 3,
        "c_e": 5,
        "c_f": 6,
        "d_0": 1,
        "d_1": 2,
        "d_2": 3,
        "d_3": 2,
        "d_4": 1,
        "e_0": 9,
        "e_1": 8,
        "e_2": 7,
        "e_3_0": 1,
        "e_3_1": 2,
        "e_4_a": "b",
        "x_0_0_0_0_0_foo": "bar",
        "x_0_0_1_0_bar": "foo",
        "g_0_x_0": 1,
        "g_0_x_1": 2,
        "g_0_x_2": 3,
        "g_1_y": "ahoj",
        "g_2_z": 42
    }
    result = flatten(d)
    print("in  ", d)
    print("out ", result)
    for key in result.keys():
        assert (result[key] == d_expected[key])
    print("Test successful")
