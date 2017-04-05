from django.core.management.base import BaseCommand, CommandError
from users.models import *


class Command(BaseCommand):
    help = 'Setup the database for the first time.'

    def handle(self, *args, **options):
        r = Role()
	    r.title = 'Security Coordinator'
	    r.save()
	    r1 = Role(title='Software Coordinator')
	    r1.save()
	    r2 = Role(title='Secretary')
	    r2.save()
	    r3 = Role(title='Librarian')
	    r3.save()
	    r4 = Role(title='Others')
	    r4.save()

	    adm1 = AdminUser(username='10101010', first_name='Default', last_name='Admin')
	    adm1.email = 'hex.omega@yandex.com'
	    adm1.set_password('qwerty123')
	    adm1.save()


        self.stdout.write(self.style.SUCCESS('Created admin user and roles.'))
