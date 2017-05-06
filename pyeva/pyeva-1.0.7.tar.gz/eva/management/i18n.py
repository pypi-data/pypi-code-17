# coding: utf-8
#
# 更新所有的 locale
#

import os
import glob

from eva.conf import settings
from eva.utils.findapps import update_apps_locale
from eva.utils.cmd import find_files, run_cmd
from eva.utils.translation.generate import update_locales


def update_translation():

    update_apps_locale()
    update_site_locales()


def update_site_locales():

    root_path = settings.PROJECT_ROOT

    backdir = os.getcwd()
    os.chdir(root_path)

    files = []
    for item in settings.SITE_TRANSLATION_FILES:
        for p in glob.glob(item):
            if os.path.isdir(p):
                files.extend( find_files(p, ['py', 'html']) )
            else:
                files.append( p )

    cmd = 'xgettext --from-code=UTF-8 -L python -k=_ ' + \
          ' --package-name={0}'.format(settings.PACKAGE_NAME) + \
          ' --package-version={0}'.format(settings.PACKAGE_VERSION) + \
          ' -o eva.po ' + ' '.join(files)

    run_cmd(cmd)

    # 测试文件是否正确生成
    if not os.path.exists('eva.po'):
        logging.debug('pass {0}'.format(root_path))
        return

    # 更新 locale 目录中所有语言的 po, mo 文件
    update_locales('eva.po', root_path)

    # 删除 eva.po
    os.unlink('eva.po')
    os.chdir(backdir)
