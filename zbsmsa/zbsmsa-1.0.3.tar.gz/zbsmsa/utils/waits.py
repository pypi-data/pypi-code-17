"""
Written by: Ian Doarn

Waits

Used to explicitly wait for events to occur
using selenium's built in explicit and implicit waits.

"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


TIME_OUT = 10

class Waits():
    """
    Waits class
    
    all methods using the explicit wait function
    from selenium have customizable time out's that
    are all defaulted at 10 by the global variable TIME_OUT
    """

    def __init__(self, selenium_driver, time_out=TIME_OUT):
        """
        :param selenium_driver: driver object
        :param time_out: how many time to retry, default @ 10
        """
        self.driver = selenium_driver
        self.time_out = time_out

    @staticmethod
    def set_time_out(t):
        """
        Set time out to new value
        
        :param t: time as int
        :return: 
        """
        global TIME_OUT
        TIME_OUT = t

    def implicit(self, time=10):
        """
        Just simply wait
        
        :param time: int
        :return: 
        """
        self.driver.implicitly_wait(time)

    @staticmethod
    def _for(s):
        """
        wait for given amount of seconds
        
        :param s: seconds to wait
        :return: 
        """
        time.sleep(s)

    def to_exist(self, selection_input, find_by=By.CSS_SELECTOR, time_out=TIME_OUT):
        """
        Wait for element to become visible or to load
        
        :param selection_input: CSS selector 
        :param find_by: what to use to find element, default By.CSS_SELECTOR
        :param time_out: Time to wait before raising timeout exception
        :return: css selector since element exists, element object
        """
        element = WebDriverWait(self.driver, time_out).until(
            EC.presence_of_element_located((find_by, selection_input))
        )
        return selection_input, element

    def clickable(self, selection_input, find_by=By.CSS_SELECTOR, time_out=TIME_OUT):
        """
        Wait till element is clicked
        
        :param selection_input: CSS selector 
        :param find_by: what to use to find element, default By.CSS_SELECTOR
        :param time_out: Time to wait before raising timeout exception
        :return: None
        """
        element = WebDriverWait(self.driver, time_out).until(
            EC.element_to_be_clickable((find_by, selection_input))
        )
        # Click if its found
        element.click()

    def send_keys_to(self, text, selection_input, find_by=By.CSS_SELECTOR, time_out=TIME_OUT):
        """
        Wait to send input to element
        
        :param text: Text to give to element
        :param selection_input: CSS selector 
        :param find_by: what to use to find element, default By.CSS_SELECTOR
        :param time_out: Time to wait before raising timeout exception
        :return: 
        """
        element = WebDriverWait(self.driver, time_out).until(
            EC.element_to_be_clickable((find_by, selection_input))
        )
        # send input to element
        element.send_keys(text)

    def clear_input(self, selection_input, find_by=By.CSS_SELECTOR, time_out=TIME_OUT):
        """
        Wait to clear element of current input
        
        :param selection_input: CSS selector 
        :param find_by: what to use to find element, default By.CSS_SELECTOR
        :param time_out: Time to wait before raising timeout exception
        :return: 
        """
        element = WebDriverWait(self.driver, time_out).until(
            EC.element_to_be_clickable((find_by, selection_input))
        )
        # Clear elements current values
        element.clear()
