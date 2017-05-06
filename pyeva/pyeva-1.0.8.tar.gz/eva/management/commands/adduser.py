# coding: utf-8
#
# 用户操作：创建/删除/查询
#
# 依赖 app.auth

import logging
import argparse

from eva.conf import settings
from eva.orm import get_db_session
from eva.management.common import EvaManagementCommand

from eva.utils.backend import load_auth_backend
backend_auth = load_auth_backend()


def adduser(username, password, email, is_superuser=False):

    db = get_db_session()
    user = backend_auth.models.create_user(
                       db,
                       username=username,
                       password=password,
                       email=email)
    if user:
        if username == 'admin' or is_superuser:
            user.is_superuser = True
            db.commit()
        logging.debug('Create user "{0}" success.'.format(username))
    else:
        logging.error('Create user {0} failed'.format(username))

    db.remove()


class Command(EvaManagementCommand):

    def __init__(self):
        super(Command, self).__init__()

        self.cmd = 'adduser'
        self.help = '创建新用户'

    def add_arguments(self, parser):
        parser.add_argument('--username', help='用户名')
        parser.add_argument('--password', help='密码')
        parser.add_argument('--email', help='邮箱')
        parser.add_argument('--is_superuser', action='store_true',
                            help='是否为管理员')

    def run(self):
        args = self.args
        adduser(args.username, args.password, args.email, args.is_superuser)
