import os
import shutil

from webdriver_controller import config
from webdriver_controller.downloader import chromedriver
from webdriver_controller.downloader import selenium_standalone


class WebdriverController(object):
    _local_driver_folder = '{}{}'.format(os.getcwd(), config.LOCAL_FOLDER)

    def __init__(self):
        pass

    def download(self):
        if not os.path.exists(self._local_driver_folder):
            os.makedirs(self._local_driver_folder)

        chromedriver.download()
        selenium_standalone.download()

    def cleanup(self):
        if os.path.exists(self._local_driver_folder):
            print('deleting {} ...'.format(self._local_driver_folder))
            shutil.rmtree(self._local_driver_folder)
        else:
            print('no Selenium Webdriver installation found')
