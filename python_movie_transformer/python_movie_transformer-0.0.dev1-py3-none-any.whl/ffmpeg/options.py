class ImageFileOptions:
    def __init__(self):
        self.__options = []
        self.__scale = None

    def set_scale(self, width):
        """
        change the size of image with maintaining
        the aspect ratio from the original image.
        :param width: Resulting image width (px)
        """
        self.__scale = 'scale='+str(width)+':-1'
        self.__options.append(self.__scale)


    def get_options(self):
        return self.__options

    options = property(get_options)
    