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

from ..logging import make_logger
log = make_logger(__name__)

import urwid
from urwid.widget import (BOX, FLOW, FIXED)
from urwid.command_map import (CURSOR_DOWN, CURSOR_UP,
                               CURSOR_PAGE_UP, CURSOR_PAGE_DOWN,
                               CURSOR_MAX_LEFT, CURSOR_MAX_RIGHT)

SCROLL_LINE_UP        = 'line up'
SCROLL_LINE_DOWN      = 'line down'
SCROLL_PAGE_UP        = 'page up'
SCROLL_PAGE_DOWN      = 'page down'
SCROLL_HALF_PAGE_UP   = 'half page up'
SCROLL_HALF_PAGE_DOWN = 'half page down'
SCROLL_TO_TOP         = 'to top'
SCROLL_TO_END         = 'to end'


class Scrollable(urwid.WidgetDecoration):
    _selectable = True
    _sizing = frozenset([BOX])

    def __init__(self, widget):
        if not any(s in widget.sizing() for s in (FIXED, FLOW)):
            raise ValueError('Not a fixed or flow widget: %r' % widget)
        self._trim_top = 0
        self._scroll_action = None
        self._forward_keypress = None
        self._old_cursor_coords = None
        self.__super.__init__(widget)

    def render(self, size, focus=False):
        maxcol, maxrow = size

        # Render original widget
        ow = self._original_widget
        ow_size = self._get_original_widget_size(size)
        log.debug('Rendering %r with size=%r, focus=%r', ow, ow_size, focus)

        canv = urwid.CompositeCanvas(ow.render(ow_size, focus))
        canv_cols, canv_rows = canv.cols(), canv.rows()

        # Pad canvas vertically/horizontally if necessary
        if canv_cols <= maxcol:
            pad_width = maxcol - canv_cols
            if pad_width > 0:
                # Canvas is narrower than available horizontal space
                # log.debug('canvas=%r needs padding=%r -> %r',
                #           (canv_cols, canv_rows),
                #           (pad_width, canv_rows),
                #           size)
                canv.pad_trim_left_right(0, pad_width)

        if canv_rows <= maxrow:
            fill_height = maxrow - canv_rows
            if fill_height > 0:
                # Canvas is lower than available vertical space
                # log.debug('canvas=%r needs filler=%r -> %r',
                #           (canv_cols, canv_rows),
                #           (canv_cols, fill_height),
                #           size)
                canv.pad_trim_top_bottom(0, fill_height)

        log.debug('canvas size=%r', (canv.cols(), canv.rows()))

        if canv_cols <= maxcol and canv_rows <= maxrow:
            # Canvas is small enough to fit without scrolling
            log.debug('no scrolling needed!')
            return canv

        # Update self._trim_top
        self._adjust_trim_top(canv, size)

        # Trim canvas if necessary
        trim_top = self._trim_top
        trim_end = canv_rows - maxrow - trim_top
        trim_right = canv_cols - maxcol
        if trim_top > 0:
            # log.debug('Removing %r lines from top of canvas', trim_top)
            canv.trim(trim_top)
        if trim_end > 0:
            # log.debug('Removing %r lines from bottom of canvas', trim_end)
            canv.trim_end(trim_end)
        if trim_right > 0:
            # log.debug('Removing %r lines from right of canvas', trim_right)
            canv.pad_trim_left_right(0, -trim_right)

        # Disable cursor display if cursor is outside of visible canvas parts
        if canv.cursor is not None:
            curscol, cursrow = canv.cursor
            if cursrow >= maxrow or cursrow < 0:
                log.debug('cursor is out of bounds: %r >= %r',
                          (curscol, cursrow), (maxcol, maxrow))
                canv.cursor = None
            else:
                log.debug('cursor is in bounds: %r < %r',
                          (curscol, cursrow), (maxcol, maxrow))

        # Let keypress() know if original_widget should get keys
        self._forward_keypress = bool(canv.cursor)
        if self._forward_keypress is None:
            log.debug('Not forwarding keypresses to original widget')
        else:
            log.debug('Forwarding keypresses to original widget')

        return canv

    def keypress(self, size, key):
        log.debug('got key: %r', key)

        # Maybe offer key to original widget
        if self._forward_keypress:
            ow = self._original_widget
            ow_size = self._get_original_widget_size(size)

            # Remember previous cursor position if possible
            if hasattr(ow, 'get_cursor_coords'):
                self._old_cursor_coords = ow.get_cursor_coords(ow_size)

            key = ow.keypress(ow_size, key)
            if key is None:
                log.debug('%r ate key', ow)
                return None

        # Handle up/down, page up/down, etc
        command_map = self._command_map
        if command_map[key] == CURSOR_UP:
            self._scroll_action = SCROLL_LINE_UP
        elif command_map[key] == CURSOR_DOWN:
            self._scroll_action = SCROLL_LINE_DOWN

        elif command_map[key] == CURSOR_PAGE_UP:
            self._scroll_action = SCROLL_PAGE_UP
        elif command_map[key] == CURSOR_PAGE_DOWN:
            self._scroll_action = SCROLL_PAGE_DOWN

        elif command_map[key] == CURSOR_MAX_LEFT:  # 'home'
            self._scroll_action = SCROLL_TO_TOP
        elif command_map[key] == CURSOR_MAX_RIGHT: # 'end'
            self._scroll_action = SCROLL_TO_END

        elif key == 'meta  ':
            self._scroll_action = SCROLL_HALF_PAGE_UP
        elif key == ' ':
            self._scroll_action = SCROLL_HALF_PAGE_DOWN

        else:
            return key

        self._invalidate()

    def mouse_event(self, size, event, button, col, row, focus):
        ow = self._original_widget
        if hasattr(ow, 'mouse_event'):
            ow_size = self._get_original_widget_size(size)
            row += self._trim_top
            return ow.mouse_event(ow_size, event, button, col, row, focus)
        else:
            return False

    @property
    def position(self):
        """Current scrolling position

        TODO: Explain boundaries (0, ...?)
        """
        return self._trim_top

    @position.setter
    def position(self, position):
        self._trim_top = position

    def _adjust_trim_top(self, canv, size):
        """Adjust self._trim_top according to self._scroll_action"""
        maxcol, maxrow = size
        action = self._scroll_action
        self._scroll_action = None
        trim_top = self._trim_top
        canv_rows = canv.rows()

        if canv_rows <= maxrow:
            self._trim_top = 0  # Reset scroll position
            return

        def ensure_bounds(new_trim_top):
            return max(0, min(canv_rows - maxrow, new_trim_top))

        if action == SCROLL_LINE_UP:
            self._trim_top = ensure_bounds(trim_top - 1)
        elif action == SCROLL_LINE_DOWN:
            self._trim_top = ensure_bounds(trim_top + 1)

        elif action == SCROLL_PAGE_UP:
            self._trim_top = ensure_bounds(trim_top - maxrow+1)
        elif action == SCROLL_PAGE_DOWN:
            self._trim_top = ensure_bounds(trim_top + maxrow-1)

        elif action == SCROLL_HALF_PAGE_UP:
            self._trim_top = ensure_bounds(trim_top - round(maxrow/2))
        elif action == SCROLL_HALF_PAGE_DOWN:
            self._trim_top = ensure_bounds(trim_top + round(maxrow/2))

        elif action == SCROLL_TO_TOP:
            self._trim_top = 0
        elif action == SCROLL_TO_END:
            self._trim_top = canv_rows - maxrow

        else:
            self._trim_top = ensure_bounds(trim_top)

        # If the cursor was moved by the most recent keypress, adjust trim_top
        # so that the new cursor position is within the displayed canvas part.
        if self._old_cursor_coords is not None and self._old_cursor_coords != canv.cursor:
            curscol, cursrow = canv.cursor
            if cursrow < self._trim_top:
                self._trim_top = cursrow
            elif cursrow >= self._trim_top + maxrow:
                self._trim_top = max(0, cursrow - maxrow + 1)

    def _get_original_widget_size(self, size):
        ow = self._original_widget
        maxcol, maxrow = size
        if FIXED in ow.sizing():
            return ()
        elif FLOW in ow.sizing():
            return (maxcol,)


