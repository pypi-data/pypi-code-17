class NLPData(object):
    def __init__(self, sentences):
        """
        :type sentences: list[str]
        """
        self.__sentences = sentences

    @property
    def sentences(self):
        return self.__sentences
