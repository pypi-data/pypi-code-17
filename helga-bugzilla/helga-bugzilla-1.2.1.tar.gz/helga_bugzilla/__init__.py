from txbugzilla import connect
from helga.plugins import match, ResponseNotReady
from helga import log, settings
from helga_bugzilla.actions import describe, search_external
from helga_bugzilla.exceptions import HelgaBugzillaError

logger = log.getLogger(__name__)


def match_bugzilla(message):
    for action in (describe, search_external):
        matches = action.match(message)
        if matches:
            return (action, matches)


@match(match_bugzilla, priority=0)
def helga_bugzilla(client, channel, nick, message, action_and_matches):
    """
    Match information related to Bugzilla.
    """
    connect_args = {}
    if hasattr(settings, 'BUGZILLA_XMLRPC_URL'):
        connect_args['url'] = settings.BUGZILLA_XMLRPC_URL
    d = connect(**connect_args)

    (action, matches) = action_and_matches
    for callback in action.callbacks:
        d.addCallback(callback, matches, client, channel, nick)
        d.addErrback(send_err, client, channel)
    raise ResponseNotReady


def send_err(e, client, channel):
    client.msg(channel, str(e.value))
    # Provide the file and line number if this was an an unexpected error.
    if not isinstance(e.value, HelgaBugzillaError):
        tb = e.getBriefTraceback().split()
        client.msg(channel, str(tb[-1]))
