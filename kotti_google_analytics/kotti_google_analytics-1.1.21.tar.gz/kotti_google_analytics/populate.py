import colander

import deform
from kotti_controlpanel.util import add_settings
from kotti_controlpanel.util import get_setting
from kotti_google_analytics import _, controlpanel_id, AnalyticsDefault, CONTROL_PANEL_LINKS


class AnalyticsSchema(colander.MappingSchema):
    client_id = colander.SchemaNode(
        colander.String(),
        name="client_id",
        title=_(u'Client ID'),
    )
    client_secret = colander.SchemaNode(
        colander.String(),
        name="client_secret",
        title=_(u'Client Secret'),
    )
    identity = colander.SchemaNode(
        colander.String(),
        name="identity",
        title=_(u'Identity'),
    )
    access_token = colander.SchemaNode(
        colander.String(),
        name="access_token",
        title=_(u'Access Token'),
        widget = deform.widget.HiddenWidget(),
        missing=True
    )
    refresh_token = colander.SchemaNode(
        colander.String(),
        name="refresh_token",
        title=_(u'Refresh Token'),
        widget = deform.widget.HiddenWidget(),
        missing=True
    )
    property_id = colander.SchemaNode(
        colander.String(),
        name="property_id",
        title=_(u'Account Property ID'),
        default=AnalyticsDefault.property_id
    )


GAControlPanel = {
    'name': controlpanel_id,
    'icon': 'kotti_google_analytics:static/analytics.png',
    'title': _(u'Google Analytics Settings'),
    'description': _(u"Settings for google_analytics"),
    'success_message': _(u"Successfully saved google_analytics settings."),
    'schema_factory': AnalyticsSchema,
    'template': "kotti_google_analytics:templates/controlpanel.pt"
}


def populate():

    add_settings(GAControlPanel, links=CONTROL_PANEL_LINKS)
