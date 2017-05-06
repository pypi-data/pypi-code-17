import os
import sys
import argparse


def apply_common_options(args):

    # 用户配置文件模块路径
    if args.settings.endswith('.py'):
        args.settings = args.settings[:-3]

    os.environ.setdefault("EVA_SETTINGS_MODULE", args.settings)

    import tornado.options
    tornado.options.options.logging = "debug" if args.debug else 'info'
    tornado.options.parse_command_line()


class EvaManagementCommand(object):

    def __init__(self):
        self.cmd = None
        self.help = None
        self.args = None

    @property
    def is_development(self):
        '''是否为开发/测试环境！
        '''
        # TODO: 更严格的检测！
        return (
            (self.args.settings.find('test') >= 0) or
            (self.args.settings.find('dev') >= 0)
        )

    def get_argument_parser(self):
        parser = argparse.ArgumentParser(prog=self.cmd)
        return parser

    def add_arguments(self, parser):
        pass

    def parse_argv(self, argv):
        parser = self.get_argument_parser()

        # 增加通用选项
        parser.add_argument('--settings', default='settings',
                            help='指定配置文件')
        parser.add_argument('-d', dest='debug', action='store_true',
                            help='show debug')
        parser.add_argument('--db-echo', action='store_true',
                            help='显示 SQLAlchemy 数据库操作详细过程')
        parser.add_argument('--ignore-env-check', action='store_true',
                            help='忽略开发/测试环境检查')

        self.add_arguments(parser)
        self.args = parser.parse_args(argv)

    def __call__(self, argv):
        self.parse_argv(argv)

        # 应用通用配置
        apply_common_options(self.args)

        self.run()
