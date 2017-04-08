from .bbridge_entity import BBridgeEntity


class RequestId(BBridgeEntity):
    def __init__(self, request_id):
        """
        :type request_id: str
        """
        self.__request_id = request_id

    @classmethod
    def from_json(cls, json_object):
        return cls(json_object["request_id"])

    @property
    def request_id(self):
        return self.__request_id
