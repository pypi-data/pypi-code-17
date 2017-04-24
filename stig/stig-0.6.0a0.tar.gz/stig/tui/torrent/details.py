# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details
# http://www.gnu.org/licenses/gpl-3.0.txt

from ...logging import make_logger
log = make_logger(__name__)

import urwid


def _make_row(label, value, label_width):
    return urwid.Text('%s : %s' % (label.rjust(label_width), value))


class BasicInfo(urwid.WidgetWrap):
    title = 'Torrent'
    width = 50
    _items = ('ID', 'Hash', 'Pieces', 'DHT', 'Comment', 'Creator')*3

    def __init__(self):
        rows = []
        label_width = max(len(label) for label in self._items)
        for label in self._items:
            row = _make_row(label, 'foo info', label_width)
            rows.append(row)

        lb = urwid.Pile(rows)
        pd = urwid.Padding(lb, width=self.width)
        super().__init__(lb)

    def render(self, size, focus=False):
        log.debug('Render %r: size=%r', self, size)
        return super().render(size, focus)

    def selectable(self):
        return True


class TorrentDetailsWidget(urwid.WidgetWrap):
    def __init__(self, torrent):
        self._torrent = torrent
        self.update(torrent)

    _items = {'Torrent': BasicInfo,
              'foo': BasicInfo,
              'bar': BasicInfo,
    }

    def __init__(self, tid, title=None):
        self.title = str(title)

        widgets = []
        self._widgets = {}
        for label in self._items:
            widget = self._items[label]()
            widgets.append(widget)
            self._widgets[label] = widget

        grid = urwid.GridFlow([], 1, 1, 1, 'left')
        for widget in widgets:
            opts = grid.options('given', widget.width)
            widget_wrapped = urwid.LineBox(widget, title=widget.title)
            grid.contents.append((widget_wrapped, opts))

        from ..scrollable import Scrollable
        super().__init__(urwid.AttrMap(
            Scrollable(grid),
            'torrentdetails'
        ))

    def render(self, size, focus=False):
        # log.debug('Render %r: size=%r', self, size)
        return super().render(size, focus)

    # def update(self, torrent):
    #     for widget in self._cells.widgets:
    #         widget.update(torrent)
    #     self._torrent = torrent


