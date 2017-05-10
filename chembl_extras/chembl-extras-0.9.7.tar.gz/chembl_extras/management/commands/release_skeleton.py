__author__ = 'mnowotka'

import django
from django.core.management import call_command
from django.core.management.commands.inspectdb import Command as BaseCommand
from django.template.loader import render_to_string
from django.db import connections
from optparse import make_option
from progressbar import ProgressBar, RotatingMarker, Bar, Percentage, ETA
from django.conf import settings
import tempfile
import shutil
import sys, os
from datetime import date
from django.db import connections
import hashlib
import subprocess
from dateutil.parser import parse
import tarfile
import gzip

try:
    from chembl_compatibility.models import TargetDictionary
except ImportError:
    from chembl_core_model.models import TargetDictionary

try:
    from chembl_compatibility.models import MoleculeDictionary
except ImportError:
    from chembl_core_model.models import MoleculeDictionary


DUMP_COMMANDS = {
    'postgres': 'pg_dump -h %(HOST)s -p %(PORT)s -U %(USER)s %(NAME)s -O --no-tablespaces -f %(FILENAME)s -W',
    'mysql': 'mysqldump -u %(USER)s -h %(HOST)s --protocol=tcp -P %(PORT)s --default-character-set=utf8 -p%(PASSWORD)s --skip-triggers %(NAME)s -r %(FILENAME)s',
    'sqlite': 'sqlite3 %(NAME)s < make_chemreps',
    'oracle': 'exp %(USER)s/%(PASSWORD)s@%(NAME)s file=%(FILENAME)s OWNER=%(USER)s GRANTS=N STATISTICS=NONE'
}

ORACLE_DUMPS = {
    '9i': {
        "ORACLE_BASE": "/sw/arch/dbtools/oracle",
        "ORACLE_HOME": "/product/9.2.0.7",
        "TNS_ADMIN": "/network/admin",
        "ORA_NLS32": "/ocommon/nls/admin/data",
        "NLS_LANG": "AMERICAN_AMERICA.US7ASCII",
        "NLS_DATE_FORMAT": "DD-MON-RRRR HH24:MI:SS",
    },

    '10g': {
        "ORACLE_BASE": "/sw/arch/x86_64-linux/dbtools/oracle",
        "ORACLE_HOME": "/product/10.2.0_msd",
        "TNS_ADMIN": "/network/admin",
        "ORA_NLS32": "/nls/data",
        "NLS_LANG": "AMERICAN_AMERICA.al32utf8",
        "NLS_DATE_FORMAT": "DD-MON-RRRR HH24:MI:SS",
    },

    '11g': {
        "ORACLE_BASE": "/sw/arch/x86_64-linux/dbtools/oracle",
        "ORACLE_HOME": "/product/11.1.0.6.2/client",
        "TNS_ADMIN": "/network/admin",
        "ORA_NLS32": "/nls/data",
        "NLS_LANG": "AMERICAN_AMERICA.al32utf8",
        "NLS_DATE_FORMAT": "DD-MON-RRRR HH24:MI:SS",
    }
}

DB_VERSIONS = {
    'mysql_ver': '5.0',
    'postgres_ver': '9.1.4',
    'sqlite_ver': '3.8.5',
}

# ----------------------------------------------------------------------------------------------------------------------


def make_env(version):
    env = os.environ.copy()
    ret = ORACLE_DUMPS.get(version, {}).copy()
    ret["ORACLE_HOME"] = ret["ORACLE_BASE"] + ret["ORACLE_HOME"]
    ret["TNS_ADMIN"] = ret["ORACLE_HOME"] + ret["TNS_ADMIN"]
    ret["ORA_NLS32"] = ret["ORACLE_HOME"] + ret["ORA_NLS32"]
    ret["LD_LIBRARY_PATH"] = ret["ORACLE_HOME"] + '/lib:' + env["LD_LIBRARY_PATH"]
    ret["PATH"] = ret["ORACLE_HOME"] + '/bin:' + env["PATH"]
    return ret

