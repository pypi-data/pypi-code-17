import re, os, logging, subprocess, platform
from tempfile import NamedTemporaryFile
from django.conf import settings


_log = logging.getLogger(__name__)

NULL_FILE = 'nul' if 'Windows' in platform.system() else '/dev/null'


class BCP(object):

    '''
    https://docs.microsoft.com/en-us/sql/tools/bcp-utility
    '''

    target_model = None
    bcp_path = None

    _command_args_base = None
    _db_args = None
    _table_name = None
    _field_column_map = None

    def __init__(self, target_model, bcp_path='bcp'):
        self.bcp_path = bcp_path
        self.set_target_model(target_model)

    def save(self, rows):

        # Create the bcp FORMAT file from target_model
        bcp_format = self._make_format()

        # Create a temporary file to hold bulk data
        with NamedTemporaryFile(delete=True) as f:
            outfile = '%s_%s.csv' % (f.name, self._table_name)

        # Write bulk data based on FORMAT file
        _log.debug('Writing bulk data file %s', outfile)

        with open(outfile, 'w') as f:
            for row in rows:
                for field in bcp_format.fields:
                    model_field = self._field_column_map[field.column_name]
                    val = row.get(model_field.name, None) or ''
                    val = getattr(val, 'id', val) # if ForeignKey, we need id
                    if model_field.__class__.__name__ == 'DecimalField':
                        val = ('%.' + str(model_field.decimal_places) + 'f') % float(val or 0)
                    f.write(str(val))
                    f.write(field.delimiter)

        # Do bulk import via bcp
        _log.debug('Calling bcp')
        import_result = _run_cmd(self._command_args_base + ['IN', outfile] + self._db_args + ['-f', bcp_format.filename])

        # Cleanup temp files
        os.remove(outfile)
        os.remove(bcp_format.filename)

        _log.debug(import_result)

        return import_result

    def set_target_model(self, target_model):
        self.target_model = target_model
        db_settings = settings.DATABASES[target_model.objects.db]
        self._table_name = target_model._meta.db_table
        DB_DSN = db_settings.get('OPTIONS', {}).get('dsn')
        full_table_name = '%s.dbo.%s' % (db_settings['NAME'], self._table_name)
        self._command_args_base = [self.bcp_path, full_table_name]
        self._db_args = [
            '-S', DB_DSN or db_settings.get('HOST'),
            '-U', db_settings['USER'],
            '-P', db_settings.get('PASSWORD')]

        if DB_DSN:
            self._db_args.append('-D')

        self._field_column_map = {(f.db_column or f.name): f for f in target_model._meta.fields}

    def _make_format(self):
        bcp_format = BCPFormat()
        bcp_format.make(self._command_args_base, self._db_args)
        return bcp_format


class BCPFormat(object):

    '''
    Deals with bcp FORMAT command
    '''

    filename = None
    fields = None

    _sql_version = None
    _num_fields = None

    def make(self, cmd_args, db_args):
        '''
        Runs bcp FORMAT command to create a format file that will assist in creating the bulk data file
        '''
        with NamedTemporaryFile(delete=True) as f:
            format_file = f.name + '.bcp-format'
        format_args = cmd_args + ['format', NULL_FILE, '-c', '-f', format_file, '-t,'] + db_args
        _run_cmd(format_args)
        self.load(format_file)
        return format_file

    def load(self, filename=None):
        '''
        Reads a non-XML bcp FORMAT file and parses it into fields list used for creating bulk data file
        '''
        fields = []
        with open(filename, 'r') as f:
            format_data = f.read().strip()

        lines = format_data.split('\n')
        self._sql_version = lines.pop(0)
        self._num_fields = int(lines.pop(0))

        for line in lines:
            # Get rid of mulitple spaces
            line = re.sub(' +', ' ', line)
            row_format = BCPFormatRow(line.split(' '))
            fields.append(row_format)

        self.fields = fields
        self.filename = filename


class BCPFormatRow(object):

    '''
    Describes a table column, obtained from a row in a bcp FORMAT file
    https://docs.microsoft.com/en-us/sql/relational-databases/import-export/media/mydepart-fmt-ident-c.gif
    '''

    _fields = [
        'client_field_i',
        'data_type',
        'data_prefix_len',
        'field_length',
        'delimiter',
        'server_field_order_i',
        'column_name',
        'str_collection'
    ]

    def __init__(self, data):
        for i in range(len(self._fields)):
            setattr(self, self._fields[i], data[i])

        self.delimiter = self.delimiter.strip('"').decode('string_escape')
        self.field_length = int(self.field_length)
        self.data_prefix_len = int(self.data_prefix_len)
        self.client_field_i = int(self.client_field_i)
        self.server_field_order_i = int(self.server_field_order_i)

        if self.data_prefix_len > 0:
            # https://docs.microsoft.com/en-us/sql/relational-databases/import-export/specify-prefix-length-in-data-files-by-using-bcp-sql-server
            raise Exception('data_prefix_length is not supported. Format file must be created using -c option')


def _run_cmd(args):
    proc = subprocess.Popen(args, stderr=subprocess.STDOUT)
    output, err = proc.communicate()
    returncode = proc.wait()
    if output:
        _log.debug(output)
    if returncode != 0:
        # Remove password so it doesn't show in logs
        args.pop(args.index('-P') + 1)
        raise Exception('BCP command failed: %s' % args)
    return output
