import os
import sys
import logging
import logging.config
from importlib import reload
from getopt import getopt, GetoptError

usage = '''Usage: %s [options] [files]
Will load and validate data from given files and directories,
then proceed according to instructions given at datafaser.run.plan in the data.
Options:
'''


class Main:

    options_schema_key = 'schema.properties.datafaser.properties.run.properties.options.properties'

    def __init__(self, command_line):
        self.command_line = command_line
        self.options = {}
        self.arguments = []

    def run_with_command_line(self):
        import datafaser.start

        runner = datafaser.start.initialize_runner()

        files = self.extract_options(runner.data_tree.reach(self.options_schema_key))
        self.setup_logging()
        runner.create_logger()
        runner.data_tree.merge(self.options, 'datafaser.run.options')
        runner.data_tree.merge(datafaser.start.create_plan_to_load_files(files, 'load files listed on command line'))

        runner.validate()
        runner.load_and_run_all_plans()

    def extract_options(self, options_schema):
        long_options = self.list_long_options(options_schema)

        try:
            options, arguments = getopt(self.command_line[1:], None, long_options)
        except GetoptError:
            self.usage(options_schema)

            raise

        for option in options:
            name = option[0][2:]
            value = options_schema[name]['type'] == 'boolean' or option[1]
            self.options[name] = value

        if 'help-on' in self.options:
            self.help_on(self.options['help-on'])
            sys.exit(1)

        if 'help' in self.options:
            self.usage(options_schema)
            sys.exit(1)

        return arguments

    def help_on(self, topic):
        topicpath = topic.split('.')
        module = __import__('datafaser.' + topic)
        for submodulename in topicpath:
            module = module.__dict__[submodulename]

        helps = []
        if 'help_topic' in module.__dict__:
            helps.append(module.help_topic.strip())
        if 'help_text' in module.__dict__:
            helps.append(module.help_text.strip())

        if helps:
            sys.stderr.write('%s\n' % '\n\n'.join(helps))
        else:
            sys.stderr.write('No help available for requested topic.\n')

    def help_topics(self):
        sys.stderr.write('\nHelp Topics:\n')
        this_dir = os.path.dirname(__file__)
        for dirname, dirs, files in os.walk(this_dir):
             for filename in files:
                 if filename.endswith('.py'):
                     modulepath = list(filter(lambda n: n, dirname[len(this_dir)+1:].split(os.sep)))
                     if not filename.startswith('__'):
                         modulepath.append(filename[:len(filename)-3])
                     modulename = '.'.join(modulepath)

                     module = __import__('.'.join(['datafaser'] + modulepath))

                     for submodulename in modulepath:
                          module = module.__dict__[submodulename]

                     if 'help_topic' in module.__dict__:
                         sys.stderr.write("  %s\t%s\n" % (modulename, module.help_topic))

    def usage(self, options_schema):
        sys.stderr.write(usage % self.command_line[0])
        for key, schema in sorted(options_schema.items(), key=lambda item: item[0]):
            value = schema['type'] != 'boolean' and '=' + schema['type'].upper() or ''
            sys.stderr.write("  --%-22s  %s\n" % (key + value, schema['title']))
        self.help_topics()

    def list_long_options(self, options_schema):
        for key, schema in options_schema.items():
            option_name = key
            if 'type' in schema and schema['type'] != 'boolean':
                option_name += '='
            yield option_name

    def setup_logging(self):
        reload(logging)
        level = self.options.get('log-level', 'INFO').upper()
        handlers = {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'console',
                'stream': 'ext://sys.stderr'
            }
        }
        if self.options.get('log-file'):
            handlers['file'] = {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'file',
                'filename': self.options.get('log-file'),
            }
        if self.options.get('syslog'):
            handlers['syslog'] = {
                '()': 'logging.handlers.SysLogHandler',
                'formatter': 'syslog'
            }
            for socket in ['/var/run/syslog', '/dev/log']:
                if os.path.exists(socket):
                    handlers['syslog']['address'] = socket
                    break

        logging.config.dictConfig({
            'version': 1,
            'formatters': {
                'console': {'format': '%(name)s %(levelname)s: %(message)s'},
                'file': {'format': '%(asctime)s %(name)s %(levelname)s: %(message)s'},
                'syslog': {'format': '%(name)s: %(message)s'},
            },
            'handlers': handlers,
            'root': {
                'level': level,
                'handlers': list(handlers.keys())
            }
        })

        logging.getLogger(self.command_line[0]).debug('Logging configured: %s' % str(handlers))


def main(argv=sys.argv):
    logging.basicConfig(level='WARN', format='Unconfigured %(name)s %(levelname)s: %(message)s')
    try:
        Main(argv).run_with_command_line()
    except Exception as e:
        logging.getLogger(argv[0]).fatal(
                '%s: %s\n' % (e.__class__.__name__, str(e)),
                exc_info=os.environ.get('DATAFASER_STACKTRACE', 0))
        sys.exit(2)

