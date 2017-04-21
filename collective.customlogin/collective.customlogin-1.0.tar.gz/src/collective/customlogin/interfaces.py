from zope.component.interfaces import IObjectEvent


class IUnauthorizedEvent(IObjectEvent):
    """
    An Event that's called during the Challenge phase of the PAS process
    Allows custom handling of access to the object
    """
