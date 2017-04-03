# Copyright 2017 Interana, Inc.
'''
ia job create
ia job read
ia job stats
ia job list
ia job pause
ia job resume
ia job delete
ia job update
ia job export

ia pipeline create "test_table" "jpipe" aws
ia transformer create jtpipe" "xz"

ia job create jtpipe yesterday today

ia job read 1

ia job list
ia job list all
ia job list done

ia job update 1 --start_day 2000-01-01

ia job delete 1
'''

from base import CommandHandler, SubCommandHandler, DoResult
from ..utils.completers import TablesCompleter, PipelinesCompleter
from ..utils.shared_parsers import add_output_parameters, add_run_mode

from collections import OrderedDict

import ast
import datetime
import json
import os

_statuses = {
    'inactive': 0,
    'active': 1,
    'done': 2,
    'paused': 3
}

_forevers = {
    'one_time': 0,
    'forever': 1,
}


class JobHandler(CommandHandler):

    name = 'job'
    description = 'Commands for managing ingest jobs.'

    def __init__(self):
        CommandHandler.__init__(self)

        self.register_subcommand(JobCreate())
        self.register_subcommand(JobRead())
        self.register_subcommand(JobStats())
        self.register_subcommand(JobList())
        self.register_subcommand(JobPause())
        self.register_subcommand(JobResume())
        self.register_subcommand(JobDelete())
        self.register_subcommand(JobUpdate())
        self.register_subcommand(JobExport())


class JobCreate(SubCommandHandler):

    name = 'create'
    description = 'Create a new ingest job for an existing dataset through a configuration file'

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        add_output_parameters(parser)
        parser.add_argument(
            'config_file',
            help='Path to the ingest configuration file',
            type=str
        )

        return parser

    def do(self):
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
                    raise Exception("could not load configuration from file '{}'.".format(self.args.config_file))

        res = self.post_json('{hostname}/import/api/ingest/create_job', data=parsed_config)
        content = json.loads(res.content)

        table_columns = [
            ('name', 'Name'),
            ('data_source_type', 'Dataset'),
            ('continuous', 'Type'),
            ('start', 'Start'),
            ('end', 'End')
        ]
        entries = [[r[f[0]] for f in table_columns] for r in content.values()]
        for e in entries:
            # Convert continuous to name: continuous = 1 -> continuous, continuous = 0 -> onetime
            e[2] = 'continuous' if e[2] else 'onetime'

        return DoResult(entries=entries, headers=['Job Name', 'Data Source', 'Type', 'Start', 'End'])


def _show_jobs(args, jobs):
    table_columns = [
        ('job_id', 'ID'),
        ('pipeline_name', 'Pipeline'),
        ('forever', 'Forever'),
        ('start_day', 'Start'),
        ('until_day', 'Until'),
        # ('is_deleted', 'Deleted'),  Unused?
        ('status', 'Status'),
    ]

    code_to_str = {code: string for string, code in _statuses.iteritems()}

    for j in jobs:
        j['status'] = "%s (%d)" % (code_to_str[j['status']], j['status'])
        j['forever'] = "%s (%d)" % ('True' if j['forever'] else 'False', j['forever'])

    entries = [[r[f[0]] for f in table_columns] for r in jobs]

    return DoResult(
        entries=entries,
        headers=[f[1] for f in table_columns]
    )


class JobRead(SubCommandHandler):

    name = 'read'
    description = 'Display more information on a specific job'

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        add_output_parameters(parser)
        parser.add_argument(
            'job_name',
            help='Name of job to display',
            type=str
        ).completer = PipelinesCompleter(self)

        return parser

    def do(self):
        params = {
            'job_name': self.args.job_name,
        }
        res = self.post_json('{hostname}/import/api/ingest/show_job', data=params)
        content = json.loads(res.content)
        if content.get('continuous') is not None:
            content['type'] = 'continuous' if content['continuous'] else 'onetime'
        table_columns = [
            ('name', 'Name'),
            ('data_source_type', 'Data Source'),
            ('table_name', 'Dataset'),
            ('type', 'Type'),
            ('start', 'Start'),
            ('end', 'End'),
            ('data_source_parameters', 'Data Source Parameters'),
            ('advanced_parameters', 'Advanced Parameters'),
            ('data_transformations', 'Transformations'),
            ('running_import_nodes', 'Running Import Nodes')
        ]
        entries = [[f[1], content.get(f[0])] for f in table_columns]
        return DoResult(entries=entries, headers=['Key', 'Value'])


