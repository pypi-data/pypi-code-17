# coding=utf-8

'''
 :Description:    设备类
 :author          80071482/bony
 :@version         V1.0
 :@Date            2016年11月
'''
import os
import re
# import time
# import subprocess
# import threading
# import inspect
# import ctypes
import platform
from Element import Element
from Memory import Memory
from System import SystemInfo
import xml.etree.cElementTree as ET

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

# 判断系统类型，windows使用findstr，linux使用grep
sys_info = platform.system()
if sys_info is "Windows":
    find_util = "findstr"
else:
    find_util = "grep"


class Device(object):
    Id = None
    Name = None
    Width = None
    High = None

    def __init__(self, Id=None, Name=None):
        self.Id = Id
        self.Name = Name
        pass

    def _init_screen_size(self):
        try:
            ScreenResolution = SystemInfo(self).getScreenResolution()
            self.Width = ScreenResolution[0]
            self.High = ScreenResolution[1]
            return True
        except Exception as e:
            raise e
            return False

    def setId(self, Id):
        if (Id == ""):
            Id = None
        self.Id = Id

    def setName(self, Name):
        self.Name = Name

    def getName(self):
        return self.Name

    def script(self, script):
        if (self.Id != None):
            script = 'adb -s ' + self.Id + ' ' + script.split('adb')[1]
        return os.popen(script).read().strip()

    def getLayoutXml(self, FileName):
        self.script('adb shell uiautomator dump --compressed /data/local/tmp/LayoutXml.xml')
        self.script('adb pull /data/local/tmp/LayoutXml.xml ' + PATH(FileName + '.xml'))
        self.script('adb shell rm -r /data/local/tmp/LayoutXml.xml')

    def getScreencap(self, FilePath=None):
        """
        get Screencap
        :param FilePath: 存放文件夹路径
        :return: file <png>
        """
        self.script('adb shell /system/bin/screencap -p /sdcard/screencap.png')
        if FilePath is None:
            self.script('adb pull /sdcard/screencap.png ./screencap.png')
        else:
            self.script('adb pull /sdcard/screencap.png ' + FilePath)
        self.script("adb shell rm /sdcard/screencap.png")

    def getScreenRecord(self, FilePath=None, time=10, size=None, bit_rate=None, rotate=None):
        """
        get Screen Record
        :param FilePath: 存放文件夹路径
        :param time: 获取时长
        :param size: 指定屏幕大小
        :param bit_rate:指定比特率
        :param rotate:是否旋转屏幕
        :return:file <mp4>
        """
        script = "adb shell screenrecord"
        if time != None:
            script = script + " --t %d" % (time)
        if size != None:
            script = script + " --size %d" % (size)
        if bit_rate != None:
            script = script + " --bit-rate %d" % (bit_rate)
        if rotate != None:
            script = script + " --rotate %d" % (rotate)
        script = script + " /sdcard/screenrecord.mp4"
        self.script(script)
        if FilePath is None:
            self.script("adb pull /sdcard/screenrecord.mp4 ./screenrecord.mp4")
        else:
            self.script("adb pull /sdcard/screenrecord.mp4  " + FilePath)

        self.script("adb shell rm /sdcard/screenrecord.mp4")

    def click(self, x, y):
        """
        点击坐标
        :param x:横坐标
        :param y:纵坐标
        :return:None
        """
        self.script('adb shell input tap %s %s' % (x, y))

    def clickBack(self):
        """
        click Back
        :return:
        """
        self.tapKeycode('KEYCODE_BACK')

    def clickEnter(self):
        """
        click Enter
        :return:
        """
        self.tapKeycode('KEYCODE_ENTER')

    def swipe(self, x, y, x1, y1):
        """
        swipe
        :param x: 起始横坐标
        :param y: 起始纵坐标
        :param x1: 终止横坐标
        :param y1: 终止纵坐标
        :return:
        """
        self.script('adb shell input swipe %s %s %s %s' % (x, y, x1, y1))

    def longPress(self, x, y):
        """
        长按某一位置
        :param x: 横坐标
        :param y: 纵坐标
        :return:
        """
        self.script('adb shell input swipe %s %s %s %s 2000' % (x, y, x, y))

    def input(self, text):
        """
        input txt
        :param text:
        :return:
        """
        self.script('adb shell input text ' + text)

    def tapKeycode(self, keycode):
        """
        tap Key code
        :param keycode:
        :return:
        """
        self.script('adb shell input keyevent ' + keycode)

    def longPressKeycode(self, keycode):
        """
        long Press Key code
        :param keycode:
        :return:
        """
        self.script('input keyevent --longpress ' + keycode)

    def intallApp(self, apkfile):
        """
        根据app路径安装app
        :param apkfile: app file path
        :return:
        """
        self.script('adb install -r ' + apkfile)

    def stopApp(self, packge):
        """
        stop app
        :param packge:包名
        :return:
        """
        self.script('adb shell am force-stop ' + packge)

    def startApp(self, packge, appActivity):
        """
        Start App
        :param packge:包名
        :param appActivity:主视图
        :return:
        """
        self.script('adb shell am start ' + packge + '/' + appActivity)

    def appClearData(self, packgeName):
        """
        Clear App Data
        :param packge:包名
        :return:
        """
        self.script('adb shell pm clear ' + packgeName)

    def clearLog(self):
        self.script('adb logcat -c')

    def getPid(self, packgeName):
        """
        get pid
        :param packgeName: 包名
        :return:pid
        """
        Rtu = self.script("adb shell \"ps |grep " + packgeName + " |grep -v :\"")
        if (Rtu == ""):
            print(packgeName + " Not have start!")
            return None
        else:
            arr = Rtu.split(' ')
            arr = filter(lambda x: x != '', arr)
            return arr[1]

    def getMemory(self, packgename=None):
        """
        get Memory
        :param packgename:包名
        :return: 内存对象
        """
        return Memory(self, packgename)

    def getFocusedPackageAndActivity(self):
        """
        获取当前应用界面的包名和Activity
        """
        pa = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
        out = self.script("adb shell dumpsys window w | " + find_util + " \/| " + find_util + " name=")
        if len(pa.findall(out)) < 1:
            return out
        else:
            return pa.findall(out)[0]

    def getElements(self, TypeName, TypeValue):
        """
        同属性多个元素，返回坐标元组列表，[(x1, y1), (x2, y2)]
        """
        ElementList = []
        self.getLayoutXml("LayoutXml")
        tree = ET.ElementTree(file=PATH("LayoutXml.xml"))
        xmlElements = tree.iter(tag="node")
        for xmlElement in xmlElements:
            if xmlElement.TypeName[TypeName] == TypeValue:
                bounds = xmlElement.TypeName["bounds"]
                pattern = re.compile(r"\d+")
                coord = pattern.findall(bounds)
                Xpoint = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                Ypoint = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                # 将匹配的元素区域的中心点添加进pointList中
                element = Element(Xpoint, Ypoint, self)
                ElementList.append(element)
        return ElementList

    def getElement(self, TypeName, Value):
        '''
        获取元素
        '''
        element = Element()
        if TypeName is "xpath":
            element = self.getXpathElement(Value)
        else:
            element = self.getTypeElement(TypeName, Value)
        return element

    def getTypeElement(self, TypeName, TypeValue):
        '''
        根据元素属性定位元素
        '''
        self.getLayoutXml("LayoutXml")
        tree = ET.ElementTree(file=PATH("LayoutXml.xml"))
        xmlElements = tree.iter(tag="node")
        element = Element(device=self)
        for xmlElement in xmlElements:
            if xmlElement.attrib[TypeName] == TypeValue:
                bounds = xmlElement.attrib["bounds"]
                pattern = re.compile(r"\d+")
                bound = pattern.findall(bounds)
                element.Xpoint = (int(bound[0]) + int(bound[2])) / 2
                element.Ypoint = (int(bound[1]) + int(bound[3])) / 2
                element.Text = xmlElement.attrib["text"]
                element.Bound = bound
        return element

    def getXpathElement(self, xpathValue):
        '''
        根据xpath定位元素
        '''
        self.getLayoutXml("LayoutXml")
        tree = ET.ElementTree(file=PATH("LayoutXml.xml"))
        root = tree.getroot()
        for index in xpathValue:
            root = root[index]
        bounds = root.attrib["bounds"]
        pattern = re.compile(r"\d+")
        bound = pattern.findall(bounds)
        Xpoint = (int(bound[0]) + int(bound[2])) / 2
        Ypoint = (int(bound[1]) + int(bound[3])) / 2
        element = Element(Xpoint, Ypoint, self)
        element.Text = root.attrib["text"]
        element.Bound = bound
        return element

    def system(self):
        '''
        返回系统信息操作对象
        '''
        return SystemInfo(self)


        # def appLog(self, packgeName, Path):
        #     Pid = self.getPid(packgeName)
        #     self.getLog("adb shell \"logcat |grep " + str(Pid) + "\"", Path)

        # def getLog(self, script, Path):
        #     GG = scriptThread(self, script + " >" + Path)
        #     GG.start()
        #     # ctypes.pythonapi.PyThreadState_SetAsyncExc(GG.ident, ctypes.py_object(SystemExit))
        #     # self.stop_thread(GG)
        #     return GG
        # def _async_raise(self, tid, exctype):
        #     """raises the exception, performs cleanup if needed"""
        #     tid = ctypes.c_long(tid)
        #     if not inspect.isclass(exctype):
        #         exctype = type(exctype)
        #     res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        #     if res == 0:
        #         raise ValueError("invalid thread id")
        #     elif res != 1:
        #         # """if it returns a number greater than one, you're in trouble,
        #         # and you should call it again with exc=NULL to revert the effect"""
        #         ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        #         raise SystemError("PyThreadState_SetAsyncExc failed")

        # def stop_thread(self, thread):
        #     self._async_raise(thread.ident, SystemExit)

# class scriptThread(threading.Thread):  # 继承父类threading.Thread
#     def __init__(self, device, script):
#         threading.Thread.__init__(self)
#         self.device = device
#         self.script = script

#     def run(self):
#         try:
#             print(self.device.Id + "　LogCat...")
#             self.device.script(self.script)
#         except Exception, e:
#             print("Not have connected Device!")
