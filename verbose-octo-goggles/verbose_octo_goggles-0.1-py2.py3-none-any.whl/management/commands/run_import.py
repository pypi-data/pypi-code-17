from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from django.utils.module_loading import import_string

from verbose_octo_goggles.config import OCTO_GOGGLES_MAPPING
from verbose_octo_goggles.core import StopImport


class Command(BaseCommand):
    help = (
        "Run import of some source. First argument is source name, second is type of import"
    )

    def add_arguments(self, parser):
        parser.add_argument('source_name', nargs=1, type=str)
        parser.add_argument('importer_type', nargs=1, type=str)

        parser.add_argument(
            '--debug',
            action='store_true',
            dest='debug',
            default=False,
            help='Launch ipdb debugger on exceptions. default is false'
        )

    def handle(self, *args, **options):
        source_name = options['source_name'][0]
        importer_type = options['importer_type'][0]
        importer = self.get_importer(source_name, importer_type)

        try:
            importer(type_code=importer_type, settings=options).process()

        except StopImport as e:
            print(e)
        except:
            if options.get('debug'):
                import sys
                exc_type, exc_value, exc_tb = sys.exc_info()
                print(exc_type, exc_value)
                import ipdb
                ipdb.post_mortem(exc_tb)
            else:
                raise

    def get_importer(self, source_name, reader_class):
        if source_name in OCTO_GOGGLES_MAPPING:
            if reader_class in OCTO_GOGGLES_MAPPING[source_name]:
                return import_string(OCTO_GOGGLES_MAPPING[source_name][reader_class])
            else:
                raise ImproperlyConfigured('Wrong import type')
        else:
            raise ImproperlyConfigured('Wrong source type')
