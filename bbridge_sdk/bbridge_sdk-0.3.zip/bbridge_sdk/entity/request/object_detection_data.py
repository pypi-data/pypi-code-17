class ObjectDetectionData(object):
    def __init__(self, url, threshold):
        """
        :type url: str
        :type threshold: float
        """
        self.__url = url
        self.__threshold = threshold

    @property
    def url(self):
        return self.__url

    @property
    def threshold(self):
        return self.__threshold
