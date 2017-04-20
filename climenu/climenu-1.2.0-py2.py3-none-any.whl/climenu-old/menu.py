#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
The base ``menu`` items.
'''

# Metadata ####################################################################
__author__ = 'Timothy McFadden'
__creationDate__ = '06-APR-2017'
__license__ = 'Proprietary'

# Globals #####################################################################
MENU_ITEMS = []


def get_items():
    '''Return a list of menu items.'''
    return MENU_ITEMS[:]


class Menu(object):
    '''A sinlge menu item with a callback'''
    def __init__(self, title, callback):
        self.callback = callback
        self.title = title


class MenuGroup(object):
    '''A group of Menu items'''
    def __init__(self, title, menus=None):
        self.title = title
        self.menus = menus or []

    def menu(self, *args, **kwargs):  # pylint: disable=W0613
        '''Decorator to add a menu item to our list'''
        def decorator(decorated_function):
            '''create a menu item decorator'''
            menu_ = Menu(
                kwargs.get('title') or decorated_function.__doc__,
                callback=decorated_function)
            self.menus.append(menu_)
            return menu_
        return decorator

    def group(self, *args, **kwargs):  # pylint: disable=W0613
        '''Decorator to add a menu group to our list'''
        def decorator(decorated_function):
            '''create a menu group decorator'''
            menu_ = MenuGroup(kwargs.get('title') or decorated_function.__doc__)
            self.menus.append(menu_)
            return menu_
        return decorator


def group(title=None):
    '''A decorator to create a new MenuGroup'''
    def decorator(decorated_function):
        '''create a menu group decorator'''
        group_ = MenuGroup(title or decorated_function.__doc__)
        MENU_ITEMS.append(group_)
        return group_
    return decorator


def menu(title=None):
    '''A decorator to create a single menu item'''
    def decorator(decorated_function):
        '''create a menu item decorator'''
        menu_ = Menu(title or decorated_function.__doc__, callback=decorated_function)
        MENU_ITEMS.append(menu_)
        return menu_
    return decorator
