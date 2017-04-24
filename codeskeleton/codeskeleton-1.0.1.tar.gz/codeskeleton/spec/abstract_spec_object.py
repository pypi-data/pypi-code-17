class AbstractSpecObject(object):
    def deserialize(self, data):
        raise NotImplementedError()

    def validate_spec(self, path):
        raise NotImplementedError()
