import os

import requests
import xmltodict

from webdriver_controller import config
from webdriver_controller.downloader import downloader


def download():
    resp = requests.get(config.STORAGE_URLS.get('selenium'))
    doc = xmltodict.parse(resp.content)
    items = doc.get('ListBucketResult').get('Contents')

    for item in reversed(items):
        if 'standalone' in item.get('Key') and 'beta' not in item.get('Key'):
            selenium_key = item.get('Key').strip()

            break

    download_url = '{}{}'.format(config.STORAGE_URLS.get('selenium'), selenium_key)
    filename = selenium_key.split('/')[1]
    folder = '{}{}'.format(os.getcwd(), config.LOCAL_FOLDER)
    dest = '{}/{}'.format(folder, filename)

    downloader.download_driver(download_url, dest)
