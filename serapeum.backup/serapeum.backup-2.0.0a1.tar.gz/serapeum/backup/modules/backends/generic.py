from os.path import isfile
import json

from serapeum.backup.modules.run import Run


class GenericRole:
    __cmd_output = ''

    @property
    def cmd_output(self):
        return self.__cmd_output

    @cmd_output.setter
    def cmd_output(self, command_output):
        self.__cmd_output += command_output

    def p__parse_sources_file(self, filename):
        dir_list = []
        if not isfile(filename):
            raise Exception('Failed to read directory list from {0}: file not found.'.format(filename))
        with open(filename, 'r') as f:
            try:
                sources_parsed = json.load(f)
                dir_list = sources_parsed['list']
            except json.JSONDecodeError:
                raise Exception('Failed to read directory list from {0}: syntax error.'.format(filename))
            except KeyError:
                raise Exception('Invalid sources file!')
        return dir_list

    def p__run(self, command, env=None):
        r = Run()
        try:
            r.run(command, env=env)
        except Exception as e:
            self.cmd_output = r.cmd_output
            raise e
        return r.cmd_output
