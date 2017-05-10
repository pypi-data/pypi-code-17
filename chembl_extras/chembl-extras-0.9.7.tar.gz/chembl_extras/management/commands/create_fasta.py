__author__ = 'mnowotka'

import django
from django.core.management.commands.inspectdb import Command as BaseCommand
from django.db import connections
from optparse import make_option
from progressbar import ProgressBar, RotatingMarker, Bar, Percentage, ETA
from django.conf import settings
from colorama import init
from termcolor import colored
import sys, os
import gzip, bz2

init()


try:
    from chembl_compatibility.models import TargetDictionary
except ImportError:
    from chembl_core_model.models import TargetDictionary


# ----------------------------------------------------------------------------------------------------------------------


class Command(BaseCommand):
    help = "This script generates a fasta file of chembl data"

# ----------------------------------------------------------------------------------------------------------------------

    def add_arguments(self, parser):
        parser.add_argument('--filename', action='store', dest='filename', default=None, help='Output file')

# ----------------------------------------------------------------------------------------------------------------------

    def handle(self, **options):
        if settings.DEBUG:
            print "Django is in debug mode, which causes memory leak. Set settings.DEBUG to False and run again."
            return

        django.db.reset_queries()
        qs = TargetDictionary.objects.all().values_list('tid', 'pref_name', 'organism',
                                                        'targetcomponents__component__sequence', 'description',
                                                        'chembl_id',
                                                        'targetcomponents__component__accession').order_by('tid')
        count = qs.count()

        filename = options.get('filename')
        if not filename:
            file = sys.stdout
        else:
            _, file_extension = os.path.splitext(filename)
            if file_extension == '.txt':
                file = open(filename, "w") if filename else sys.stdout
            elif file_extension == '.gz':
                file = gzip.open(filename, 'wb')
            elif file_extension == '.bz2':
                file = bz2.BZ2File(filename, 'w')
            else:
                print (colored('Unrecognized file extension: %s' % file_extension, 'red'))
                sys.exit()

        pbar = ProgressBar(
            widgets=['CREATING BLAST DB: ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA()],
            maxval=count,
            fd=open(os.devnull, "w") if not filename else sys.stderr).start()

        counter = 0

        for res in qs:
            if res[3]:
                name = res[1] or res[4]
                accession = '[%s]' % res[6] if res[6] else ''
                file.write(">%s %s %s (%s)\n%s\n" % (res[5], accession, name, res[2], res[3]))
            pbar.update(counter)
            counter += 1
        pbar.update(count)
        pbar.finish()

# ----------------------------------------------------------------------------------------------------------------------
