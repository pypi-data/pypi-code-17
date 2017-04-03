# Copyright 2017 Interana, Inc.
'''
ia table create
ia table delete
ia table delete-time-range
ia table export
ia table list
ia table add-shard-key
ia table remove-shard-key

'''

from base import CommandHandler, SubCommandHandler, DoResult
from base import _pretty_print_dict
from ..utils.completers import TablesCompleter, ShardKeyCompleter
from ..utils.shared_parsers import add_output_parameters, add_run_mode
from collections import OrderedDict

import ast
import datetime
import json
import os
import re
import locale

COL_NAME_SUB_REGEX = re.compile(r'[\'"`~+\-*/\\\\!%$^()\[\]{}<>= ]')
TIMESTAMP_CONVERSION_FUNCTIONS = {
    'seconds': 'second_to_milli',
    'milliseconds': 'to_milli',
    'microseconds': 'micro_to_milli'
}
FILE_SIZE_LIMIT_MB = 100


class TableHandler(CommandHandler):

    name = 'table'
    description = 'Commands for managing event tables.'

    def __init__(self):
        CommandHandler.__init__(self)

        self.register_subcommand(TableCreate())
        self.register_subcommand(TableList())
        self.register_subcommand(TableDelete())
        self.register_subcommand(TableDeleteTimeRange())
        self.register_subcommand(TableExport())
        self.register_subcommand(TableAddShardKey())
        self.register_subcommand(TableRemoveShardKey())
        self.register_subcommand(TableImport())


class TableCreate(SubCommandHandler):

    name = 'create'
    description = ('Create a new table by specifying the table name, time column, and shard keys or '
                   'through a configuration file.')

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        add_output_parameters(parser)
        parser.add_argument(
            'table_name',
            help='Name of table to create.',
            type=str,
            nargs='?'
        )
        parser.add_argument(
            'time_column',
            help='Name of the time column in the data.',
            type=str,
            nargs='?'
        )
        parser.add_argument(
            'time_column_format',
            help='Time column\'s datetime format: seconds, milliseconds, microseconds, '
            'or a Python strptime format (i.e. "%%Y-%%m-%%dT%%H:%%M:%%S.%%fZ").',
            type=str,
            nargs='?'
        )
        parser.add_argument(
            'shard_key',
            nargs='*',
            help='Name of columns to shard on. Multiple columns may be specified.',
            type=str,
        )
        parser.add_argument(
            '--config-file',
            help='Path to the dataset configuration file.',
            type=str
        )

        advanced = parser.add_argument_group("Advanced")

        advanced.add_argument(
            '--shards-per-node',
            dest='shards_per_node',
            type=int,
            default=None,
            help='Number of shards per data host.')

        return parser

    def do(self):
        table_create_args = [self.args.table_name, self.args.time_column, self.args.time_column_format,
                             self.args.shard_key]
        if not any(table_create_args) and not self.args.config_file:
            raise Exception('Either table creation parameters or a configuration file must be specified.')

        if (any(table_create_args) and self.args.config_file):
            raise Exception('Both creation table parameters and a configuration file may not be specified. Please '
                            'specify only one option.')

        if any(table_create_args) and not all(table_create_args):
            raise Exception('When specifying table creation parameters, table_name, time_column, time_column_format, '
                            'and shard_key(s) must all be specified.')

        if all(table_create_args):
            # Check time column format
            conversion_function = None
            conversion_function_params = ''
            if self.args.time_column_format in ('seconds', 'milliseconds', 'microseconds'):
                conversion_function = TIMESTAMP_CONVERSION_FUNCTIONS.get(self.args.time_column_format)
            else:
                conversion_function = 'date_to_milli'
                conversion_function_params = self.args.time_column_format

            definition_dict = {
                    'table_alias': self.args.table_name,
                    'table_type': 'Event',
                    'time_column': self.args.time_column,
                    'shard_keys': self.args.shard_key,
                    'columns': [
                        {
                            'name': self.args.time_column,
                            'alias': re.sub(COL_NAME_SUB_REGEX, '_', self.args.time_column),
                            'column_type': 'milli_time',
                            'column_semantic': '',
                            'conversion_function': conversion_function,
                            'conversion_params': conversion_function_params,
                            'elapsed_milli': 0,
                        }
                    ],
                    'is_json': 1,
                    'is_csv': 0
                }
            params = {
                'table_name': self.args.table_name,
                'definition_dict': json.dumps(definition_dict),
                'shard_width_multiplier': self.args.shards_per_node,
            }
            res = self.post('{hostname}/import/api/create_table', data=params)
            content = json.loads(res.content)
            return DoResult(entries=[content.values()], headers=content.keys())
        else:
            # config file
            if not os.path.isfile(self.args.config_file):
                raise Exception('{} is not a file'.format(self.args.config_file))
            parsed_config = None
            with open(self.args.config_file, 'rb') as config_fh:
                config_text = config_fh.read()
                try:
                    parsed_config = ast.literal_eval(config_text)
                except:
                    try:
                        parsed_config = json.loads(config_text)
                    except:
                        print "ERROR - could not load configuration from file."
                        return

            res = self.post_json('{hostname}/import/api/ingest/setup_table', data=parsed_config)
            content = json.loads(res.content)
            rows = []
            for component, result in content.iteritems():
                if isinstance(result, list):
                    for res in result:
                        rows.append([component, _pretty_print_dict(res)])
                else:
                    rows.append([component, _pretty_print_dict(result)])
            return DoResult(entries=rows, headers=['Type', 'Results'])


