"""
Input/Output image file with options.
"""

class ImageFile:
    """
    Image file object with ffmpeg options.
    """

    def __init__(self, **kwargs):
        self.__file_name = kwargs.get('file_name')
        self.__options = kwargs.get('options')



    def get_file_name(self):
        """
        get file name.
        """
        return self.__file_name

    def set_file_name(self, file_name):
        """
        set file name.
        :param file_name: file name.
        """
        self.__file_name = file_name

    file_name = property(get_file_name, set_file_name)

    def get_options(self):
        """
        getter of options
        """
        return self.__options

    def set_options(self, options):
        """
        setter of options
        """
        self.__options = options

    options = property(get_options, set_options)

    def get_options_string(self):
        """
        returns option string
        :returns: option string
        """
        if self.__options is None:
            return None

        options_string = ' -vf'
        for opt in self.__options.options:
            options_string = options_string + ' ' + opt
        return options_string

    options_string = property(get_options_string)

    def get_file_property(self):
        """
        get the image file property
        Todo: implement.
        """
        pass




  