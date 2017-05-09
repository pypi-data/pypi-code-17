# -*- coding: utf-8 -*-

"""
Created on 2016-06-18
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

from kotti.util import Link
from kotti.resources import File
from kotti.views.slots import assign_slot
from pyramid.i18n import TranslationStringFactory
from kotti_controlpanel.util import get_setting, set_setting


controlpanel_id = 'kotti_google_analytics'

_ = TranslationStringFactory(controlpanel_id)

CONTROL_PANEL_LINKS = [
    Link('analytics-report', title=_(u"Google Analytics Report")),
    Link('analytics-setup', title=_(u"Setup Google Analytics"))
]


class AnalyticsDefault(object):
    property_id = None

def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_google_analytics.kotti_configure

        to enable the ``kotti_google_analytics`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """

    settings['pyramid.includes'] += ' kotti_google_analytics'
    settings['kotti.populators'] += ' kotti_google_analytics.populate.populate'
    settings['kotti.fanstatic.view_needed'] += ' kotti_google_analytics.fanstatic.css_and_js'
    assign_slot('analytics-code', 'belowcontent')


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """

    config.add_translation_dirs('kotti_google_analytics:locale')
    AnalyticsDefault.property_id = \
        config.registry.settings.get("kotti_google_analytics.tracking_id", None)
    config.add_static_view('static-kotti_google_analytics', 'kotti_google_analytics:static')

    config.scan(__name__)
