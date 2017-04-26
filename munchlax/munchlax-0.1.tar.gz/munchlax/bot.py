import asyncio  
import traceback
from .slack import Slack

class Command(object):
    def __init__(self, cmd, func, requires, transforms):
        self.cmd = cmd
        self.requires = requires
        self.transforms = transforms
        self.func = func

    async def try_run(self, message):
        for transform in self.transforms:
            message = transform(message)

        if len(self.requires) > 0:
            if not all([await x(message) for x in self.requires]):
                return

        try:
            await self.func(message)
        except:
            traceback.print_exc()

class Bot(Slack):
    def __init__(self):
        Slack.__init__(self)
        self._commands = {}
        self._prefix = None

    ########################################
    # COMMAND REGISTRATION DECORATOR
    ########################################

    def command(self, cmd=None, requires=[], transforms=[]):
        def dec(func):
            nonlocal cmd

            if cmd is None:
                cmd = func.__name__

            self._commands[cmd] = Command(cmd, func, requires, transforms)
            return func
        return dec

    ########################################
    # EVENT HANDLERS (ASYNC)
    ########################################

    def _check_prefix(self, message):
        if message.startswith(self._prefix):
            return True
        return False

    ########################################
    # EVENT HANDLERS (ASYNC)
    ########################################

    async def _handle_message(self, message):
        if not self._check_prefix(message.text):
            return

        message.text = message.text.replace(self._prefix, '', 1)

        command = message.text.split(' ')[0]

        if command in self._commands:
            await self._commands[command].try_run(message)

    ########################################
    # EXPOSED FUNCTiONS
    ########################################

    def set_prefix(self, prefix):
        self._prefix = prefix

    def start(self, token, prefix):
        self.set_token(token)
        self.on('message', self._handle_message)

        self._prefix = prefix

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.listen())