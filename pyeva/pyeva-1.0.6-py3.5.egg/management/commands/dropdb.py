import sys

from eva.management.common import EvaManagementCommand
from eva.management.db import load_models
from eva.orm import drop_all


class Command(EvaManagementCommand):

    def __init__(self):
        super(Command, self).__init__()

        self.cmd = 'dropdb'
        self.help = '清空数据库'

    def run(self):

        if not self.args.ignore_env_check:
            if not self.is_development:
                print('dropdb 只能在开发/测试环境中使用!')
                sys.exit(1)

        load_models()
        drop_all(self.args.db_echo)
