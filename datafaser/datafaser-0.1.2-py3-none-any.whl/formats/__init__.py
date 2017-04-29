default_settings = {
    'format_handlers_by_name': {
        'csv': 'datafaser.formats.csv',
        'yaml': 'datafaser.formats.yaml',
        'json': 'datafaser.formats.json',
        'text': 'datafaser.formats.text',
        'xml': 'datafaser.formats.xml',
        'ignore': None
    },
    'formats_by_filename_extension': {
        'ignore': 'ignore',
        'csv': 'csv',
        'json': 'json',
        'xml': 'xml',
        'yaml': 'yaml',
        'yml': 'yaml',
        'skip': 'ignore',
        'text': 'text',
        'txt': 'text'
    }
}


class FormatRegister:
    """
    FormatRegister provides extensible reference point for file formats.
    You can provide a custom FormatRegister for access to files in exceptional formats.
    Default is to provide datafaser.formats.*

    Each format is only imported when actually used, so that applications that do not use
    formats such as yaml do not need to depend on unnecessary external libraries.

    Each format module provides functions to read and write streams in that format.
    """

    def __init__(self, format_handlers_by_name, formats_by_filename_extension):
        self.format_handlers_by_name = format_handlers_by_name
        self.formats_by_filename_extension = formats_by_filename_extension

    def get_format_by_name(self, name):
        """
        :param name: string: name of format
        :return: Any: module implementing the format or None to ignore it
        """

        if name in self.format_handlers_by_name:
            module_name = self.format_handlers_by_name[name]
            if module_name is None:
                return None
            namespace, relative_name = module_name.rsplit('.', 1)
            return __import__(module_name, fromlist=[relative_name])
        else:
            raise KeyError('Unknown format name: "%s"' % name)

    def get_format_by_filename_extension(self, extension):
        if extension not in self.formats_by_filename_extension:
            raise KeyError('Unknown filename extension: "%s"' % extension)
        return self.get_format_by_name(self.formats_by_filename_extension[extension])

    def is_known_format_name(self, name):
        return name in self.format_handlers_by_name

    def is_known_filename_extension(self, extension):
        return extension in self.formats_by_filename_extension

    def register(self, module_name, format_name, filename_extension_list=None):
        self.format_handlers_by_name[format_name] = module_name
        if filename_extension_list:
            for extension in filename_extension_list:
                self.formats_by_filename_extension[extension] = format_name

    def unregister(self, format_name):
        del self.format_handlers_by_name[format_name]
        self.formats_by_filename_extension = {
            key: value for key, value in self.formats_by_filename_extension.items() if value != format_name
        }
