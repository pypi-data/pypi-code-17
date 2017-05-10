__author__ = 'mnowotka'

import django
from django.core.management.commands.inspectdb import Command as BaseCommand
from django.db import connections
from optparse import make_option
from progressbar import ProgressBar, RotatingMarker, Bar, Percentage, ETA
from django.conf import settings
import sys, os
import gzip, bz2

try:
    from chembl_compatibility.models import TargetDictionary
except ImportError:
    from chembl_core_model.models import TargetDictionary

try:
    from chembl_compatibility.models import MoleculeDictionary
except ImportError:
    from chembl_core_model.models import MoleculeDictionary

SETTINGS = {
    'DOWNLOAD': [
        {
            'filename': 'chembl_22.fa.gz',
            'values': ['chembl_id', 'targetcomponents__component__accession',
                       'targetcomponents__component__description', 'targetcomponents__component__organism',
                       'targetcomponents__component__sequence'],
            'model': TargetDictionary,
            'filters': {'targetcomponents__component__component_type': 'PROTEIN'},
            'line_template': '> %(chembl_id)s [%(targetcomponents__component__accession)s] %(targetcomponents__component__description)s (%(targetcomponents__component__organism)s)\n%(targetcomponents__component__sequence)s\n',
        },
        {
            'filename': 'chembl_22_bio.fa.gz',
            'values': ['chembl_id', 'biotherapeutics__bio_component_sequences__component_id',
                       'biotherapeutics__bio_component_sequences__description',
                       'biotherapeutics__bio_component_sequences__organism',
                       'biotherapeutics__bio_component_sequences__sequence'],
            'model': MoleculeDictionary,
            'filters': {'biotherapeutics__bio_component_sequences__sequence__isnull': False},
            'line_template': '> %(chembl_id)s [%(biotherapeutics__bio_component_sequences__component_id)s] %(biotherapeutics__bio_component_sequences__description)s (%(biotherapeutics__bio_component_sequences__organism)s)\n%(biotherapeutics__bio_component_sequences__sequence)s\n',
        }
    ],
    'INTERFACE': [
        {
            'filename': 'chembl_22.fa',
            'values': ['tid', 'pref_name', 'organism', 'targetcomponents__component__sequence'],
            'model': TargetDictionary,
            'filters': {'targetcomponents__component__component_type': 'PROTEIN'},
            'line_template': '>%(tid)s %(pref_name)s (%(organism)s)\n%(targetcomponents__component__sequence)s\n',
        },
        {
            'filename': 'chembl_22_mab.fa',
            'values': ['biotherapeutics__bio_component_sequences__component_id',
                       'biotherapeutics__bio_component_sequences__sequence'],
            'model': MoleculeDictionary,
            'filters': {'biotherapeutics__bio_component_sequences__sequence__isnull': False},
            'line_template': '> %(biotherapeutics__bio_component_sequences__component_id)s\n%(biotherapeutics__bio_component_sequences__sequence)s\n',
        }
    ]
}

# ----------------------------------------------------------------------------------------------------------------------


class Command(BaseCommand):

    help = "This script generates a blast db out of chembl data"

# ----------------------------------------------------------------------------------------------------------------------

    def add_arguments(self, parser):
        parser.add_argument('--model', action='store', dest='mode', help='mode (can be "download" or "interface")')

# ----------------------------------------------------------------------------------------------------------------------

    def handle(self, **options):
        if settings.DEBUG:
            print "Django is in debug mode, which causes memory leak. Set settings.DEBUG to False and run again."
            return

        mode = options.get('mode')

        files = SETTINGS[mode.upper()]
        for file in files:
            self.db_to_file(**file)

# ----------------------------------------------------------------------------------------------------------------------

    def db_to_file(self, values, filename, model, filters, line_template):
        django.db.reset_queries()
        qs = model.objects.all()
        if filters:
            qs = qs.filter(**filters)
        qs = qs.values(*values)
        count = qs.count()

        if not filename:
            file = sys.stdout
        else:
            _, file_extension = os.path.splitext(filename)
            if file_extension == '.gz':
                file = gzip.open(filename, 'wb')
            elif file_extension == '.bz2':
                file = bz2.BZ2File(filename, 'w')
            else:
                file = open(filename, "w") if filename else sys.stdout

        pbar = ProgressBar(
            widgets=['Writing %s: ' % filename, Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA()],
            maxval=count,
            fd=open(os.devnull, "w") if not filename else sys.stderr).start()

        counter = 0

        for res in qs:
            line = line_template % res
            line = line.replace(' (None)', '')
            line = line.replace(' None', '')
            line = line.replace(' \n', '\n')
            file.write(line)
            pbar.update(counter)
            counter += 1
        pbar.update(count)
        pbar.finish()

# ----------------------------------------------------------------------------------------------------------------------

