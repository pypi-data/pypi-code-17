import re
import time

from cloudshell.cli.command_mode_helper import CommandModeHelper
from cloudshell.networking.cli_handler_impl import CliHandlerImpl
from cloudshell.shell.core.api_utils import decrypt_password_from_attribute

from cloudshell.networking.arista.cli.arista_command_modes import AristaDefaultCommandMode, \
    AristaEnableCommandMode, AristaConfigCommandMode


class AristaCliHandler(CliHandlerImpl):
    def __init__(self, cli, context, logger, api):
        super(AristaCliHandler, self).__init__(cli, context, logger, api)
        modes = CommandModeHelper.create_command_mode(context)
        self.default_mode = modes[AristaDefaultCommandMode]
        self.enable_mode = modes[AristaEnableCommandMode]
        self.config_mode = modes[AristaConfigCommandMode]

    def default_mode_service(self):
        return self.get_cli_service(self.enable_mode)

    def config_mode_service(self):
        return self.get_cli_service(self.config_mode)

    def on_session_start(self, session, logger):
        """Send default commands to configure/clear session outputs
        :return:
        """

        self.enter_enable_mode(session=session, logger=logger)
        session.hardware_expect('terminal length 0', AristaEnableCommandMode.PROMPT, logger)
        session.hardware_expect('terminal width 300', AristaEnableCommandMode.PROMPT, logger)
        # session.hardware_expect('terminal no exec prompt timestamp', EnableCommandMode.PROMPT, logger)
        self._enter_config_mode(session, logger)
        session.hardware_expect('no logging console', AristaConfigCommandMode.PROMPT, logger)
        session.hardware_expect('exit', AristaEnableCommandMode.PROMPT, logger)

    def _enter_config_mode(self, session, logger):
        max_retries = 5
        error_message = 'Failed to enter config mode, please check logs, for details'
        output = session.hardware_expect(AristaConfigCommandMode.ENTER_COMMAND,
                                         '{0}|{1}'.format(AristaConfigCommandMode.PROMPT, AristaEnableCommandMode.PROMPT), logger)

        if not re.search(AristaConfigCommandMode.PROMPT, output):
            retries = 0
            while not re.search(r"[Cc]onfiguration [Ll]ocked", output, re.IGNORECASE) or retries == max_retries:
                time.sleep(5)
                output = session.hardware_expect(AristaConfigCommandMode.ENTER_COMMAND,
                                                 '{0}|{1}'.format(AristaConfigCommandMode.PROMPT, AristaEnableCommandMode.PROMPT),
                                                 logger)
            if not re.search(AristaConfigCommandMode.PROMPT, output):
                raise Exception('_enter_config_mode', error_message)

    def enter_enable_mode(self, session, logger):
        """
        Enter enable mode

        :param session:
        :param logger:
        :raise Exception:
        """
        result = session.hardware_expect('', '{0}|{1}'.format(AristaDefaultCommandMode.PROMPT, AristaEnableCommandMode.PROMPT),
                                         logger)
        if not re.search(AristaEnableCommandMode.PROMPT, result):
            enable_password = decrypt_password_from_attribute(api=self._api,
                                                              password_attribute_name='Enable Password',
                                                              context=self._context)
            expect_map = {'[Pp]assword': lambda session, logger: session.send_line(enable_password, logger)}
            session.hardware_expect('enable', AristaEnableCommandMode.PROMPT, action_map=expect_map, logger=logger)
            result = session.hardware_expect('', '{0}|{1}'.format(AristaDefaultCommandMode.PROMPT, AristaEnableCommandMode.PROMPT),
                                             logger)
            if not re.search(AristaEnableCommandMode.PROMPT, result):
                raise Exception('enter_enable_mode', 'Enable password is incorrect')
