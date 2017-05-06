import os
import sys
import logging
import argparse
import unittest

from eva.conf import settings
from eva.utils.findapps import get_app_abspath
from eva.utils.importlib import import_module
from eva.management.common import EvaManagementCommand


def _find_tests(dir):
    _orig_path = os.getcwd()
    os.chdir(dir)

    tests = []
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.startswith('test_') and f.endswith('.py'):
                m = os.path.join(root, f).replace('/', '.').lstrip('.')[:-3]
                tests.append(m)

    os.chdir(_orig_path)
    return tests


def _load_tests(subdir):
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    # 加载 models 测试
    for app in settings.INSTALLED_APPS:

        p = get_app_abspath(app)
        logging.debug('APP(%s:%s)', app, p)

        mp = os.path.join(p, subdir)

        if not os.path.isdir(mp):
            logging.debug('%s: no %s, PASS', app, subdir)
            continue

        for t in _find_tests(mp):
            m = import_module('.'.join([app, subdir.replace('/', '.'), t]))
            s = loader.loadTestsFromModule(m)
            suite.addTests(s)

    return suite


def load_model_tests():
    logging.debug('load model tests')
    return _load_tests('tests/model')


def load_api_tests():
    logging.debug('load api tests')
    return _load_tests('tests/api')


class Command(EvaManagementCommand):

    def __init__(self):
        self.cmd = 'runtest'
        self.help = '运行测试用例'

    def run(self, argv=[]):

        if not self.args.ignore_env_check:
            if not self.is_development:
                print('runtest should use a test settings.py!')
                sys.exit(1)

        from eva.orm import create_all, drop_all

        try:
            create_all(echo=self.args.db_echo)
            runner = unittest.TextTestRunner(verbosity=2)

            # run model TestSuite
            suite = load_model_tests()
            runner.run(suite)

            # run api TestSuite
            suite = load_api_tests()
            runner.run(suite)

        finally:
            drop_all(echo=self.args.db_echo)
