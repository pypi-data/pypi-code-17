"""
Operations on plain deep data structures.
"""


class DataTree:
    """
    Data object contains a free form data structure.

    Nested dictionaries and lists can be accessed with key lists.

    Dictionary contents can be merged and lists appended to.

    Other data types can only be stored as leaves of the data tree structure.
    """

    def __init__(self, data, separator='.'):
        self.data = data is None and {} or data
        self.separator = separator

    def reach(self, key_path, create_containers=False):
        """
        Get an object from deep within this data tree.

        :param key_path: a list of keys or a string with keys combined by separator characters (default is ".")
        :param create_containers: whether to fail on or create missing keys on the path
        :return: object at the point specified by key_path
        """
        return self._reach_to(key_path, create_containers)[0]

    def _reach_to(self, key_path, create_containers=False, set_key=None, set_value=None):
        if isinstance(key_path, str):
            key_path = key_path.split(self.separator)
        data = self.data

        for index, key in enumerate(key_path):
            if isinstance(data, dict):
                if key not in data:
                    if create_containers:
                        data[key] = {}
                    else:
                        raise KeyError('Missing "%s" in "%s"' % (key, self.separator.join(key_path[:index])))
                data = data[key]
            elif isinstance(data, list):
                try:
                    data = data[int(key)]
                except Exception as e:
                    raise KeyError('Invalid list index "%s" at "%s": %s %s' %
                        (key, self.separator.join(key_path[:index]), e.__class__.__name__, str(e)))
            else:
                raise KeyError('No container at "%s" trying to get "%s"' %
                    (self.separator.join(key_path[:index]), self.separator.join(key_path)))

        if set_key:
            data[set_key] = set_value

        return data, key_path

    def merge(self, add_data, key_path=None):
        if key_path and len(key_path):
            my_data, key_path = self._reach_to(key_path, create_containers=True)
        else:
            my_data = self.data
            key_path = []

        result = self._merge_node(add_data, my_data, {})

        if len(key_path):
            self._reach_to(key_path[:-1], set_key=key_path[-1], set_value=result)
        else:
            self.data = result

    def _merge_node(self, add_data, my_data, results):
        if isinstance(add_data, dict):
            if isinstance(my_data, dict):
                return self._merge_dictionaries(add_data, my_data, results)
        elif isinstance(add_data, list):
            if isinstance(my_data, list):
                return my_data + add_data

        return add_data

    def _merge_dictionaries(self, add_data, my_data, results):

        my_id = id(my_data)
        if my_id in results:  # cyclic reference already being merged.
            return results[my_id]

        new_data = my_data.copy()
        results[my_id] = new_data

        for key, value in add_data.items():
            if key in my_data:
                new_data[key] = self._merge_node(value, my_data[key], results)
            else:
                new_data[key] = value
        
        return new_data

