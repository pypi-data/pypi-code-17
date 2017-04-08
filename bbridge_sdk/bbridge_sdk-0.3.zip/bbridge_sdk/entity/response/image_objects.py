from .bbridge_entity import BBridgeEntity


class ImageObjects(BBridgeEntity):
    def __init__(self, objects):
        """
        :type objects: list[bbridge_sdk.entity.response.image_objects.Object]
        """
        self.__objects = objects

    @classmethod
    def from_json(cls, json_object):
        objects = [Object.from_json(x) for x in json_object["objects"]]
        return ImageObjects(objects)

    @property
    def objects(self):
        return self.__objects


class Object(BBridgeEntity):
    def __init__(self, cls_name, score, x, y, w, h):
        """
        :type cls_name: str
        :type score: float
        :type x: float
        :type y: float
        :type w: float
        :type h: float
        """
        self.__cls_name = cls_name
        self.__score = score
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h

    @classmethod
    def from_json(cls, json_object):
        return Object(json_object["cls_name"], json_object["score"], json_object["x"], json_object["y"],
                      json_object["w"], json_object["h"])

    @property
    def cls_name(self):
        return self.__cls_name

    @property
    def score(self):
        return self.__score

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def w(self):
        return self.__w

    @property
    def h(self):
        return self.__h
