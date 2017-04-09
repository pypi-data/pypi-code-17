import sys
import click
from typing import Tuple
import mechanize
import requests

__version__ = '0.1.2'


class JobCan(object):

    URL = 'https://ssl.jobcan.jp/login/pc-employee/?client_id={}'
    EVENT_WORK_START = 'work_start'
    EVENT_WORK_END = 'work_end'

    def __init__(self, email, password, group_id, client_id):
        # type: (str, str, int, str) -> None
        self.email = email
        self.password = password
        self.group_id = group_id
        self.client_id = client_id

    def __get_url(self):
        return JobCan.URL.format(self.client_id)

    def __open(self):
        # type: () -> Tuple[str, str, mechanize.Browser]
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.open(self.__get_url())
        assert br.viewing_html()

        # Login
        br.select_form('form')
        br['email'] = self.email
        br['password'] = self.password
        br.submit()

        # Get token
        token = br.forms()[0]['token']  # type: str
        post_url = '{}/index/adit'.format(br.geturl())
        return token, post_url, br

    def work_start(self):
        token, post_url, br = self.__open()
        resp = requests.post(
            post_url,
            data={
                "token": token,
                "is_yakin": 0,
                "adit_item": JobCan.EVENT_WORK_START,
                "adit_group_id": self.group_id,
                "notice": ""
            },
            cookies=br.cookiejar
        )
        if resp.status_code != 200:
            raise RuntimeError('Failed to work_start')

    def work_end(self):
        token, post_url, br = self.__open()
        resp = requests.post(
            post_url,
            data={
                "token": token,
                "is_yakin": 0,
                "adit_item": JobCan.EVENT_WORK_END,
                "adit_group_id": self.group_id,
                "notice": ""
            },
            cookies=br.cookiejar
        )
        if resp.status_code != 200:
            raise RuntimeError('Failed to work_start')


@click.command()
@click.option('--command', '-c', type=click.STRING, default="start", required=False)
@click.option('--email', '-e', type=click.STRING, required=False)
@click.option('--password', '-p', type=click.STRING, required=False)
@click.option('--gid', '-g', type=click.INT, required=False)
@click.option('--cid', '-c', type=click.STRING, required=False)
@click.option('--version', "-v", is_flag=True, required=False)
def main(command, email, password, gid, cid, version):
    # type: (str, str, str, int, str, bool) -> None
    if version:
        sys.stdout.write('{}\n'.format(__version__))
        exit(0)

    job = JobCan(email, password, gid, cid)
    if command == "start":
        job.work_start()
        sys.stdout.write('Success to start working as {}\n'.format(email))
        exit(0)

    elif command == 'end':
        job.work_end()
        sys.stdout.write('Success to end working as {}\n'.format(email))
        exit(0)

    else:
        raise ValueError('Invalid option. option must be "start" or "end".')


if __name__ == "__main__":
    main()
