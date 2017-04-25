#Academic Torrents: Set downloading priorities to files within a torrent

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

""" NpyScreen console interface for setting downloading priorities """

import npyscreen

glb_handles = None
glb_so = None


class PriorityForm(npyscreen.FormMultiPageAction):
    """ Class adds support for multi-page forms. By default, scrolling down off
    the last widget on a page moves to the next page, and moving up from the
    first widget moves back a page."""

    def afterEditing(self):
        """ Called when the form is exited.

        Based in the priorityDict obtained in the create() method which contains
        just the position index of the selected items, a new_priorityList is
        created by matching the index positions and placing 1 to download when
        there is match and 0 to not download when there is no match. Finally,
        this new_priorityList gets inserted again in the prioryDict dictionary.
        """

        self.parentApp.setNextForm(None)
        tempDict = self.priorityDict
        for h, priorityList in tempDict.items():
            new_priorityList = []
            for i in range(h.get_torrent_info().num_files()):
                if i in priorityList.value:
                    new_priorityList.append(1)
                else:
                    new_priorityList.append(0)
            self.priorityDict[h] = new_priorityList
        global glb_so
        glb_so = self.priorityDict
        #self.editing = False

    def on_ok(self):
        """ Called when the ok button is pressed."""
        pass

    def on_cancel(self): # pragma: no cover
        """ Called when the cancel button is pressed."""
        exit()

    def create(self):
        """ This method is called by the Form\'s constructor.

        It creates the priorityDict dictionary from the torrent info and from
        the user input through the add_widget_intelligent() method.
        npyscreen.TitleMultiselect offers the user a list of options, allow
        him or her to select more than one of them. The value attribute is
        a list of the indexes user's choices. The list of choices is stored
        in the attribue values.
        """

        self.priorityDict = {}
        for h in glb_handles:
            paths = []
            for f in h.get_torrent_info().files():
                paths.append(f.path)
            self.priorityDict[h] = self.add_widget_intelligent( \
                npyscreen.TitleMultiSelect, max_height=5, value=[1,],
                name=h.name(), values=paths, scroll_exit=True)


class PriorityApp(npyscreen.NPSAppManaged):
    """ NPSAppManaged manages the application."""

    def onStart(self):
        """ Performs initialization of PriorityForm. """

        self.addForm('MAIN', PriorityForm, name='Files to download')

    def set_handler(self, handles):
        """ Sets the list of torrent handles to a global list variable.

        Args:
            handles: a list of libtorrent torrent handler objects.
        """

        global glb_handles
        glb_handles = handles


def get_so():
    """ Returns the global dictionary variable. """

    return glb_so
