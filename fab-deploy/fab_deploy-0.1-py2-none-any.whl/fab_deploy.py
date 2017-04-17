from fabric.api import cd, lcd, local
from contextlib import contextmanager
from fabric.state import env


class ENV(dict):
    def __init__(self, *args, **kwargs):
        super(ENV, self).__init__(*args, **kwargs)
        self.__dict__ = self
        self.REPO_PATH = None
        self.DOMAIN = None
        self.DJANGO_MAJOR_APP = None
        self.WORK_DIR = None
        self.IP = env.host
        self.USER = env.user

    @property
    def REPO(self):
        return self.REPO_PATH.split('/')[-1].split('.')[0]

    @property
    def PROJECT_PATH(self):
        return "~/%s" % self.REPO_NAME


_env = ENV()


@contextmanager
def just_try(*exceptions):
    try:
        yield
    except exceptions:
        pass


def put(local_path, remote_path, **kwargs):
    from fabric.api import put

    temp_path = '%s' % os.path.basename(local_path)

    with open(temp_path, 'w') as ofile:
        ofile.write(open(local_path).read() % _env)

    return put(temp_path % _env, remote_path % _env, **kwargs)


def run(cmd, *args, **kwargs):
    from fabric.api import run

    return run(cmd % _env, *args, **kwargs)


def sudo(cmd, *args, **kwargs):
    from fabric.api import sudo

    return sudo(cmd % _env, *args, **kwargs)


# SETUP VM
def update_system():
    sudo('apt-get update -y')
    sudo('apt-get install git -y')
    sudo('apt-get install python-pip python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev zlib1g-dev libjpeg-dev libpng-dev -y')
    sudo('apt-get install libmysqlclient-dev -y')
    sudo('apt-get install zsh -y')

    with just_try(Exception):
        run('sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"')

    sudo('apt-get purge -y python-pip')
    run('wget -N https://bootstrap.pypa.io/get-pip.py')
    sudo('python ./get-pip.py')
    sudo('apt-get install python-pip')
    sudo('pip install pdbpp ipython')
    sudo('pip install virtualenv')


# SETUP DATABASE
def setup_mysql():
    sudo('apt-get install mysql-server -y')
    put('./deploy/init.sql', '/home/%(USER)s')
    run('mysql -uroot < /home/%(USER)s/init.sql')
    run('mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -D mysql -u root')
    run('mysql -u root -e "flush tables;" mysql')


# SETUP NGINX SERVER
def setup_server():
    sudo('apt-get install nginx -y')
    sudo('pip install uwsgi')

    sudo("mkdir -p /etc/uwsgi")
    sudo("mkdir -p /etc/uwsgi/vassals")
    sudo("ln -sf /home/%(USER)s/%(REPO)s/mysite_uwsgi.ini /etc/uwsgi/vassals/")

    put('./deploy/mysite_nginx.conf', '/home/%(USER)s/%(REPO)s')
    put('./deploy/uwsgi_params', '/home/%(USER)s/%(REPO)s')
    put('./deploy/mysite_uwsgi.ini', '/home/%(USER)s/%(REPO)s')
    sudo('ln -sf /home/%(USER)s/%(REPO)s/mysite_nginx.conf /etc/nginx/sites-enabled/')
    put('./deploy/rc.local', '/etc/rc.local', use_sudo=True, mode='755')


# RESTART SERVICE
def server_restart():
    sudo('/etc/init.d/nginx stop')
    sudo('/etc/init.d/nginx start')


# STARTUP REPO
def setup_app():
    with just_try(Exception):
        run('git clone %(REPO_PATH)s')

    with cd(env.PROJECT_PATH):
        with just_try(Exception):
            run('virtualenv venv')

        put('./deploy/local.env', '/home/davidchen/%(USER)s/src/%(REPO)s/settings/local.env')


def install_requirements():
    with cd(env.PROJECT_PATH):
        run('venv/bin/pip install -r requirements/local.txt')
        run('venv/bin/pip install -r requirements/production.txt')


def migrate():
    with cd(env.PROJECT_PATH + '/src'):
        run('source ../venv/bin/activate && ../venv/bin/python manage.py migrate')
        run('../venv/bin/python manage.py collectstatic --noinput')


def pull_repo():
    with cd(env.PROJECT_PATH):
        run('git pull')