class TableList(SubCommandHandler):

    name = 'list'
    description = 'List all tables for the registered customer.'

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        add_output_parameters(parser)
        parser.add_argument(
            '--type',
            help='Type of tables to list (event, lookup, or all); all by default.',
            type=str,
            choices=['event', 'lookup', 'all'],
            default='all'
        )
        return parser

    def do(self):
        params = {"type": self.args.type}
        res = self.get('{hostname}/import/api/get_tables', params=params)
        tables = json.loads(res.content)['tables']

        headers = ['ID', 'Name', 'Type', 'Time Col', 'Shard Keys']
        entries = [[
            r['table_id'],
            r['table_name'],
            r['table_type'],
            r['time_column_name'],
            ', '.join(r['shard_keys'])
        ] for r in tables]

        return DoResult(
            entries=entries,
            headers=headers,
            empty_warning='You have no tables! Import one today and be happy tomorrow!'
        )


class TableDelete(SubCommandHandler):

    name = 'delete'
    description = (
        'Deletes all the data and import records for a given table. '
        'Will mark table and associated column definitions as deleted, unless specified otherwise. '
        'Defaults to dry-run mode.'
    )

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        add_output_parameters(parser)
        parser.add_argument(
            'table_name',
            help='Name of the table.',
            type=str
        ).completer = TablesCompleter(self)
        parser.add_argument(
            '--keep-metadata',
            help='Use to persist the metadata (table definitions).',
            action='store_const',
            const=1,
            default=0,
        )
        add_run_mode(parser)

        return parser

    def do(self):
        params = {
            'table_name': self.args.table_name,
            'keep_metadata': self.args.keep_metadata,
            'dry_run': 1 if self.args.run is 0 else 0  # api takes in dry_run, which is opposite of run
        }

        print 'Initiating deletion {}for table {}, please wait...\n'.format(
                'preview ' if not self.args.run else '',
                self.args.table_name)
        res = self.post('{hostname}/import/api/delete_table', data=params)
        content = json.loads(res.content)
        headers = ['Table']
        entries = [[self.args.table_name]]

        # num_events formatting
        locale.setlocale(locale.LC_NUMERIC, '')
        if not self.args.run:
            if content.get('folders_to_delete'):
                headers += ['# of Folders to be Deleted', '# of Events']
                num_folders = len(content['folders_to_delete'])
                num_shards = content.get('num_shards')
                if not num_shards:
                    num_shards = 1
                # info is (folder, num_events)
                num_events = sum(info[1] for info in content['folders_to_delete']) / num_shards
                entries[0] += [
                    num_folders,
                    locale.format("%d", num_events, grouping=True)
                ]
            else:
                headers += ['Result']
                entries[0] += [content['result']]
            next_action = 'This is a preview mode. Rerun with --run option to delete table {}.'.format(
                    self.args.table_name)
        else:
            num_string_columns = len(content['strings'])
            import_record_status = content['import_records']
            metadata_status = content['metadata']

            headers += [
                    'Metadata',
                    'Import Record',
                    '# String Columns Deleted'
            ]

            entries[0] += [
                    metadata_status,
                    import_record_status,
                    num_string_columns
            ]

            # deletes on lookup tables does not return field 'data'
            if content.get('data'):
                num_folders = len(content['data']['details'])
                num_shards = content['data'].get('num_shards')
                if not num_shards:
                    num_shards = 1

                num_events = sum(info[1] for info in content['data']['details']) / num_shards
                headers += [
                        '# Folders Deleted',
                        '# Events Deleted',
                ]
                entries[0] += [
                        num_folders,
                        locale.format("%d", num_events, grouping=True),
                ]
            else:
                lookup_delete_result = content['result']
                headers += ['Result']
                entries[0] += [lookup_delete_result]

            next_action = 'Table {} has been deleted. Use ia table list to see the status of tables.'.format(
                    self.args.table_name)

        return DoResult(headers=headers, entries=entries, message=next_action)


