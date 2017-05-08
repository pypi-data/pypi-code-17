class BaseObject(object):
    def __init__(self, data={}):
        self.set_attributes_from_data(data)

    def set_attributes_from_data(self, data):
        for key in data:
            setattr(self, key, data[key])
