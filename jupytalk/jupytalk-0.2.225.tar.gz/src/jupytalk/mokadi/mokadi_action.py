"""
@file
@brief Defines an action for Mokadi.
"""


class MokadiAction:
    """
    Action.
    """

    def __init__(self, fLOG=None):
        """
        Constructor.
        """
        if fLOG is not None:
            self._fLOG = fLOG

    def fLOG(self, *l, **p):
        """
        logging function
        """
        if hasattr(self, "_fLOG") and self._fLOG is not None:
            self._fLOG(*l, **p)

    def __str__(self):
        """
        usual
        """
        return self.__class__.__name__

    def __repr__(self):
        """
        usual
        """
        return self.__class__.__name__

    def can_do(self, interpreted, message):
        """
        Tells if the class can process the message.

        @param      interpreted     interpreted message
        @param      message         message
        @return                     true if the class can process the message
        """
        raise NotImplementedError("You should overload this method.")

    def process_interpreted_message(self, interpretation, message):
        """
        Process the interpreted message.

        @param      interpretation      interpretation
        @param      message             original message
        @return                         iterator on Info
        """
        raise NotImplementedError("You should overload this method.")
