# Copyright (C) 2017 Michał Góral.
#
# This file is part of Feed Commas
#
# Feed Commas is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Feed Commas is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Feed Commas. If not, see <http://www.gnu.org/licenses/>.

'''Custom widgets used by Feed Commas'''

import os
import functools
import collections
import webbrowser
import threading
import urwid

import feedcommas.model as model
import feedcommas.config as config
from feedcommas.content import ReadType
from feedcommas.actions import handle_key
from feedcommas.locale import _
from feedcommas.log import log, status, Level


class Progress:
    '''I couldn't resist implementing this. Displays a rotating "circle"
    indicating that some action currently takes place.'''
    def __init__(self, urwid_loop):
        self._loop = urwid_loop
        self._chars = r'\|/-\|/-'
        self._char_index = 0
        self._max = 100
        self._progress = 0
        self._text = ''
        self._alarm_handle = None
        self._on_finish = None

    def setup(self, max_val, start=0, text='', on_finish=None):
        '''Setup a new progress.'''
        assert max_val > 0
        assert start >= 0
        self._char_index = 0
        self._max = max_val
        self._progress = start
        self._text = text
        self._on_finish = on_finish
        self._print()

    def update(self, add=1):
        '''Update a value of currently running progress.'''
        assert add > 0
        self._progress += add
        self._print(change_ch=False)
        if self._progress >= self._max:
            self._loop.remove_alarm(self._alarm_handle)
            status.clear('notif')
            if self._on_finish:
                self._on_finish()

    def cancel(self):
        '''Cancels progress.'''
        self._loop.remove_alarm(self._alarm_handle)
        if self._on_finish:
            self._on_finish()
        status.clear('notif')

    def _print(self, change_ch=True):
        text = []
        text.append(self._chars[self._char_index % len(self._chars)])
        if self._text:
            text.append(self._text)
        text.append('[%d%%]' % (self._progress / self._max * 100))
        status.set_text('notif', ' '.join(text))

        if change_ch is True:
            self._char_index += 1
            self._alarm_handle = self._loop.event_loop.alarm(0.3, self._print)


class MenuItem(urwid.Text):
    '''Selectable and clickable menu item'''
    _selectable = True

    def __init__(self, data, selected=False):
        if selected is True:
            style = 'menu selected'
        else:
            style = 'menu item'

        markup = []

        if data.id and data.id != 'all' and data.parent.id != 'all':
            markup.append('  ' * (data.depth - 1))

        markup.append((style, data.name))

        if data.unread:
            markup.append(('metadata', '(%d)' % data.unread))

        super().__init__(markup)
        self.id = data.id

    def keypress(self, size, key):
        '''Implement keypress to handle input when this widget is focused.'''
        return key


class Menu(urwid.ListBox):
    '''Scrollable menu'''
    focus_map = {
        'menu item': 'focus menu item',
        'menu selected': 'reverse',
    }

    signals = ['active_changed']

    def __init__(self, display):
        self._root = None
        self._active_id = 'all'
        super().__init__(urwid.SimpleFocusListWalker([]))

        self._actions = {'activate': self._selection_changed}

    def keypress(self, size, key):
        '''Implement keypress to handle input when this widget is focused.'''
        default = functools.partial(super().keypress, size, key)
        return handle_key(key, self._actions, self._command_map, default)

    def set_feeds(self, root):
        '''Replaces displayed feeds with a new tree, starting with a given root
        node.'''
        _, pos = self.get_focus()

        self.body.clear()  # pylint: disable=no-member
        self._root = root
        for node in root.dfs():
            selected = (node.id == self._active_id)
            w = urwid.AttrMap(MenuItem(node, selected), None, self.focus_map)
            self.body.append(w)  # pylint: disable=no-member

        # This keeps focus (not selection) on the same position, not the same
        # node. It's less astonishing than a 'focus jump' to the other part of
        # feed list.
        if pos and pos < len(self.body):
            self.set_focus(pos)

    def find(self, id_):
        '''Returns a Feed with a given id.'''
        for feed in self._root.bfs():
            if feed.id == id_:
                return feed
        return None

    def handle_read(self, feed_id, read):
        '''`mark_read` signal handler. Updates a number of unread articles.'''
        node = self.find(feed_id)
        if node is None:
            return

        if node.unread is not None:
            if read is True and node.unread > 0:
                node.unread -= 1
            elif read is False:
                node.unread += 1
        self.refresh()

    @property
    def focused(self):
        '''Returns currently focused feed or category.'''
        widget, _ = self.get_focus()
        if not widget:
            return
        return self.find(widget.original_widget.id)

    @property
    def active(self):
        '''Returns currently active (highlighted) feed or category.'''
        return self.find(self._active_id)

    def read_all(self):
        '''Set unread count for currently selected feed and all its descendants
        to 0.'''
        active = self.active
        for feed in active.dfs():
            feed.unread = 0
        self.refresh()

    def refresh(self):
        '''Refreshes a list of feeds.'''
        self.set_feeds(self._root)

    def _selection_changed(self):
        data = self.focused

        if data.id and self._active_id != data.id:
            self._active_id = data.id
            self.refresh()
            urwid.emit_signal(self, 'active_changed', data)


