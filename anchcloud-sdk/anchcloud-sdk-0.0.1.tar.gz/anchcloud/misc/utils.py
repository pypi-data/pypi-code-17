from anchcloud.iaas.errors import InvalidParameterError


def err_occur(error_msg):
    raise InvalidParameterError(error_msg)


def is_integer(param, value):
    try:
        int(value)
    except:
        err_occur("parameter [%s] should be integer in directive [%s]" % (param, value))
    return True


def check_params(directive, required_params=None, integer_params=None):
    if not isinstance(directive, dict):
        err_occur('[%s] should be dict type' % directive)
        return False
    if required_params:
        check_required_params(directive, required_params)
    if integer_params:
        check_integer_params(directive, integer_params)
    return True


def check_integer_params(directive, params):
    """ Specified params should be `int` type if in directive
    @param directive: the directive to check
    @param params: the params that should be `int` type.
    """
    for param in params:
        if param not in directive:
            continue
        val = directive[param]
        if not isinstance(val, int):
            if is_integer(param, val):
                directive[param] = int(val)


def check_required_params(directive, params):
    key_list = []
    for k, v in directive.items():
        key_list.append(k)
        if isinstance(v, dict):
            for key, val in v.items():
                key_list.append(key)
    # print 1111111111111
    # print key_list
    # print 2222222222222
    for param in params:
        if param not in key_list:
            err_occur(
                "[%s] should be specified in directive [%s]" % (param, directive))
