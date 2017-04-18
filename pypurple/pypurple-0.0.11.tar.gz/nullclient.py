#!/usr/bin/python3
#
#  Copyright (c) 2008 INdT - Instituto Nokia de Tecnologia
#
#  This file is part of python-purple.
#
#  python-purple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  python-purple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import inspect
import getpass
import sys
import ctypes
import time
import threading
import sys
import queue

from ctypes import CDLL

# The information below is needed by libpurple
__NAME__ = "nullclient"
__VERSION__ = "0.0.1"
__WEBSITE__ = "N/A"
__DEV_WEBSITE__ = "N/A"

gcore = None
gqueue = None
gacc = None

def test(title, primary, secondary, default_action, req_act_list):
    #title = b'SSL Certificate Verification'
    #primary = b'Accept certificate for talk.google.com?'
    #secondary = b'The certificate for talk.google.com could not be validated.\nThe certificate claims to be from "gmail.com" instead. This could mean that you are not connecting to the service you believe you are.'
    #default_action = 0
    #req_act_list = [b'Accept', b'Reject', b'_View Certificate...']
    core.call_action(default_action)

def send_message(purple, account, name, message):
    conv = pypurple.Conversation('IM', account, name)
    conv.new()
    conv.im_send(message)

def test():

    global gcore
    CDLL("/usr/lib/libpurple.so", mode=ctypes.RTLD_GLOBAL)

    import pypurple

    # Sets initial parameters
    core = pypurple.Purple(__NAME__, __VERSION__, __WEBSITE__, __DEV_WEBSITE__, \
            debug_enabled=False, default_path="/dev/null")
    gcore = core

    # Initializes libpurple
    core.purple_init()
    core.run()

def handle_connected():
    print ("well.....")


if __name__ == '__main__':

   import pypurple, time

   t = threading.Thread(target=test)
   t.start()
   time.sleep(1)
   p = pypurple.SProtocol("prpl-jabber", gcore)
   print("account..")
   a = pypurple.Account("andrey@embeddedwits.com", p, gcore)
   print("acc done")
   gacc = a
   a.new()
   info = {}
   info['connect_server'] = 'talk.google.com'
   info['port'] = '5222'
   info['old_ssl'] = False
   a.set_protocol_options(info)
   a.set_callback(pypurple.SIGNAL_SIGNED_ON, handle_connected)
   a.set_password("aquahelix00")
   a.set_enabled(True)
