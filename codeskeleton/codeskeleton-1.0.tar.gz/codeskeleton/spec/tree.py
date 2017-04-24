from codeskeleton.spec.abstract_toplevel import AbstractToplevel
from codeskeleton.spec.files import Files


class Tree(AbstractToplevel):
    """
    Defines the spec for generating a directory tree.
    """
    def __init__(self, base_directory, id=None, title=None, description=None,
                 context=None, variables=None, files=None):
        """

        Args:
            base_directory: Base directory where the files for the spec template files are located.
                Normally the directory where the spec file is located.
            id: The ID of the tree spec. Used to uniquely identify this tree spec.
            title (optional): Short user friendly description of what this tree spec creates.
            description (optional): Long user friendly description of what this tree spec creates.
            context (optional): The context this tree spec belongs to. Typically the programming
                language (python, javascript, ...), or the framework (django, react, ...) or
                a project name for a project specific tree spec. Must be a single word, all in
                lowercase (can only contain a-z and numbers).
            variables (codeskeleton.spec.variables.Variables): Variable definitions for the spec.
            files (codeskeleton.spec.files.Files): Output file definitions for the spec.
        """
        self.files = files or Files()
        super(Tree, self).__init__(
            base_directory, id=id, title=title, description=description,
            context=context, variables=variables)

    def deserialize(self, data):
        """
        Deserialize the provided data.

        Args:
            data: Same format as :meth:`codeskeleton.spec.abstract_toplevel.AbstractToplevel.deserialize`
                with the following additional key value pairs:

                - ``files`` (optional): Data on a format that can be parsed by
                  :meth:`codeskeleton.spec.files.Files.deserialize`.
        """
        super(Tree, self).deserialize(data)
        self.files = Files()
        self.files.deserialize(data.get('files', {}))

    def collect_writers(self, output_directory, overwrite=False):
        """
        Collect :class:`writers <codeskeleton.spec.file.FileSystemWriter>` for
        the tree.

        Does not write any files, but collects the writers that can be used
        to write the files, and information about skipped writers for files
        that should not be overwritten.

        Args:
            output_directory:
            overwrite (bool): Overwrite existing files? Defaults to ``False``.

        Returns:
            tuple: A ``(skipped_writers, writers)`` tuple where:

            - ``skipped_writers`` is a list of :class:`codeskeleton.spec.file.FileSystemWriter`
              objects that should be skipped (not written). This will always be empty if
              ``overwrite=True``.
            - ``writers`` is a list of :class:`codeskeleton.spec.file.FileSystemWriter`
              objects that should be written to disk.
        """
        template_environment = self.make_template_environment()
        skipped_writers = []
        writers = []
        for file in self.files:
            writer = file.get_filesystem_writer(output_directory=output_directory,
                                                template_environment=template_environment)
            if writer.output_path_exists() and not overwrite:
                skipped_writers.append(writer)
            else:
                writers.append(writer)
        return skipped_writers, writers
