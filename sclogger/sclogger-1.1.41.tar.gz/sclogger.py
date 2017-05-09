"""
Simple colorized logger
Current version is 1.1.41
Author: Kit Scribe
Author email: kit.scribe@protonmail.com
Find examples into 'examples/' folder on GitHub
GitHub link source: https://github.com/Kit-Scribe/sclogger
Find pycolorize source on https://github.com/Kit-Scribe/pycolorize
Look for other projects on https://github.com/Kit-Scribe/
"""
from datetime import datetime
from pycolorize import colorize, cprint
from enum import Enum
import re


class MessageType(Enum):
    INFO = 10
    SUCCESS = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


message_color = {
    'INFO': 'gray',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'SUCCESS': 'cyan',
    'CRITICAL': 'magenta'
}


class Logger:
    # ================= #
    # Initialize Logger #
    # ================= #
    def __init__(self, fp, delimiter=' ', protected_mode=False):
        # Setups
        if protected_mode:
            self.__file = open(fp, 'x')
        else:
            self.__file = open(fp, 'w')
        self.__delimiter = delimiter

        # Message types counter
        self.__data = {
            'INFO': 0,
            'WARNING': 0,
            'ERROR': 0,
            'SUCCESS': 0,
            'CRITICAL': 0
        }

        self.__write_head()  # write the template at the first line

    def __write_head(self):
        # ================================================== #
        # Writing the template at the first line of log file #
        # ================================================== #
        template = self.__delimiter.join(['Date', 'Time', 'Message', 'Message type\n'])
        self.__file.write(template)

    def message(self, message, message_type: MessageType, to_print=True, include_microseconds=False):
        # ===================== #
        # Generate message data #
        # ===================== #
        mt = str(message_type).replace('MessageType.', '')
        date = datetime.today().date()
        if not include_microseconds:
            time = datetime.today().time().replace(microsecond=0)
        else:
            time = datetime.today().time()

        # update count of the message type
        self.__data[mt] += 1

        # create message with join
        message = self.__delimiter.join([str(date), str(time), message, mt])

        # writing message with removing colorized lines bytes
        self.__file.write(re.sub(r'(\x1b\[.*?m)', '', message + '\n'))

        # print message if to_print is True
        if to_print:
            cprint(message, message_color[mt])

    def custom_message(self, message):
        # ===================================== #
        # Write a custom, not templated message #
        # ===================================== #
        self.__file.write(message)

    def get_stats(self):
        # ==================== #
        # Print messages count #
        # ==================== #
        info = str(self.__data['INFO'])
        warning = str(self.__data['WARNING'])
        error = str(self.__data['ERROR'])
        success = str(self.__data['SUCCESS'])
        critical = str(self.__data['CRITICAL'])

        cprint('INFO MESSAGES COUNT: {}\n'
               'WARNING MESSAGES COUNT: {}\n'
               'ERROR MESSAGES COUNT: {}\n'
               'CRITICAL MESSAGES COUNT: {}\n'
               'SUCCESS MESSAGES COUNT: {}'.format
               (colorize(info, 'magenta'), colorize(warning, 'magenta'),
                colorize(error, 'magenta'), colorize(critical, 'magenta'),
                colorize(success, 'magenta')), 'green')

    def close(self):
        # close the file if necessary
        self.__file.close()


class LogReader:
    # ==================== #
    # Initialize LogReader #
    # ==================== #
    def __init__(self, fp):
        self.__log = open(fp)

    def read_messages(self, message_type: MessageType = None):
        # ============================== #
        # Read messages with typed color #
        # ============================== #
        if message_type is None:
            for line in self.__log.readlines()[1:]:
                line = line.strip()
                end = ''
                for char in line[::-1]:
                    if not char.isspace():
                        end += char
                    else:
                        end = end[::-1]
                        break
                try:
                    cprint(line.strip(), message_color[end])
                except KeyError:
                    cprint('Key not found. Add it to message_color dict in sclogger module', 'yellow')
                    print(line.strip())
        else:
            end = str(message_type).replace('MessageType.', '')
            for line in self.__log.readlines()[1:]:
                line = line.strip()
                if line.endswith(end):
                    cprint(line.strip(), message_color[end])
