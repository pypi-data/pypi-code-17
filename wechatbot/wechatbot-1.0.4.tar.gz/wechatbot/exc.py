# -*- coding:utf-8 -*-
from enum import Enum


class BotErrorCode(Enum):

    MISSING_PARAMETER = 0
    UNKNOWN_COMMAND = 1
    RESERVED_COMMAND = 2
    DUPLICATED_COMMAND = 3
    SEND_MSG_ERROR = 4
    LOGIN_ERROR = 5
    GET_UUID_ERROR = 6
    SYNC_ERROR = 7
    SYNC_CHECK_ERROR = 8
    SYNC_HOST_CHECK_ERROR = 9
    BOT_INIT_ERROR = 10


TRANSLATIONS = {
    BotErrorCode.MISSING_PARAMETER: u'you may omit some parameters',
    BotErrorCode.UNKNOWN_COMMAND: u'sorry, i can not understand.',
    BotErrorCode.RESERVED_COMMAND: u'sorry, this command is a reserved keyword.',
    BotErrorCode.DUPLICATED_COMMAND: u'duplicate commands.',
    BotErrorCode.SEND_MSG_ERROR: u'failed to send msg',
    BotErrorCode.LOGIN_ERROR: u'failed to login',
    BotErrorCode.GET_UUID_ERROR: u'failed to get uuid',
    BotErrorCode.SYNC_CHECK_ERROR: u'failed to sync check',
    BotErrorCode.SYNC_HOST_CHECK_ERROR: u'failed to sync host check',
    BotErrorCode.BOT_INIT_ERROR: u'failed to init bot',
    BotErrorCode.SYNC_ERROR: u'failed to sync'
}


class BotException(Exception):

    def __init__(self, err_code, err_msg=None):
        self.err_code = err_code
        self.err_msg = err_msg

    def __str__(self):
        return repr(self.err_msg if self.err_msg else
                    TRANSLATIONS[self.err_code])


class BotUserExceptioin(BotException):
    pass


class BotSystemException(BotException):
    pass


class BotServerException(BotException):
    pass
