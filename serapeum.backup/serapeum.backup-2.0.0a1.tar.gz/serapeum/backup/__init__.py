from serapeum.backup.modules.config.arguments import Arguments

from serapeum.backup.modules.config import Config
from serapeum.backup.modules.log import logger

config = Config(Arguments().config_file)

from serapeum.backup.modules.ds.stack import Stack
from serapeum.backup.modules.files import Files
from serapeum.backup.modules.mysql import MySQLBackup
from serapeum.backup.modules.mail import Mail
from serapeum.backup.modules.remotes import Remotes


def job_queue(app_config):
    jobs = Stack()
    if app_config.config['BACKUP'].get('remote_host'):
        jobs.add(Files(
            backend=app_config.config['BACKUP'].get('backend'),
            host=app_config.config['BACKUP'].get('remote_host')
        ))
    elif app_config.config['BACKUP'].get('remote_host_list'):
        for remote in Remotes(app_config.config['BACKUP'].get('remote_host_list')).remotes:
            jobs.add(Files(
                backend=app_config.config['BACKUP'].get('backend'),
                host=remote
            ))
    if app_config.config['MYSQL'].getboolean('backup_mysql') is True:
        if app_config.config['MYSQL'].get('remote_loc'):
            jobs.add(
                MySQLBackup(local_path=app_config.config['MYSQL']['local_path'], server_host=config.config['MYSQL']['host'],
                            server_user=app_config.config['MYSQL']['username'],
                            server_password=app_config.config['MYSQL']['password'],
                            backup_destination_path=app_config.config['MYSQL']['backup_path'],
                            backup_remote_host=app_config.config['MYSQL']['remote_loc'],
                            backup_remote_user=app_config.config['MYSQL']['remote_user'],
                            backup_ssh=app_config.config['MYSQL']['remote_ssh']))
        elif app_config.config['MYSQL'].get('remote_list'):
            for remote in Remotes(app_config.config['MYSQL'].get('remote_list')).remotes:
                if app_config.config['BACKUP']['remote_role'] == 'source':
                    destination_path = '{0}/{1}'.format(app_config.config['MYSQL']['backup_path'], remote)
                    jobs.add(
                        MySQLBackup(local_path=app_config.config['MYSQL']['local_path'],
                                    server_host=app_config.config['MYSQL']['host'],
                                    server_user=app_config.config['MYSQL']['username'],
                                    server_password=app_config.config['MYSQL']['password'],
                                    backup_destination_path=destination_path,
                                    backup_remote_host=remote,
                                    backup_remote_user=app_config.config['MYSQL']['remote_user'],
                                    backup_ssh=app_config.config['MYSQL']['remote_ssh']))
                elif app_config.config['BACKUP']['remote_role'] == 'backup':
                    jobs.add(
                        MySQLBackup(local_path=app_config.config['MYSQL']['local_path'],
                                    server_host=app_config.config['MYSQL']['host'],
                                    server_user=app_config.config['MYSQL']['username'],
                                    server_password=app_config.config['MYSQL']['password'],
                                    backup_destination_path=app_config.config['MYSQL']['backup_path'],
                                    backup_remote_host=remote,
                                    backup_remote_user=app_config.config['MYSQL']['remote_user'],
                                    backup_ssh=app_config.config['MYSQL']['remote_ssh']))
    return jobs


def main():
    jobs = job_queue(config)
    failures = False
    while True:
        job = jobs.pop()
        if job is None:
            break
        try:
            job.run()
        except Exception as e:
            m = Mail(server=config.config['MAIL']['smtp_server'], port=config.config['MAIL']['smtp_port'],
                     username=config.config['MAIL']['smtp_username'], password=config.config['MAIL']['smtp_password'])
            m.send(sender=config.config['MAIL']['smtp_username'], recipient=config.config['MAIL']['mail_dest'],
                   msg_text="{0}\n{1}".format(job.cmd_output, e), subject='The backup job for {0} ({1}) failed.'
                   .format(job.remote, str(job)))
            logger.exception(job.cmd_output)
            failures = True
    if failures is True:
        return False
    return True
