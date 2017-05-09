#-*- coding: utf-8 -*-
"""
@file
@brief Defines a message for mokadi.
"""
from .mokadi_grammar import interpret
from .mokadi_exceptions import MokadiException


class MokadiMessage:
    """
    Defines a message for mokadi.
    """

    def __init__(self, message: str, confidence: float):
        """
        Constructor

        @param      message         message (string)
        @param      confidence
        """
        self._message = message
        self._confidence = confidence

    def __str__(self):
        """
        message to string
        """
        return self._message

    def __repr__(self):
        """
        message to string
        """
        return "MokadiMessage('%s', %f)" % (self._message.replace("'", "\\'"), self._confidence)

    def _repr_html_(self):
        """
        for notebooks
        """
        return "<b>%1.2f<b> <i>%s</i>" % (self._confidence, self._message)

    @property
    def message(self):
        """
        property
        """
        return self._message

    @property
    def confidence(self):
        """
        property
        """
        return self._confidence

    def interpret(self, exc=True, MokadiGrammarParser=None, MokadiGrammarLexer=None,
                  MokadiGrammarListener=None):
        """
        Interpret the message with the grammar.

        @param      exc                     raises an exception if error
        @param      MokadiGrammarParser     parser for a specific language (cannot be None despite the default value)
        @param      MokadiGrammarLexer      lexer for a specific language (cannot be None despite the default value)
        @param      MokadiGrammarListener   listener for a specific language (cannot be None despite the default value)
        @return                             interpretation
        """
        if MokadiGrammarParser is None:
            raise MokadiException("MokadiGrammarParser cannot be None")
        if MokadiGrammarLexer is None:
            raise MokadiException("MokadiGrammarLexer cannot be None")
        if MokadiGrammarListener is None:
            raise MokadiException("MokadiGrammarListener cannot be None")
        if exc:
            return interpret(self._message, MokadiGrammarParser, MokadiGrammarLexer, MokadiGrammarListener)
        else:
            try:
                return interpret(self._message, MokadiGrammarParser, MokadiGrammarLexer, MokadiGrammarListener)
            except Exception as e:
                if not hasattr(self, "_errors"):
                    self._errors = []
                self._errors.append(e)
                return e
