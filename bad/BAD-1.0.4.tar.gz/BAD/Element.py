# coding=utf-8
import time

'''
 :Description:    控件类
 :author          80071482/bony
 :@version         V1.0
 :@Date            2016年11月
'''


class Element(object):
    _text_ = None
    _device_ = None
    _bound_ = None

    def __init__(self, x=None, y=None, device=None):
        self._x_point_ = x
        self._y_point_ = y
        self._device_ = device

    def click(self):
        self._device_.click(self._x_point_, self._y_point_)

    def input(self, text):
        self.click()
        time.sleep(1)
        self._device_.input(text)

    def long_click(self):
        self._device_.longPress(self._x_point_, self._y_point_)
