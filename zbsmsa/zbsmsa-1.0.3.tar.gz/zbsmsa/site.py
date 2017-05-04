"""
Written by: Ian Doarn

Login page and main page

Base class for all site interactions
"""
from zbsmsa.page import Page
from zbsmsa.utils.utilities import load_selectors
from zbsmsa.utils.waits import Waits
from zbsmsa.utils.exceptions import SiteNotLoaded, LoginFailed

class Site:
    """
    Site class can be an object that must be passed to other page 
    objects. all other pages that are no the login page or main page
    will inherit this class.
    """
    def __init__(self, username, password, path_to_driver, launch=True):
        """
        sets the username and password as well as the path to
        the chromedriver to be passed to the Page object
        
        :param username: Your username
        :param password: Your password
        :param path_to_driver: path to the chromedriver.exe
        :param launch: Launch webdriver on instantiation
        """
        self.username = username
        self.password = password

        self.driver = None
        self.driver_path = path_to_driver
        self.driver_uri = None
        self.driver_session_id = None

        self.login_page_selectors = load_selectors('loginPage.json')
        self.main_page_selectors = load_selectors('mainPage.json')
        self.user_settings_selectors = load_selectors('userSettings.json')
        self.site_settings_selectors = load_selectors('siteSettings.json')

        self.website_url = self.login_page_selectors["url"]
        self.wait = None
        self.site_name = None

        if launch:
            self.launch()

    def launch(self, maximize=True):
        """
        Loads driver with Page class,
        sets the driver, driver url, and driver session id
        
        Sets up Wait class
        :param maximize: Maximize window on launch
        :return: None
        """
        driver, uri, session_id = Page.create_driver(self.driver_path,
                                                     init_site=self.website_url)
        self.driver = driver
        self.driver_uri = uri
        self.driver_session_id = session_id
        self.wait = Waits(driver)

        if maximize:
            self.driver.maximize_window()

    def login(self):
        """
        Logs into SMS with your credentials
        
        Throws a LoginFailed if it has failed
        
        Because the website can take multiple minutes
        to fully load into the login screen, we can not 
        simply launch and login, the user will have to be 
        prompted to wait or so sort of wait function
        will have to be built
        
        :return: 
        """
        if self.driver is not None:
            try:
                self.wait.clear_input(self.login_page_selectors["username"])
                self.wait.send_keys_to(self.username,
                                       self.login_page_selectors["username"])
                self.wait.clear_input(self.login_page_selectors["password"])
                self.wait.send_keys_to(self.password,
                                       self.login_page_selectors["password"])
                self.wait.clickable(self.login_page_selectors["loginbutton"])

            except Exception as error:
                raise LoginFailed("Unable to login as {}!".format(self.username),
                                  parent=error)
        else:
            # Raise if launch() was not called
            raise SiteNotLoaded

        self.set_site_name()

    def close(self):
        """
        Closes webdriver
        
        :return: None 
        """
        if self.driver is not None:
            self.driver.close()
        else:
            # If you for some reason try to close when the webdriver wasn't launched
            raise SiteNotLoaded(msg="Can not close webdriver")

    def ribbon(self, ribbon_button_name):
        """
        Takes parameter of ribbon name to go to the different tabs
        on the main page.
        
        :param ribbon_button_name: ribbon key name
        :return: None
        """
        if ribbon_button_name in self.main_page_selectors.keys():
            self.wait.clickable(self.main_page_selectors[ribbon_button_name])
        else:
            raise KeyError("Key does not exists in {}".format("mainPage.json"))

    def set_site_name(self):
        """
        Set the name of the site we are currently logged into
        
        :return: 
        """
        self.site_name = self.get_inner_html(self.main_page_selectors["checkSite"])

    def get_site_name(self):
        """
        Get the name of the site we are currently logged into
        
        :return: Site name
        """
        if self.site_name is None:
            self.set_site_name()
        return self.site_name

    def get_inner_html(self, selector):
        _, element = self.wait.to_exist(selector)
        return element.get_attribute('innerHTML')

    def change_site(self, site, auto_login=True, sleep=1):
        """
        Switch to a different ZB site
        
        list of applicable sites located 
        in the file utils/json/siteSettings.json
        
        :param site: site to change to
        :param auto_login: Login automatically after change, default @ true
        :param sleep: time to sleep for in between switches, default @ 1
        :return: 
        """
        new_site = '_'.join(site.split(' '))

        self.driver.get(self.website_url)
        self.wait.to_exist(self.login_page_selectors["loginbutton"])
        self.login()

        self.wait.clickable(self.user_settings_selectors["upUser"])
        self.wait.clickable(self.user_settings_selectors["upUserSettingsButton"])
        self.wait.clickable(self.site_settings_selectors["listBoxSites"][new_site]["path"])
        self.wait.clickable(self.site_settings_selectors["listBoxSites"]["saveButton"]["path"])
        self.wait._for(sleep)

        if auto_login:
            self.wait._for(sleep)
            self.driver.get(self.website_url)
            self.wait.to_exist(self.login_page_selectors["loginbutton"])
            self.login()
