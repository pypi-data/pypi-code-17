from django.core.management.base import BaseCommand

from ...contstants import STATUS_ARCHIVED

from ...models import Log


class Command(BaseCommand):

    def handle(self, *args, **options):
        logs = Log.objects.filter(status=STATUS_ARCHIVED)
        logs.delete()
