#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
#  Copyright (C) 2017 Broadcom Ltd.  All rights reserved.                     #
#                                                                             #
###############################################################################
'''
This module includes helper functions.
'''

# Imports #####################################################################
from __future__ import print_function
import os
import sys


# Metadata ####################################################################
__author__ = 'Timothy McFadden'
__creationDate__ = '07-APR-2017'


# Globals #####################################################################
(IS_WIN, IS_LIN) = ('win' in sys.platform, 'lin' in sys.platform)


def clear_screen():
    '''Clears the terminal window'''
    if IS_WIN:
        os.system('cls')
    elif IS_LIN:
        os.system('clear')
    else:
        raise NotImplementedError("Your platform has not been implemented: %s" % sys.platform)


def get_user_input(prompt=None, test_value=None):
    '''
    Prompt the user for input.

    :param str prompt: The text to show the user
    :param var test_value: If this is not none, the user will not be prompted
        and this value is returned.
    '''
    if prompt:
        print(prompt, end='')

    if test_value is not None:
        return test_value

    if sys.version_info.major == 2:
        return raw_input()
    else:
        return input()
