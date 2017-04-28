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
        """
        A decorator function for creating Slack commands.

        This decorator is expected to be used with async functions.

        Args:
            cmd (string): The desired command string. If this is kept
                as ``None`` then the function's name will be used as
                the command string.

            requires (list (Function)): A list of functions that must
                pass in order for the command execution function to run.
                All functions should be asynchronous functions. Functions
                will be run like so: ``await required_func(message)``.

            transforms (list (Function)): A list of transformation functions
                to be run on the message before it is passed to the require
                functions. Transform functions should not be async functions.
                Transformation functions are run like so: ``message = transform(message)``
                Note that transformation functions are run in the order that
                they are specified.

        Returns:
            Decorator: A decorator that takes a function.
        """
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
        if self._prefix is None:
            self._prefix = '@<{}>'.format(self.me.user_id)

        if message.startswith(self._prefix):
            return True
        return False

    ########################################
    # EVENT HANDLERS (ASYNC)
    ########################################

    async def _handle_message(self, message):
        if not self._check_prefix(message.text):
            return

        message.text = message.text.replace(self._prefix, '', 1).strip()

        command = message.text.split(' ')[0]

        if command in self._commands:
            await self._commands[command].try_run(message)

    ########################################
    # EXPOSED FUNCTiONS
    ########################################

    def set_prefix(self, prefix=None):
        """
        Sets the bot's prefix.

        Args:
            prefix (str): The prefix to use for the bot.  If ``None`` is specified
                then a user mention will be used as the prefix. Defaults to
                ``None``.
        """
        self._prefix = prefix

    def set_token(self, token):
        """
        Sets the token to be used by the bot
        when connecting to Slack.

        Args:
            token (str): The token to use for Slack.

        Raises:
            SlackError: Raised in the event that Slack does not return ``ok``.
        """
        Slack.set_token(self, token)

    def start(self):
        """
        Starts the bot.
        """
        self.on('message', self._handle_message)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.listen())