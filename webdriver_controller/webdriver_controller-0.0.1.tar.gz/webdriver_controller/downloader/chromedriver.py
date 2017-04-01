import os
import subprocess

import requests

from webdriver_controller import config
from webdriver_controller.downloader import downloader
from webdriver_controller.tools import tools


def download():
    host = config.STORAGE_URLS.get('chromedriver')
    latest_rel_doc_url = '{}LATEST_RELEASE'.format(host)
    platform = tools.get_platform()

    resp = requests.get(latest_rel_doc_url)
    latest_verison = resp.text.strip()

    filename = 'chromedriver_{}.zip'.format(platform)
    download_url = '{}{}/{}'.format(host, latest_verison, filename)

    folder = '{}{}'.format(os.getcwd(), config.LOCAL_FOLDER)
    dest = '{}/{}'.format(folder, filename)

    downloader.download_driver(download_url, dest)

    # unzip the driver
    subprocess.run(['unzip', '-oq', dest, '-d', folder])