class JobUpdate(SubCommandHandler):

    name = 'update'
    description = ('Update an existing job\'s parameters and transformation config or '
                   'update multiple jobs through a configuration file')

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        add_output_parameters(parser)
        parser.add_argument(
            'job',
            help='Name of job to update',
            type=str,
            nargs='?'
        ).completer = PipelinesCompleter(self)
        parser.add_argument(
            '-p',
            '--parameter',
            help='Name of parameter and value to update to. '
            'Can be specified multiple times to update multiple parameters. To update the running_import_nodes, '
            'use the value "all" or a comma separated list of import nodes (i.e. "import000,import001")',
            nargs=2,
            metavar=('PARAMETER NAME', 'VALUE'),
            action='append'
        )
        parser.add_argument(
            '-t',
            '--transformation-config',
            help='Path to file with transformation configuration to update job with',
            type=str
        )
        parser.add_argument(
            '--config-file',
            help='Path to the job updates configuration file',
            type=str
        )

        return parser

    def do(self):
        single_job_update_args = [self.args.parameter, self.args.transformation_config]
        if not self.args.job and not any(single_job_update_args) and not self.args.config_file:
            raise Exception('Either job update parameters or a configuration file must be specified.')

        if self.args.job and not any(single_job_update_args):
            raise Exception('Parameters and/or transformation config must be specified when updating a single job')

        if not self.args.job and any(single_job_update_args):
            raise Exception('Job must be specified when updating parameters and/or transformation config')

        if (self.args.job or any(single_job_update_args)) and self.args.config_file:
            raise Exception('Both job update parameters and a configuration file may not be specified. Please '
                            'specify only one option.')

        # Update a single job
        if self.args.job and any(single_job_update_args):
            transformation_config = None
            if self.args.transformation_config:
                if not os.path.isfile(self.args.transformation_config):
                    raise Exception('{} is not a file'.format(self.args.transformation_config))

                with open(self.args.transformation_config, 'rb') as config_fh:
                    try:
                        transformation_config = config_fh.read()
                        ast.literal_eval(transformation_config)
                    except:
                        raise Exception("could not load transformation configuration from file '{}'.".format(
                            self.args.transformation_config))

            # Convert list of parameters to dict
            parameter_dict = None
            if self.args.parameter:
                parameter_dict = {param[0]: param[1] for param in self.args.parameter}

                # Special case for running_import_nodes
                if parameter_dict.get('running_import_nodes'):
                    if parameter_dict.get('running_import_nodes') != 'all':
                        parameter_dict['running_import_nodes'] = parameter_dict['running_import_nodes'].split(',')

            params = {
                'job_name': self.args.job,
                'parameters': parameter_dict,
                'transformation_config': transformation_config
            }
            res = self.post_json('{hostname}/import/api/ingest/update_job', data=params)
            return self._handle_basic_response(res)
        else:
            # Update jobs through a config file
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
                        raise Exception("could not load configuration from file '{}'.".format(self.args.config_file))

            res = self.post_json('{hostname}/import/api/ingest/batch_update_jobs', data=parsed_config)
            content = json.loads(res.content)
            rows = []
            if content.get('updated_jobs'):
                rows = [[j['job'], ', '.join(j['ignored_params'])] for j in content.get('updated_jobs')]
            return DoResult(entries=rows, headers=['Updated Jobs', 'Skipped Parameters'],
                            message='Skipped parameters are parameters not permitted to be updated. '
                                    'All other parameters were updated.')


