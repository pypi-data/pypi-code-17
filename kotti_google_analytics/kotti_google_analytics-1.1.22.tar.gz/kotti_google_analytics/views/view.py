# -*- coding: utf-8 -*-

"""
Created on 2016-06-18
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
import os
import json

from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid import httpexceptions as httpexc

import googleanalytics as ga
from kotti_controlpanel.util import set_setting, get_setting, get_settings
from kotti_google_analytics import _, AnalyticsDefault, CONTROL_PANEL_LINKS
from kotti_google_analytics.fanstatic import css_and_js, ga_css_js
from kotti_google_analytics.views import BaseView
from oauth2client.client import FlowExchangeError


@view_config(
    name='analytics-code',
    renderer='kotti_google_analytics:templates/tracking_code.pt')
class CartView(BaseView):

    def __call__(self):
        return {
            "tracking_id": AnalyticsDefault.property_id
        }


class Analytics(BaseView):

    @property
    def credentials(self):
        if not hasattr(self, "__credentials"):
            self.__credentials = self.flow.step2_exchange(get_setting("refresh_token"))
        return self.__credentials

    @property
    def flow(self):
        client_id = get_setting("client_id")
        client_secret = get_setting("client_secret")
        if not client_id or not client_secret:
            return None
        if not hasattr(self, "__flow"):
            self.__flow = ga.auth.Flow(
                client_id,
                client_secret,
                redirect_uri=self.request.resource_url(
                    self.context, "google-analytics-callback"))
        return self.__flow

    @view_config(name='analytics-report', root_only=True,
                 permission="admin",
                 renderer="kotti_google_analytics:templates/analytics.pt")
    def view(self):
        ga_css_js.need()
        property_id = get_setting("property_id") or AnalyticsDefault.property_id
        access_token = get_setting("access_token")
        if not property_id or not access_token:
            return httpexc.HTTPFound(
                location="{}?setting_id=kotti_google_analytics".format(
                    self.request.resource_url(self.context, 'controlpanel'))
            )
        data = {
            "property_id": property_id,
            "access_token": access_token,
            "client_email": None,
            "refresh_token": get_setting("refresh_token"),
            "client_id": get_setting("client_id"),
            "client_secret": get_setting("client_secret"),
            "identity": get_setting("identity")
        }
        return {
            "google_analytics": data
        }

    @view_config(name='analytics-setup', root_only=True, permission="admin")
    def setup_analytics(self):
        if not self.flow:
            return httpexc.HTTPFound(
                location="{}?setting_id=kotti_google_analytics".format(
                    self.request.resource_url(self.context, 'controlpanel'))
            )
        authorize_url = self.flow.step1_get_authorize_url()
        return httpexc.HTTPFound(location=authorize_url)

    @view_config(name="google-analytics-callback", root_only=True,
                 permission="admin", renderer="kotti_google_analytics:templates/redirect_result.pt")
    def callback(self):
        try:
            if not self.flow:
                return httpexc.HTTPFound(
                    location="{}?setting_id=kotti_google_analytics".format(
                        self.request.resource_url(self.context, 'controlpanel'))
                )
            credentials = self.flow.step2_exchange(self.request.params['code'])
        except FlowExchangeError:
            return httpexc.HTTPFound(location=self.request.resource_url(self.context, 'analytics-setup'))
        jcred = credentials.serialize()
        set_setting("access_token", jcred.get("access_token"))
        set_setting("refresh_token", jcred.get("refresh_token"))
        set_setting("identity", jcred.get("identity"))
        return {
            "cp_links": CONTROL_PANEL_LINKS,
            "credentials": jcred
        }
