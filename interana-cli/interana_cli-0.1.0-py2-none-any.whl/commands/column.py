# Copyright 2017 Interana, Inc.
'''
ia column list
ia column update
ia column delete
'''

import json
from base import CommandHandler, SubCommandHandler, DoResult
from ..utils.completers import TablesCompleter, ColumnsCompleter, ColumnTypeCompleter
from ..utils.shared_parsers import add_output_parameters, add_run_mode

supported_types = ['int', 'int_set', 'string', 'string_set', 'decimal', 'dollars', 'parsed_user_agent',
                   'geo_ip', 'parsed_url', 'browser_id', 'identifier']

type_to_conversion_function_map = {
    'int': 'to_int',
    'int_set': 'to_int_set',
    'string': 'to_string',
    'string_set': 'to_string_set',
    'decimal': 'to_decimal',
    'dollars': 'to_dollars',
    'parsed_user_agent': 'to_parsed_user_agent',
    'geo_ip': 'ip_to_geo',
    'parsed_url': 'to_parsed_url',
    'browser_id': 'to_browser_id',
    'identifier': 'to_hash_lower'
}

conversion_function_to_type_map = {
    'to_int': 'int',
    'to_int_set': 'int_set',
    'to_string': 'string',
    'to_string_set': 'string_set',
    'to_decimal': 'decimal',
    'to_dollars': 'dollars',
    'to_parsed_user_agent': 'parsed_user_agent',
    'ip_to_geo': 'geo_ip',
    'to_parsed_url': 'parsed_url',
    'to_browser_id': 'browser_id',
    'to_hash_lower': 'identifier'
}


class ColumnHandler(CommandHandler):

    name = 'column'
    description = 'Commands for managing columns.'

    def __init__(self):
        CommandHandler.__init__(self)

        self.register_subcommand(ColumnList())
        self.register_subcommand(ColumnUpdate())
        self.register_subcommand(ColumnDelete())


class ColumnList(SubCommandHandler):

    name = 'list'
    description = 'List columns.'

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        add_output_parameters(parser)
        parser.add_argument(
            'table',
            help='Name of the table',
            type=str
        ).completer = TablesCompleter(self)
        return parser

    def do(self):
        params = {
            'table_name': self.args.table
        }

        res = self.get('{hostname}/import/api/get_table_columns', params=params)
        columns = json.loads(res.content)['columns']

        headers = ['Column ID',
                   'Table ID',
                   'Col Name',
                   'Type',
                   'Shard Key',
                   'Conversion',
                   'Conversion Params']
        entries = [[
            r['column_id'],
            r['table_id'],
            r['name'],
            r['column_type'],
            'X' if bool(r['shard_key']) else '',
            r['conversion_function'],
            r['conversion_function_params'],
        ] for r in columns]

        return DoResult(
            entries=entries,
            headers=headers
        )


class ColumnUpdate(SubCommandHandler):

    name = 'update'
    description = 'Update an existing column. Currently only supports changing column types.'

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        add_output_parameters(parser)
        parser.add_argument(
            'table',
            help='Table containing column to change',
            type=str
        ).completer = TablesCompleter(self)
        parser.add_argument(
            'column',
            help='Column to change',
            type=str
        ).completer = ColumnsCompleter(self)
        parser.add_argument(
            '--type',
            help='New type for column as conversion function',
            type=str,
            choices=supported_types,
            required=True
        ).completer = ColumnTypeCompleter(self)
        parser.add_argument(
            '--keep-old-column',
            help='Keep the old data and strings of the column being changed instead of deleting them',
            action='store_true'
        )
        parser.add_argument(
            '--hex-digits',
            type=int,
            help='Number of digits for hexN support. Must be used with identifier and be a multiple of 8',
            default=0
        )
        add_run_mode(parser)

        return parser

    def do(self):
        table = self.args.table
        column = self.args.column
        if self.args.keep_old_column:
            full_delete = 0
        else:
            full_delete = 1

        # If attempting conversion to identifier and not providing hex digits, raise exception
        assert not (self.args.type == 'identifier' and not self.args.hex_digits),\
            "Hex digits must be provided for identifier conversion"

        conversion_function = type_to_conversion_function_map[self.args.type]

        post_data = {'table_name': table, 'column_name': column, 'conversion_function': conversion_function,
                     'full_delete': full_delete, 'revert': False, 'run': self.args.run,
                     'hex_digits': self.args.hex_digits}
        res = self.post('{hostname}/import/api/change_column_type', data=post_data)
        content = json.loads(res.content)
        headers = ['Table', 'Column', 'Old type', 'New type']
        old_type = conversion_function_to_type_map[content['old_conversion_function']]
        new_type = conversion_function_to_type_map[content['conversion_function']]
        entries = [[content['table_name'], content['column_name'], old_type, new_type]]
        if self.args.run:
            next_action = "The changes have been committed."
        else:
            next_action = "This is a preview mode. Rerun with --run option for changes to take effect."
        return DoResult(
            entries=entries,
            headers=headers,
            message=next_action
        )


class ColumnDelete(SubCommandHandler):

    name = 'delete'
    description = 'Delete a column.'

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        add_output_parameters(parser)
        parser.add_argument(
            'table_name',
            help='Table containing column to delete',
            type=str
        ).completer = TablesCompleter(self)
        parser.add_argument(
            'column_name',
            help='Column to delete. Required if not using match-pattern',
            type=str,
            nargs='?'
        ).completer = ColumnsCompleter(self)
        parser.add_argument(
            '--match-pattern',
            type=str,
            help='Delete all columns in table matching the given pattern, using SQL pattern matching',
        )
        parser.add_argument(
            '--keep_metadata',
            help='Keep column metadata and delete data only',
            action='store_const',
            const=1,
            default=0,
        )
        add_run_mode(parser)

        return parser

    def do(self):
        table = self.args.table_name
        column_name = self.args.column_name
        match_pattern = self.args.match_pattern
        if not match_pattern and not column_name:
            raise Exception('If not pattern matching using match-pattern, column name must be specified.')
        if match_pattern and column_name:
            raise Exception('If using match-pattern, column_name argument must be empty.')

        if self.args.keep_metadata:
            full_delete = 0
        else:
            full_delete = 1
        run = self.args.run

        if match_pattern:
            where_clause = json.dumps([["name", match_pattern]])
            post_data = {
                'table_name': table,
                'where_clause': where_clause,
                'full_delete': full_delete
            }
            if self.args.run:
                res = self.post('{hostname}/import/api/column_sql_delete', data=post_data)
                content = json.loads(res.content)
                columns_deleted = [[str(column)] for column in content['column_names']]
            else:
                res = self.post('{hostname}/import/api/test_column_sql', data=post_data)
                content = json.loads(res.content)
                columns_deleted = [[str(column['name'])] for column in content['column_info']]

        else:
            post_data = {
                'table_name': table,
                'column_name': column_name,
                'full_delete': full_delete,
                'run': run
            }
            res = self.post('{hostname}/import/api/delete_column', data=post_data)
            content = json.loads(res.content)
            columns_deleted = [[str(column)] for column in content['column_names']]

        headers = ['Columns deleted'] if self.args.run else ['Columns to be deleted']
        entries = columns_deleted

        if not columns_deleted:
            next_action = 'No columns were found matching the given pattern.'
        elif run:
            next_action = 'The changes have been committed.'
        else:
            next_action = 'This is a preview mode. Rerun with --run option for changes to take effect.'

        return DoResult(headers=headers, entries=entries, message=next_action)
