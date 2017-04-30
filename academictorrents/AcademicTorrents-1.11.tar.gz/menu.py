#Academic Torrents Menu

#Copyright (C) [2017] Ronald D. Barrios

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

""" Horizontal Menu for AcademicTorrents
New menus appear on the right and push old menus off the left side of the screen.
The look of buttons and other menu elements are heavily customized and new
widget classes are used instead of factory functions.
"""

import urwid
import six


class MenuButton(urwid.Button):
    """ MenuButton is a customized Button widget.

    Button uses WidgetWrap to create its appearance and this class replaces
    the display widget created by Button by the wrapped widget in self._w.

    Attributes:
        _w: wraped widget
    """

    def __init__(self, caption, callback):
        super(MenuButton, self).__init__("")
        urwid.connect_signal(self, 'click', callback)
        self._w = urwid.AttrMap(urwid.SelectableIcon(
            [u'  \N{BULLET} ', caption], 2), None, 'selected')


class SubMenu(urwid.WidgetWrap):
    """ SubMenu is implemented with a MenuButton but uses WidgetWrap to hide the
    implementation instead of inheriting from MenuButton.

    The constructor builds a widget for the menu that this button will open and
    stores it in self.menu.
    """

    def __init__(self, caption, choices):
        super(SubMenu, self).__init__(MenuButton(
            [caption, u"\N{HORIZONTAL ELLIPSIS}"], self.open_menu))
        line = urwid.Divider(u'\N{LOWER ONE QUARTER BLOCK}')
        listbox = urwid.ListBox(urwid.SimpleFocusListWalker([
            urwid.AttrMap(urwid.Text([u"\n  ", caption]), 'heading'),
            urwid.AttrMap(line, 'line'),
            urwid.Divider()] + choices + [urwid.Divider()]))
        self.menu = urwid.AttrMap(listbox, 'options')

    def open_menu(self, button):
        """ Open menu options by retrieving the unique instance of
        HorizontalBoxes class"""

        top = singleton(HorizontalBoxes)
        top.open_box(self.menu)


class Choice(urwid.WidgetWrap):
    """ Choice is like SubMenu but displays the item chosen instead of another menu."""

    def __init__(self, caption):
        super(Choice, self).__init__(
            MenuButton(caption, self.item_chosen))
        self.caption = caption

    def item_chosen(self, button):
        """ Saves the selected option and prepares a response upon completion."""

        savechosen(self.caption)
        response = urwid.Text([u'  You chose ', self.caption, u'\n'])
        done = MenuButton(u'Ok', exit_program)
        response_box = urwid.Filler(urwid.Pile([response, done]))
        top = singleton(HorizontalBoxes)
        top.open_box(urwid.AttrMap(response_box, 'options'))


def exit_program(key):
    """ Exits urwid Main Loop"""

    raise urwid.ExitMainLoop()


focus_map = {
    'heading': 'focus heading',
    'options': 'focus options',
    'line': 'focus line'}


class HorizontalBoxes(urwid.Columns):
    """ HorizontalBoxes arranges the menus displayed. There is no special
    handling required for going to previous menus here because Columns already
    handles switching focus when LEFT or RIGHT is pressed. AttrMap with the
    focus_map dict is used to change the appearance of a number of the display
    attributes when a menu is in focus.
    """

    _instance = None

    def __init__(self):
        super(HorizontalBoxes, self).__init__([], dividechars=1)

    def open_box(self, box):
        """ Updates contents"""

        if self.contents:
            del self.contents[self.focus_position + 1:]
        self.contents.append((urwid.AttrMap(box, 'options', focus_map),
                              self.options('given', 24)))
        self.focus_position = len(self.contents) - 1


def singleton(klass):
    """ a method for retrieving a previously created instance. If there is no
    instance, then a new one is created.
    """

    if not klass._instance:
        klass._instance = klass()
    return klass._instance

glb_chosen = six.text_type('')


def savechosen(chosen):
    """ Modifies the _chosen global variable."""

    global glb_chosen
    glb_chosen = chosen


def getchosen():
    """ Returns the modified _chosen global variable."""

    return glb_chosen
