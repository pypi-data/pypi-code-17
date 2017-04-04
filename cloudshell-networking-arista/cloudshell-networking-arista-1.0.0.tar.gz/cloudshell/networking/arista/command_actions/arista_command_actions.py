import re

from cloudshell.networking.arista.command_templates.arista_configuration_templates import BOOT_SYSTEM_FILE, \
    SHOW_BOOT
from cloudshell.networking.arista.command_templates.cisco_configuration_templates import COPY


def copy(session, logger, source, destination, vrf=None, action_map=None, error_map=None):
    """Copy file from device to tftp or vice versa, as well as copying inside devices filesystem.

    :param session: current session
    :param logger:  logger
    :param source: source file
    :param destination: destination file
    :param vrf: vrf management name
    :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
    :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
    :raise Exception:
    """

    if not vrf:
        vrf = None
    output = session.send_command(
        **COPY.get_command(src=source, dst=destination, vrf=vrf, action_map=action_map, error_map=error_map))

    status_match = re.search(r'\d+ bytes copied|copied.*[\[\(].*[0-9]* bytes.*[\)\]]|[Cc]opy complete', output,
                             re.IGNORECASE)
    if not status_match:
        match_error = re.search('Error copying.*|TFTP put operation failed.*|sysmgr.*not supported.*\n', output, re.IGNORECASE)
        message = 'Copy Command failed. '
        if match_error:
            logger.error(message)
            message += re.sub('^%|\\n', '', match_error.group())
        else:
            error_match = re.search(r"error.*\n|fail.*\n", output, re.IGNORECASE)
            if error_match:
                logger.error(message)
                message += error_match.group()
        raise Exception('Copy', message)


def install_firmware(config_session, logger, firmware_file_name):
    """Set boot firmware file.

    :param config_session: current config session
    :param logger:  logger
    :param firmware_file_name: firmware file name
    """

    config_session.send_command(**BOOT_SYSTEM_FILE.get_command(firmware_file_name=firmware_file_name))
    # config_session.send_command(**CONFIG_REG.get_command())

def show_boot(session):
    """Retrieve os version

    :param session: current session
    :return:
    """

    return session.send_command(**SHOW_BOOT.get_command())