# ----------------------------------------------------------------------------------------------------------------------


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    shutil.rmtree(source_dir)

# ----------------------------------------------------------------------------------------------------------------------


def sha256_for_file(path, block_size=4096):
    try:
        with open(path, 'rb') as rf:
            h = hashlib.sha256()
            for chunk in iter(lambda: rf.read(block_size), b''):
                h.update(chunk)
        return h.hexdigest()
    except IOError:
        return None, path

# ----------------------------------------------------------------------------------------------------------------------


def make_checksums_file(directory, file='checksums.txt'):
    with open(os.path.join(directory, file), 'w') as f:
        f.write('file\tSHA256\n\n')
        for _, _, filenames in os.walk(directory, topdown=False):
            for filename in filenames:
                hash = sha256_for_file(os.path.join(directory, filename))
                f.write('%s\t%s\n' % (filename, hash))

# ----------------------------------------------------------------------------------------------------------------------


def gzip_file(file_path):
    f_in = open(file_path)
    f_out = gzip.open(file_path + '.gz', 'wb')
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()
    os.remove(file_path)

# ----------------------------------------------------------------------------------------------------------------------


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

# ----------------------------------------------------------------------------------------------------------------------


class Command(BaseCommand):

    help = "This script generates a blast db out of chembl data"

# ----------------------------------------------------------------------------------------------------------------------

    def add_arguments(self, parser):
        parser.add_argument('--release', action='store', dest='release', help='release name, for example chembl_14')
        parser.add_argument('--date', action='store', dest='date', help='release date, default is today')
        parser.add_argument('--contact', action='store', dest='contact', default="chembl-help@ebi.ac.uk",
                            help='contact email, default is chembl-help@ebi.ac.uk')