class JobPause(SubCommandHandler):

    name = 'pause'
    description = 'Pause a running ingest job. Can specify multiple jobs'

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        add_output_parameters(parser)
        parser.add_argument(
            'job_name',
            help='Names of jobs to be paused',
            type=str,
            nargs='*',
        ).completer = PipelinesCompleter(self)
        parser.add_argument(
            '--all',
            help='Pause all running jobs',
            action='store_const',
            const=1,
            default=0,
        )
        parser.add_argument(
            '--table',
            help='Pause all active jobs for the table',
            type=str,
        ).completer = TablesCompleter(self)

        return parser

    def do(self):
        if sum(1 for p in [self.args.job_name, self.args.all, self.args.table] if p) != 1:
            raise Exception('Exactly one of  --all, --table, or job_name must be specified')

        params = {
            'job_names': self.args.job_name,
            'action': 'pause',
            'all': self.args.all,
            'table': self.args.table
        }
        res = self.post_json('{hostname}/import/api/ingest/toggle_job_status', data=params)
        return self._handle_basic_response(res)


class JobResume(SubCommandHandler):

    name = 'resume'
    description = 'Resume a paused ingest job. Can specify multiple jobs'

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        add_output_parameters(parser)
        parser.add_argument(
            'job_name',
            help='Names of jobs to be resumed',
            type=str,
            nargs='*',
        ).completer = PipelinesCompleter(self)
        parser.add_argument(
            '--all',
            help='Resume all paused jobs',
            action='store_const',
            const=1,
            default=0,
        )
        parser.add_argument(
            '--table',
            help='Resume all paused jobs for the table',
            type=str,
        ).completer = TablesCompleter(self)
        return parser

    def do(self):
        if sum(1 for p in [self.args.job_name, self.args.all, self.args.table] if p) != 1:
            raise Exception('Exactly one of  --all, --table, or job_name must be specified')

        params = {
            'job_names': self.args.job_name,
            'action': 'resume',
            'all': self.args.all,
            'table': self.args.table
        }
        res = self.post_json('{hostname}/import/api/ingest/toggle_job_status', data=params)
        return self._handle_basic_response(res)


class JobDelete(SubCommandHandler):

    name = 'delete'
    description = 'Delete an ingest job. Can specify multiple jobs'

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        add_output_parameters(parser)
        parser.add_argument(
            'job_name',
            help='Names of jobs to be deleted',
            type=str,
            nargs='*',
        ).completer = PipelinesCompleter(self)
        parser.add_argument(
            '--all',
            help='Delete all running and paused jobs',
            action='store_const',
            const=1,
            default=0,
        )
        parser.add_argument(
            '--table',
            help='Pause all running and paused jobs for the table',
            type=str,
        ).completer = TablesCompleter(self)
        add_run_mode(parser)

        return parser

    def do(self):
        if sum(1 for p in [self.args.job_name, self.args.all, self.args.table] if p) != 1:
            raise Exception('Exactly one of  --all, --table, or job_name must be specified')

        params = {
            'job_names': self.args.job_name,
            'action': 'delete',
            'all': self.args.all,
            'table': self.args.table,
            'run': self.args.run
        }
        res = self.post_json('{hostname}/import/api/ingest/toggle_job_status', data=params)
        if not self.args.run:
            print "This is preview mode, the following changes are what would happen if --run/-r was used."
        return self._handle_basic_response(res)


class JobList(SubCommandHandler):

    name = 'list'
    description = 'List ingest jobs. Can filter based on status, table, and type'

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        add_output_parameters(parser)
        parser.add_argument(
            '--status',
            help='List jobs with a specific status',
            choices=['running', 'paused', 'done'],
            type=str,
        )
        parser.add_argument(
            '--table',
            help='List jobs for the given table',
            type=str,
        ).completer = TablesCompleter(self)
        parser.add_argument(
            '--type',
            help='List jobs of the provided type - continuous or onetime',
            choices=['continuous', 'onetime'],
            type=str,
        )

        return parser

    def do(self):
        params = {
            'status': self.args.status,
            'table': self.args.table,
            'type': self.args.type
        }
        res = self.post_json('{hostname}/import/api/ingest/list_jobs', data=params)
        content = json.loads(res.content)

        table_columns = [
            ('name', 'Name'),
            ('table', 'Table'),
            ('type', 'Type'),
            ('start', 'Start'),
            ('end', 'End'),
            ('status', 'Status'),
            ('running_import_nodes', 'Running Import Nodes')
        ]
        entries = [[r[f[0]] for f in table_columns] for r in content.get('jobs', [])]

        table_msg = " for table '{}'".format(self.args.table) if self.args.table else ""
        type_msg = " of type '{}'".format(self.args.type) if self.args.type else ""
        status_msg = " with status '{}'".format(self.args.status) if self.args.status else ""
        empty_warning = "No jobs{}{}{} were found.".format(table_msg, type_msg, status_msg)

        return DoResult(entries=entries, headers=[tc[1] for tc in table_columns], empty_warning=empty_warning)


