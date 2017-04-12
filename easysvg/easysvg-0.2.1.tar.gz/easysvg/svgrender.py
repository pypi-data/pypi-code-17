"""
SVG Drawing Functions, originally created for http://sleep.fig14.com/
"""

import logging
import math

__author__ = 'Stephen Brown (Little Fish Solutions LTD)'

log = logging.getLogger(__name__)


class SvgPathGenerator(object):
    def __init__(self):
        self.data = []

    def put(self, string):
        self.data.append(string)

    def move_to(self, x, y):
        self.put('M %s %s' % (x, y))

    def line_to(self, x, y):
        self.put('L %s %s' % (x, y))

    def arc_to(self, rx, ry, x_axis_rotation, large_arc_flag, sweep_flag, dx, dy):
        self.put('A %s %s %s %s %s %s %s' % (rx, ry, x_axis_rotation, large_arc_flag, sweep_flag, dx, dy))

    def get_d(self):
        """
        :return: Svg path "d" attribute
        """
        return ' '.join(self.data)


class SvgGenerator(object):
    def __init__(self):
        self.data = []

    @staticmethod
    def _polar_to_cartesian(cx, cy, r, theta):
        """
        :param cx: X coord of circle
        :param cy: Y coord of circle
        :param r: Radius of circle
        :param theta: Degrees from vertical, clockwise, in radians
        :return: (x, y)
        """
        return cx - r * math.sin(theta), cy - r * math.cos(theta)

    def put(self, string):
        self.data.append(string)
    
    def begin(self, width, height, onload=None, view_box_mode=False):
        self.put('<svg xmlns:svg="http://www.w3.org/2000/svg" ')
        self.put('xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" ')

        if view_box_mode:
            self.put('viewBox="0 0 ')
            self.put(str(width))
            self.put(' ')
            self.put(str(height))
        else:
            self.put('width="')
            self.put(str(width))
            self.put('" height="')
            self.put(str(height))

        self.put('" version="1.1"')
        if onload:
            self.put(' onload="')
            self.put(onload)
            self.put('"')
        self.put('>')
        self.put('\n <!-- Generated using the Little Fish Solutions LTD SVG Generator Library. Enjoy! -->\n')
    
    def end(self):
        self.put('</svg>')
    
    def line(self, x1, y1, x2, y2, stroke='black', stroke_width=1):
        self.put(' <line x1="')
        self.put(str(x1))
        self.put('" y1="')
        self.put(str(y1))
        self.put('" x2="')
        self.put(str(x2))
        self.put('" y2="')
        self.put(str(y2))
        self.put('" stroke="')
        self.put(stroke)
        self.put('" stroke-width="')
        self.put(str(stroke_width))
        self.put('"/>\n')
    
    def rect(self, x, y, width, height, fill=None, stroke=None,
             stroke_width=1, onmousemove=None, onmouseout=None,
             hidden=False, css_class=None, id=None, link_target=None):
        self.put(' ')
        if link_target:
            self.put('<a xlink:href="')
            self.put(link_target)
            self.put('">')
        self.put('<rect x="')
        self.put(str(x))
        self.put('" y="')
        self.put(str(y))
        self.put('" width="')
        self.put(str(width))
        self.put('" height="')
        self.put(str(height))
        self.put('" stroke-width="')
        self.put(str(stroke_width))
        self.put('"')
        
        if fill:
            self.put(' fill="')
            self.put(fill)
            self.put('"')
        if stroke:
            self.put(' stroke="')
            self.put(stroke)
            self.put('"')
        if onmousemove:
            self.put(' onmousemove="')
            self.put(onmousemove)
            self.put('"')
        if onmouseout:
            self.put(' onmouseout="')
            self.put(onmouseout)
            self.put('"')
        if hidden:
            self.put(' visibility="hidden"')
        if css_class:
            self.put(' class="')
            self.put(css_class)
            self.put('"')
        if id:
            self.put(' id="')
            self.put(str(id))
            self.put('"')
            
        self.put('/>')
        if link_target:
            self.put('</a>\n')

    def text(self, text, x, y, fill='black', font_size=14, anchor='start', alignment_baseline=None,
             hidden=False, css_class=None, id=None, transform=None):
        self.put(' <text x="')
        self.put(str(x))
        self.put('" y="')
        self.put(str(y))
        self.put('" fill="')
        self.put(fill)
        self.put('" font-size="')
        self.put(str(font_size))
        self.put('" text-anchor="')
        self.put(anchor)
        self.put('"')
        if alignment_baseline:
            self.put(' alignment-baseline="')
            self.put(alignment_baseline)
            self.put('"')
        if hidden:
            self.put(' visibility="hidden"')
        if transform:
            self.put(' transform="')
            self.put(transform)
            self.put('"')
        if css_class:
            self.put(' class="')
            self.put(css_class)
            self.put('"')
        if id:
            self.put(' id="')
            self.put(str(id))
            self.put('"')
        self.put('>')
        self.put(str(text))
        self.put('</text>\n')

    def circle(self, cx, cy, r, stroke=None, fill=None, stroke_width=1):
        """
        :param cx: Center X
        :param cy: Center Y
        :param r: Radius
        """
        self.put(' <circle cx="')
        self.put(str(cx))
        self.put('" cy="')
        self.put(str(cy))
        self.put('" r="')
        self.put(str(r))
        self.put('" stroke-width="')
        self.put(str(stroke_width))
        self.put('"')
        if fill:
            self.put(' fill="')
            self.put(fill)
            self.put('"')
        if stroke:
            self.put(' stroke="')
            self.put(stroke)
            self.put('"')
        self.put('/>\n')

    def polygon(self, points, stroke=None, fill=None, stroke_width=1, disable_anti_aliasing=False):
        """
        :param points: List of points
        """
        self.put(' <polygon points="')
        self.put(' '.join(['%s,%s' % p for p in points]))
        self.put('" stroke-width="')
        self.put(str(stroke_width))
        self.put('"')
        if fill:
            self.put(' fill="')
            self.put(fill)
            self.put('"')
        if stroke:
            self.put(' stroke="')
            self.put(stroke)
            self.put('"')
        if disable_anti_aliasing:
            self.put(' shape-rendering="crispEdges"')
        self.put('/>\n')

    def arc(self, cx, cy, r, start_radians, end_radians, fill=None):
        """
        NOTE: This will leave gaps between adjacent segments. You can fix this by disabling anti-aliasing using
              shape-rendering="crispEdges" on the path tag

              If you want to add a stroke to this, it's advisable to create a second path that just strokes the
              outside of the circle

        :param cx: Center X
        :param cy: Center Y
        :param r: Radius
        :param start_radians: Start of arc in radians, clockwise from vertical
        :param end_radians: End of arc in radians, clockwise from vertical
        """

        # This is tricky - we have to use a path, and for that we need to know the start and end points of the arc
        # in cartesian coordinates

        start = self._polar_to_cartesian(cx, cy, r, start_radians)
        end = self._polar_to_cartesian(cx, cy, r, end_radians)

        total_radians = start_radians - end_radians
        if total_radians < 0:
            total_radians *= -1
        large_arc_flag = 1 if total_radians > math.pi else 0

        path = SvgPathGenerator()
        path.move_to(end[0], end[1])
        path.line_to(cx, cy)
        path.line_to(start[0], start[1])
        path.arc_to(r, r, 0, large_arc_flag, 0, end[0], end[1])

        self.put(' <path d="')
        self.put(path.get_d())
        self.put('"')
        if fill:
            self.put(' fill="')
            self.put(fill)
            self.put('"')
        self.put('/>\n')

    def get_svg(self):
        return ''.join(self.data)


def rotation_transform(degrees, x_center, y_center):
    return 'rotate(%s %s %s)' % (degrees, x_center, y_center)


def render_error_svg(error_text, width=800, height=600, view_box_mode=True):
    svg = SvgGenerator()
    svg.begin(width, height, view_box_mode=view_box_mode)
    svg.text(error_text, 10, 280, fill='#AA0000')
    svg.end()

    return svg.get_svg()

