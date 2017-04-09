# -*- coding: utf-8 -*-
"""
    pip_services_logging.logic.LoggingCommandSet
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Logging command set implementation
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.data import FilterParams, PagingParams
from pip_services_commons.commands import Command, CommandSet

from ..data.version1.LogMessageV1 import LogMessageV1
from .ILoggingBusinessLogic import ILoggingBusinessLogic

class LoggingCommandSet(CommandSet):
    _controller = None

    def __init__(self, controller):
        super(LoggingCommandSet, self).__init__()

        self._controller = controller

        self.add_command(self.make_read_messages_command())
        self.add_command(self.make_read_errors_command())
        self.add_command(self.make_write_message_command())
        self.add_command(self.make_write_messages_command())
        self.add_command(self.make_clear_command())


    def make_read_messages_command(self):
        def handler(correlation_id, args):
            filter = FilterParams.from_value(args.get("filter"))
            paging = PagingParams.from_value(args.get("paging"))
            return self._controller.read_messages(correlation_id, filter, paging)

        return Command(
            "read_messages",
            None,
            handler
        )

    def make_read_errors_command(self):
        def handler(correlation_id, args):
            filter = FilterParams.from_value(args.get("filter"))
            paging = PagingParams.from_value(args.get("paging"))
            return self._controller.read_errors(correlation_id, filter, paging)

        return Command(
            "read_errors",
            None,
            handler
        )

    def make_write_message_command(self):
        def handler(correlation_id, args):
            message = LogMessageV1.from_json(args.get("message"))
            return self._controller.write_message(correlation_id, message)

        return Command(
            "write_message",
            None,
            handler
        )

    def make_write_messages_command(self):
        def handler(correlation_id, args):
            items = args.get("messages")
            messages = []
            for item in items:
                message = LogMessageV1.from_json(item)
                messages.append(message)
            return self._controller.write_messages(correlation_id, messages)

        return Command(
            "write_messages",
            None,
            handler
        )

    def make_clear_command(self):
        def handler(correlation_id, args):
            return self._controller.clear(correlation_id)

        return Command(
            "clear",
            None,
            handler
        )
