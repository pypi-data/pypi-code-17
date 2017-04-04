import json
from pathlib import Path
import shutil

from webdriver_controller import config
from webdriver_controller.drivers.chromedriver import ChromeDriver
from webdriver_controller.drivers.selenium_standalone import SeleniumStandalone


class WebdriverController(object):
    __installation_folder = Path('{}{}'.format(Path.cwd(),
                                               config.INSTALLATION_FOLDER))
    __installation_file = Path('{}{}/{}'.format(Path.cwd(),
                                                config.INSTALLATION_FOLDER,
                                                config.INSTALLATION_FILE))
    __outdated_file = Path('{}.old'.format(__installation_file))

    def __check_installation_file(self) -> None:
        if self.__installation_file.exists():
            self.__installation_file.rename(self.__outdated_file)

    def __remove_outdated_installation_file(self) -> None:
        if self.__outdated_file.exists():
            self.__outdated_file.unlink()

    def __write_installation_file(self, version_info: dict) -> None:
        with open(self.__installation_file, 'w') as fh:
            json.dump(version_info, fh)

    def download(self):
        if not self.__installation_folder.exists():
            self.__installation_folder.mkdir()

        self.__check_installation_file()

        chromedriver = ChromeDriver()
        chromedriver.download_driver()

        selenium_standalone = SeleniumStandalone()
        selenium_standalone.download_driver()

        version_info = {
            'chrome': chromedriver.version,
            'selenium': selenium_standalone.version
        }

        self.__write_installation_file(version_info)
        self.__remove_outdated_installation_file()

    def cleanup(self):
        if self.__installation_folder.exists():
            print('deleting {} ...'.format(self.__installation_folder))
            shutil.rmtree(self.__installation_folder)
        else:
            print('no Selenium Webdriver installation found')

    def list(self):
        if self.__installation_folder.exists():
            if self.__installation_file.exists():
                version_info = {}
                with open(self.__installation_file, 'r') as fh:
                    version_info = json.load(fh)

                print('ChromeDriver version: {}'.format(version_info.get('chrome')))
                print('Selenium standalone version: {}'.format(version_info.get('selenium')))
            else:
                print('no installation file found')
        else:
            print('no Selenium Webdriver installation found')
