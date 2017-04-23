from __future__ import print_function
import time
from datetime import datetime, timedelta
import getpass
import click
from .client import Client, config
import web

# initialized in cli
client = None

@click.group()
def cli():
    """rorocloud is the command-line interface to the rorocloud service.
    """
    global client
    client = Client()


@cli.command()
def login():
    """Log into rorocloud service.
    """
    email = input("E-mail: ")
    pw = getpass.getpass("Password: ")
    client.login(email, pw)


@cli.command()
def whoami():
    """prints the details of current user.
    """
    user = client.whoami()
    print(user['email'])


@cli.command(context_settings={"allow_interspersed_args": False})
@click.argument("command", nargs=-1)
@click.option("--shell/--no-shell", default=False, help="execute the given command using shell")
@click.option("--foreground", default=False, is_flag=True)
def run(command, shell=None, foreground=False):
    """Runs a command in the cloud.

    Typical usage:

        rorocloud run python myscript.py
    """
    job = client.run(command, shell=shell)
    print("-- created new job", job.id)
    if foreground:
        _logs(job.id, follow=True)

@cli.command()
def status():
    """Shows the status of recent jobs.
    """
    print("{:10s} {:17s} {:15s} {:>8s} {:20s}".format("JOB ID", "STATUS", "WHEN", "TIME", "CMD"))
    for job in client.jobs():
        start = _parse_time(job.start_time)
        end = _parse_time(job.end_time)
        total_time = (end - start)
        total_time = timedelta(total_time.days, total_time.seconds)
        line = "{id:10s} {status:17s} {when:15s} {time:>8s} {command:20s}".format(
            id=job.id, command=job.command, status=job.status,
            when=web.datestr(start), time=str(total_time)
        )
        print(line)

def _parse_time(timestr):
    if not timestr:
        return datetime.utcnow()
    return datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S.%f")

@cli.command()
@click.option("-f", "--follow", default=False, is_flag=True)
@click.option("-t", "--show-timestamp", default=False, is_flag=True)
@click.argument("job_id")
def logs(job_id, follow=False, show_timestamp=False):
    _logs(job_id, follow=follow, show_timestamp=show_timestamp)

def _display_logs(logs, show_timestamp=False):
    def parse_time(timestamp):
        t = datetime.fromtimestamp(timestamp//1000)
        return t.isoformat()

    if show_timestamp:
        log_pattern = "[{timestamp}] {message}"
    else:
        log_pattern = "{message}"

    for line in logs:
        line['timestamp'] = parse_time(line['timestamp'])
        print(log_pattern.format(**line))


def _logs(job_id, follow=False, show_timestamp=False):
    """Shows the logs of job_id.
    """
    if follow:
        seen = 0
        while True:
            response = client.get_logs(job_id)
            logs = response.get('logs', [])
            _display_logs(logs[seen:], show_timestamp=show_timestamp)
            seen = len(logs)
            job = client.get_job(job_id)
            if job.status == 'command exited':
                break
            time.sleep(0.5)
    else:
        response = client.get_logs(job_id)
        if response.get('message', None):
            print(response['message'])
        else:
            _display_logs(response.get('logs'), show_timestamp=show_timestamp)

@cli.command()
@click.argument("job_id")
def stop(job_id):
    """Stops a job.
    """
    client.stop_job(job_id)


def main():
    cli()

def main_dev():
    config["ROROCLOUD_URL"] = "https://rorocloud.staging.rorodata.com/"
    cli()
