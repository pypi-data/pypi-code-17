from django.core.management.base import BaseCommand, CommandError
from users.utils import start_schedule_thread, tasks_email_schedule, project_deadline_schedule


class Command(BaseCommand):
    help = 'Starts the threads for scheduled tasks'

    def handle(self, *args, **options):
        tasks_email_schedule()
        project_deadline_schedule()
        # start_schedule_thread()
        self.stdout.write(self.style.SUCCESS('Completed scheduled tasks for the day.'))
