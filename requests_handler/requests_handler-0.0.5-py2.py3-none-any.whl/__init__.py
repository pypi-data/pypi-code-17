"""
Handler for logging records to a Restful API.

:param api_url: URL to post records to.
:param auth: Credentials in format (username, password).
:param level: Logging level (DEBUG, INFO, ERROR, WARNING, CRITICAL).
:param filter: Minimum record level to emit.
:param bubble: Should bubble.
"""

from .handlers import RequestsHandler

__version__ = "0.0.5"