class ScrollBar(urwid.WidgetDecoration):
    _sizing = frozenset([BOX])
    _selectable = True

    def __init__(self, widget,
                 thumb_char='\u2588', trough_char='\u2591',
                 side='right', width=1):
        self.__super.__init__(widget)
        self._thumb_char = thumb_char
        self._trough_char = trough_char
        self.scrollbar_side = side
        self.scrollbar_width = width

    def render(self, size, focus=False):
        maxcol, maxrow = size
        pos = self.scrollpos
        posmax = self.scrollpos_max
        log.debug('Rendering scrollbar with pos=%r, posmax=%r, maxrow=%r',
                  pos, posmax, maxrow)

        thumb_weight = min(1, maxrow / max(1, posmax+maxrow))
        # log.debug('thumb_weight=%r', thumb_weight)
        thumb_height = max(1, round(thumb_weight * maxrow))
        # log.debug('thumb_height=%r', thumb_height)

        top_weight = pos / max(1, posmax)
        # log.debug('top_weight=%r',top_weight)
        top_height = round((maxrow-thumb_height) * top_weight)
        # log.debug('top_height=%r', top_height)
        bottom_height = maxrow - thumb_height - top_height
        # log.debug('bottom_height=%r', bottom_height)

        log.debug('top=%r, thumb=%r, bottom=%r', top_height, thumb_height, bottom_height)
        assert thumb_height + top_height + bottom_height == maxrow

        sb_width = self._scrollbar_width
        top = urwid.SolidCanvas(self._trough_char, sb_width, top_height)
        thumb = urwid.SolidCanvas(self._thumb_char, sb_width, thumb_height)
        bottom = urwid.SolidCanvas(self._trough_char, sb_width, bottom_height)
        sb_canv = urwid.CanvasCombine([
            (top, None, False),
            (thumb, None, True),
            (bottom, None, False),
        ])

        ow_size = (maxcol-sb_width, maxrow)
        log.debug('ow_size=%r', ow_size)
        ow_canv = self._original_widget.render(ow_size, focus)

        combinelist = [(ow_canv, None, True, ow_size[0]),
                       (sb_canv, None, False, sb_width)]
        if self._scrollbar_side != 'left':
            return urwid.CanvasJoin(combinelist)
        else:
            return urwid.CanvasJoin(reversed(combinelist))

    @property
    def scrollpos(self):
        ow = self._original_widget
        if isinstance(ow, urwid.ListBox):
            log.debug('Getting scroll pos from "ListBox"')
            log.debug(ow.body.get_focus())
            pos = ow.body.get_focus()[1]

        log.debug('  -> %r', pos)
        return 0 if pos is None else pos


    @scrollpos.setter
    def scrollpos(self, position):
        ow = self._original_widget
        if isinstance(ow, urwid.ListBox):
            log.debug('Setting scroll pos in ListBox = %r', position)

    @property
    def scrollpos_max(self):
        return len(self._original_widget.body)

    @property
    def scrollbar_width(self):
        return self._scrollbar_width

    @scrollbar_width.setter
    def scrollbar_width(self, width):
        self._scrollbar_width = max(1, int(width))
        self._invalidate()

    @property
    def scrollbar_side(self):
        return self._scrollbar_side

    @scrollbar_side.setter
    def scrollbar_side(self, side):
        if side not in ('left', 'right'):
            raise ValueError('scrollbar_side must be "left" or "right", not %r' % side)
        self._scrollbar_side = side
        self._invalidate()

    def keypress(self, size, key):
        return self._original_widget.keypress(size, key)

    # def needed(self, position, position_max):
    #     """Whether a scrollbar is warranted given `size`

    #     Use this during rendering to check if you want to display a scroll bar.
    #     """
    #     return True

    #     pos = position
    #     posmax = position_max
    #     log.debug('scrollbar needed? pos=%r, posmax=%r', pos, posmax)
    #     if pos >= posmax:
    #         log.debug('Scrollbar not needed')
    #         return False
    #     else:
    #         log.debug('Scrollbar needed')
    #         return True




