#! /usr/bin/env python
# coding: utf-8

import os
import logging
from logging.handlers import TimedRotatingFileHandler
from JYAliYun import DATETIME_FORMAT, LOG_MSG_FORMAT, DEFAULT_LOGGER_NAME
from JYAliYun.Tools import ConfigManager, ConvertObject
from JYAliYun.AliYunAccount import RAMAccount

__author__ = 'ZhouHeng'


# logging.basicConfig(level=logging.DEBUG, format=LOG_MSG_FORMAT, datefmt=DATETIME_FORMAT)


class ObjectManager(object):
    def __init__(self, *args, **kwargs):
        self.cfg = ConfigManager(**kwargs)
        self.server_url = None
        self.access_key_id = ""
        self.access_key_secret = ""
        self.is_internal = False
        self.ram_account = None
        if "ram_account" in kwargs:
            ram_account = kwargs["ram_account"]
            assert isinstance(ram_account, RAMAccount)
            self.ram_account = ram_account
        if len(args) > 0:
            ram_account = args[0]
            if isinstance(ram_account, RAMAccount):
                self.ram_account = ram_account
        if self.ram_account is not None:
            self.ram_account.assign_account_info(self)

        self.env = self.cfg.get("env", "")
        self.logger_name = DEFAULT_LOGGER_NAME
        if "logger_name" in kwargs:
            self.logger_name = kwargs["logger_name"]
        self.logger = logging.getLogger(self.logger_name)
        self.init_logging()

    def init_logging(self):
        logging_dir = self.cfg.get("logging_dir", "")
        logging_name = self.cfg.get("logging_name", self.logger_name.lower())
        filename = os.path.join(logging_dir, logging_name)
        try:
            fmt = logging.Formatter(LOG_MSG_FORMAT, DATETIME_FORMAT)
            log = TimedRotatingFileHandler(filename=filename, when='W0', interval=4)
            log.setLevel(logging.INFO)
            log.suffix = "%Y%m%d_%H%M.log"
            log.setFormatter(fmt)
            self.logger.addHandler(log)
        except Exception as e:
            self.logger.error(e.message)

    def set_server_url(self, server_url):
        self.server_url = server_url

    def set_access_key_id(self, access_key_id):
        self.access_key_id = access_key_id

    def set_access_key_secret(self, access_key_secret):
        self.access_key_secret = access_key_secret

    def set_is_internal(self, is_internal):
        self.is_internal = is_internal

    def set_env(self, env):
        self.env = env

    @staticmethod
    def _handler_log_msg(message, *args):
        message = ConvertObject.decode(message)
        if len(args) >= 0:
            for item in args:
                message += "\n" + ConvertObject.decode(item)
        return message

    def error_info(self, message, *args):
        message = self._handler_log_msg(message, *args)
        self.logger.error(message)

    def waring_log(self, message, *args):
        message = self._handler_log_msg(message, *args)
        self.logger.warning(message)

    def info_log(self, message, *args):
        message = self._handler_log_msg(message, *args)
        self.logger.info(message)
