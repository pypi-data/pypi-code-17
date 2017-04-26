# -*- coding: utf-8 -*-
"""
    __init__

"""
from trytond.pool import Pool
from attachment import Attachment


def register():
    "Register models to tryton pool"
    Pool.register(
        Attachment,
        module='attachment_s3', type_='model'
    )
