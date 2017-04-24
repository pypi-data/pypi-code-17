import clipboard

from codeskeleton import exceptions
from codeskeleton.spec.abstract_toplevel import AbstractToplevel


class Snippet(AbstractToplevel):
    """
    Defines the spec for generating a directory tree.
    """
    def __init__(self, base_directory, id=None, title=None, description=None, variables=None,
                 context=None, template=None, templatepath=None):
        """

        Args:
            base_directory: Base directory where the files for the spec template files are located.
                Normally the directory where the spec file is located.
            id: The ID of the snippet spec. Used to uniquely identify this snippet spec.
            title (optional): Short user friendly description of what this snippet spec creates.
            description (optional): Long user friendly description of what this snippet spec creates.
            context (optional): The context this snippet spec belongs to. Typically the programming
                language (python, javascript, ...), or the framework (django, react, ...) or
                a project name for a project specific snippet spec. Must be a single word, all in
                lowercase (can only contain a-z and numbers).
            variables (codeskeleton.spec.variables.Variables): Variable definitions for the spec.
            template (str): Jinja2 template as a string.
                See :func:`codeskeleton.template.make_environment` for the codeskeleton
                specific variabe and block syntax for jinja2 templates.
            templatepath (str): Jinja2 template as a string.
                See :func:`codeskeleton.template.make_environment` for the codeskeleton
                specific variabe and block syntax for jinja2 templates.
        """
        self.template = template
        self.templatepath = templatepath
        super(Snippet, self).__init__(
            base_directory, id=id, title=title, description=description,
            context=context, variables=variables)

    def deserialize(self, data):
        """
        Deserialize the provided data.

        Args:
            data: Same format as :meth:`codeskeleton.spec.abstract_toplevel.AbstractToplevel.deserialize`
                with the following additional key value pairs:

                - ``template`` (optional): See :meth:`.__init__`.
                - ``templatepath`` (optional): See :meth:`.__init__`.
        """
        super(Snippet, self).deserialize(data)
        self.template = data.get('template')
        self.templatepath = data.get('templatepath')

    def render(self, keep_end_marker=False):
        """
        Render the snippet.

        Returns:
            str: The resulting snippet after applying the variables to the template or
                templatepath jinja2 templates.
        """
        template_environment = self.make_template_environment()
        if self.template:
            result = template_environment.from_string(self.template).render()
        else:
            result = template_environment.get_template(self.templatepath).render()
        if not keep_end_marker:
            result = result.replace('$$$END$$$', '')
        return result

    def render_to_clipboard(self, keep_end_marker=False):
        """
        Renders the snippet using :meth:`.render`, and copies the result to the clipboard.
        """
        clipboard.copy(self.render(keep_end_marker=keep_end_marker).encode('utf-8'))

    def validate_spec(self):
        super(Snippet, self).validate_spec()
        if self.template is None and not self.templatepath:
            raise exceptions.SpecValidationError(
                path='template|templatepath',
                message='"template" or "templatepath" is required for a snippet spec.'
            )
