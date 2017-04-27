from datetime import datetime
from datetime import timedelta

from django.core.management.base import BaseCommand

from ...contstants import STATUS_ARCHIVED
from ...models import Log


class Command(BaseCommand):

    def handle(self, *args, **options):
        end_date = datetime.today().date()
        start_date = end_date + timedelta(days=-30)
        logs = Log.objects.filter(created_at__gte=start_date)
        logs.update(status=STATUS_ARCHIVED)
