import requests
import settings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui as webDriverUi
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException


class SeleniumVisitor(object):
    DRIVER_WAIT_FOR_ELEMENT_TIMEOUT = 120
    DRIVER_PAGELOAD_TIMEOUT = 120

    USE_PHANTOM_JS = settings.PHANTOMJS_IN_USE


    def __init__(self, proxy=None, proxy_type=None, user_agent=None,
            width=1024, height=728):

        if proxy and '://' in proxy:
            self._proxy_type, self._proxy = proxy.split('://', 2)
        else:
            self._proxy = proxy
            self._proxy_type = proxy_type or '[http|ssl|ftp]'

        self._user_agent = user_agent
        self._width, self._height = width, height
        self._driver = None
        self._after_get_force = None


    # --- waiting functions ----------------------------------------------------

    def wait_multi(self, search_params):
        def wait(driver):
            for sp in search_params:
                try:
                    element = driver.find_element(sp[0], sp[1])
                    if element:
                        return element
                except:
                    pass

            return False

        return webDriverUi.WebDriverWait(
            self._driver, self.DRIVER_WAIT_FOR_ELEMENT_TIMEOUT).until(wait)


    def wait(self, by, value):
        return self.wait_multi([[by, value]])


    def wait_by_id(self, value):
        return self.wait_multi([[By.ID, value]])


    def wait_by_class_name(self, value):
        return self.wait_multi([[By.CLASS_NAME, value]])


    def wait_by_css_selector(self, value):
        return self.wait_multi([[By.CSS_SELECTOR, value]])


    def wait_by_xpath(self, value):
        return self.wait_multi([[By.XPATH, value]])


    # --- element functions ----------------------------------------------------

    def set_element_value(self, element, value):
        if element.tag_name.lower() == 'select':
            select_wrapper = webDriverUi.Select(element)
            select_wrapper.select_by_value(value)
            return
        element.clear()
        element.send_keys(value)


    def get_selected_option(self, element):
        select_wrapper = webDriverUi.Select(element)
        return select_wrapper.first_selected_option


    # --- driver object functions ----------------------------------------------

    def get_driver(self):
        if not self._driver:
            return self._get_new_driver()
        return self._driver


    @property
    def driver(self):
        return self.get_driver()


    def _get_new_driver(self, proxy=None, proxy_type=None, user_agent=None):
        if self._driver:
            self.close_driver()

        if not proxy: proxy = self._proxy
        if not proxy_type: proxy_type = self._proxy_type
        if not user_agent: user_agent = self._user_agent

        if self.USE_PHANTOM_JS:
            service_args = ["--ssl-protocol=any", "--load-images=no"]
            if proxy:
                service_args += ['--proxy={}'.format(proxy),
                                 '--proxy-type={}'.format(proxy_type)]
            if user_agent:
                dcap = dict(DesiredCapabilities.PHANTOMJS)
                dcap["phantomjs.page.settings.userAgent"] = user_agent
            else:
                dcap = DesiredCapabilities.PHANTOMJS
            
            kwargs = {
                'service_args': service_args,
                'desired_capabilities': dcap,
            }
            if settings.PHANTOMJS_SERVICE_LOG_PATH:
                kwargs['service_log_path'] = settings.PHANTOMJS_SERVICE_LOG_PATH
            if settings.PHANTOMJS_EXECUTABLE_PATH:
                kwargs['executable_path'] = settings.PHANTOMJS_EXECUTABLE_PATH
            self._driver = webdriver.PhantomJS(**kwargs)
        else:
            chrome_options = webdriver.ChromeOptions()
            if proxy:
                chrome_options.add_argument(
                    '---proxy-server={}://{}'.format(proxy_type, proxy))
            if user_agent:
                chrome_options.add_argument(
                    '--user-agent={}'.format(user_agent))
            args = []
            kwargs = {
                'chrome_options': chrome_options
            }
            if settings.CHROMEDRIVER_EXECUTABLE_PATH:
                args.append(settings.CHROMEDRIVER_EXECUTABLE_PATH)
            self._driver = webdriver.Chrome(*args, **kwargs)

        self._driver.set_window_size(self._width, self._height)
        self._driver.set_page_load_timeout(self.DRIVER_PAGELOAD_TIMEOUT)
        return self._driver


    def quit(self):
        if self._driver:
            self._driver.quit()
        self._driver = None


    # --- get URL functions ----------------------------------------------------

    def get(self, url):
        self.get_driver().get(url)


    def get_fast(self, url, timeout=4):
        self._driver.set_page_load_timeout(timeout)
        try:
            self.get_driver().get(url)
        except TimeoutException:
            pass

        self._driver.set_page_load_timeout(self.DRIVER_PAGELOAD_TIMEOUT)


    def set_after_get_force(self, func):
        self._after_get_force = func


    def get_force(self, url, do_after_get=False):
        try:
            self.get_driver().get(url)
            if do_after_get and self._after_get_force:
                self._after_get_force()
        except Exception as e:
            print("Failed to get the page: %s" % str(e))
            print("Restarting driver...")
            self._get_new_driver()
            return self.driver_get_force(url, True)


    # --- other ----------------------------------------------------------------

    def save_screenshot(self, *args, **kwargs):
        self.get_driver().save_screenshot(*args, **kwargs)


    def set_window_size(self, width, height):
        self._width, self._height = width, height
        if self._driver:
            self._driver.set_window_size(self._width, self._height)


    def inject_cookies_into_requests_session(self, session):
        if not self._driver:
            return session

        cookie_map = (('name', 'name'),  # (other_name, this_name)
                      ('value', 'value'),
                      ('domain', 'domain'),
                      ('path', 'path'),
                      ('secure', 'secure'),
                      ('expires', 'expiry'))
        for cookie in self.driver.get_cookies():
            session.cookies.set(
                **{other_name: cookie[this_name]
                        for other_name, this_name in cookie_map
                            if this_name in cookie})

        return session


    def create_requests_session(self, *args, **kwargs):
        session = requests.Session(*args, **kwargs)
        return self.inject_cookies_into_requests_session(session)


    # --- context manager ------------------------------------------------------

    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.quit()



