from .object import Object

class User(Object):
    """
    Represents a Slack user.
    """
    def __init__(self, slack, user):
        Object.__init__(self, user)
        self._slack = slack