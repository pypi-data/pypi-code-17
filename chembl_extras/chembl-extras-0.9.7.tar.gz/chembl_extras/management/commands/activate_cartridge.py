__author__ = 'mnowotka'

import django
from django.core.management.commands.inspectdb import Command as BaseCommand
from django.db import connections, DEFAULT_DB_ALIAS
from optparse import make_option
from django.core.management.base import CommandError
from progressbar import ProgressBar, RotatingMarker, Bar, Percentage, ETA, Counter
import sys
from colorama import init
from termcolor import colored
from django.conf import settings
from django.db import transaction

init()

LINE = '#' + '-' * 119

# ----------------------------------------------------------------------------------------------------------------------

INDEX_PREFIX_NAME = 'MOLIDX_CMPDMO%'

DEACTIVATE_OLD_CARTRIDGE_SQL = 'mdlaux.unsetup'

ACTIVATE_NEW_CARTRIDGE_SQL = 'C$DIRECT2016.MDLAUXOP.SETUP'

COLLECT_STATS = "DBMS_STATS.GATHER_TABLE_STATS"

DROP_INDEXES_SQL = """SELECT 'DROP ' || object_type || ' ' || object_name || ';'
FROM user_objects where object_name like %s;"""

DROP_TABLES_SQL = 'drop table COMPOUND_MOLS'

CREATE_TABLES_SQL = """
CREATE TABLE "COMPOUND_MOLS"
  (	"MOLREGNO" NUMBER(9,0),
	"CTAB" BLOB,
	 CONSTRAINT "PK_CMPDMOL_MOLREGNO" PRIMARY KEY ("MOLREGNO")
USING INDEX PCTFREE 10 INITRANS 2 MAXTRANS 255 COMPUTE STATISTICS
STORAGE(INITIAL 15728640 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1 BUFFER_POOL DEFAULT),
	 CONSTRAINT "FK_CMPDMOL_MOLREGNO" FOREIGN KEY ("MOLREGNO")
	  REFERENCES "MOLECULE_DICTIONARY" ("MOLREGNO") ENABLE
  ) PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 NOCOMPRESS LOGGING
STORAGE(INITIAL 796917760 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1 BUFFER_POOL DEFAULT)
LOB ("CTAB") STORE AS BASICFILE (
DISABLE STORAGE IN ROW )
        """

CREATE_INDEXES_SQL = """CREATE INDEX MOLIDX_CMPDMOL ON
        COMPOUND_MOLS(CTAB) INDEXTYPE IS "C$DIRECT2016"."MXIXMDL"
        PARAMETERS ('TEMPDIR=/transport/TEMPDIR');"""


COUNT_STRUCTURES_SQL = "SELECT COUNT(*) FROM compound_structures"

SELECT_MOLREGNO_SQL = "SELECT molregno FROM compound_structures"

ADD_COMPOUND_TO_INDEX_SQL = """insert into COMPOUND_MOLS (molregno, ctab)
select compound_structures.molregno, mol(compound_structures.molfile)
from compound_structures
where molregno=%s"""

COUNT_MOLECULES_SQL = "SELECT COUNT(*) FROM COMPOUND_MOLS"

# ----------------------------------------------------------------------------------------------------------------------


class Command(BaseCommand):
    help = "This script removes all cartridge related objects, activates new Biovia Direct cartridge and recreates " \
           "necessary objects and indexes."

    r_connection = None
    w_connection = None
    r_cursor = None
    w_cursor = None

# ----------------------------------------------------------------------------------------------------------------------

    def add_arguments(self, parser):
        parser.add_argument('--source', action='store', dest='source',
                            default=DEFAULT_DB_ALIAS, help='connection details for reading the database')
        parser.add_argument('--target', action='store', dest='target',
                            default=DEFAULT_DB_ALIAS + '_write', help='connection details for writing the database')

# -----------------------------------------------------------------------------------------------------------------------

    def handle(self, **options):
        if settings.DEBUG:
            print "Django is in debug mode, which causes memory leak. Set settings.DEBUG to False and run again."
            return

        django.db.reset_queries()
        self.handle_activation(options)

