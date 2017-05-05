import os
import json
import click
import arrow
from jira import JIRA


def format_time(time_string):
    time = arrow.get(time_string)
    return time.format('YYYY-MM-DD HH:mm:ss ZZ')


def get_timedelta(begin, end):
    arrow_begin = arrow.get(begin)
    arrow_end = arrow.get(end)

    return arrow_end - arrow_begin


def create_jira():
    config = get_config()

    if set(['server', 'user', 'password']).issubset(set(config)):
        server = config['server']
        user = config['user']
        password = config['password']
    else:
        server = click.prompt('JIRA server address')
        user = click.prompt('User')
        password = click.prompt('Password', hide_input=True)

        if click.confirm('Do you want to save?'):
            config = get_config()
            config.update({
                'server': server,
                'user': user,
                'password': password
            })
            set_config(config)

    options = {'server': server}
    jira = JIRA(options, basic_auth=(user, password))

    return jira


def get_config():
    config_file_path = os.path.expanduser('~/.cliraconfig')
    if os.path.isfile(config_file_path):
        with open(config_file_path, 'r') as f:
            config_json = f.read()
            config = json.loads(config_json)

        return config

    return {}


def set_config(config):
    config_file_path = os.path.expanduser('~/.cliraconfig')
    with open(config_file_path, 'w') as f:
        config_json = json.dumps(config)
        f.write(config_json)
