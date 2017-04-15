# coding=utf-8
import re
import platform

'''
 :Description:    系统操作类
 :author          80071482/bony
 :@version         V1.0
 :@Date            2016年11月
'''

# from Core.Utils.adb_interface import AdbInterface

# adb_interface = AdbInterface()

# 判断系统类型，windows使用findstr，linux使用grep
system_info = platform.system()
if system_info is "Windows":
    find_util = "findstr"
else:
    find_util = "grep"


class SystemInfo(object):
    device = None

    def __init__(self, device=None):
        self.device = device

    def getCpukinds(self):
        return self.device.script("adb shell getprop ro.product.cpu.abi")

    def getDeviceState(self):
        """
        获取设备状态： offline | bootloader | device
         usage: getDeviceState()
        """
        return self.device.script("adb get-state").split("\n")[0]

    def getDeviceID(self):
        """
        获取设备id号，return serialNo
         usage: getDeviceID()
        """
        return self.device.script("adb get-serialno").split("\n")[0]

    def getDeviceIDlist(self):
        """
        获取设备id号，return list(serialNo)
         usage: getDeviceIDlist()
        """
        l = []
        tmp = []
        l = self.device.script("adb devices").split("\r\n")
        del l[0]
        for x in l:
            if x != "":
                tmp.append(x.split("\t")[0].strip('\''))
        return tmp

    def getAppList(self):
        """
        获取设备中安装的应用包名列表
         usage: getAppList()
        """
        app = []
        for packages in self.device.script("adb shell pm list packages").split():
            app.append(packages.split(":")[1])

        return app

    def getSystemAppList(self):
        """
        获取设备中安装的系统应用包名列表
         usage: getSystemAppList()
        """
        sysApp = []
        for packages in self.device.script("adb shell pm list packages -s").split():
            sysApp.append(packages.split(":")[1])

        return sysApp

    def getThirdAppList(self):
        """
        获取设备中安装的第三方应用包名列表
         usage: getThirdAppList()
        """
        thirdApp = []
        for packages in self.device.script("adb shell pm list packages -3").split():
            thirdApp.append(packages.split(":")[1])

        return thirdApp

    def getMatchingAppList(self, keyword):
        """
        模糊查询与keyword匹配的应用包名列表
         args:
        - keyword -: 关键字
        usage: getMatchingAppList("qq")
        """
        matApp = []
        for packages in self.device.script("adb shell pm list packages " + keyword).split():
            matApp.append(packages.split(":")[1])
        return matApp

    def getAppAddressFromPname(self, packagename):
        """
        根据包名查询应用地址
        args:
        - packagename -: 包名
        usage: getAppAddressFromPname("com.android.test")
        """
        address = self.device.script("adb shell pm list packages -f |" + find_util + " " + packagename)
        return address.split(":")[1].split("=")[0]

    def getAppAddressFromKeyList(self, key):
        """
        根据关键字查找应用地址
        args:
        - key -: 关键字
        usage: getAppAddressFromKeyList("android")
        """
        l = []
        tmp = []
        l = self.device.script("adb shell pm list packages -f |" + find_util + " " + key).split("\n")
        for x in l:
            if x != "":
                tmp.append(x.split(":")[1].split("=")[0])
        return tmp

    def getAppAddressList(self):
        """
        获取安装应用地址
        usage: getAppAddressList()
        """
        l = []
        tmp = []
        l = self.device.script("adb shell pm list packages -f").split("\n")
        for x in l:
            if x != "":
                tmp.append(x.split(":")[1].split("=")[0])
        return tmp

    def getAppNo(self):
        """
        获取应用数量
        usage: getAppNo()
        """
        return len(self.getAppList())

    def get_sys_appno(self):
        """
        获取系统应用数量
        usage: get_sys_appNo()
        """
        return len(self.getSystemAppList())

    def get_third_appno(self):
        """
        获取第三方应用数量
        usage: getThirdAppNo()
        """
        return len(self.getThirdAppList())

    def get_sdk_version(self):
        """
        得到sdk版本号
        usage: getSdkVersion()
        """
        return self.device.script("adb shell getprop ro.build.version.sdk").split("\r\n")[0]

    def get_cur_handle(self):
        """
        得到当前的handle
        usage: getCurHandle()
        """
        fname = []
        l = self.device.script("adb shell dumpsys SurfaceFlinger").split("\r\n")
        n = 0
        z = 0
        for x in l:
            n += 1
            if "----------+-" in x:
                fname = l[n - 2].split("|")
                break
        for y in fname:
            z += 1
            if "handle" in y:
                handle = l[n].split("|")
                return handle[z - 1]

    def get_screen_resolution(self):
        """
        获取设备屏幕分辨率，return (width, high)
        usage: getScreenResolution()
        """
        if int(self.get_sdk_version()) < 14:  # 如果版本低于4。0，返回一个320,480
            return 320, 480
        pattern = re.compile(r"\d+")
        try:
            out = self.device.script("adb shell dumpsys display | " + find_util + " PhysicalDisplayInfo")
            display = pattern.findall(out)
            if len(display) < 1:
                raise Exception('Unable to get PhysicalDisplayInfo' + str(out))
            else:
                return int(display[0]), int(display[1])
        except Exception as e:
            out = self.device.script("adb shell wm size")
            display = pattern.findall(out)
            if len(display) < 1:
                raise Exception('Unable to get PhysicalDisplayInfo' + str(out))
            else:
                return int(display[0]), int(display[1])