class TableDeleteTimeRange(SubCommandHandler):

    name = 'delete-time-range'
    description = (
        'Deletes a time range of data for a given table. '
        'Will also delete strings associated with the data if start-time is not specified.'
        'Defaults to dry-run mode.'
    )

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        add_output_parameters(parser)
        parser.add_argument(
            'table_name',
            help='Name of the Event table.',
            type=str
        ).completer = TablesCompleter(self, 'event')
        parser.add_argument(
            'start_time',
            help='Start time of the deletion, optional. If specified, strings will not be deleted. Use epoch/unix time',
            type=int,
            nargs='?'
        )
        parser.add_argument(
            'end_time',
            help='End time of the deletion, required. Use epoch/unix time',
            type=int
        )
        parser.add_argument(
            '--keep-strings',
            help='Force the deletion to keep strings no matter what.',
            action='store_const',
            const=1,
            default=0,
        )
        parser.add_argument(
            '--delete-import-records',
            help='Deletes all import records for this table.',
            action='store_const',
            const=1,
            default=0,
        )
        parser.add_argument(
            '--im-feeling-lucky',
            help='Use to expedite the deletion of data signifcantly by only deleting folders that '
                 'completely fall within the time range specified. However, this method will most likely '
                 'under-delete. Great if you are simply rolling off old data.',
            dest='by_folder',
            action='store_const',
            const=1,
            default=0,
        )
        add_run_mode(parser)
        return parser

    def do(self):
        params = {
            'table_name': self.args.table_name,
            'start_time': self.args.start_time,
            'end_time': self.args.end_time,
            'import_records': self.args.delete_import_records,
            'by_folder': self.args.by_folder,
            'dry_run': 1 if self.args.run is 0 else 0  # api takes in dry_run, which is opposite of run
        }

        # special delete strings logic:
        date_msg = '\nTime-range specified (IN UTC): \n'
        if self.args.start_time:
            delete_strings = 0
            if not self.args.keep_strings:
                print "Note: start_time was specified, so strings will not be deleted."

            # modify date_msg
            date_msg += "Start: {} -> ".format(
                datetime.datetime.utcfromtimestamp(self.args.start_time / 1000)
            )

        else:
            date_msg += "Start: Not specified, "
            delete_strings = 1 if self.args.keep_strings is 0 else 1
        params['delete_strings'] = delete_strings

        print "{}End: {}\n".format(date_msg, datetime.datetime.utcfromtimestamp(self.args.end_time / 1000))

        # special by_folder logic:
        if self.args.by_folder:
            print ("Note: You specified by_folder deletion through '--im-feeling-lucky',"
                   "which is faster but might under-delete. \n")
        elif self.args.run:
            print ("Note: You are doing precise deletion, this might take up to an hour. Please do not close this"
                   " prompt. To monitor progress, tail the import-api-server logs on import-api nodes. \n")

        # also post here for dry-run, so that we can detect any routine error that
        # will cause problems when we actually run it.
        res = self.post('{hostname}/import/api/delete_table_data', data=params)
        content = json.loads(res.content)

        headers = ['Table']
        entries = [[self.args.table_name]]

        # this is for num_events formatting.
        locale.setlocale(locale.LC_NUMERIC, '')

        if not self.args.run:
            # fetch event count from external api
            params = {
                'query': json.dumps({
                    "dataset": self.args.table_name,
                    "start": self.args.start_time if self.args.start_time else 0,
                    "end": self.args.end_time,
                    "sampled": True,
                    "queries": [{
                        "type": "single_measurement",
                        "measure": {
                            "aggregator": "count_star",
                        },
                    }]
                })
            }
            res = self.get('{hostname}/api/v1/query', data=params)
            content = json.loads(res.content)
            num_events = content['rows'][0]['values'][1]

            headers += ['Number of Events that will be Deleted']
            entries[0] += [locale.format("%d", num_events, grouping=True)]

            if not self.args.by_folder:
                print ("If your dataset is larger than 10M events, precise delete might be slow."
                       " Maybe try --im-feeling-lucky?\n")

            next_action = 'This is the preview mode. Rerun with --run option to perform partial deletion on table {}.'\
                .format(self.args.table_name)
        else:
            data_delete_result = content['data']['details']
            num_shards = content['data'].get('num_shards')
            if not num_shards:
                num_shards = 1
            num_folders_affected = sum(1 for info in data_delete_result if info[1] > 0)
            num_events = sum(info[1] for info in data_delete_result) / num_shards
            string_delete_status = content['strings']
            import_record_status = content['import_records']

            headers += [
                    '# Folders affected',
                    '# Events Deleted',
                    'String Delete Status',
                    'Import Record Status',
            ]

            entries[0] += [
                    "approx. {}".format(num_folders_affected),  # it will be close...
                    locale.format("%d", num_events, grouping=True),
                    string_delete_status,
                    import_record_status,
            ]


            if num_events:
                next_action = 'Table {} has completed time-range delete.'.format(
                        self.args.table_name)
            else:
                next_action = 'Warning: No events were deleted, please check that your time range includes events.'

        return DoResult(headers=headers, entries=entries, message=next_action)


