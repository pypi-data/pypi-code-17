#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This module holds the application settings class.
'''

# Metadata ####################################################################
__author__ = 'Timothy McFadden'
__creationDate__ = '07-APR-2017'


# Globals #####################################################################
class Settings(object):
    '''
    This class is used to store the settings for ``climenu``.
    '''
    clear_screen = True
    text = {
        'main_menu_title': 'Main Menu',
        'main_menu_prompt': 'Enter the selection (0 to exit): ',

        # NOTE: submenu title is read from the function
        'submenu_prompt': 'Enter the selection (0 to return): ',

        'invalid_selection': 'Invalid selection.  Please try again. ',

        'continue': 'Press Enter to continue: ',
    }

    # Add ``''`` to this list to go back one level if the user doesn't
    # enter anything
    back_values = ['0']


settings = Settings()  # pylint: disable=C0103
