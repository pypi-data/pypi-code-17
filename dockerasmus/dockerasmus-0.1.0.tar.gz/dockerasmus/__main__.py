# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

from .cli import parser


args = parser.parse_args()
print(args)