class JobExport(SubCommandHandler):

    name = 'export'
    description = 'Export ingest job configurations to a file'

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        add_output_parameters(parser)
        parser.add_argument(
            'job',
            help='Name of ingest jobs to export. Can specify multiple jobs.',
            type=str,
            nargs='+'
        ).completer = PipelinesCompleter(self)
        parser.add_argument(
            '-o',
            '--output-file',
            help='File to write configuration to. Default output file is '
            '<ingest job name>_job_config.txt in the current directory',
            type=str
        )
        return parser

    def do(self):
        output_file = '{}_job_config.txt'.format('_'.join(self.args.job))
        if self.args.output_file:
            output_file = self.args.output_file
            if os.path.isfile(output_file):
                print 'Note: a file exists at \'{}\', it will be overwritten.'.format(output_file)
        params = {
            'jobs': self.args.job,
        }
        res = self.post_json('{hostname}/import/api/ingest/export_job', data=params)
        content = json.loads(res.content, object_pairs_hook=OrderedDict)
        try:
            with open(output_file, 'w') as out_fh:
                out_fh.write(json.dumps(content, indent=4))
        except:
            print 'Error writing to file: {}'.format(output_file)
            raise


class JobStats(SubCommandHandler):

    name = 'stats'
    description = ('Display stats for a job. Stats include file count, total raw file sizes, total transformed '
                   'file sizes, and total line count and are grouped by date. A date range may be specified, '
                   'but if not specified, continuous jobs will display stats from their scan window, and '
                   'onetime jobs will display their entire date range')

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        add_output_parameters(parser)
        parser.add_argument(
            'job',
            help='Name of job to get stats for',
            type=str
        ).completer = PipelinesCompleter(self)
        parser.add_argument(
            '-s',
            '--start',
            help='Start of date range of stats to retrieve (inclusive). Date must be in '
            'YYYY-MM-dd or YYYY-MM-ddTHH:mm:ss formats.',
            type=str
        )
        parser.add_argument(
            '-e',
            '--end',
            help='End of date range of stats to retrieve (inclusive). Date must be in '
            'YYYY-MM-dd or YYYY-MM-ddTHH:mm:ss formats.',
            type=str
        )
        return parser

    def _validate_date(self, date_str):
        # return empty if false, parsed date if true
        for fmt in ('%Y-%m-%d', '%Y-%m-%dT%H:%M:%S'):
            try:
                return datetime.datetime.strptime(date_str, fmt)
            except:
                pass
        return None

    def do(self):
        date_range_args = (self.args.start, self.args.end)
        if any(date_range_args) and not all(date_range_args):
            raise Exception('When specifying a date range, both start and end must be specified')

        if all(date_range_args):
            validated_start = self._validate_date(self.args.start)
            validated_end = self._validate_date(self.args.end)
            if not validated_start:
                raise Exception('Invalid start time: {}'.format(self.args.start))
            if not validated_end:
                raise Exception('Invalid end time: {}'.format(self.args.end))
            if validated_end < validated_start:
                raise Exception("End time '{}' cannot be earlier than start time '{}'."
                                .format(self.args.end, self.args.start))

        params = {
            'job_name': self.args.job,
            'start': self.args.start,
            'end': self.args.end
        }
        res = self.post_json('{hostname}/import/api/ingest/job_stats', data=params)
        content = json.loads(res.content)

        table_columns = [
            ('iteration_date', 'Date'),
            ('status', 'Status'),
            ('file_count', 'Files'),
            ('total_raw_size', 'Raw File Size'),
            ('total_transformed_size', 'Transformed File Size'),
            ('total_line_count', 'Line Count')
        ]
        entries = [[r[f[0]] for f in table_columns] for r in content.get('stats', [])]

        empty_warning = ("No statistics were found for {}. It likely did not import anything yet "
                         "(during the timerange if specified).".format(self.args.job))
        return DoResult(entries=entries, headers=[tc[1] for tc in table_columns], empty_warning=empty_warning)
