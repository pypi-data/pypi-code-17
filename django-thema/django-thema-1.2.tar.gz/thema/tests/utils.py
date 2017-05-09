# -*- coding: utf-8 -*-
import os
from os import path
from shutil import rmtree
from os.path import join

TEMPORARY_TEST_DATA_DIR = join(
    path.dirname(path.realpath(__file__)),
    'test_data'
)


class ThemaTemporaryFilesMixin(object):

    random_codes = {
        'AMVD': {
            'en': 'City & town planning: architectural aspects',
            'da': 'Byplanlægning: arkitektoniske aspekter',
            'es': 'Urbanismo y urbanización: aspectos arquitectónicos',
            'parent': 'AMV',
        },
        'MBNH4': {
            'en': 'Birth control, contraception, family planning',
            'da': 'Prævention, fødselskontrol og familieplanlægning',
            'es': 'Control de la natalidad, anticoncepción y '
                  'planificación familiar',
            'parent': 'MBNH',
        },
        'PBB': {
            'en': 'Philosophy of mathematics',
            'da': 'Matematikkens filosofi',
            'es': 'Filosofía de las matemáticas',
            'parent': 'PB',
        },
        'RGBR': {
            'en': 'Coral reefs',
            'da': 'Koralrev',
            'es': 'Arrecifes de coral',
            'parent': 'RGB',
        },
        'VXQM': {
            'en': 'Monsters & legendary beings',
            'da': 'Monstre og mytiske væsner',
            'es': 'Monstruos y seres legendarios',
            'parent': 'VXQ',
        },
    }

    def setUp(self):
        """Create a temporary location for testing files."""
        if not path.exists(TEMPORARY_TEST_DATA_DIR):
            os.makedirs(TEMPORARY_TEST_DATA_DIR)

    def tearDown(self):
        """Remove the temporary test location and all its content."""
        rmtree(TEMPORARY_TEST_DATA_DIR)
