"""
@file
@brief Exception for Mokadi.
"""


class MokadiException(Exception):
    """
    Mokadi exception.
    """
    pass


class CognitiveException(Exception):
    """
    Failure when calling the API.
    """
    pass


class WikipediaException(Exception):
    """
    Issue with wikipedia
    """
    pass


class MokadiAuthentification(Exception):
    """
    Issue with authentification
    """
    pass