# class ScrollBar(urwid.Widget):
#     _sizing = frozenset([BOX])
#     _selectable = True

#     def __init__(self, thumb_char='\u2588', trough_char='\u2591'):
#         self._thumb_char = thumb_char
#         self._trough_char = trough_char
#         self._position = 0
#         self._position_max = 0

#     @property
#     def position(self):
#         return self._position

#     @position.setter
#     def position(self, position):
#         p = round(position)
#         if self._position != p:
#             self._invalidate()
#         self._position = p

#     @property
#     def position_max(self):
#         return self._position_max

#     @position_max.setter
#     def position_max(self, position_max):
#         pm = round(position_max)
#         if self._position_max != pm:
#             self._invalidate()
#         self._position_max = pm

#     def needed(self, position, position_max):
#         """Whether a scrollbar is warranted given `size`

#         Use this during rendering to check if you want to display a scroll bar.
#         """
#         return True

#         pos = position
#         posmax = position_max
#         log.debug('scrollbar needed? pos=%r, posmax=%r', pos, posmax)
#         if pos >= posmax:
#             log.debug('Scrollbar not needed')
#             return False
#         else:
#             log.debug('Scrollbar needed')
#             return True

#     def render(self, size, focus=False):
#         maxcol, maxrow = size
#         pos = self._position
#         posmax = self._position_max
#         if pos > posmax:
#             pos = self._position = posmax

#         log.debug('Rendering scrollbar with pos=%r, posmax=%r, maxrow=%r',
#                   self._position, self._position_max, maxrow)

#         thumb_weight = min(1, maxrow / max(1, posmax+maxrow))
#         # log.debug('thumb_weight=%r', thumb_weight)
#         thumb_height = max(1, round(thumb_weight * maxrow))
#         # log.debug('thumb_height=%r', thumb_height)

#         top_weight = pos / max(1, posmax)
#         # log.debug('top_weight=%r',top_weight)
#         top_height = round((maxrow-thumb_height) * top_weight)
#         # log.debug('top_height=%r', top_height)
#         bottom_height = maxrow - thumb_height - top_height
#         # log.debug('bottom_height=%r', bottom_height)

#         # log.debug('top=%r, thumb=%r, bottom=%r', top_height, thumb_height, bottom_height)
#         assert thumb_height + top_height + bottom_height == maxrow

#         top = urwid.SolidCanvas(self._trough_char, maxcol, top_height)
#         thumb = urwid.SolidCanvas(self._thumb_char, maxcol, thumb_height)
#         bottom = urwid.SolidCanvas(self._trough_char, maxcol, bottom_height)

#         return urwid.CanvasCombine([
#             (top, None, False),
#             (thumb, None, True),
#             (bottom, None, False),
#         ])
