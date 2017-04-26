"""
Functions and accompanying CLI Tools to generate pseudo-random passwords and
UUIDs (GUIDs)
"""

from .gen_pass_cli import gen_pass, main as gen_pass_cli
from .gen_uuid_cli import gen_uuid, main as gen_uuid_cli

__version__ = "0.0.7"
