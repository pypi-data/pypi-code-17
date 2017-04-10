#!/usr/bin/env python3

""" database integrity testing """

import os
from gtcms.core import cfg, ROOTPATH
from nose.tools import eq_


class TestDB(object):

    """ Test class """

    def test_compare_structure(self):

        """Compare live database to reference one."""

        import difflib
        import subprocess

        pgEnv = os.environ.copy()
        dbcfg = cfg.get('db')
        pgEnv['PGUSER'] = dbcfg.get('user')
        pgEnv['PGPASSWORD'] = dbcfg.get('password')
        pgEnv['PGHOST'] = dbcfg.get('host')
        pgEnv['PGPORT'] = str(dbcfg.get('port', '5432'))
        pgEnv['PGDATABASE'] = dbcfg.get('database')[:-5]
        olddb = [a.decode() for a in
                 subprocess.Popen(['pg_dump', '-Os'],
                                  stdout=subprocess.PIPE,
                                  env=pgEnv, bufsize=-1).stdout]
        pgEnv['PGDATABASE'] = dbcfg.get('database')
        newdb = [a.decode() for a in
                 subprocess.Popen(['pg_dump', '-Os'],
                                  stdout=subprocess.PIPE,
                                  env=pgEnv, bufsize=-1).stdout]
        diff = list(difflib.unified_diff(olddb, newdb,
                                         fromfile='production.sql',
                                         tofile='reference.sql', n=3))
        with (ROOTPATH / 'caches/testdb-current.sql').open('w') as dst:
            dst.write(''.join(olddb))
        with (ROOTPATH / 'caches/testdb-reference.sql').open('w') as dst:
            dst.write(''.join(newdb))
        eq_(olddb, newdb,
            'Databases structure differ (%d lines diff)\n' % len(diff) +
            ''.join(diff))
