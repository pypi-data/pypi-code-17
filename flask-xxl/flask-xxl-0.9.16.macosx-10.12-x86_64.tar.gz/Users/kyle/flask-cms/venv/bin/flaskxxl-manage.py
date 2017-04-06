#!/Users/kyle/flask-cms/venv/bin/python
# EASY-INSTALL-ENTRY-SCRIPT: 'flask-xxl==0.9.16','console_scripts','flaskxxl-manage.py'
__requires__ = 'flask-xxl==0.9.16'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('flask-xxl==0.9.16', 'console_scripts', 'flaskxxl-manage.py')()
    )
