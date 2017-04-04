""""
aiodictcc - an async way to translate by using `http://dict.cc` as a base.
"""

from aiodictcc.wrapper import UnavailableLanguageError, Translate

__version__ = "1.0.3"
__author__ = "Nils Theres"

__all__ = ("UnavailableLanguageError", "Translate")
