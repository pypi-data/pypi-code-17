# Copyright 2017 Interana, Inc.
from base import CommandHandler, SubCommandHandler


class DataHandler(CommandHandler):

    name = 'data'
    description = 'Commands for managing string and table data'

    def __init__(self):
        CommandHandler.__init__(self)


class DataList(SubCommandHandler):

    name = 'list'
    description = 'List data files on disk'

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        return parser


class DataDelete(SubCommandHandler):

    name = 'delete'
    description = 'Delete data for a table'

    def parser_setup(self, sps):
        parser = self.init_parser(sps)
        return parser