class Article(urwid.Pile):
    '''Text area with customized markup for displaying articles.'''
    _selectable = False

    def __init__(self, article):
        self.data = article
        super().__init__(self._markup())
        self.focus_item = self[-2]  # focus body

    def keypress(self, size, keys):
        '''Implement keypress to handle input when this widget is focused.'''
        return keys

    def update(self):
        '''Re-draws article contents (header, body and a footer).'''
        self.contents.clear()
        for widget in self._markup():
            self.contents.append((widget, ('weight', 1)))
        self.focus_item = self[-2]  # focus body

    @staticmethod
    def _make_header(article):
        title = urwid.Text([('title', article.title)])
        date = urwid.Text([('metadata', article.date)], align='right')
        return [('weight', 10, title), ('weight', 3, date)]

    @staticmethod
    def _make_footer(article):
        metadata = ''
        if article.starred:
            metadata += '\u2605'  # unicode BLACK STAR

        if article.markable:
            # unicode BALLOT BOX and BALLOT BOX WITH CHECK
            metadata += '\u2611' if article.read else '\u2610'

        status_widget = urwid.Text([('metadata', metadata)])

        source_markup = []
        if article.author:
            source_markup.append(('metadata', '%s, ' % article.author))
        source_markup.append(('metadata', article.feed_name))

        source_widget = urwid.Text(source_markup, align='right')

        return [('weight', 1, status_widget), ('weight', 10, source_widget)]

    def _markup(self):
        header = urwid.Columns(self._make_header(self.data))
        body = urwid.Text([('article', self.data.content)])
        footer = urwid.Columns(self._make_footer(self.data))
        body._selectable = True  # pylint: disable=protected-access
        return [header, urwid.Divider(), body, footer]


class Indicator(urwid.Text):
    '''Indicator displayed on an article list telling that "something" is
    happening right now.'''
    def __init__(self, text):
        markup = [('metadata', text)]
        super().__init__(markup, align='center')


