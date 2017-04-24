import os
import textwrap
from collections import OrderedDict

import fire
import sys

from codeskeleton import exceptions
from codeskeleton import spec
from codeskeleton.cli import cliutils
from codeskeleton.cli import colorize
from codeskeleton.config import Config


class Cli(object):
    """
    TODO: Help
    """

    def __get_config(self):
        return Config.load_or_create()

    def __is_skeleton_directory(self, directory):
        return os.path.isdir(os.path.join(directory, 'trees')) or \
               os.path.isdir(os.path.join(directory, 'snippets'))

    def __validate_skeleton_directory(self, directory):
        if not self.__is_skeleton_directory(directory):
            cliutils.print_error('{!r} is not a codeskeleton directory. Must have '
                                 'a "trees" or a "snippets" subdirectory.'.format(directory))
            raise SystemExit()

    def __print_variables_help(self, variables):
        for variable in variables.iterate_input_variables():
            suffix = ''
            if variable.is_required():
                suffix = colorize.colored_text('    [REQUIRED]', color=colorize.COLOR_YELLOW,
                                               bold=True)
            cliutils.safe_print('--{} <value>{}'.format(variable.name.replace('_', '-'), suffix))
            indent = '    '
            if variable.help_text:
                cliutils.safe_print(textwrap.indent(
                    textwrap.fill(variable.help_text),
                    indent))
            if variable.default:
                if variable.default.variable:
                    message = 'Defaults to the value of the {!r} variable.'.format(
                        variable.default.variable)
                else:
                    message = 'Defaults to {!r}.'.format(variable.default.value)
                cliutils.safe_print(textwrap.indent(message, indent))

    def __print_spec_help(self, toplevel_spec):
        cliutils.safe_print('')
        cliutils.print_bold('ABOUT:')
        cliutils.safe_print('id: {}'.format(toplevel_spec.full_id))
        if toplevel_spec.title:
            cliutils.safe_print(toplevel_spec.title)
        if toplevel_spec.description:
            cliutils.safe_print('')
            cliutils.safe_print(toplevel_spec.description)
        cliutils.safe_print('')

        if toplevel_spec.variables:
            cliutils.print_bold('VARIABLES:')
            self.__print_variables_help(variables=toplevel_spec.variables)

    def __group_specs_by_context(self, specs):
        grouped_specs = OrderedDict()
        for spec_object in sorted(specs, key=lambda s: s.full_id):
            if spec_object.context not in grouped_specs:
                grouped_specs[spec_object.context] = []
            grouped_specs[spec_object.context].append(spec_object)
        return grouped_specs

    def __list_specs(self, spec_class, create_command_name, quiet=False):
        config = self.__get_config()
        specs = spec.FileSystemLoader(config, spec_class).find()
        for context, spec_objects in self.__group_specs_by_context(specs).items():
            if not quiet:
                cliutils.safe_print('')
                cliutils.print_bold('{}:'.format(context))
            for spec_object in spec_objects:
                output = spec_object.full_id
                if not quiet and spec_object.title:
                    output = '{} ({})'.format(output, spec_object.title)
                cliutils.safe_print('- {}'.format(output))
        if not quiet:
            cliutils.safe_print('')
            cliutils.print_bold('Use:')
            cliutils.safe_print(
                '{prefix} {scriptname} {create_command_name} <id> --help'.format(
                    prefix=colorize.colored_text('$ ', color=colorize.COLOR_GREY, bold=True),
                    scriptname=os.path.basename(sys.argv[0]),
                    create_command_name=create_command_name))
            cliutils.print_bold('to show usage help for a {}.'.format(spec_class.__name__.lower()))

    def register(self, directory=None):
        """
        Register a skeleton directory.

        --directory
            The directory to register. Must be a directory
            with a ``trees`` or ``snippets`` subdirectory.
            Defaults to the current directory.
        """
        directory = directory or os.getcwd()
        self.__validate_skeleton_directory(directory=directory)
        config = self.__get_config()
        absolute_directory_path = os.path.abspath(directory)
        if config.has_spec_directory(directory):
            cliutils.print_warning('{!r} is already registered as a skeleton directory.'.format(
                absolute_directory_path))
        else:
            config.register_spec_directory(directory)
            config.save_to_disk()
            cliutils.print_success('{!r} is now registered as a skeleton directory.'.format(
                absolute_directory_path))

    def unregister(self, directory=None):
        """
        Unregister a skeleton directory.

        --directory
            The directory to unregister. Must be a directory
            with a ``trees`` or ``snippets`` subdirectory.
            Defaults to the current directory.
        """
        directory = directory or os.getcwd()
        self.__validate_skeleton_directory(directory=directory)
        config = self.__get_config()
        absolute_directory_path = os.path.abspath(directory)
        if config.has_spec_directory(directory):
            config.unregister_spec_directory(directory)
            config.save_to_disk()
            cliutils.print_success('{!r} is no longer registered as a skeleton directory.'.format(
                absolute_directory_path))
        else:
            cliutils.print_error('{!r} is not a registered skeleton directory.'.format(
                absolute_directory_path))
            raise SystemExit()

    def list_directories(self):
        config = self.__get_config()
        for spec_directory in sorted(config.spec_directories):
            cliutils.safe_print('- {}'.format(spec_directory))

    def list_trees(self, quiet=False):
        self.__list_specs(spec_class=spec.Tree, quiet=quiet,
                          create_command_name='create-tree')

    def __print_create_tree_preview(self, writers, skipped_writers, previewmode='short'):
        if previewmode == 'none':
            return
        if writers:
            for writer in writers:
                cliutils.print_success(writer.get_absolute_output_path())
                if previewmode == 'filenames':
                    continue
                content = writer.get_content().strip()
                if not content:
                    content = '--- EMPTY FILE ---'
                if previewmode != 'full':
                    contentlines = content.split('\n')
                    if len(contentlines) > 3:
                        contentlines = contentlines[:3]
                        contentlines.append('...')
                    content = '\n'.join(contentlines)
                    # if len(contentlines) > 3:
                    #     cliutils.print_blue('...')
                cliutils.safe_print(textwrap.indent(content, prefix='    '))
                cliutils.safe_print('')
        if skipped_writers:
            cliutils.print_warning('Will skip the following files - they already exist:')
            for writer in skipped_writers:
                cliutils.safe_print('- {}'.format(writer.get_absolute_output_path()))
            cliutils.print_bold('Use --overwrite to overwrite these files.')
        if not writers:
            cliutils.print_warning('All files already exist.')

    def __get_tree_by_id(self, config, full_id):
        tree_cache = spec.SpecCache(*spec.FileSystemLoader(config, spec.Tree).find())
        try:
            return tree_cache.get_spec(full_id)
        except KeyError:
            cliutils.print_error('No tree skeleton with this id: {}'.format(full_id))
            raise SystemExit()

    def __validate_values(self, variables, valuedict):
        errors = []
        for variable in variables.iterate_input_variables():
            value = valuedict.get(variable.name, None)
            if value is None:
                if variable.is_required():
                    errors.append('Variable {!r}: This variable is required.'.format(variable.name))
            else:
                try:
                    variable.validate_value(value=value)
                except exceptions.ValueValidationError as error:
                    errors.append('Variable {!r}: {}'.format(variable.name, error))
        if errors:
            for error in errors:
                cliutils.print_error(error)
            cliutils.safe_print('')
            cliutils.print_bold('Try adding --help for documentation for all the variables.')
            raise SystemExit()

    def create_tree(self, id, out=None, overwrite=False,
                    preview='short', help=False, pretend=False, **variables):
        """
        Create a directory tree from a ``skeleton.tree.yaml`` file.

        --id <id>
            The ID of a tree skeleton spec. Use "list-trees" to list all available IDs.
            REQUIRED.
        --help
            Show help for the the tree spec. This includes information about the
            tree spec, and all the available variables.
        --out <directory>
            The output directory. Will be created if it does not exist.
            Defaults to the current directory.
        --overwrite
            If you use this, existing files in the output directory will be overwritten.
        --preview <none|filenames|short|full>
            Controls the level of verbosity for the preview of what will be created:

            - none: No preview.
            - filenames: Only list filenames.
            - short (default): List filenames and the 3 first lines of each file.
            - full: List filenames and the full content of each file.
        --pretend
            Do not change anything, just show what would be created.
        --<variable-name> <value>
            Set variables for the tree spec. Use --help to see the available variables.
            I.E.: If the tree spec takes a variable named ``project_name``, you would
            specify a value for this variable using ``--project-name "My project"``.
        """
        config = self.__get_config()
        tree = self.__get_tree_by_id(config=config, full_id=id)
        tree.validate_spec()
        if help:
            self.__print_spec_help(toplevel_spec=tree)
            return
        self.__validate_values(variables=tree.variables, valuedict=variables)
        tree.variables.set_variable_values(**variables)
        output_directory = out or os.getcwd()
        try:
            skipped_writers, writers = tree.collect_writers(
                output_directory=output_directory,
                overwrite=overwrite)
        except exceptions.SpecError as error:
            cliutils.print_error(error)
            raise SystemExit()
        if preview != 'none':
            cliutils.print_bold('The following will be created:')
        self.__print_create_tree_preview(writers=writers, skipped_writers=skipped_writers,
                                         previewmode=preview)
        if pretend or not writers:
            return
        if cliutils.confirm('Create the tree?'):
            for writer in writers:
                writer.write()

    def list_snippets(self, quiet=False):
        self.__list_specs(spec_class=spec.Snippet, quiet=quiet,
                          create_command_name='snippet')

    def __get_snippet_by_id(self, config, full_id):
        snippet_cache = spec.SpecCache(*spec.FileSystemLoader(config, spec.Snippet).find())
        try:
            return snippet_cache.get_spec(full_id=full_id)
        except KeyError:
            cliutils.print_error('No snippet skeleton with this id: {}'.format(full_id))
            raise SystemExit()

    def snippet(self, id, help=False, no_clipboard=False, no_stdout=False, **variables):
        """
        Build a snippet from a ``skeleton.snippet.yaml`` file.

        --id <id>
            The ID of a snippet spec. Use "list-snippets" to list all available IDs.
            REQUIRED.
        --help
            Show help for the snippet spec. This includes information about the
            snippet spec, and all the available variables.
        --no-clipboard
            Do not copy results to clipboard.
        --no-stdout
            Do not write results to stdout.
        --<variable-name> <value>
            Set variables for the snippet spec. Use --help to see the available variables.
            I.E.: If the tree snippet takes a variable named ``project_name``, you would
            specify a value for this variable using ``--project-name "My project"``.
        """
        config = self.__get_config()
        snippet = self.__get_snippet_by_id(config=config, full_id=id)
        snippet.validate_spec()
        if help:
            self.__print_spec_help(toplevel_spec=snippet)
            return
        self.__validate_values(variables=snippet.variables, valuedict=variables)
        snippet.variables.set_variable_values(**variables)
        if not no_stdout:
            cliutils.safe_print(snippet.render())
        if not no_clipboard:
            snippet.render_to_clipboard()
            cliutils.safe_print('')
            cliutils.print_success('Copied to clipboard')

    def gui(self):
        from codeskeleton.gui.gui import CodeSkeletonApp
        CodeSkeletonApp(codeskeleton_config=self.__get_config()).run()


def main():
    fire.Fire(Cli)
