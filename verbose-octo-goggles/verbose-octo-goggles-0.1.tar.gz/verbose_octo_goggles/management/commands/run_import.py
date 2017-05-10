from datetime import datetime

from django.conf import settings as django_settings
from django.core.management.base import BaseCommand

from config import OCTO_GOGGLES_MAPPING


class Command(BaseCommand):
    help = (
        "Run import of some source. First argument is source name,"
        " second is type of import (look at clients.sources.__init__)"
    )

    def add_arguments(self, parser):
        parser.add_argument('source_name', nargs=1, type=str)
        parser.add_argument('importer_type', nargs=1, type=str)

        parser.add_argument(
            '--datetime',
            action='store',
            dest='datetime',
            default=False,
            help='Push some date to the importer YEAR-MO-DY'
        )

        parser.add_argument(
            '--start-from',
            action='store',
            dest='start-from',
            default=False,
            help='Skip some pages from the import'
        )

        # temporary argument to run import for united kingdom
        parser.add_argument(
            '--clear',
            action='store_true',
            dest='clear_folder',
            default=False,
            help='Clear working directory of the reader/importer'
        )

        # An option for multireader-based importers
        parser.add_argument(
            '--reader',
            action='store',
            dest='reader_name',
            default=False,
            help='Put a name of the reader class here.'
        )

        # For initial importers - so that only inserts occur
        parser.add_argument(
            '--initial',
            action='store_true',
            dest='is_initial',
            default=False,
            help='Perform iserts only. Collection is blank.'
        )
        # An option to read a single item.
        # You can see implementation of this option at companieshouse.reader.APIReader
        parser.add_argument(
            '--item_id',
            action='store',
            dest='item_id',
            default=False,
            help='Put an id of the item to grab.'
        )

        # An option to pass to reader.
        parser.add_argument(
            '--filename',
            action='store',
            dest='filename',
            default=False,
            help='Define a filename.'
        )
        parser.add_argument(
            '--path',
            action='append',
            dest='sources',
            default=[],
            help='Define a list of FTP folders to parse from EDGAR'
        )
        parser.add_argument(
            '--keyword',
            action='append',
            dest='sources',
            default=[],
            help='Define a list of keywords to search with company in Twitter Search API'
        )

        parser.add_argument(
            '--debug',
            action='store_true',
            dest='is_debug',
            default=False,
            help='Launch pdb debugger on exceptions. default is false'
        )

    def handle(self, *args, **options):
        source_name = options['source_name'][0]
        importer_type = options['importer_type'][0]
        importer = OCTO_GOGGLES_MAPPING[source_name][importer_type]
        settings = {}
        if options.get('datetime'):
            if options.get('datetime') == 'None':
                arg_datetime = None
            else:
                arg_datetime = datetime.strptime(
                    options['datetime'], '%Y-%m-%d-%H-%M'
                )
            importer.arg_datetime = arg_datetime
            settings['arg_datetime'] = arg_datetime
        if options.get('start-from'):
            importer.start_from = int(options.get('start-from'))
            settings['start_from'] = int(options.get('start-from'))
        if options.get('clear_folder'):
            settings['clear_folder'] = options.get('clear_folder')
        if options.get('reader_name'):
            settings['reader_name'] = options.get('reader_name')
        if options.get('is_initial'):
            settings['is_initial'] = options.get('is_initial')
        if options.get('item_id'):
            settings['item_id'] = options.get('item_id')
        if options.get('filename'):
            settings['filename'] = options.get('filename')
        if options.get('sources'):
            settings['sources'] = options.get('sources')

        settings['debug'] = options.get('is_debug', False)

        importer(type_code=importer_type, settings=settings).process()

