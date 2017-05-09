#-*- coding: utf-8 -*-
"""
@file
@brief Defines an action for Mokadi.
"""
import os
import random
from .mokadi_action import MokadiAction
from .mokadi_info import MokadiInfo
from .mokadi_exceptions import MokadiException
from .mokadi_wikipedia import definition_wikipedia, synonyms_wiktionary


class MokadiActionConversation(MokadiAction):
    """
    Action. Conversation.
    """

    _sounds = {"hello": os.path.join(os.path.abspath(os.path.dirname(__file__)), "data", "hello.wav"),
               "faux_rire": os.path.join(os.path.abspath(os.path.dirname(__file__)), "data", "faux_rire.wav"),
               "applaudit": os.path.join(os.path.abspath(os.path.dirname(__file__)), "data", "applaus.wav"),
               "toilette": os.path.join(os.path.abspath(os.path.dirname(__file__)), "data", "toilet_flush_2.wav")
               }

    _messages = {"hello": ["hello", "bonjour", "salut"],
                 "bye": ["au revoir", "salut", "adieu", "à la prochaine", "à la revoyure"]}

    @staticmethod
    def peak_random(mes: list):
        """
        Pick a random message

        @param      mes     list of strings
        @return             one string
        """
        i = random.randint(0, len(mes) - 1)
        return mes[i]

    def __init__(self, fLOG=None):
        """
        Constructor.

        @param      folder      folder where to look for presentation
        @param      fLOG        logging function
        """
        MokadiAction.__init__(self, fLOG=fLOG)

    def can_do(self, interpreted, message):
        """
        Tells if the class can process the message.

        @param      interpreted     interpreted message
        @param      message         message
        @return                     true if the class can process the message

        The function should be optimized for a subset of answers
        quite long to build.
        """
        if len(interpreted) <= 1:
            return False
        res = self.process_interpreted_message(interpreted, message)
        try:
            for info in res:
                return True
        except MokadiException:
            return False
        return False

    def process_interpreted_message(self, interpretation, message):
        """
        Process the interpreted message.

        @param      interpretation      interpretation
        @param      message             original message
        @return                         iterator on Info
        """
        sentance = [w[0].lower() for w in interpretation[1:]]
        joined = " ".join(sentance).lower().replace("d'", "").replace("l'", "")
        if sentance[0] in {"hello", "bonjour", "salut"}:
            options = MokadiActionConversation._messages["hello"]
            yield MokadiInfo("ok", MokadiActionConversation.peak_random(options))
        elif sentance[0] in {"bye", "au revoir", "salut"}:
            options = MokadiActionConversation._messages["bye"]
            yield MokadiInfo("ok", MokadiActionConversation.peak_random(options))
        elif sentance[0] in {"papa", "papounet"}:
            if "ordinateur" in joined:
                yield MokadiInfo("ok", "", sound=MokadiActionConversation._sounds["faux_rire"])
            else:
                raise MokadiException(
                    "Unable to answer to '{0}'.".format(sentance))
        elif sentance[0] in {"bruit", "son"}:
            if "toilette" in joined:
                yield MokadiInfo("ok", "", sound=MokadiActionConversation._sounds["toilette"])
            elif "applaudissement" in joined:
                yield MokadiInfo("ok", "", sound=MokadiActionConversation._sounds["applaudit"])
            else:
                raise MokadiException(
                    "Unable to answer to '{0}'.".format(sentance))
        elif sentance[0] in {"quel", "quelle", "comment", "pourquoi"}:
            yield MokadiInfo("ok", "Je ne sais pas répondre à la question: {0}".format(sentance))
        elif joined.startswith("c'est quoi") or interpretation[1][1] in {":definition:"}:
            if "intelligence" in joined and "artificielle" in joined:
                yield MokadiInfo("ok", "C'est moi.")
            else:
                query = " ".join(_[0] for _ in interpretation[
                                 2:-1] if _[1] not in {":stopword:"})
                self.fLOG(
                    "[MokadiActionConversation.process_interpreted_message] definition of '{0}'".format(query))
                res = definition_wikipedia(query)
                if res is None or len(res) == 0:
                    yield MokadiInfo("ok", "Je n'ai pas trouvé de définition pour {0}.".format(query))
                else:
                    yield MokadiInfo("ok", res)
        elif interpretation[1][1] in {":synonym:"}:
            query = " ".join(_[0] for _ in interpretation[
                             2:-1] if _[1] not in {":stopword:"})
            self.fLOG(
                "[MokadiActionConversation.process_interpreted_message] synonym of '{0}'".format(query))
            res = synonyms_wiktionary(query)
            if res is None or len(res) == 0:
                yield MokadiInfo("ok", "Je n'ai pas trouvé de synonyme.")
            else:
                yield MokadiInfo("ok", " ".join(res))
        else:
            raise MokadiException(
                "Unable to answer to '{0}'.".format(sentance))
