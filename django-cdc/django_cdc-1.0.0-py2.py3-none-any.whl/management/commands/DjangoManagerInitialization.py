from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('table_name', nargs='+', type=str)

    def handle(self, *args, **options):
        for table_name in options['table_name']:
            try:
                self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % table_name))
            except:
                raise CommandError('Something went wrong!!')
