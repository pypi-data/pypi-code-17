# coding=utf-8
import time

'''
 :Description:    控件类
 :author          80071482/bony
 :@version         V1.0
 :@Date            2016年11月
'''


class Element(object):
    def __init__(self, x=None, y=None, device=None):
        self.TEXT = None
        self.BOUND = None
        self.X_COORDINATE = x
        self.Y_COORDINATE = y
        self._device_ = device

    def click(self):
        self._device_.click(self.X_COORDINATE, self.Y_COORDINATE)

    def input(self, text):
        self.click()
        time.sleep(1)
        self._device_.input(text)

    def long_click(self):
        self._device_.longPress(self.X_COORDINATE, self.Y_COORDINATE)
