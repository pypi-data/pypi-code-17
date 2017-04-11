# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import requests


class RedOctoberException(EnvironmentError):
    """ This exception is raised from errors in the RedOctober Library. """

class RedOctoberRemoteException(RedOctoberException):
    """ This exception is raised to indicate issues returned from API. """

class RedOctoberDecryptException(RedOctoberRemoteException):
    """ This exception is raised when there are errors decrypting a file. """
