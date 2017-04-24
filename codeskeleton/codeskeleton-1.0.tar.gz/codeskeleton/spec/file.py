import os

from codeskeleton import exceptions
from codeskeleton.spec.abstract_spec_object import AbstractSpecObject


class FileSystemWriter(object):
    """
    A file-system writer for a :class:`.File`.
    """
    def __init__(self, file, output_directory, template_environment):
        """

        Args:
            file: A :class:`.File`.
            output_directory: The root directory to write the file relative to.
            template_environment (jinja2.environment.Environment): The template enviroment,
                normally created with :func:`codeskeleton.template.make_environment`.

        """
        self.file = file
        self.output_directory = output_directory
        self.template_environment = template_environment

    def get_absolute_output_path(self):
        """
        Get the absolute output path to write the file to.
        """
        relative_path = self.file.get_output_path(template_environment=self.template_environment)
        if relative_path.startswith('/'):
            raise exceptions.FileSpecError(
                path=self.file.path,
                message='Path evaluates to {!r}, which starts with /. This is not allowed. '
                        'You probably have some error in your template variables.'.format(relative_path)
            )
        return os.path.abspath(os.path.join(self.output_directory, relative_path))

    def output_path_exists(self):
        """
        Returns ``True`` if the :meth:`.get_output_path` already exists.
        """
        return os.path.exists(self.get_absolute_output_path())

    def get_content(self):
        """
        Get the content to write to the output file.
        """
        return self.file.get_content(template_environment=self.template_environment)

    def write(self):
        """
        Write the file contents to disk.
        """
        output_path = self.get_absolute_output_path()
        directory = os.path.dirname(output_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(output_path, 'wb') as f:
            f.write(self.get_content().encode('utf-8'))


class File(AbstractSpecObject):
    """
    Defines a file to generate.

    Files are generated from one of:

    - ``content``: A string with static content (no templating).
    - ``contentpath``: A file with static content (no templating).
    - ``template``: A string with a jinja2 template.
    - ``templatepath``: A file with a jinja2 template.

    The jinja2 templates does not use the standard block, variable and comment
    start/end strings. See :func:`codeskeleton.template.make_environment`.

    The jinja2 templates has all the variables within the spec as context variables.
    """
    def __init__(self, path,
                 content=None, contentpath=None, template=None, templatepath=None):
        self.path = path
        self.content = content
        self.contentpath = contentpath
        self.template = template
        self.templatepath = templatepath

    def deserialize(self, data):
        """
        Deserialize the provided data.

        Args:
            data (dict): A dict like object with one of the following key/value pairs:

                - ``content`` (optional): A string with static content (no templating).
                - ``contentpath`` (optional): A file with static content (no templating).
                - ``template`` (optional): A string with a jinja2 template.
                - ``templatepath (optional)``: A file with a jinja2 template.

                They are checked in this order, so if you provided both ``content`` and
                ``templatepath``, only ``content`` is used.
        """
        if 'content' in data:
            self.content = data.get('content')
        elif 'contentpath' in data:
            self.contentpath = data.get('contentpath')
        elif 'template' in data:
            self.template = data.get('template')
        elif 'templatepath' in data:
            self.templatepath = data.get('templatepath')

    def _read_file(self, template_environment, path):
        return template_environment.loader.get_source(environment=template_environment,
                                                      template=path)[0]

    def get_output_path(self, template_environment):
        """
        Get the real output path.

        Parses the ``path`` as a template and returns the result.

        Args:
            template_environment (jinja2.environment.Environment): The template enviroment,
                normally created with :func:`codeskeleton.template.make_environment`.

        Normally not used directly, but used rather used indirectly when using
        :meth:`~codeskeleton.spec.file.FileSystemWriter.get_absolute_output_path`
        on the :class:`.FileSystemWriter` returned by :meth:`.get_filesystem_writer`.
        """
        return template_environment.from_string(self.path).render()

    def get_content(self, template_environment):
        """
        Get the content of the file as it should be written to disk (parsed as a
        template if using ``template`` or ``templatepath``.

        Args:
            template_environment (jinja2.environment.Environment): The template enviroment,
                normally created with :func:`codeskeleton.template.make_environment`.

        Returns:
            str: The content of the output file.
        """
        if self.content is not None:
            return self.content
        if self.contentpath is not None:
            return self._read_file(template_environment=template_environment,
                                   path=self.contentpath)
        if self.template:
            return template_environment.from_string(self.template).render()
        if self.templatepath:
            return template_environment.get_template(self.templatepath).render()

    def get_filesystem_writer(self, output_directory, template_environment):
        """
        Get a :class:`.FileSystemWriter` for this file.

        Args:
            output_directory: The root directory to write the relative file to.
            template_environment (jinja2.environment.Environment): The template enviroment,
                normally created with :func:`codeskeleton.template.make_environment`.

        Returns:
            .FileSystemWriter: A FileSystemWriter for this file.
        """
        return FileSystemWriter(file=self,
                                output_directory=output_directory,
                                template_environment=template_environment)
