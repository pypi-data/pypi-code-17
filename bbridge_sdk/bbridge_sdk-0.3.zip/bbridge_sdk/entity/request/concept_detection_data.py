class ConceptDetectionData(object):
    def __init__(self, image_urls, count):
        """
        :type image_urls: list[str]
        :type count: int
        """
        self.__image_urls = image_urls
        self.__count = count

    @property
    def image_urls(self):
        return self.__image_urls

    @property
    def count(self):
        return self.__count
