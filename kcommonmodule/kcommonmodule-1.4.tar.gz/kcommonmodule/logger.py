#!/usr/bin/env python
# coding=utf-8
import logging
import logging.handlers
import os

# 默认日志路径在/var/log/%(project_name)/%(project_name).log
BASE_LOG = '/var/log/'


class KLog(object):
    def __init__(self, project_name, logfile=None):
        # 保存 project name
        self._project_name = project_name

        # 设定 formatter
        formatter = logging.Formatter(project_name + ' %(name)s | %(asctime)s | %(filename)s:%(lineno)s | %(message)s')
        self._formatter = formatter

        # 创建 console 的 logger
        console_logger = logging.getLogger()
        console_logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        console_handler.setFormatter(formatter)
        console_logger.addHandler(console_handler)
        self.console = console_logger

        # 创建 file 的 logger
        file_logger = logging.getLogger('important')
        file_logger.setLevel(logging.WARNING)
        if logfile is None:
            logfile = os.path.join(BASE_LOG, project_name, project_name + '.log')
        file_handler = logging.FileHandler(logfile)
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(formatter)
        file_logger.addHandler(file_handler)
        self.file_logger = file_logger


    def setEmail(self, email_host, user, passwd, fromaddr, toaddr, subject=None, debug_mode=True):
        if subject is None:
            subject = 'error or critical occured, you must pay attendtion to it'
        email_handler = logging.handlers.SMTPHandler(email_host, fromaddr, toaddr, subject, (user, passwd), secure=())
        email_handler.setLevel(logging.ERROR)
        email_handler.setFormatter(self._formatter)

        email_logger = logging.getLogger('email')
        email_logger.setLevel(logging.ERROR)
        email_logger.addHandler(email_handler)
        self.email_logger = email_logger
        self._debug_mode = debug_mode

    def sendemail(self, msg):
        if not self._debug_mode:
            self.email_logger.error(msg)
        else:
            self.file.error(msg)

if __name__ == '__main__':
    MODULE = 'KLog'
    logger = KLog(MODULE)
    logger.console.debug('hello %s' % 'zhaodl')
    logger.console.info('this is info msg %s' % 'zhaodl')
    logger.console.warning('this is warning msg %s' % 'zhaodl')
    logger.console.error('this is error msg %s' % 'zhaodl')
    logger.console.critical('this is critical msg %s' % 'zhaodl')
    logger.file_logger.critical('this is critical msg %s' % 'zhaodl')

    logger.setEmail('smtp.qq.com', '554028116@qq.com', '', '554028116@qq.com', 'zhaodl@knownsec.com', None, False)
    logger.sendemail('this is email notify %s' % 'zhaodl')