class TableExport(SubCommandHandler):

    name = 'export'
    description = 'Export the table configuration to a file - includes column info and ingest jobs.'

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        add_output_parameters(parser)
        parser.add_argument(
            'table_name',
            help='Name of dataset to export.',
            type=str
        ).completer = TablesCompleter(self)
        parser.add_argument(
            '-o',
            '--output-file',
            help='File to write configuration to. Default output file is <table name>_table_config.txt '
            'in the current directory.',
            type=str
        )
        return parser

    def do(self):
        output_file = '{}_table_config.txt'.format(self.args.table_name)
        if self.args.output_file:
            output_file = self.args.output_file
            if os.path.isfile(output_file):
                print 'Note: a file exists at \'{}\', it will be overwritten.'.format(output_file)
        params = {
            'table': self.args.table_name,
        }
        res = self.post_json('{hostname}/import/api/ingest/export_table', data=params)
        content = json.loads(res.content, object_pairs_hook=OrderedDict)
        try:
            with open(output_file, 'w') as out_fh:
                out_fh.write(json.dumps(content, indent=4))
        except:
            print 'Error writing to file: {}'.format(output_file)
            raise


class TableAddShardKey(SubCommandHandler):
    name = 'add-shard-key'
    description = 'Add a shard key to a table.'

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        add_output_parameters(parser)
        parser.add_argument(
            'table_name',
            help='Name of the Event table.',
            type=str,
        ).completer = TablesCompleter(self, 'event')
        parser.add_argument(
            'shard_key',
            help='Name of the shard key.',
            type=str,
        )

        return parser

    def do(self):
        params = {
            'table_name': self.args.table_name,
            'shard_key': self.args.shard_key
        }

        res = self.post('{hostname}/import/api/add_shard_key', data=params)
        content = json.loads(res.content)
        headers = ['Table Affected', 'Shard Key Added', 'All Shard Keys']
        entries = [[content['table_name'], content['shard_key'], ','.join(content['all_shard_keys'])]]
        next_action = ('Please re-import existing data to populate the new shard key '
                       '(new data will be imported automatically).')
        return DoResult(headers=headers, entries=entries, message=next_action)


