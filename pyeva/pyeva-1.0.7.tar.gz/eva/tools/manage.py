#! /usr/bin/env python
# coding: UTF-8 

# 加载 Python 内置库
import os
import sys

# 加载开发路径
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'project'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'vendor'))


def main():
    if len(sys.argv) < 2:
        print('Usage: {0} opt'.format(sys.argv[0]))
        print('''
    syncdb
    dropdb
    adduser
    reset_password
    create_app
''')
        sys.exit(1)

    # 用户配置文件模块路径
    os.environ.setdefault("EVA_SETTINGS_MODULE", "settings")

    import tornado.options

    tornado.options.options.logging = "debug"
    tornado.options.parse_command_line()

    opt = sys.argv[1]

    if opt == 'syncdb':  # 注意：这里的同步只更新新建的表
        import eva.management.db

        eva.management.db.syncdb()

    elif opt == 'dropdb':
        # print("!!! disabled !!!")
        """
        python3 manage.py dropdb
        python3 manage.py syncdb
        """
        import eva.management.db
        eva.management.db.dropdb()

    elif opt == 'adduser':
        if len(sys.argv) != 5:
            print('Usage: {0} adduser username password email'.format(sys.argv[0]))
            sys.exit(1)
        else:
            username = sys.argv[2]
            password = sys.argv[3]
            email = sys.argv[4]
            import eva.management.user

            eva.management.user.adduser(username, password, email)

    elif opt == "reset_password":
        if len(sys.argv) != 3:
            print('Usage: {0} reset_password username'.format(sys.argv[0]))
            sys.exit(1)
        else:
            username = sys.argv[2]
            import eva.management.user

            eva.management.user.reset_password(username)

    else:
        print('unknown opt: {0}'.format(opt))


if __name__ == '__main__':
    main()
