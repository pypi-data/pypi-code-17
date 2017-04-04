from cloudshell.cli.command_mode import CommandMode


class AristaDefaultCommandMode(CommandMode):
    PROMPT = r'>\s*$'
    ENTER_COMMAND = ''
    EXIT_COMMAND = ''

    def __init__(self, context):
        """
        Initialize Default command mode, only for cases when session started not in enable mode

        :param context:
        """
        self._context = context
        CommandMode.__init__(self, AristaDefaultCommandMode.PROMPT, AristaDefaultCommandMode.ENTER_COMMAND,
                             AristaDefaultCommandMode.EXIT_COMMAND)


class AristaEnableCommandMode(CommandMode):
    PROMPT = r'#\s*$'
    ENTER_COMMAND = 'enable'
    EXIT_COMMAND = ''

    def __init__(self, context):
        """
        Initialize Enable command mode - default command mode for Arista Shells

        :param context:
        """
        self._context = context

        CommandMode.__init__(self, AristaEnableCommandMode.PROMPT, AristaEnableCommandMode.ENTER_COMMAND,
                             AristaEnableCommandMode.EXIT_COMMAND)


class AristaConfigCommandMode(CommandMode):
    PROMPT = r'\(config.*\)#\s*$'
    ENTER_COMMAND = 'configure terminal'
    EXIT_COMMAND = 'end'

    def __init__(self, context):
        """
        Initialize Config command mode

        :param context:
        """
        self._context = context
        CommandMode.__init__(self, AristaConfigCommandMode.PROMPT,
                             AristaConfigCommandMode.ENTER_COMMAND,
                             AristaConfigCommandMode.EXIT_COMMAND)


CommandMode.RELATIONS_DICT = {
    AristaDefaultCommandMode: {
        AristaEnableCommandMode: {
            AristaConfigCommandMode: {}
        }
    }
}