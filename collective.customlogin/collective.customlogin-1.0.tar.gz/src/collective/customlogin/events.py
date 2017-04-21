from collective.customlogin.interfaces import IUnauthorizedEvent
from plone.app.contentrules.handlers import execute
from zope.component.interfaces import ObjectEvent
from zope.interface import implements


class UnauthorizedEvent(ObjectEvent):
    """
    """
    implements(IUnauthorizedEvent)


def unauthorized_handler(event):
    """
    Execute any rules that are triggered by the IUnauthorizedEvent
    """
    execute(event.object, event)
