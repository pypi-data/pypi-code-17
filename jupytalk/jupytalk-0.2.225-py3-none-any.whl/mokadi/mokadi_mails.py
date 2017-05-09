"""
@file
@brief Look into the mail box
"""
import datetime
from pyquickhelper.loghelper import noLOG
from .mokadi_exceptions import MokadiAuthentification


def enumerate_last_mails(user, pwd, server, nb=5, fLOG=noLOG):
    """
    Returned the last mails

    @param  user        user
    @param  pwd         password
    @param  server      server something like ``imap.domain.ext``
    @param  ssl         select ``IMPA_SSL`` or ``IMAP``
    @param  nb          number of mails to retrieve
    @param  fLOG        logging function

    We use the examples from
    `Capturing a single image from my webcam in Java or Python <http://stackoverflow.com/questions/11094481/capturing-a-single-image-from-my-webcam-in-java-or-python>`_.

    See `pymmails <http://www.xavierdupre.fr/app/pymmails/helpsphinx/index.html>`_.
    """
    from pymmails.grabber import MailBoxImap
    now = datetime.datetime.now() - datetime.timedelta(1)
    date = now.strftime("%d-%b-%Y")
    pattern = "SINCE %s" % date
    fLOG("[enumerate_last_mails] pattern ", pattern)
    box = MailBoxImap(user, pwd, server, ssl=True, fLOG=fLOG)
    try:
        box.login()
    except Exception as e:
        raise MokadiAuthentification("Unable to connect to the mailbox") from e

    def enumerate_mails(iter):
        for mail in iter:
            yield mail.get_date(), mail

    mails = box.enumerate_mails_in_folder("inbox", pattern=pattern)
    for i, (dt, mail) in enumerate(sorted(enumerate_mails(mails), reverse=True)):
        yield mail
        if i >= nb:
            break
    box.logout()