# ----------------------------------------------------------------------------------------------------------------------

    def handle(self, **options):
        if settings.DEBUG:
            print "Django is in debug mode, which causes memory leak. Set settings.DEBUG to False and run again."
            return

        self.release = options.get('release')
        self.date = parse(options.get('date') or '')
        self.contact = options.get('contact')

        if not self.release:
            print 'No release name given, please specify release name (for example chembl_14)'
            return

        base_folder = tempfile.mkdtemp()

        print 'Saving to %s' % base_folder

        new_location = os.path.join(base_folder, self.release)
        os.mkdir(new_location)

        mysql_dir = os.path.join(new_location,'%s_mysql' % self.release)
        postgres_dir = os.path.join(new_location,'%s_postgresql' % self.release)
        sqlite_dir = os.path.join(new_location,'%s_sqlite' % self.release)
        oracle_11g_dir = os.path.join(new_location,'%s_oracle11g' % self.release)
        oracle_10g_dir = os.path.join(new_location,'%s_oracle10g' % self.release)
        oracle_9i_dir = os.path.join(new_location,'%s_oracle9i' % self.release)

        os.mkdir(mysql_dir)
        os.mkdir(postgres_dir)
        os.mkdir(sqlite_dir)
        os.mkdir(oracle_11g_dir)
        os.mkdir(oracle_10g_dir)
        os.mkdir(oracle_9i_dir)

        self.template_2_file(os.path.join(new_location, 'LICENSE'), 'chembl_extras/LICENSE.tmpl')
        self.template_2_file(os.path.join(new_location, 'README'), 'chembl_extras/README.tmpl')
        self.template_2_file(os.path.join(new_location, 'REQUIRED.ATTRIBUTION'), 'chembl_extras/REQUIRED.ATTRIBUTION.tmpl')

        self.template_2_file(os.path.join(mysql_dir, 'INSTALL'), 'chembl_extras/mysql/INSTALL.tmpl')
        self.template_2_file(os.path.join(oracle_11g_dir, 'INSTALL'), 'chembl_extras/oracle_11g/INSTALL.tmpl')
        self.template_2_file(os.path.join(oracle_10g_dir, 'INSTALL'), 'chembl_extras/oracle_10g/INSTALL.tmpl')
        self.template_2_file(os.path.join(oracle_9i_dir, 'INSTALL'), 'chembl_extras/oracle_9i/INSTALL.tmpl')
        self.template_2_file(os.path.join(postgres_dir, 'INSTALL'), 'chembl_extras/postgres/INSTALL.tmpl')
        self.template_2_file(os.path.join(sqlite_dir, 'INSTALL'), 'chembl_extras/sqlite/INSTALL.tmpl')

        print 'OK, directory structure, installation instruction, licenses and readme files are now in place.'
        print 'Generating other files...'

        with cd(new_location):
            call_command('create_blastdb', mode="download")
            # call_command('sdfexport')

        # self.make_dump('oracle', os.path.join(oracle_9i_dir, '%s_9i.dmp' % self.release), my_env=make_env('9i'))
        # self.make_dump('oracle', os.path.join(oracle_9i_dir, '%s_10g.dmp' % self.release), my_env=make_env('10g'))
        # self.make_dump('oracle', os.path.join(oracle_9i_dir, '%s_11g.dmp' % self.release), my_env=make_env('11g'))
        # self.make_dump('postgres', os.path.join(postgres_dir, '%s.pgdump.sql' % self.release))
        # self.make_dump('mysql', os.path.join(mysql_dir, '%s.mysqldump.sql' % self.release))
        # self.template_2_file('make_chemreps', 'chembl_extras/sqlite/make_chemreps.tmpl')
        # chemreps = os.path.join(new_location, '%s_chemreps.txt' % self.release)
        # self.make_dump('sqlite', chemreps)
        # gzip_file(chemreps)
        # os.remove('make_chemreps')

        print 'compressing data dumps...'
        make_tarfile(os.path.join(new_location,'%s_mysql.tar.gz' % self.release), mysql_dir)
        make_tarfile(os.path.join(new_location,'%s_postgresql.tar.gz' % self.release), postgres_dir)
        make_tarfile(os.path.join(new_location,'%s_sqlite.tar.gz' % self.release), sqlite_dir)
        make_tarfile(os.path.join(new_location,'%s_oracle11g.tar.gz' % self.release), oracle_11g_dir)
        make_tarfile(os.path.join(new_location,'%s_oracle10g.tar.gz' % self.release), oracle_10g_dir)
        make_tarfile(os.path.join(new_location,'%s_oracle9i.tar.gz' % self.release), oracle_9i_dir)

        make_checksums_file(new_location)

        # shutil.rmtree(base_folder)


# ----------------------------------------------------------------------------------------------------------------------

    def template_2_file(self, filepath, template_name):
        context = {'release_version': self.release, 'release_date': self.date, 'contact': self.contact}
        context.update(DB_VERSIONS)
        content = render_to_string(template_name, context)
        with open(filepath, 'w') as f:
            f.write(content)

# ----------------------------------------------------------------------------------------------------------------------

    def make_dump(self, engine, output, my_env=None):

        if engine not in connections.databases:
            print 'There is no connection named %s in the django settings so, dumping %s will be ignored' % (engine, engine)
            return
        if engine not in DUMP_COMMANDS:
            print "I don't know the dump command for the %s engine. Ignoring." % engine
            return
        print 'Generating %s data dump' % engine
        conn = connections.databases[engine].copy()
        conn.update({'FILENAME': output})
        command = 'time(%s)' % (DUMP_COMMANDS[engine] % conn)
        print 'command:'
        print command
        env = None
        if my_env:
            env = os.environ.copy()
            env.update(my_env)
        proc = subprocess.Popen(command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, shell=True, env=env)
        proc.communicate()
        print '%s dump process has finished with the status code %s' % (engine, proc.returncode)

# ----------------------------------------------------------------------------------------------------------------------



