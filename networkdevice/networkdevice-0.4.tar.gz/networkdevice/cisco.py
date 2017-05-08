#!/usr/bin/env python

import linux
import json
import pexpect
import xmltodict
import sys

class CiscoDevice(linux.LinuxDevice):
    '''
    A base class for common Cisco device.
    '''
    version = '0.1'
    def __init__(self, device = None, **kwargs):

        linux.LinuxDevice.__init__(self, device, **kwargs)
        self.log('Not support yet.')