class ArticleList(urwid.ListBox):
    '''Scrollable list of articles'''
    _focus_map = {
        None: 'focus line',  # hacky, but works. :)
        'title': 'focus title',
        'article': 'focus article',
    }

    _GetType = collections.namedtuple('GetType', ('type_', 'id'))

    signals = ['marked', 'navigated']

    def __init__(self, display):
        self._loop = display.urwid_loop

        self.walker = urwid.SimpleFocusListWalker([])
        self.walker.set_focus_changed_callback(self._focus_changed)

        super().__init__(self.walker)

        self._actions = {
            'open-browser': self._open_browser,
            'read-toggle': self._toggle_read_current,
            'star-toggle': self._toggle_star_current,
        }

        display.cmd_handler.register_actions(self._actions, self)

        self._indicators_count = 0

    def keypress(self, size, key):
        '''Implement keypress to handle input when this widget is focused.'''
        name = self._command_map[key]
        if name and name.startswith('cursor '):
            urwid.emit_signal(self, 'navigated', self.focus_position)
            return super().keypress(size, key)

        default = functools.partial(super().keypress, size, key)
        return handle_key(key, self._actions, self._command_map, default)

    @property
    def current(self):
        '''Unwraps Article widget and returns it.'''
        try:
            return self._unwrap_article(self.focus)
        except AttributeError:
            return None

    @property
    def count(self):
        '''Returns number of displayed articles'''
        return len(self.walker) - self._indicators_count

    def clear(self):
        '''Clears all contents of ArticleList.'''
        self.walker.clear()
        self._indicators_count = 0

    def read_all(self):
        '''Marks all shown articles as read.'''
        for widget in self.walker:
            article = self._unwrap_article(widget)
            if article and article.data.markable and article.data.read is False:
                article.data.read = True
                article.update()

    def indicate(self, text):
        '''Adds an indicator with a given text to the current view.'''
        self.walker.append(Indicator(text))
        self._indicators_count += 1
        self._loop.draw_screen()

    def remove_indicators(self):
        '''Removes all currently displayed indicators.'''
        for i, elem in enumerate(self.walker):
            if isinstance(elem, Indicator):
                del self.walker[i]
        self._indicators_count = 0

    def add_articles(self, articles):
        '''Appends given articles to the current view.'''
        reset_pos = (self.count == 0)

        for article in articles:
            text = urwid.LineBox(Article(article))
            self.walker.append(urwid.AttrMap(text, None, self._focus_map))

        if reset_pos and self.count > 0:
            if self.focus_position == 0:
                # A small hack for misbehaving urwid. It sets initial position
                # to 0 so it doesn't detect when focus changes from 0 to 0. But
                # we want to detect this situation.
                self._focus_changed(0)
            self.focus_position = 0

    def _focus_changed(self, new_pos):
        # after position change, automatically mark a new article as read after
        # a few seconds, but only if it's still focused after that time.
        article = self._unwrap_article(self.walker[new_pos])
        if article and article.data.read is False:
            tm = config.get_value('settings.mark-read-time', -1)
            if tm >= 0:
                cb = functools.partial(self._auto_read, new_pos)
                self._loop.event_loop.alarm(tm, cb)

    def _unwrap_article(self, widget):
        try:
            while not isinstance(widget, Article):
                widget = widget.original_widget
        except AttributeError:
            return None
        return widget

    def _toggle_star_current(self):
        pos = self.focus_position
        try:
            data = self.current.data
        except (IndexError, AttributeError):
            return
        self._star(pos, not data.starred)

    def _toggle_read_current(self):
        pos = self.focus_position
        try:
            data = self.current.data
        except (IndexError, AttributeError):
            return
        self._read(pos, not data.read)

    def _auto_read(self, pos):
        if pos == self.focus_position:
            self._read(pos, True)

    def _read(self, pos, read):
        try:
            article = self._unwrap_article(self.walker[pos])
            data = article.data
        except (IndexError, AttributeError):
            return
        if data.markable and data.read != read:
            data.read = read
            urwid.emit_signal(self, 'marked', 'read', data, read)
            article.update()

    def _star(self, pos, star):
        try:
            article = self._unwrap_article(self.walker[pos])
            data = article.data
        except (IndexError, AttributeError):
            return
        if data.starred != star:
            data.starred = star
            urwid.emit_signal(self, 'marked', 'star', data, star)
            article.update()

    def _open_browser(self):
        if not self.current:
            return

        # Browsers like to print. we don't like prints because they appear in
        # the middle of gui. Suppress the prints!
        savout = os.dup(1)
        saverr = os.dup(2)
        os.close(1)
        os.close(2)

        os.open(os.devnull, os.O_RDWR)
        try:
            # new=2: try opening in a new tab
            webbrowser.open(self.current.data.url, new=2)
            self._read(self.focus_position, True)
        finally:
            os.dup2(savout, 1)
            os.dup2(saverr, 2)


class Commandline(urwid.Pile):
    '''Bottom command line activated by pressing a colon key.'''
    signals = ['command', 'command_cancel']
    _selectable = True

    class _Status:
        def __init__(self, value, on):
            self.value = value
            self.on = on

    def __init__(self, abbrev_getter, *args, **kwargs):
        self._e = urwid.Edit(multiline=True)
        self._statuses = {
            'offline': self._Status('o', config.get_value('settings.offline')),
            'unread': self._Status('u', not config.get_value('settings.show-read')),
            'notif': self._Status('', True),
        }
        self._status_line = urwid.Text('')

        attrm = urwid.AttrMap(urwid.Padding(self._status_line), 'status')
        super().__init__([attrm, self._e])

        self._abbrev = abbrev_getter
        self._abbrev_mode = False
        self._compl_index = None
        self._uncompl_cmd = ''

        self._update_status_line()

    def set_status_text(self, name, text):
        '''Changes displayed text for a status with a given name.'''
        self._statuses[name].value = text
        if self._statuses[name].on:
            self._update_status_line()

    def enable_status(self, name, enable=True):
        '''Enables or disables showing a status string with a given name.'''
        prev_on = self._statuses[name].on
        self._statuses[name].on = enable
        if prev_on != enable:
            self._update_status_line()

    def set_caption(self, markup):
        '''Forward `set_caption` to the underlying urwid.Edit'''
        self._e.set_caption(markup)

    def keypress(self, size, key):
        '''Implement keypress to handle input when this widget is focused.'''
        self._e.set_caption('')
        if key == 'enter':  # hardcoded by design
            urwid.emit_signal(self, 'command', self._e.edit_text[1:])
            self._e.set_edit_text('')
            self._edited()
        elif key == 'tab':
            self._complete()
        elif key == 'backspace' and self._e.edit_text == ':':
            self._e.set_edit_text('')
            urwid.emit_signal(self, 'command_cancel')
            self._edited()
        elif key == 'esc':
            self._e.set_edit_text('')
            urwid.emit_signal(self, 'command_cancel')
            self._edited()
        else:
            ret = super().keypress(size, key)
            self._edited()
            return ret

    def _update_status_line(self):
        if self._abbrev_mode:
            return

        schema = config.get_value('settings.status-line', '')

        on_statuses = {}
        for name, st in self._statuses.items():
            if st.on:
                on_statuses[name] = st.value
            else:
                on_statuses[name] = ''

        self._status_line.set_text(schema.format(**on_statuses))

    def _edited(self):
        self._hide_abbrev()
        self._compl_index = 0
        self._uncompl_cmd = self._e.edit_text[1:]

    def _complete(self):
        completions = self._abbrev(self._uncompl_cmd)
        completions.sort()
        if len(completions) == 0:
            return

        if self._compl_index >= len(completions):
            self._compl_index = 0

        self._e.set_edit_text(':%s' % completions[self._compl_index])
        self._e.set_edit_pos(len(self._e.edit_text))
        self._show_abbrev(completions)
        self._compl_index += 1

    def _show_abbrev(self, abbr_list):
        if len(abbr_list) < 2:
            return

        markup = []
        for i, abbr in enumerate(abbr_list):
            if i == self._compl_index:
                markup.append(('reverse', abbr))
            else:
                markup.append(('status', abbr))
            markup.append('  ')
        markup.pop()

        self._abbrev_mode = True
        self._status_line.set_text(markup)

    def _hide_abbrev(self):
        if self._abbrev_mode:
            self._abbrev_mode = False
            self._update_status_line()


