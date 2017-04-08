from .bbridge_entity import BBridgeEntity


class NER(BBridgeEntity):
    def __init__(self, results):
        """
        :type results: list[list[bbridge_sdk.entity.response.ner.Entity]]
        """
        self.__results = results

    @classmethod
    def from_json(cls, json_object):
        results = [[Entity.from_json(x) for x in xs] for xs in json_object["results"]]
        return NER(results)

    @property
    def results(self):
        return self.__results


class Entity(BBridgeEntity):
    def __init__(self, count, text, entity_type):
        """
        :type count: int
        :type text: str
        :type entity_type: str
        """
        self.__count = count
        self.__text = text
        self.__type = entity_type

    @classmethod
    def from_json(cls, json_object):
        return Entity(json_object["count"], json_object["text"], json_object["type"])

    @property
    def count(self):
        return self.__count

    @property
    def text(self):
        return self.__text

    @property
    def type(self):
        return self.__type
