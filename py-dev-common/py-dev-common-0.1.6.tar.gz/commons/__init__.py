class ResultItem(dict):
    @staticmethod
    def from_dict(d):
        ret = ResultItem(**d)
        return ret

    @staticmethod
    def _parse_item(x):
        if isinstance(x, dict):
            return ResultItem.from_dict(x)
        elif isinstance(x, (set, list, tuple)) and len(x) > 0:
            return [ResultItem._parse_item(y) for y in x]
        else:
            return x

    def __setattr__(self, key, value):
        if isinstance(value, (set, list, tuple)) and len(value) > 0:
            super().__setitem__(key, ResultItem._parse_item(value))
        elif not isinstance(value, ResultItem) and isinstance(value, dict):
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
        if not isinstance(value, ResultItem) and isinstance(value, (dict, list, set, tuple)) and len(value) > 0:
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


class ApiException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


PLATFORM_IOS = 'ios'
PLATFORM_ANDROID = 'android'
PLATFORM_WEB = 'web'
PLATFORM_WX = 'wx'
PLATFORM_WX_CYCLE = 'wxcycle'
PLATFORM_TRD = 'trd'
