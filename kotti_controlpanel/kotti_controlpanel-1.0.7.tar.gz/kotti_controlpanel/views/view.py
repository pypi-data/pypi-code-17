# -*- coding: utf-8 -*-

"""
Created on 2016-06-15
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid import httpexceptions as httpexc
from pyramid.renderers import render_to_response

from kotti.views.util import is_root

from kotti_controlpanel.forms import SettingsFormView

from kotti import DBSession
from kotti.util import Link
from kotti.views import users as kotti_users
from kotti.fanstatic import jquery_form
from kotti_controlpanel import _, util, CONTROL_PANEL_LINKS
from kotti_controlpanel.config import SETTINGS
from kotti_controlpanel.resources import ControlPanel
from kotti_controlpanel.fanstatic import css_and_js
from kotti_controlpanel.views import BaseView


class BaseSettingViews(BaseView):

    @view_config(name="controlpanel-dump", permission="admin", root_only=True,
                 renderer="kotti_controlpanel:templates/controlpanel-dump.pt")
    def dump_all_settings(self):
        settings = util.get_settings()
        return {
            "all_settings": settings,
            "UCP_LINKS": CONTROL_PANEL_LINKS
        }

    @view_config(name='controlpanel',
                 custom_predicates=(is_root, ),
                 permission='admin',
                #  request_method = 'GET',
                 renderer='kotti_controlpanel:templates/controlpanel.pt')
    def view(self):
        setting_id = self.request.params.get("setting_id")
        if not setting_id:
            settings_form_views = []
            for settings in SETTINGS.values():
                settings_form_views.append(
                    settings
                )
            return {
                "settings": settings_form_views,
                "UCP_LINKS": CONTROL_PANEL_LINKS
            }
        settings = SETTINGS.get(setting_id)
        if not settings:
            return httpexc.HTTPNotFound()
        args = {
            'title': settings.title,
            'description': settings.description,
            'name': settings.name,
            'schema_factory': settings.schema_factory,
            'settings': settings,
            'success_message': settings.success_message,
            'active': True,
        }
        View = type(str(setting_id), (SettingsFormView,), args)
        view = View(self.context, self.request)
        form = view()
        form["view"] = view
        links = util.get_links(setting_id)

        link1 = Link('controlpanel', title=_(u'Control Panel'))
        if link1 not in links:
            links.append(
                link1
            )
        if self.request.has_permission("admin"):
            link2 = Link("controlpanel-dump", title=_(u'All Settings'))
            if link2 not in links:
                links.append(
                    link2
                )

        template = (settings.template or
                    'kotti_controlpanel:templates/settings.pt')
        return render_to_response(
            template,
            {
                "settings": settings,
                "settings_form": form,
                "cp_links": links,
                "UCP_LINKS": CONTROL_PANEL_LINKS
            },
            request=self.request)
