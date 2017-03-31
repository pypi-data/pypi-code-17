# coding=utf-8
import time

'''
 :Description:    控件类
 :author          80071482/bony
 :@version         V1.0
 :@Date            2016年11月
'''


class Element(object):
    Text = None
    Xpoint = None
    Ypoint = None
    device = None
    Bound = None

    def __init__(self, x=0, y=0, device=None):
        self.Xpoint = x
        self.Ypoint = y
        self.device = device

    def click(self):
        self.device.click(self.Xpoint, self.Ypoint)

    def input(self, Str):
        self.click()
        time.sleep(1)
        self.device.input(Str)

    def longPress(self):
        self.device.longPress(self.Xpoint, self.Ypoint)
