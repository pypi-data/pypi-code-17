#! /usr/bin/env python
# coding: UTF-8

import logging

from eva.conf import settings
from eva.utils.findapps import get_app_submodule

def load_models():
    logging.debug('LOAD APP MODELS')
    for app_name in settings.INSTALLED_APPS:
        models = get_app_submodule(app_name, 'models')
        if models:
            logging.debug('{0}: load models.py SUCCESS'.format(app_name))
        else:
            logging.debug('{0}: no models.py, PASS'.format(app_name))


def create_table():
    logging.error('uncompleted!')


def drop_table():
    logging.error('uncompleted!')
