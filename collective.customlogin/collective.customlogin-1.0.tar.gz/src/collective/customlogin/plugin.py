from AccessControl.SecurityInfo import ClassSecurityInfo
from collective.customlogin.events import UnauthorizedEvent
from collective.customlogin.utils import find_context
from collective.customlogin.utils import get_challenge_status
from Globals import DTMLFile
from plone import api
from Products.PluggableAuthService.interfaces.plugins import IChallengePlugin
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from zope.event import notify

manage_addCustomLoginForm = DTMLFile("zmi/challenger", globals())


def manage_addCustomLogin(self, id, title='', REQUEST=None):
    """Add a CustomLogin to a Pluggable Authentication Service.
    """
    c = CustomLogin(id, title)
    self._setObject(c.getId(), c)

    if REQUEST is not None:
        REQUEST["RESPONSE"].redirect(
            "%s/manage_workspace"
            "?manage_tabs_message=CustomLogin+added." %
            self.absolute_url()
        )


class CustomLogin(BasePlugin):
    """Simple challenge plugin giving a static no-access page.
    """

    meta_type = "Custom Login plugin"
    security = ClassSecurityInfo()

    _properties = ({
        "id": "title",
        "label": "Title",
        "type": "string",
        "mode": "w",
    },)

    def __init__(self, id, title=None):
        self._setId(id)
        self.title = title

    def challenge(self, request, response):
        ob = find_context(request)
        event = UnauthorizedEvent(ob)
        notify(event)
        # Get the status of the challenge
        if get_challenge_status(request):
            return True
        return False


classImplements(CustomLogin, IChallengePlugin)

# vi: sw=4 expandtab
