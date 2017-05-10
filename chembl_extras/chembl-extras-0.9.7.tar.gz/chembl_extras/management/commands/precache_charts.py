__author__ = 'mnowotka'

from django.conf import settings
from django.db import DEFAULT_DB_ALIAS
from django.core.management.base import BaseCommand
from optparse import make_option

from blessings import Terminal
from progressbar import ProgressBar, RotatingMarker, Bar, Percentage, ETA
from chembl_core_model.models import ChemblIdLookup

from time import sleep
from random import random
from urlparse import urlparse
from threading import Thread
import httplib
from Queue import Queue

# ----------------------------------------------------------------------------------------------------------------------

term = Terminal()

WEB_UI_BASE_URL = getattr(settings, 'WEB_UI_BASE_URL', 'https://wwwdev.ebi.ac.uk')
TOTAL_RETRIES = getattr(settings, 'TOTAL_RETRIES', 3)
BACKOFF_FACTOR = getattr(settings, 'BACKOFF_FACTOR', 2)
CONCURRENT_SIZE = getattr(settings, 'CONCURRENT_SIZE', 5)
PROXIES = getattr(settings, 'PROXIES', None)
q = Queue(CONCURRENT_SIZE * 2)

WIDGETS = {
    'COMPOUND': [
        "/chembl/widget/create/compound_activity_chart/compound/activity/",
        "/chembl/widget/create/compound_activity_chart/compound/assay/",
        "/chembl/widget/create/compound_activity_chart/compound/target/",
    ],
    'TARGET': [
        "/chembl/widget/create/target_activity_chart/target/activity/",
        "/chembl/widget/create/target_assay_chart/target/assay/",
        "/chembl/widget/create/target_compoundmw_chart/target/compound_mw/",
        "/chembl/widget/create/target_compoundalogp_chart/target/compound_alogp/",
        "/chembl/widget/create/target_compoundpsa_chart/target/compound_psa/",
        "/chembl/widget/create/target_ligeff_chart/target/lig_eff/"
    ],
    'ASSAY': [
        "/chembl/widget/create/target_activity_chart/target/activity/",
        "/chembl/widget/create/target_assay_chart/target/assay/",
        "/chembl/widget/create/target_compoundmw_chart/target/compound_mw/",
        "/chembl/widget/create/target_compoundalogp_chart/target/compound_alogp/",
        "/chembl/widget/create/target_compoundpsa_chart/target/compound_psa/",
        "/chembl/widget/create/target_ligeff_chart/target/lig_eff/"
    ],
    'DOCUMENT': [
        "/chembl/widget/create/assay_activity_chart/assay/activity/",
        "/chembl/widget/create/assay_compoundmw_chart/assay/compound_mw/",
        "/chembl/widget/create/assay_compoundalogp_chart/assay/compound_alogp/",
        "/chembl/widget/create/assay_compoundpsa_chart/assay/compound_psa/",
        "/chembl/widget/create/assay_target_chart/assay/target/",
    ]}

# ----------------------------------------------------------------------------------------------------------------------

def doWork():
    while True:
        url = q.get()
        tries_left = TOTAL_RETRIES
        status, url = getStatus(url)
        tries_left -= 1
        while status != 200 and tries_left > 0:
            sleep(random())
            status, url = getStatus(url)
            if status != 429:
                tries_left -= 1
        if status != 200:
            print('url {0} returned status {1}'.format(url, status))
        q.task_done()

# ----------------------------------------------------------------------------------------------------------------------

def getStatus(ourl):
    try:
        url = urlparse(ourl)
        conn = httplib.HTTPConnection(url.netloc)
        conn.request("GET", url.path)
        res = conn.getresponse()
        return res.status, ourl
    except:
        return "error", ourl

# ----------------------------------------------------------------------------------------------------------------------


class Writer(object):
    """Create an object with a write method that writes to a
    specific place on the screen, defined at instantiation.
    This is the glue between blessings and progressbar.
    """
    def __init__(self, location):
        """
        Input: location - tuple of ints (x, y), the position
        of the bar in the terminal
        """
        self.location = location

    def write(self, string):
        with term.location(*self.location):
            print(string)

# ----------------------------------------------------------------------------------------------------------------------


class Command(BaseCommand):

    help = "Generate cache for ChEMBL web UI widgets."
    args = '[--database]'

# ----------------------------------------------------------------------------------------------------------------------

    def add_arguments(self, parser):
        parser.add_argument('--database', dest='db',
            default=DEFAULT_DB_ALIAS, help='database')

# ----------------------------------------------------------------------------------------------------------------------

    def handle(self, *args, **options):
        self.db = options.get('db')
        self.verbosity = options.get('verbosity')

        if self.verbosity > 1:
            print self.help
        with term.fullscreen():
            print(term.clear())
            for i in range(CONCURRENT_SIZE):
                t = Thread(target=doWork)
                t.daemon = True
                t.start()
            try:
                writer = Writer((0, 0))
                objects = ChemblIdLookup.objects.using(self.db).all()
                count = objects.count()
                pbar = ProgressBar(widgets=['OBJECTS: ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA()],
                    fd=writer, maxval=count).start()
                for i in range(0,count,CONCURRENT_SIZE):
                    chunk = objects[i:i+CONCURRENT_SIZE]
                    for obj in chunk:
                        for widget_url in WIDGETS[obj.entity_type]:
                            url = '{0}{1}{2}'.format(WEB_UI_BASE_URL, widget_url, obj.pk)
                            q.put(url)
                    q.join()
                    pbar.update(i)

                pbar.update(count)
                pbar.finish()

            except Exception as e:
                print e.message

# ----------------------------------------------------------------------------------------------------------------------