# ----------------------------------------------------------------------------------------------------------------------

    def handle_activation(self, options):

        # source and target should point to the same schema, we just need two separate DB connections
        # one for reading and one for writing
        source = options.get('source')
        target = options.get('target')

        with transaction.atomic(using=target):

            self.r_connection = connections[source]
            self.w_connection = connections[target]
            if self.r_connection.vendor != 'oracle' or self.w_connection.vendor != 'oracle':
                raise NotImplementedError
            self.r_cursor = self.r_connection.cursor()
            self.w_cursor = self.w_connection.cursor()

            self.try_execute_proc(DEACTIVATE_OLD_CARTRIDGE_SQL, [], 'Disabling old cartridge...', ['PLS-00201'])
            self.try_execute_proc(ACTIVATE_NEW_CARTRIDGE_SQL, [], 'Activating new cartridge...')

            print 'Dropping cartridge specific objects...'
            self.r_cursor.execute(DROP_INDEXES_SQL, [INDEX_PREFIX_NAME])
            result = self.r_cursor.fetchmany()
            while result:
                for drop_statement in result:
                    try:
                        self.w_cursor.execute(drop_statement[0])
                    except Exception as e:
                        if 'ORA-01418: specified index does not exist' in str(
                                e.message) or 'ORA-00942: table or view does not exist' in str(e.message) or 'ORA-02289: sequence does not exist' in str(e.message):
                            print (colored('Warning: %s' % e.message, 'yellow'))
                            continue
                        print (colored('Error dropping object using statement %s (%s)' % (drop_statement[0], e.message), 'red'))
                        raise e
                result = self.r_cursor.fetchmany()

        print (colored('Done.\n', 'green'))

        self.try_execute_sql(DROP_TABLES_SQL, [], 'Dropping molecules table..', ['ORA-00942'])
        self.try_execute_sql(CREATE_TABLES_SQL, [], 'Creating molecules table...')

        self.try_execute_sql(CREATE_INDEXES_SQL, [], 'Creating indexes... (This may take a while)')
        self.r_cursor.execute(COUNT_STRUCTURES_SQL)
        count = int(self.r_cursor.fetchall()[0][0])
        pbar = ProgressBar(widgets=['INDEXING OBJECTS: [', Counter(), '/%s' % count, '] ', Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA()],
                    maxval=count).start()
        self.r_cursor.execute(SELECT_MOLREGNO_SQL)
        result = self.r_cursor.fetchmany()
        counter = 0
        failed = 0
        with self.w_connection.constraint_checks_disabled():
                while result:
                    with transaction.atomic(using=target):
                        for molregno in result:
                            try:
                                self.w_cursor.execute(ADD_COMPOUND_TO_INDEX_SQL, molregno)
                            except Exception as e:
                                failed += 1
                                print (colored('Error generating binary object for molecule %s (%s)' % (molregno, e.message), 'red'))
                            counter += 1
                            pbar.update(counter)
                        result = self.r_cursor.fetchmany(1000)

        pbar.update(count)
        pbar.finish()

        self.r_cursor.execute(COUNT_MOLECULES_SQL)
        total = int(self.r_cursor.fetchall()[0][0])

        print 'Created %s records in compound_mols.' % total
        print 'There was %s records in compounds structures' % count
        print 'Out of which %s records caused errors' % failed
        print "count - failed = %s, total = %s" % (count-failed, total)

        print 'Dropping cartridge specific objects...'
        self.r_cursor.execute(DROP_INDEXES_SQL, [INDEX_PREFIX_NAME])
        result = self.r_cursor.fetchmany()
        while result:
            for drop_statement in result:
                try:
                    self.w_cursor.execute(drop_statement[0])
                except Exception as e:
                    if 'ORA-01418: specified index does not exist' in str(
                            e.message) or 'ORA-00942: table or view does not exist' in str(e.message) or 'ORA-02289: sequence does not exist' in str(e.message):
                        print (colored('Warning: %s' % e.message, 'yellow'))
                        continue
                    print (colored('Error dropping object using statement %s (%s)' % (drop_statement[0], e.message), 'red'))
                    raise e
            result = self.r_cursor.fetchmany()
        transaction.commit(using=target)
        print (colored('Done.\n', 'green'))

        self.try_execute_sql(CREATE_INDEXES_SQL, [], 'Creating indexes... (This may take a while)')

        self.try_execute_proc(COLLECT_STATS, ['CHEMBL_APP', 'COMPOUND_MOLS'], 'Collecting stats..', [])

        self.r_connection.close()
        self.w_connection.close()

# ----------------------------------------------------------------------------------------------------------------------

    def try_execute_sql(self, sql, params, desc, ignores=None):
        print LINE + '\n'
        print desc
        if not ignores:
            ignores = []
        try:
            self.r_cursor.execute(sql, params)
        except Exception as e:
            if any(ign in str(e.message) for ign in ignores):
                print (colored('Warning: %s' % e.message, 'yellow'))
                return
            print (colored('Failed: %s' % e.message, 'red'))
            sys.exit()
        print (colored('Done.\n', 'green'))

# ----------------------------------------------------------------------------------------------------------------------

    def try_execute_proc(self, proc, params, desc, ignores=None):
        print LINE + '\n'
        print desc
        if not ignores:
            ignores = []
        try:
            self.r_cursor.callproc(proc, params)
        except Exception as e:
            if any(ign in str(e.message) for ign in ignores):
                print (colored('Warning: %s' % e.message, 'yellow'))
                return
            print (colored('Failed: %s' % e.message, 'red'))
            sys.exit()
        print (colored('Done.\n', 'green'))

# ----------------------------------------------------------------------------------------------------------------------
