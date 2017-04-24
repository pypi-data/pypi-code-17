from codeskeleton.spec.abstract_spec_object import AbstractSpecObject
from codeskeleton.spec.file import File


class Files(AbstractSpecObject):
    """
    Defines files to generate.
    """
    def __init__(self):
        self._files = []

    def deserialize(self, data):
        """
        Deserialize the provided data.

        Args:
            data (dict): A map object, such as an OrderedDict or a dict. Maps
                file-paths to valid data for :meth:`codeskeleton.spec.file.File.deserialize`.
        """
        for path, file_data in data.items():
            file = File(path=path)
            file.deserialize(file_data)
            self._files.append(file)

    def add_files(self, *files):
        """
        Add files.

        Args:
            *files: One or more :class:`codeskeleton.spec.file.File` object.
        """
        for file in files:
            self._files.append(file)

    def __iter__(self):
        """
        Iterate the files. Returns an iterator yielding
        :class:`codeskeleton.spec.file.File` objects.
        """
        return iter(self._files)

    def __len__(self):
        """
        Get the number of files in the Files object.
        """
        return len(self._files)
