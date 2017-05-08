class ResultItem(dict):
    def __setattr__(self, key, value):
        if not isinstance(value, ResultItem) and isinstance(value, dict):
            self[key] = ResultItem()
            for k, v in value.items():
                self[key].__setattr__(k, v)
        else:
            self[key] = value

    def __getattr__(self, key):
        return self.get(key)

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        if not isinstance(value, ResultItem) and isinstance(value, dict):
            self.__setattr__(key, value)
        else:
            super().__setitem__(key, value)

    def __init__(self, **kwargs):
        super().__init__()
        for argk, argv in kwargs.items():
            self[argk] = argv


class ApiResult(ResultItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
