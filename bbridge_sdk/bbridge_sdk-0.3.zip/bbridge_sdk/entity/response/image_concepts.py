from .bbridge_entity import BBridgeEntity


class ImagesConcepts(BBridgeEntity):
    def __init__(self, results):
        """
        :type results: list[bbridge_sdk.entity.response.image_concepts.Concepts]
        """
        self.__results = results

    @classmethod
    def from_json(cls, json_object):
        results = [Concepts.from_json(x) for x in json_object["results"]]
        return ImagesConcepts(results)

    @property
    def results(self):
        return self.__results


class Concepts(BBridgeEntity):
    def __init__(self, concepts=None, error=None):
        """
        :type concepts: dict | None
        :type error: str | None
        """
        self.__concepts = concepts
        self.__error = error

    @classmethod
    def from_json(cls, json_object):
        return Concepts(json_object.get("concepts"), json_object.get("error"))

    @property
    def concepts(self):
        return self.__concepts

    @property
    def error(self):
        return self.__error