class DisplayController(urwid.Columns):
    '''Main two-column display'''
    _Handler = collections.namedtuple('Handler', ('obj', 'fn'))

    def __init__(self, provider, urwid_loop, cmd_handler):
        self._provider = provider
        self.urwid_loop = urwid_loop
        self.cmd_handler = cmd_handler

        self._articles = ArticleList(self)
        self._menu = Menu(self)
        vline = urwid.AttrMap(urwid.SolidFill(u'\u2502'), 'menu line')
        super().__init__([('weight', 2, self._menu),
                          ('fixed', 1, vline),
                          ('weight', 7, self._articles)])

        self.focus_position = 2

        self._sync_lock = threading.Lock()

        self._actions = {
            'show-all': lambda: self._configure_read(True),
            'show-unread': lambda: self._configure_read(False),
            'read-all': self._read_all,
            'refresh': self._refresh,
            'offline-toggle': self._toggle_offline,
            'sync': self._sync
        }

        self.cmd_handler.register_actions(self._actions, self)

        urwid.connect_signal(self._menu, 'active_changed',
                             self._load_articles)
        urwid.connect_signal(self._articles, 'marked', self._marked)
        urwid.connect_signal(self._articles, 'navigated',
                             self._articles_navigated)

        self._art_has_more = False

    def keypress(self, size, key):
        '''Implement keypress to handle input when this widget is focused.'''
        default = functools.partial(super().keypress, size, key)
        return handle_key(key, self._actions, self._command_map, default)

    def load(self):
        '''Load a fresh copy of everything. Blocks until loading is complete'''
        self._articles.clear()
        self._articles.indicate(_('Loading articles...'))

        articles = self._get_articles(model.Feed('all', '', is_category=True))
        feeds = self._get_feeds()
        articles.wait()
        feeds.wait()
        self._add_articles(articles.get())
        self._set_feeds(feeds.get())

    def _articles_navigated(self, newpos):
        try:
            focus_percentage = int(100 * newpos / self._articles.count)
        except ZeroDivisionError:
            focus_percentage = 0

        if self._art_has_more and focus_percentage > 75:
            active = self._menu.active
            if active is None:
                return

            self._art_has_more = False  # don't add multiple "Loading..." labels
            self._articles.indicate(_('Loading next articles...'))
            self._get_articles(active, self._add_articles,
                               offset=self._articles.count)

    def _get_articles(self, feed, cb=None, **kwargs):
        type_ = 'category' if feed.is_category else 'feed'
        limit = 20
        return self._provider.get_articles(type_, feed.id, limit=limit,
                                           read_type=ReadType.current(),
                                           callback=cb, **kwargs)

    def _get_feeds(self, cb=None, **kwargs):
        return self._provider.get_feeds(cb, **kwargs)

    def _add_articles(self, meta):
        self._articles.remove_indicators()
        self._articles.add_articles(meta.articles)
        self._art_has_more = meta.has_more
        if self._articles.count == 0:
            self._articles.indicate(_('No articles'))

    def _set_feeds(self, root):
        self._menu.set_feeds(root)

    def _load_articles(self, feed):
        self._articles.clear()
        self._articles.indicate(_('Loading articles...'))
        self._get_articles(feed, self._add_articles)

    def _marked(self, mark_type, article, value):
        if mark_type == 'read':
            self._menu.handle_read(article.feed_id, value)
            self._provider.mark(article.id, value)
        elif mark_type == 'star':
            self._provider.star(article.id, article.feed_id, value)

    def _configure_read(self, show_read):
        config.set_value('settings.show-read', show_read)
        status.enable('unread', not show_read)
        active = self._menu.active
        if active:
            self._load_articles(active)

    def _toggle_offline(self):
        current = config.get_value('settings.offline')
        config.set_value('settings.offline', not current)
        status.enable('offline', not current)

    def _read_all(self):
        active = self._menu.active
        if not active:
            log.error(_('No feed selected'))
            return
        self._provider.mark_all_read(active)
        self._articles.read_all()
        self._menu.read_all()

    def _refresh(self):
        active = self._menu.active
        if not active:
            return

        self._provider.reset_network_error()
        self._articles.clear()
        self._articles.indicate(_('Refreshing...'))
        self._get_articles(active, self._add_articles)
        self._get_feeds(self._set_feeds)

    def _sync(self):
        '''Synchronize feeds to the limit set by
        `settings.sync-article-count`'''
        if not self._provider.online():
            log.error(_('Offline mode - cannot synchronize articles.'))
            return

        limit = config.get_value('settings.sync-article-count', 0)
        if limit <= 0:
            log.info(_('sync-article-count: %d. Aborting sync.' % limit))
            return

        if not self._sync_lock.acquire(blocking=False):
            log.error(_('Synchronization already in progress.'))
            return

        def _on_finish():
            self._sync_lock.release()

        # Divide requests to several steps, each with a limited number of
        # articles fetched at a time.
        #
        # This serves 2 purposes:
        #   1. Comma Feed seems to respond better for smaller requests
        #   2. It allows to give users a nice feedback (instead of 0 - 100%)
        offsets = []
        if limit > 130:
            steps = int(limit / 100)
            remainder = limit % 100
            for i in range(steps):
                offsets.append((i * 100, 100))
            if remainder != 0:
                offsets.append((len(offsets) * 100, remainder))
        else:
            offsets = [(0, limit)]

        progress = Progress(self.urwid_loop)
        progress.setup(len(offsets) + 1, text=_('Synchronization'),
                       on_finish=_on_finish)

        def _cb(*args):
            progress.update()

        self._provider.get_feeds(_cb)
        for offset, limit in offsets:
            self._provider.get_articles(type_='category', feed_id='all',
                                        read_type=ReadType.ALL, limit=limit,
                                        offset=offset, callback=_cb)


