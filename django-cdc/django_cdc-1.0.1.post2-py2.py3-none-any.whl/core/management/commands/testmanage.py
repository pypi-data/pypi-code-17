from django.core.management import BaseCommand
from django.apps import apps

# The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
    # Show this when the user types help
    help = "My test command"


    # A command must define handle()
    def handle(self, *args, **options):
        for ct in apps.get_models():
            self.stdout.write(ct)