class TableRemoveShardKey(SubCommandHandler):
    name = 'remove-shard-key'
    description = 'Remove a shard key from a table by deleting its corresponding tablecopy.'

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        add_output_parameters(parser)
        parser.add_argument(
            'table_name',
            help='Name of the event table.',
            type=str,
        ).completer = TablesCompleter(self, 'event')
        parser.add_argument(
            'shard_key',
            help='Name of the shard key.',
            type=str,
        ).completer = ShardKeyCompleter(self)
        add_run_mode(parser)

        return parser

    def do(self):
        params = {
            'table_name': self.args.table_name,
            'shard_key': self.args.shard_key,
            'run': self.args.run
        }

        res = self.post('{hostname}/import/api/delete_shard_key', data=params)
        content = json.loads(res.content)
        headers = [header for header in content if header != 'delete_feedback']
        headers.append('Result')
        entries = [[entry for header, entry in content.iteritems() if header != 'delete_feedback']]
        entries[0].append(content['delete_feedback']['result'])

        if not self.args.run:
            next_action = 'This is a preview mode. Rerun with --run option for changes to take effect.'
        else:
            next_action = 'The changes have been committed. Use ia table list to see the status of tables.'

        return DoResult(headers=headers, entries=entries, message=next_action)


def expand_to_absolute_path(path_pattern):
    return os.path.abspath(os.path.expanduser(os.path.expandvars(path_pattern)))


class TableImport(SubCommandHandler):
    name = 'import'
    description = 'Set up one-time import of data from one or more files to a table.'

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        add_output_parameters(parser)
        parser.add_argument(
            'table_name',
            help='Name of the table.',
            type=str,
        ).completer = TablesCompleter(self)
        parser.add_argument(
            'file_names',
            help='Name of the file(s) to import. '
                 'Files are imported from the current directory, or from the Interana node if no-upload is selected.',
            nargs='+',
            type=str,
        )
        parser.add_argument(
            '--delete-files',
            help='Delete the files from the Interana node after data is imported.',
            action='store_const',
            const=1,
            default=0,
        )
        parser.add_argument(
            '--no-upload',
            help='Import previously uploaded files from disk instead of uploading from local directory.',
            action='store_const',
            const=1,
            default=0,
        )
        parser.add_argument(
            '--force',
            help='Force reingesting of files that have already been imported.',
            action='store_const',
            const=1,
            default=0,
        )

        return parser

    def do(self):
        files = self.args.file_names
        if not self.args.no_upload:
            import_filenames = []
            for file in files:
                file_path = expand_to_absolute_path(file)

                if not os.path.isfile(file_path):
                    print ("File {} not found and will be skipped.".format(file))
                    continue

                file_size = os.stat(file_path).st_size
                if file_size > (FILE_SIZE_LIMIT_MB * 1024 * 1024):
                    print("File {0} size exceeds limit of {1} MB, skipping".format(file, FILE_SIZE_LIMIT_MB))
                    continue
                with open(file_path) as file_obj:
                    files = {
                        'filearg': (file_obj.name, file_obj)
                    }

                    upload_params = {
                        "save_as": file
                    }
                    print "Uploading file: {}".format(file_path)
                    res = self.post('{hostname}/import/api/data/upload', files=files, data=upload_params)
                content = json.loads(res.content)
                import_filenames.append(content['name'])

        else:
            import_filenames = files

        import_params = {
            'table_name': self.args.table_name,
            'file_names': import_filenames,
            'delete_after_import': self.args.delete_files,
            'force': self.args.force
        }
        import_res = self.post('{hostname}/import/api/data/add_to_fast_import', data=import_params)
        content = json.loads(import_res.content)
        headers = ['File', 'Status']
        entries = []
        files_added = False
        files_skipped = False

        for file, status in content.iteritems():
            entries.append([file, status])
            if status == 'Queued for import':
                files_added = True
            elif status == 'Skipped':
                files_skipped = True

        message = ''
        if files_added:
            message += 'Files have been added to import queue. They may take a few minutes to finish importing.\n'
        if files_skipped:
            message += 'Some files were skipped because they have already been imported. ' \
                       'Use the --force option to reimport.'
        return DoResult(headers=headers, entries=entries, message=message)
