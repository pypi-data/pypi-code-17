from .bbridge_entity import BBridgeEntity


class Sentiments(BBridgeEntity):
    def __init__(self, results):
        """
        :type results: list[float]
        """
        self.__results = results

    @classmethod
    def from_json(cls, json_object):
        return Sentiments(json_object["results"])

    @property
    def results(self):
        return self.__results
