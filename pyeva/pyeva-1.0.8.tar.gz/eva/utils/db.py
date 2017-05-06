# coding: utf-8

import os
from eva.conf import settings
from eva.exceptions import WebDBError


def get_db_uri():

    '''获取数据库访问接口

    http://docs.sqlalchemy.org/en/latest/core/engines.html
    '''

    DB = settings.DB
    engine = DB.get('engine')    

    if engine == 'sqlite':
        path = DB.get('path')
        if not path:
            path = 'data.db'

        if not os.path.isabs(path):
            path = os.path.join(
                settings.PROJECT_ROOT, path)

        DB['path'] = path
        DB_URI = '{engine}:///{path}'

    else:
        DB_URI = '{engine}://{username}:{password}' + \
                 '@{host}/{database}'


    return DB_URI.format(**settings.DB)
