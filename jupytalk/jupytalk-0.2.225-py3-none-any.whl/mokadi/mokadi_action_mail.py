#-*- coding: utf-8 -*-
"""
@file
@brief Defines an action for Mokadi.
"""
from .mokadi_action import MokadiAction
from .mokadi_info import MokadiInfo
from .mokadi_exceptions import MokadiException, MokadiAuthentification
from .mokadi_mails import enumerate_last_mails
from .mokadi_helper import parse_string_int


class MokadiActionMail(MokadiAction):
    """
    Action. Mail.
    """

    def __init__(self, user, pwd, server, fLOG=None):
        """
        Constructor.

        @param      user        login
        @param      pwd         password
        @param      server      server
        @param      fLOG        logging function
        """
        MokadiAction.__init__(self, fLOG=fLOG)
        self._user = user
        self._pwd = pwd
        self._server = server

    def can_do(self, interpreted, message):
        """
        Tells if the class can process the message.

        @param      interpreted     interpreted message
        @param      message         message
        @return                     true if the class can process the message
        """
        if len(interpreted) < 2:
            return False
        word = interpreted[1]
        for word in interpreted[1:]:
            if word[1] == ":mails:":
                return True
        return False

    def process_interpreted_message(self, interpretation, message):
        """
        Process the interpreted message.

        @param      interpretation      interpretation
        @param      message             original message
        @return                         iterator on Info
        """
        done = False
        stop = -1
        keep = -1
        good = False
        body = False
        interpretation0 = interpretation
        interpretation = [_ for _ in interpretation if _[1] != ":numero:"]
        interpretation_clean = [
            _ for _ in interpretation if _[1] != ":stopword:"]
        if len(interpretation_clean) == 6:
            if interpretation_clean[1][1] == ":verb_voir:" and interpretation_clean[2][1] == ":mails:" and \
                    interpretation_clean[3][1] == ":int:" and interpretation_clean[4][1] == ":entier:":
                keep = parse_string_int(interpretation_clean[3][0])
                good = True
                body = True
        elif len(interpretation) == 5:
            if interpretation[1][1] == ":verb_voir:" and interpretation[2][1] == ":int:" and \
                    interpretation[3][1] == ":mails:":
                stop = parse_string_int(interpretation[2][0])
                good = True
            elif interpretation[1][1] == ":verb_voir:" and interpretation[2][1] == ":mails:" and \
                    interpretation[3][1] == ":int:":
                keep = parse_string_int(interpretation[3][0])
                good = True
        if not good and len(interpretation_clean) == 4:
            if interpretation_clean[1][1] == ":verb_voir:" and interpretation_clean[2][1] == ":mails:":
                good = True
        if good:
            fetch = max(keep + 1, 5)
            try:
                mails = enumerate_last_mails(
                    self._user, self._pwd, self._server, fLOG=self.fLOG, nb=fetch)
            except MokadiAuthentification as e:
                yield MokadiInfo("error", "Il m'est impossible de me connecter à la boîte mail de {0}.".format(self._user))

            try:
                for i, mail in enumerate(mails):
                    if i == stop:
                        break
                    if keep != -1 and i != keep:
                        continue
                    self.fLOG(mail.get_name(), "**", mail.get_nb_attachements(),
                              "**", mail.get_date_str())
                    h = mail.get_date().hour
                    yield MokadiInfo("ok", "Mail reçu vers {0} heures de {1}.".format(h, mail.get_name()))
                    yield MokadiInfo("ok", mail.get_field("subject").split("\n")[0])
                    nb = mail.get_nb_attachements()
                    if nb > 0:
                        yield MokadiInfo("ok", "Ce mail a {0} pièces jointes.".format(nb))
                    if body:
                        # The content of the mail includes past answers.
                        # This should be removed as well as html tags.
                        for line in mail.body.split("\n"):
                            yield MokadiInfo("ok", line)
            except MokadiAuthentification as e:
                yield MokadiInfo("error", "Il m'est impossible de me connecter à la boîte mail de {0}.".format(self._user))

            done = True
        if not done:
            raise MokadiException(
                "Unable to interpret '{0}'\n{1} - {2}\n.".format(message, len(interpretation0), interpretation, interpretation_clean))
