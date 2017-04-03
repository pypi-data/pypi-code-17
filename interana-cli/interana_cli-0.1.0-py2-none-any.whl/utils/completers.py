# Copyright 2017 Interana, Inc.
import json


class ApiFetchCompleter(object):
    '''Base class for completers that query the API'''

    def __init__(self, command):
        self.c = command


class TablesCompleter(ApiFetchCompleter):
    '''tab-completes names of all tables, unless specified otherwise'''

    def __init__(self, command, type='all'):
        assert (type in {'all', 'event', 'lookup'})  # no other types are allowed
        super(TablesCompleter, self).__init__(command)
        self.type = type

    def __call__(self, prefix, parsed_args, **kwargs):
        self.c.initialize(parsed_args)
        res = self.c.get('{hostname}/import/api/get_tables', params={'type': self.type})
        tables = json.loads(res.content)
        names = (t['table_name'] for t in tables['tables'])
        return (n for n in names if n.startswith(prefix))


class ShardKeyCompleter(ApiFetchCompleter):
    '''tab-completes names of shard_keys of tables'''

    def __call__(self, prefix, parsed_args, **kwargs):
        self.c.initialize(parsed_args)
        res = self.c.get('{hostname}/import/api/get_tables')
        tables = json.loads(res.content)['tables']
        table_name = self.c.args_dict['table_name']
        for table in tables:
            if table['table_name'] == table_name:
                shard_keys = table['shard_keys']
                break

        return (shard_key for shard_key in shard_keys if shard_key.startswith(prefix))


class ColumnsCompleter(ApiFetchCompleter):
    '''tab-completes names of columns of table'''

    def __call__(self, prefix, parsed_args, **kwargs):
        self.c.initialize(parsed_args)
        table_name = self.c.args_dict['table']
        res = self.c.get('{hostname}/import/api/get_table_columns', params={'table_name': table_name})
        content = json.loads(res.content)
        names = (c['name'] for c in content['columns'])
        results = (n for n in names if n.startswith(prefix))
        return results


class PipelinesCompleter(ApiFetchCompleter):
    '''tab-completes names of pipelines'''

    def __call__(self, prefix, parsed_args, **kwargs):
        self.c.initialize(parsed_args)
        res = self.c.get('{hostname}/import/api/pipelines/readall')
        pipelines = json.loads(res.content)
        names = (p['pipeline_name'] for p in pipelines['pipelines'])
        return (n for n in names if n.startswith(prefix))


class TransformerTypesCompleter(ApiFetchCompleter):

    def __call__(self, prefix, parsed_args, **kwargs):
        self.c.initialize(parsed_args)
        res = self.c.get('{hostname}/import/api/transformers/list_types')
        types = json.loads(res.content)
        type_names = (t['transformer_type_name'] for t in types['types'])
        return (n for n in type_names if n.startswith(prefix))


class ColumnTypeCompleter(ApiFetchCompleter):

    def __call__(self, prefix, parsed_args, **kwargs):
        types = ['int', 'int_set', 'string', 'string_set', 'decimal', 'dollars', 'parsed_user_agent',
                 'geo_ip', 'parsed_url', 'browser_id', 'identifier']
        return (n for n in types if n.startswith(prefix))
