#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This module is used to create *simple* menu-based CLI programs in Python.

This package is **highly** inspired by Click (http://click.pocoo.org).
'''

# Imports #####################################################################
from __future__ import print_function
from .menu import menu, get_items, group, MenuGroup
from .helpers import clear_screen, get_user_input
from .settings import settings
from .version import __version__

# Metadata ####################################################################
__author__ = 'Timothy McFadden'
__creationDate__ = '06-APR-2017'


# Globals #####################################################################
__all__ = ['menu', 'group', 'settings']


def _show_main_menu(menu_items):
    '''Show the main menu and return the selected item.'''

    while True:
        print(settings.text['main_menu_title'])

        for index, menu_group in enumerate(menu_items):
            print("%2i : %s" % (index + 1, menu_group.title))

        print()
        value = get_user_input(settings.text['main_menu_prompt'])

        if value in settings.back_values:
            return None

        if not(value.isdigit()) or (int(value) > len(menu_items)):
            print(settings.text['invalid_selection'])
            continue

        return menu_items[int(value) - 1]


def _show_group_menu(menu_group):
    '''Show a submenue and return the selected item.'''
    while True:
        print(menu_group.title)

        submenu_items = menu_group.menus
        for index, submenu in enumerate(submenu_items):
            print("%2i : %s" % (index + 1, submenu.title))

        print()
        value = get_user_input(settings.text['submenu_prompt'])

        if value in settings.back_values:
            return None

        if not(value.isdigit()) or (int(value) > len(submenu_items)):
            print(settings.text['invalid_selection'])
            continue

        return submenu_items[int(value) - 1]


def run():
    '''
    Runs the menuing system.
    '''
    menu_stack = []
    menu_items = get_items()
    current_group = None

    if not menu_items:
        raise ValueError("No menu items defined")

    while True:
        # Clear the screen in-between each menu
        if settings.clear_screen:
            clear_screen()

        if not current_group:
            menu_item = _show_main_menu(menu_items)
            if not menu_item:
                break
        else:
            menu_item = _show_group_menu(current_group)

        if (not menu_item) and menu_stack:
            back_one = menu_stack.pop()
            if back_one != current_group:
                current_group = back_one
            elif menu_stack:
                # Pop another one off
                current_group = menu_stack.pop()
            else:
                # Show the main menu (nothing left in the stack)
                current_group = None
            continue

        # Check for a sub-menu.  Sub-menu's don't
        # have a callback, so just set the current
        # group and loop.
        if isinstance(menu_item, MenuGroup):
            menu_stack.append(menu_item)
            current_group = menu_item
            continue

        # If we should show the *main* menu, then
        # ``menu_item`` will be None here.
        if menu_item:
            menu_item.callback()
            get_user_input(settings.text['continue'])
        else:
            # Nothing left in the stack; make
            # ``current_group == None`` so we'll
            # show the main menu the next time through
            # the loop.
            current_group = None
