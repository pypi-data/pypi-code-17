class User(object):
    def __init__(self, text=[], image_urls=[]):
        """
        :type text: list[str]
        :type image_urls: list[str]
        """
        self.__text = text
        self.__image_urls = image_urls

    @property
    def text(self):
        return self.__text

    @property
    def image_urls(self):
        return self.__image_urls
