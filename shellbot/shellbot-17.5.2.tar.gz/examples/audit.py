#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Audit interactions in real-time

In this example we create a shell with one simple command: audit

- command: audit
- provides clear status if this room is currently audited or not

- command: audit on
- starts auditing

- command: audit off
- ensure private interactions


To run this script you have to provide a custom configuration, or set
environment variables instead::

- ``CHAT_ROOM_MODERATORS`` - You have at least your e-mail address
- ``CHAT_TOKEN`` - Received from Cisco Spark when you register your bot
- ``SERVER_URL`` - Public link used by Cisco Spark to reach your server

The token is specific to your run-time, please visit Cisco Spark for
Developers to get more details:

    https://developer.ciscospark.com/

For example, if you run this script under Linux or macOs with support from
ngrok for exposing services to the Internet::

    export CHAT_ROOM_MODERATORS="alice@acme.com"
    export CHAT_TOKEN="<token id from Cisco Spark for Developers>"
    export SERVER_URL="http://1a107f21.ngrok.io"
    python hello.py


"""

import logging
from multiprocessing import Process, Queue
import os

from shellbot import ShellBot, Context, Command, Speaker
from shellbot.spaces import SparkSpace
Context.set_logger()

# create a bot and load command
#
class Hello(Command):
    keyword = 'hello'
    information_message = u"Hello, World!"

bot = ShellBot(command=Hello())

# load configuration
#
os.environ['CHAT_ROOM_TITLE'] = 'Audit tutorial'
bot.configure()

# create a chat room
#
bot.bond(reset=True)

# create a secondary room
#
class Audit(object):

    def filter(self, item):
        logging.debug(u'Filter: {}'.format(item['text']))
        self.mouth.put(item['text'])
        return item


audit = Audit()
audit.context = bot.context
audit.mouth = Queue()
audit.space = SparkSpace(bot=audit)

title = u"{} - {}".format(
    bot.context.get('spark.room', 'Test'), u"Audited content")

audit.space.connect()
audit.space.bond(title=title)

# fork incoming items
#
bot.listener.filter = audit.filter

# speak to secondary room
#
audit.speaker = Speaker(bot=audit)
audit.speaker.run()

# run the bot
#
bot.run()

# delete the chat room when the bot is stopped
#
bot.dispose()
