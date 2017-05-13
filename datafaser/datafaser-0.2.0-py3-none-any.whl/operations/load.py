import logging

from datafaser.data_tree import DataTree
from datafaser.files import FileLoader, FileSaver
from datafaser.formats import FormatRegister


help_topic = 'Load operation'
help_text = '''
Load data between files and branches of data tree in memory:

    - "Load data from files":
      - load:
          from:
            file: "directory/*"
          to:
            branch: "data from files"

    - "Load data from memory to file":
      - load:
          from:
            branch: "data for file"
          to:
            file: "directory/file.yaml"
            format: "yaml"

    - "Load data from one branch to another in memory":
      - load:
          from:
            branch: "original data branch"
          to:
            branch: "another data branch"

    - "Load data from one file to another":
      - load:
          from:
            file: "original.yaml"
          to:
            file: "another.json"
            format: "json"
'''


class Loader:
    """
    Copy data structures between different sources and targets such as files and memory.
    """

    def __init__(self, data_tree):
        """
        :param data_tree: DataTree object holding datafaser.formats configuration for FormatRegister
        """

        self.format_register = FormatRegister(**data_tree.reach('datafaser.formats'))
        self.data_tree = data_tree
        self.logger = logging.getLogger(__name__)

    def load(self, data_tree, directives):

        if 'from' in directives:
            new_data = DataTree({})
            source = directives['from']
            if not isinstance(source, dict):
                raise TypeError('Not a dictionary of sources to load from: %s' % type(source).__name__)
            if 'file' in source:
                FileLoader(new_data, self.format_register, source.get('format') or self._get_default_format()).load(source['file'])
            if 'branch' in source:
                self.logger.info('Load from branch: "%s"' % source['branch'])
                new_data.merge(data_tree.reach(source['branch']))
        else:
            new_data = DataTree(data_tree.data.copy())

        if 'to' in directives:
            self._save_new_data(data_tree, new_data, directives['to'])
        else:
            data_tree.merge(new_data.data)

    def _save_new_data(self, data_tree, new_data, target):
        if not isinstance(target, dict):
            raise TypeError('Not a dictionary of target types to targets to save to: %s' % type(target).__name__)

        if 'branch' in target:
            self.logger.info('Store to branch: "%s"' % target['branch'])
            data_tree.merge(new_data.data, target['branch'])

        if 'file' in target:
            self.logger.info('Save to file: "%s"' % target['file'])

            writer = FileSaver(new_data.data, self.format_register)
            filename = target['file']
            if not isinstance(filename, str):
                raise TypeError('Not a filename to save to: %s' % type(filename).__name__)

            output_format = target.get('format') or self._get_default_format()
            if not isinstance(output_format, str):
                raise ValueError('Missing format for file to write: "%s"' % filename)
            writer.save(filename, output_format)

    def _get_default_format(self):
        return self.data_tree.reach('datafaser.run').get('options', {}).get('default-format')
