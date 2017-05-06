# coding: utf-8

import logging

import mako
from mako.lookup import TemplateLookup

import eva.utils
from eva.conf import settings
from eva.utils.findapps import get_site_template_dirs


def get_template_lookup():

    template_dirs = get_site_template_dirs()
#    logging.debug('Find Template Dirs: \n{0}'.format(
#        eva.utils.yprint(template_dirs)))

    # 初始化 mako
    mako.runtime.UNDEFINED = '' # 未定义的变量不会出错

    lookup = TemplateLookup(template_dirs, input_encoding="utf-8")

    return lookup