class MainWindow(urwid.Frame):
    '''Urwid top widget.'''
    def __init__(self, provider, urwid_loop, cmd_handler):
        self.commandline = Commandline(cmd_handler.get_abbrev_names)
        urwid.connect_signal(log, 'log', self.log)
        urwid.connect_signal(log, 'clear', self.log_clear)

        urwid.connect_signal(status, 'set_text', self.status_set_text)
        urwid.connect_signal(status, 'enable', self.status_enable)

        self.display = DisplayController(provider, urwid_loop, cmd_handler)
        super().__init__(self.display, footer=self.commandline)

        urwid.connect_signal(self.commandline, 'command',
                             self._command_finished)
        urwid.connect_signal(self.commandline, 'command',
                             cmd_handler.call)
        urwid.connect_signal(self.commandline, 'command_cancel',
                             self._command_finished)

    def keypress(self, size, key):
        if key == ':':  # hardcoded by design
            self.focus_position = 'footer'
        return super().keypress(size, key)

    def log(self, level, text):
        '''Common, reliable way of displaying log prints.'''
        if level == Level.error:
            style = 'error'
        else:
            style = 'log'
        self.commandline.set_caption([(style, text)])

    def log_clear(self):
        '''Clear current print.'''
        self.commandline.set_caption('')

    def status_set_text(self, name, text):
        '''Set text displayed for a given status'''
        self.commandline.set_status_text(name, text)

    def status_enable(self, name, enable):
        '''Enable or disable displaying of a given status.'''
        self.commandline.enable_status(name, enable)

    def _command_finished(self, *args, **kwargs):
        self.focus_position = 'body'
