"""
Jisho API wrapper
An asynchronous wrapper for the Jisho.org API
"""

from .jisho import Jisho, SyncJisho

__all__ = ['Jisho', 'SyncJisho']
