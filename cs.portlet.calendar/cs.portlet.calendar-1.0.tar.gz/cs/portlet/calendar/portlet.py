from plone.app.layout.navigation.root import getNavigationRootObject
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from cs.portlet.calendar import MessageFactory as _
from plone.app.portlets.portlets import base
from plone.app.uuid.utils import uuidToObject
from plone.app.vocabularies.catalog import CatalogSource
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.i18nmessageid import MessageFactory
from zope.interface import implementer
from plone import api


try:
    from plone.app.contenttypes.behaviors.collection import ISyndicatableCollection as ICollection  # noqa
    from plone.app.contenttypes.interfaces import IFolder
    search_base_uid_source = CatalogSource(object_provides={
        'query': [
            ICollection.__identifier__,
            IFolder.__identifier__
        ],
        'operator': 'or'
    })
except ImportError:
    search_base_uid_source = CatalogSource(is_folderish=True)
    ICollection = None

PLMF = MessageFactory('plonelocales')


class ICalendarPortlet(IPortletDataProvider):
    """A portlet displaying a calendar
    """

    state = schema.Tuple(
        title=_(u"Workflow state"),
        description=_(u"Items in which workflow state to show."),
        default=None,
        required=False,
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.WorkflowStates")
    )

    search_base_uid = schema.Choice(
        title=_(u'portlet_label_search_base', default=u'Search base'),
        description=_(
            u'portlet_help_search_base',
            default=u'Select search base Folder or Collection to search for '
                    u'events. If empty, the nearest navigation root '
                    u'will be searched and the event listing view will be '
                    u'called on the site root.'
        ),
        required=False,
        source=search_base_uid_source,
    )

    link_base_uid = schema.Choice(
        title=_(u'portlet_label_link_base', default=u'Link base'),
        description=_(
            u'portlet_help_link_base',
            default=u'The URL to this item will be used to link '
                    u'to in calendar searches. If empty, the neaerest '
                    u'navigation root will be used.'
        ),
        required=False,
        source=search_base_uid_source,
    )

    view_name = schema.TextLine(
        title=_(u'portlet_label_view_name', default=u'View name'),
        description=_(
            u'portlet_help_view_name',
            default=u'The name of the view which will be appended to the '
                    u'Link base option to create the links of the days'
        ),
        required=False,
    )


@implementer(ICalendarPortlet)
class Assignment(base.Assignment):
    title = _(u'Calendar')

    # reduce upgrade pain
    state = None
    search_base = None
    link_base_uid = None
    view_name = None

    def __init__(self, state=None, search_base_uid=None, link_base_uid=None, view_name=None): # noqa
        self.state = state
        self.search_base_uid = search_base_uid
        self.link_base_uid = link_base_uid
        self.view_name = view_name


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('portlet.pt')

    _search_base = None
    _link_base = None

    @property
    def search_base(self):
        if not self._search_base:
            self._search_base = uuidToObject(self.data.search_base_uid)
        # aq_inner, because somehow search_base gets wrapped by the renderer
        return aq_inner(self._search_base)

    @property
    def search_base_path(self):
        search_base = self.search_base
        if search_base is not None:
            search_base = '/'.join(search_base.getPhysicalPath())
        return search_base

    @property
    def link_base(self):
        if not self._link_base:
            self._link_base = uuidToObject(self.data.link_base_uid)
        # aq_inner, because somehow link_base gets wrapped by the renderer
        return aq_inner(self._link_base)

    @property
    def link_base_path(self):
        link_base = self.link_base
        if link_base is not None:
            link_base = '/'.join(link_base.getPhysicalPath())
        return link_base

    def update(self):
        context = aq_inner(self.context)

        self.calendar_url = get_calendar_url(context, self.link_base_path, self.data.view_name) # noqa
        self.event_base_url = get_calendar_url(context, self.link_base_path)
        self.language = api.portal.get_current_language()


class AddForm(base.AddForm):
    schema = ICalendarPortlet
    label = _(u"Add Calendar Portlet")
    description = _(u"This portlet displays events in a calendar.")

    def create(self, data):
        return Assignment(
            state=data.get('state', None),
            search_base_uid=data.get('search_base_uid', None),
            link_base_uid=data.get('link_base_uid', None),
            view_name=data.get('view_name', None),
            )


class EditForm(base.EditForm):
    schema = ICalendarPortlet
    label = _(u"Edit Calendar Portlet")
    description = _(u"This portlet displays events in a calendar.")


def get_calendar_url(context, link_base, view_name=None):
    portal = api.portal.get()
    calendar_url = None
    if link_base:
        navigation_root = getNavigationRootObject(context, portal)
        link_base = '/'.join(link_base.split('/')[2:])
        calendar_url = navigation_root.unrestrictedTraverse(
            link_base.lstrip('/')  # start relative, first slash is omitted
        ).absolute_url()
    else:
        navigation_root = getNavigationRootObject(context, portal)
        calendar_url = navigation_root.absolute_url()

    if view_name:
        calendar_url = '{}/{}'.format(calendar_url, view_name)

    return calendar_url
