# -*- coding: utf-8 -*-

"""
Created on 2016-06-18
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

from __future__ import absolute_import

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource


library = Library("kotti_google_analytics", "static")

css = Resource(
    library,
    "styles.css",
    minified="styles.min.css")
js = Resource(
    library,
    "scripts.js",
    minified="scripts.min.js")
    

js_moment = Resource(
    library,
    "moment.min.js"
)
js_widget = Resource(
    library,
    "widget.js"
)
js_chart = Resource(
    library,
    "Chart.min.js"
)

js_activeuser = Resource(
    library,
    "active-users.js"
)
js_datarange = Resource(
    library,
    "date-range-selector.js"
)
js_viewselector2 = Resource(
    library,
    "view-selector2.js"
)
js_embed = Resource(
    library,
    "embed.js",
    depends=[js_moment, js_chart, js_activeuser,
             js_datarange, js_viewselector2, js_viewselector2, js_widget]
)
css_visualize = Resource(
    library,
    "chartjs-visualizations.css"
)


css_and_js = Group([css, js])
ga_css_js = Group([css_visualize, js_embed])
