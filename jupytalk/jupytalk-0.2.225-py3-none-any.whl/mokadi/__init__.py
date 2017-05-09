"""
@file
@brief Shorcuts
"""

from .mokadi_engine import MokadiEngine
from .mokadi_exceptions import MokadiException
from .gui_mokadi import gui_mokadi
from .mokadi_grammar import interpret
from .mokadi_info import MokadiInfo
from .mokadi_mails import enumerate_last_mails
from .mokadi_message import MokadiMessage
from .mokadi_picture import take_picture
from .mokadi_record import record_speech, play_speech
from .mokadi_speak import speak
from .mokadi_wikipedia import definition_wikipedia, suggestions_wikipedia, synonyms_wiktionary
