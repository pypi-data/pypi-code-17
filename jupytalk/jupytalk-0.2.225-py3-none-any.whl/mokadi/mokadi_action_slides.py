#-*- coding: utf-8 -*-
"""
@file
@brief Defines an action for Mokadi.
"""
import os
from .mokadi_action import MokadiAction
from .mokadi_info import MokadiInfo
from .mokadi_exceptions import MokadiException
from .pptx_helper import pptx_enumerate_text
from .mokadi_helper import parse_string_int
import pptx


class MokadiActionSlides(MokadiAction):
    """
    Action present slides.
    """

    def __init__(self, folder, fLOG=None):
        """
        Constructor.

        @param      folder      folder where to look for presentation
        """
        MokadiAction.__init__(self, fLOG=fLOG)
        self._folder = folder
        if not os.path.exists(folder):
            raise FileNotFoundError(folder)

    def can_do(self, interpreted, message):
        """
        Tells is the class.

        @param      interpreted     interpreted message
        @param      message         message
        @return                     true if the class can process the message
        """
        if len(interpreted) < 2:
            return False
        word = interpreted[1]
        for word in interpreted[1:3]:
            if word[1] == ":presentation:":
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
        interpretation0 = interpretation
        interpretation = [_ for _ in interpretation if _[1] != ":numero:"]
        if len(interpretation) == 4:
            if interpretation[1][1] == ":verb_voir:" and interpretation[2][1] == ":presentation:":
                pres = list(self.enumerate_listdir())
                yield MokadiInfo("ok", "Il y a {0} présentations.".format(len(pres)))
                for name in pres:
                    yield MokadiInfo("ok", name)
                done = True
        elif len(interpretation) == 7:
            if interpretation[1][0] == "lire" and interpretation[2][1] == ":presentation:" and \
               interpretation[3][1] == ":int:" and interpretation[4][1] == ":slide:" and \
               interpretation[5][1] == ":int:":
                presn = parse_string_int(interpretation[3][0])
                slide = parse_string_int(interpretation[5][0])
                pres = list(self.enumerate_listdir())
                if presn <= 0 or presn > len(pres):
                    yield MokadiInfo("error", error="La présentation {0} n'existe pas.".format(presn))
                    done = True
                else:
                    name = os.path.join(self._folder, pres[presn - 1])
                    self.fLOG("[MokadiActionSlides] open '%s' from '%s'" % (
                        os.path.split(name)[-1], os.path.dirname(name)))
                    ptx = pptx.Presentation(name)
                    if slide <= 0 or slide > len(ptx.slides):
                        yield MokadiInfo("error", error="La présentation ne contient pas le transparent {0}.".format(slide))
                        done = True
                    else:
                        for islide, ishape, ip, text in pptx_enumerate_text(ptx):
                            if islide == slide - 1:
                                yield MokadiInfo("ok", text)
                        done = True
        if not done:
            raise MokadiException(
                "Unable to interpret '{0}'\n{1} - {2}.".format(message, len(interpretation0), interpretation))

    def enumerate_listdir(self):
        """
        Return all presentations in a folder.

        @return         list of presentation
        """
        for name in os.listdir(self._folder):
            if os.path.splitext(name)[-1] == ".pptx":
                yield name
