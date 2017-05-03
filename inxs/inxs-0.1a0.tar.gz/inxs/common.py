def sorter(object_name, key):
    def wrapped(transformation):
        return sorted(transformation._available_dependencies[object_name], key=key)
    return wrapped
