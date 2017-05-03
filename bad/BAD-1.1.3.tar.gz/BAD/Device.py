# coding=utf-8

"""
 :Description:    设备类
 :author          80071482/bony
 :@version         V1.0
 :@Date            2016年11月
"""
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
from SurfaceStatsCollector import SurfaceStatsCollector
import xml.etree.cElementTree as ET

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

# 判断系统类型，windows使用findstr，linux使用grep
sys_info = platform.system()
if sys_info is "Windows":
    find_util = "findstr"
else:
    find_util = "grep"


class Device(object):
    def __init__(self, ID=None, NAME=None):
        self.Debug = False
        self.WIDTH = None
        self.HIGH = None
        self.ID = ID
        self.NAME = NAME
        self._system_ = self.system()
        self._SurfaceStatsCollector_ = None
        pass

    def init_screen_size(self):
        try:
            wh = self._system_.get_screen_resolution()
            self.WIDTH = wh[0]
            self.HIGH = wh[1]
            return True
        except Exception as e:
            print(e.message)
            # raise e

    def script(self, script):
        if self.ID is not None:
            script = 'adb -s ' + self.ID + ' ' + script.split('adb')[1]
        if self.Debug is True:
            print script
        ret = os.popen(script).read().strip()
        return ret

    def rm(self, path):
        """
        删除文件
        """
        self.script('adb shell rm -rf ' + path)

    def sdcard_rm(self, path):
        """
        删除sdcard中的文件
        """
        path = '/mnt/sdcard' + path
        self.rm(path)

    def get_layout_xml(self, path):
        self.script('adb shell uiautomator dump --compressed /data/local/tmp/LayoutXml.xml')
        self.script('adb pull /data/local/tmp/LayoutXml.xml ' + PATH(path))
        self.script('adb shell rm -r /data/local/tmp/LayoutXml.xml')

    def get_screencap(self, path=None):
        """
        get screencap
        :param path: 存放文件夹路径
        :return: file <png>
        """
        self.script('adb shell /system/bin/screencap -p /sdcard/screencap.png')
        if path is None:
            self.script('adb pull /sdcard/screencap.png ./screencap.png')
        else:
            self.script('adb pull /sdcard/screencap.png ' + path)
        self.script("adb shell rm /sdcard/screencap.png")

    def screen_record(self, path=None, time=10, size=None, bit_rate=None, rotate=None):
        """
        get Screen Record
        :param path: 存放文件夹路径
        :param time: 获取时长
        :param size: 指定屏幕大小
        :param bit_rate:指定比特率
        :param rotate:是否旋转屏幕
        :return:file <mp4>
        """
        script_text = "adb shell screenrecord"
        if time is not None:
            script_text += script_text + " --t %d" % time
        if size is not None:
            script_text += " --size %d" % size
        if bit_rate is not None:
            script_text += " --bit-rate %d" % bit_rate
        if rotate is not None:
            script_text += " --rotate %d" % rotate
        script_text += " /sdcard/screenrecord.mp4"
        self.script(script_text)
        if path is None:
            self.script("adb pull /sdcard/screenrecord.mp4 ./screenrecord.mp4")
        else:
            self.script("adb pull /sdcard/screenrecord.mp4  " + path)

        self.script("adb shell rm /sdcard/screenrecord.mp4")

    def click(self, x, y):
        """
        点击坐标
        :param x:横坐标
        :param y:纵坐标
        :return:None
        """
        self.script('adb shell input tap %s %s' % (x, y))

    def click_back(self):
        """
        click Back
        :return:
        """
        self.click_keycode('KEYCODE_BACK')

    def click_star(self):
        """
        click star
        :return:
        """
        self.click_keycode('KEYCODE_STAR')

    def click_enter(self):
        """
        click Enter
        :return:
        """
        self.click_keycode('KEYCODE_ENTER')

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

    def swipe_left(self):
        """
        向左滑动
        """
        if self.WIDTH is None or self.HIGH is None:
            self.init_screen_size()
            self.swipe(self.WIDTH * 0.9, self.HIGH * 0.5, self.WIDTH * 0.1, self.HIGH * 0.5)
        else:
            self.swipe(self.WIDTH * 0.9, self.HIGH * 0.5, self.WIDTH * 0.1, self.HIGH * 0.5)

    def swipe_right(self):
        """
        向右滑动
        """
        if self.WIDTH is None or self.HIGH is None:
            self.init_screen_size()
            self.swipe(self.WIDTH * 0.1, self.HIGH * 0.5, self.WIDTH * 0.9, self.HIGH * 0.5)
        else:
            self.swipe(self.WIDTH * 0.1, self.HIGH * 0.5, self.WIDTH * 0.9, self.HIGH * 0.5)

    def swipe_up(self):
        """
        向上滑动
        """
        if self.WIDTH is None or self.HIGH is None:
            self.init_screen_size()
            self.swipe(self.WIDTH * 0.5, self.HIGH * 0.8, self.WIDTH * 0.5, self.HIGH * 0.2)
        else:
            self.swipe(self.WIDTH * 0.5, self.HIGH * 0.8, self.WIDTH * 0.5, self.HIGH * 0.2)

    def swipe_down(self):
        """
        向下滑动
        """
        if self.WIDTH is None or self.HIGH is None:
            self.init_screen_size()
            self.swipe(self.WIDTH * 0.5, self.HIGH * 0.2, self.WIDTH * 0.5, self.HIGH * 0.8)
        else:
            self.swipe(self.WIDTH * 0.5, self.HIGH * 0.2, self.WIDTH * 0.5, self.HIGH * 0.8)

    def long_click(self, x, y):
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

    def click_keycode(self, keycode):
        """
        tap Key code
        :param keycode:
        :return:
        """
        self.script('adb shell input keyevent ' + keycode)

    def long_click_keycode(self, keycode):
        """
        long Press Key code
        :param keycode:
        :return:
        """
        self.script('input keyevent --longpress ' + keycode)

    def install_app(self, apk_path):
        """
        根据app路径安装app
        :param apk_path: app file path
        :return:
        """
        self.script('adb install -r ' + apk_path)

    def stop_app(self, package):
        """
        stop app
        :param package:包名
        :return:
        """
        self.script('adb shell am force-stop ' + package)

    def start_app(self, package, activity):
        """
        Start App
        :param package:包名
        :param activity:主视图
        :return:
        """
        self.script('adb shell am start ' + package + '/' + activity)

    def app_clear_data(self, package):
        """
        Clear App Data
        :param package:包名
        :return:
        """
        self.script('adb shell pm clear ' + package)

    def wifi_stop(self):
        """
        wifi stop
        """
        self.script('adb shell svc wifi disable')

    def wifi_start(self):
        """
        wifi start
        """
        self.script('adb shell svc wifi enable')

    def pid(self, package):
        """
        get pid
        :param package: 包名
        :return:pid
        """
        rtu = self.script("adb shell \"ps |grep " + package + " |grep -v :\"")
        if rtu == "":
            print(package + " Not have start!")
            return None
        else:
            arr = rtu.split(' ')
            arr = filter(lambda x: x != '', arr)
            return arr[1]

    def get_memory(self, package=None):
        """
        get Memory
        :param package:包名
        :return: 内存对象
        """
        return Memory(self, package)

    def get_focused_package_activity(self):
        """
        获取当前应用界面的包名和Activity
        """
        pa = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
        out = self.script("adb shell dumpsys window w | " + find_util + " \/| " + find_util + " name=")
        if len(pa.findall(out)) < 1:
            return out
        else:
            return pa.findall(out)[0]

    def find_elements(self, _type, value):
        """
        同属性多个元素
        """
        element_list = []
        self.get_layout_xml("LayoutXml.xml")
        tree = ET.ElementTree(file=PATH("LayoutXml.xml"))
        xml_elements = tree.iter(tag="node")
        for xmlElement in xml_elements:
            if xmlElement.attrib[_type] == value:
                bounds = xmlElement.attrib["bounds"]
                pattern = re.compile(r"\d+")
                bound = pattern.findall(bounds)
                x = (int(bound[2]) - int(bound[0])) / 2.0 + int(bound[0])
                y = (int(bound[3]) - int(bound[1])) / 2.0 + int(bound[1])
                # 将匹配的元素区域的中心点添加进pointList中
                element = Element(x, y, self)
                element.TEXT = xmlElement.attrib["text"]
                element.BOUND = bound
                element_list.append(element)
        return element_list

    def find_element(self, _type, value):
        """
        获取元素
        """
        if type is "index_path":
            element = self.find_index_path_element(value)
            return element
        else:
            element = self.find_type_element(_type, value)
            return element

    def find_type_element(self, _type, value):
        """
        根据元素属性定位元素
        """
        self.get_layout_xml("LayoutXml.xml")
        tree = ET.ElementTree(file=PATH("LayoutXml.xml"))
        xml_elements = tree.iter(tag="node")
        element = Element(device=self)
        for xmlElement in xml_elements:
            if xmlElement.attrib[_type] == value:
                bounds = xmlElement.attrib["bounds"]
                pattern = re.compile(r"\d+")
                bound = pattern.findall(bounds)
                element.X_COORDINATE = (int(bound[0]) + int(bound[2])) / 2
                element.Y_COORDINATE = (int(bound[1]) + int(bound[3])) / 2
                element.TEXT = xmlElement.attrib["text"]
                element.BOUND = bound
        return element

    def find_index_path_element(self, value):
        """
        根据xpath定位元素
        """
        self.get_layout_xml("LayoutXml.xml")
        tree = ET.ElementTree(file=PATH("LayoutXml.xml"))
        root = tree.getroot()
        for index in value:
            root = root[index]
        bounds = root.attrib["bounds"]
        pattern = re.compile(r"\d+")
        bound = pattern.findall(bounds)
        x = (int(bound[0]) + int(bound[2])) / 2
        y = (int(bound[1]) + int(bound[3])) / 2
        element = Element(x, y, self)
        element.TEXT = root.attrib["text"]
        element.BOUND = bound
        return element

    def system(self):
        """
        返回系统信息操作对象
        """
        return SystemInfo(self)

    def get_surface_stats_collector(self):
        """
        :return SurfaceStatsCollector
        """
        return self._SurfaceStatsCollector_

    def fps_stats_start(self, focuse_name=None):
        """
        开始收集fps
        :param focuse_name:包名None or SurfaceView
        """
        self._SurfaceStatsCollector_ = SurfaceStatsCollector(self)
        if focuse_name is not None:
            self._SurfaceStatsCollector_._focuse_name = focuse_name
        self._SurfaceStatsCollector_.DisableWarningAboutEmptyData()
        self._SurfaceStatsCollector_.Start()

    def fps_stats_stop(self, result_name=None):
        """
        结束收集fps，并返回结果
        """
        self._SurfaceStatsCollector_.Stop()
        results = self._SurfaceStatsCollector_.GetResults()
        if result_name is not None:
            for result in results:
                if result.name in result_name:
                    return result
            return None
        else:
            return results

    def clear_log(self):
        """
        清除设备日志缓存
        """
        self.script("adb shell logcat -c")

    def get_log(self, grep=None, fname=None):
        """
        获取设备运行缓存日志
        :param fname:日志保存路径
        :param grep:过滤条件，可以是list或字符串
        """
        cmd_text = "adb shell \" logcat -d"
        if isinstance(grep, list):
            for value in grep:
                cmd_text += " |grep \'" + str(value) + "\'"
        else:
            cmd_text += "|grep " + str(grep)
        cmd_text += " \" "
        if fname is not None:
            cmd_text += "> " + fname
            self.script(cmd_text)
        else:
            return self.script(cmd_text)

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
