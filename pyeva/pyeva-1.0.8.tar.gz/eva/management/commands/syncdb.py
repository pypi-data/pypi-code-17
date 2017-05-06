from eva.management.common import EvaManagementCommand
from eva.management.db import load_models
from eva.orm import create_all


class Command(EvaManagementCommand):

    def __init__(self):
        super(Command, self).__init__()

        self.cmd = 'syncdb'
        self.help = '同步数据库(如果表不存在，则创建之)'

    def run(self):
        load_models()
        create_all(self.args.db_echo)
