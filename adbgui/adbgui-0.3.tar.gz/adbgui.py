#!/usr/bin/env python
## Copyright 2012, En7788.com, Inc. All rights reserved.
##
## FormUI is a easy used GUI framwork for python, which is based on wxpython.
## FormUI is a free software: you can redistribute it and/or modify it under
## the terms of version 3 of the GNU Lesser General Public License as
## published by the Free Software Foundation.
##
## You should have received a copy of the GNU Lesser General Public License
## along with AndBug.  If not, see <http://www.gnu.org/licenses/>.
import sys

sys.path.append('../')
import subprocess
import commands

from FormUI import *

# Load layout xml file
builder = Builder()
builder.loadLayout(os.path.split(os.path.realpath(__file__))[0] + os.path.sep +'adbgui.xml')

try:
    from advance import *
    if loadAdvance:
        loadAdvance(builder)
except:
    pass

def shellRun(adbcmd,cmd):
    if adbcmd != '' and adbcmd != 'adb':
        cmd = 'alias adb="' + adbcmd + '"\n' + cmd
    subprocess.call(['/bin/bash','-c', cmd])

def getShellOutput(adbcmd,cmd):
    if adbcmd != '' and adbcmd != 'adb':
        cmd = 'alias adb="' + adbcmd + '"\n' + cmd
    p = subprocess.Popen(['/bin/bash','-c', cmd],stdout = subprocess.PIPE)
    p.wait()
    if p.returncode != 0:
        print "Error."
        return None
    ret = p.stdout.read()
    return  ret

gCommandRegist = {}
gCommandRegist['id_adb_devices'] = "adb devices"
gCommandRegist['id_list_package'] = "adb shell pm list packages"
gCommandRegist['id_list_sys_package'] = "adb shell pm list packages -s"
gCommandRegist['id_list_3rd_package'] = "adb shell pm list packages -3"
gCommandRegist['id_screen_shot'] = 'adb shell screencap -p | sed "s/\r$//" > sc.png'
# "adb shell screencap -p /sdcard/sc.png;adb pull /sdcard/sc.png"
gCommandRegist['id_screen_record'] = "adb shell screenrecord /sdcard/sr.mp4;adb pull /sdcard/sr.mp4"
gCommandRegist['id_dump_activities'] = "adb shell dumpsys activity activities"
gCommandRegist['id_dump_services'] = "adb shell dumpsys activity services"
gCommandRegist['id_dump_display'] = "adb shell dumpsys window displays"
gCommandRegist['id_info_product'] = "adb shell getprop ro.product.model"
gCommandRegist['id_dump_battery'] = "adb shell dumpsys battery"
gCommandRegist['id_info_screen_size'] = "adb shell wm size"
gCommandRegist['id_info_screen_density'] = "adb shell wm density"
gCommandRegist['id_info_android_id'] = "adb shell settings get secure android_id"
gCommandRegist['id_info_imei'] = "adb shell dumpsys iphonesubinfo"
gCommandRegist[
    'id_info_network'] = "adb shell ifconfig;adb shell ifconfig wlan0;adb shell netcfg;adb shell cat /sys/class/net/wlan0/address"
gCommandRegist['id_info_cpu'] = "adb shell cat /proc/cpuinfo"
gCommandRegist['id_info_memory'] = "adb shell cat /proc/meminfo"
gCommandRegist['id_info_wifi_passwd'] = "echo su > cmd.sh;echo cat /data/misc/wifi/*.conf >> cmd.sh; adb shell < cmd.sh"
gCommandRegist['id_info_ps'] = "adb shell ps"
gCommandRegist['id_info_top'] = "adb shell top"
gCommandRegist['id_kernel_log'] = "adb shell dmesg"
gCommandRegist[
    'id_current_activity'] = "adb shell dumpsys window w | grep \/ | grep name= | cut -d = -f 3 | cut -d \) -f 1"

def onDefaultHandler(windowHandler, handlerPara):
    global gCommandRegist
    if handlerPara.getEventId() in gCommandRegist.keys():
        windowHandler.showWindow(False)
        hideAllPanel(windowHandler)
        cmd = gCommandRegist[handlerPara.getEventId()]
        print('\033[1;31;40m' + cmd + '\033[0m')
        #subprocess.call([cmd], shell=True)
        shellRun(handlerPara.getValue('id_setting_adb_path'),cmd)
        raw_input("Press Enter to continue:")
        windowHandler.showWindow(True)


builder.setDefaultHandler(onDefaultHandler)


def hideAllPanel(windowHandler):
    panels = ['pid_install_app', 'pid_input_keyevent', 'pid_reboot', 'pid_logcat', 'pid_dump', 'pid_adb_pull',
              'pid_adb_push']
    for panel in panels:
        windowHandler.showCtrl(panel, False)


def onInstallApp(windowHandler, handlerPara):
    hideAllPanel(windowHandler)
    windowHandler.showCtrl('pid_install_app', True)


builder.setCtrlHandler('id_install_app', onInstallApp)


def onInstallAppButton(windowHandler, handlerPara):
    cmd = "adb install "
    if handlerPara.getValue('id_install_sdcard') == 'true':
        cmd = cmd + " -s "
    if handlerPara.getValue('id_install_grand_permission') == 'true':
        cmd = cmd + " -g "
    cmd = cmd + handlerPara.getValue('id_install_apk_file')
    #subprocess.call([cmd], shell=True)
    shellRun(handlerPara.getValue('id_setting_adb_path'),cmd)


builder.setCtrlHandler('id_button_install_apk', onInstallAppButton)


def onUninstallApp(windowHandler, handlerPara):
    windowHandler.showWindow(False)
    cmd = "adb shell pm list packages"
    #subprocess.call([cmd], shell=True)
    shellRun(handlerPara.getValue('id_setting_adb_path'),cmd)
    sel = raw_input("Please Input the package need uninstall:")
    cmd = "adb uninstall " + sel
    #subprocess.call([cmd], shell=True)
    shellRun(handlerPara.getValue('id_setting_adb_path'),cmd)
    windowHandler.showWindow(True)


builder.setCtrlHandler('id_uninstall_app', onUninstallApp)


def onClearData(windowHandler, handlerPara):
    windowHandler.showWindow(False)
    cmd = "adb shell pm list packages"
    #subprocess.call([cmd], shell=True)
    shellRun(handlerPara.getValue('id_setting_adb_path'),cmd)
    sel = raw_input("Please Input the package:")
    cmd = "adb shell pm clear " + sel
    #subprocess.call([cmd], shell=True)
    shellRun(handlerPara.getValue('id_setting_adb_path'),cmd)
    windowHandler.showWindow(True)


builder.setCtrlHandler('id_clear_data', onClearData)



def onSetting(windowHandler, handlerPara):
    hideAllPanel(windowHandler)
    windowHandler.showCtrl('pid_setting', True)
builder.setCtrlHandler('id_setting', onSetting)

def onSettingButton(windowHandler, handlerPara):
    global formUI
    seting = {}
    seting['id_setting_adb_path'] = handlerPara.getValue('id_setting_adb_path')
    formUI.saveCachedValue(os.path.expanduser('~') + "/.adbgui.cfg", seting)
builder.setCtrlHandler('id_setting_btn', onSettingButton)

def onStopApp(windowHandler, handlerPara):
    windowHandler.showWindow(False)
    cmd = "adb shell pm list packages"
    #subprocess.call([cmd], shell=True)
    shellRun(handlerPara.getValue('id_setting_adb_path'),cmd)
    sel = raw_input("Please Input the package:")
    cmd = "adb shell am force-stop " + sel
    #subprocess.call([cmd], shell=True)
    shellRun(handlerPara.getValue('id_setting_adb_path'),cmd)
    windowHandler.showWindow(True)


builder.setCtrlHandler('id_stop_app', onStopApp)


def onInputKeyevent(windowHandler, handlerPara):
    hideAllPanel(windowHandler)
    windowHandler.showCtrl('pid_input_keyevent', True)


builder.setCtrlHandler('id_input_keyevent', onInputKeyevent)

global keyeventList
keyeventList = {}
keyeventList['home'] = 3
keyeventList['return'] = 4
keyeventList['dail'] = 5
keyeventList['hung up'] = 6
keyeventList['power'] = 26
keyeventList['light on'] = 224
keyeventList['light off'] = 223
keyeventName = ''
for (k, v) in keyeventList.items():
    if keyeventName != '':
        keyeventName = keyeventName + ";"
    keyeventName = keyeventName + k
builder.setCtrlAttribute('id_keyevent', 'choices', keyeventName)


def onInputKeyeventButton(windowHandler, handlerPara):
    global keyeventList
    if handlerPara.getValue('id_keyevent') in keyeventList.keys():
        keyCode = keyeventList[handlerPara.getValue('id_keyevent')]
        cmd = "adb shell input keyevent " + str(keyCode)
        print cmd
        #subprocess.call([cmd], shell=True)
        shellRun(handlerPara.getValue('id_setting_adb_path'),cmd)


builder.setCtrlHandler('id_button_input_keyevent', onInputKeyeventButton)


def onReboot(windowHandler, handlerPara):
    hideAllPanel(windowHandler)
    windowHandler.showCtrl('pid_reboot', True)


builder.setCtrlHandler('id_reboot', onReboot)


def onRebootButton(windowHandler, handlerPara):
    cmd = "adb install "
    type = handlerPara.getValue('id_reboot_type')
    if type == 'normal':
        type = ''
    cmd = "adb reboot " + type
    #subprocess.call([cmd], shell=True)
    shellRun(handlerPara.getValue('id_setting_adb_path'),cmd)


builder.setCtrlHandler('id_reboot_button', onRebootButton)


def onLogCat(windowHandler, handlerPara):
    hideAllPanel(windowHandler)
    windowHandler.showCtrl('pid_logcat', True)


builder.setCtrlHandler('id_logcat', onLogCat)


def onLogCatButton(windowHandler, handlerPara):
    windowHandler.showWindow(False)
    cmd = 'adb logcat'
    priority = handlerPara.getValue('id_logcat_priority')
    priority = priority[0:1]
    cmd = cmd + " *:" + priority
    format = handlerPara.getValue('id_logcat_format')
    if format != '':
        cmd = cmd + " -v " + format
    if handlerPara.getValue('id_logcat_grep') != '':
        cmd = cmd + "|grep '" + handlerPara.getValue('id_logcat_grep') + "'"
    print cmd
    #subprocess.call([cmd], shell=True)
    shellRun(handlerPara.getValue('id_setting_adb_path'),cmd)
    windowHandler.showWindow(True)


builder.setCtrlHandler('id_logcat_button', onLogCatButton)


def getDumpServices(handlerPara):
    choise = ''
    serviceList = getShellOutput(handlerPara.getValue('id_setting_adb_path'),"adb shell dumpsys | grep 'DUMP OF SERVICE'")
    if serviceList is None:
        return
    serviceList = serviceList.strip()
    serviceList = serviceList.split('\n')
    for service in serviceList:
        service = service[len('DUMP OF SERVICE'):-1]
        if choise != '':
            choise = choise + ";"
        choise = choise + service
    return choise


def onDump(windowHandler, handlerPara):
    windowHandler.showWindow(False)
    print('\033[1;31;40m' + "Loading Services..." + '\033[0m')
    choices = getDumpServices(handlerPara)
    builder.setCtrlAttribute('id_service', 'choices', choices)
    windowHandler.update(builder, False)
    hideAllPanel(windowHandler)
    windowHandler.showCtrl('pid_dump', True)
    windowHandler.showWindow(True)


builder.setCtrlHandler('id_dump', onDump)


def onDumpServiceButton(windowHandler, handlerPara):
    windowHandler.showWindow(False)
    cmd = 'adb shell dumpsys '
    serviceList = handlerPara.getValue('id_service')
    for service in serviceList:
        currentCmd = cmd + service
        print('\033[1;31;40m' + currentCmd + '\033[0m')
        #subprocess.call([currentCmd], shell=True)
        shellRun(handlerPara.getValue('id_setting_adb_path'),cmd)
    windowHandler.showWindow(True)


builder.setCtrlHandler('id_dump_service', onDumpServiceButton)

import DeviceFile


def onAdbPull(windowHandler, handlerPara):
    hideAllPanel(windowHandler)
    windowHandler.showCtrl('pid_adb_pull', True)


builder.setCtrlHandler('id_adb_pull', onAdbPull)


def onAdbPullBtn(windowHandler, handlerPara):
    windowHandler.showWindow(False)
    cmd = 'adb pull '
    cmd = cmd + handlerPara.getValue('id_adb_pull_file') + "  "
    cmd = cmd + handlerPara.getValue('id_adb_pull_save')
    #subprocess.call([cmd], shell=True)
    shellRun(handlerPara.getValue('id_setting_adb_path'),cmd)
    windowHandler.showWindow(True)


builder.setCtrlHandler('id_adb_pull_button', onAdbPullBtn)


def onAdbPullFileBtn(windowHandler, handlerPara):
    devicePath = handlerPara.getValue('id_adb_pull_file')
    if devicePath == '':
        devicePath = '/'
    DeviceFile.initFileManger(devicePath)
    returnOk, valueList = windowHandler.showForm(DeviceFile.deviceFile, True)
    if returnOk:
        windowHandler.setValue('id_adb_pull_file', valueList['return'])


builder.setCtrlHandler('id_adb_pull_file_btn', onAdbPullFileBtn)


def onAdbPush(windowHandler, handlerPara):
    hideAllPanel(windowHandler)
    windowHandler.showCtrl('pid_adb_push', True)

builder.setCtrlHandler('id_adb_push', onAdbPush)


def onAdbPushBtn(windowHandler, handlerPara):
    windowHandler.showWindow(False)
    cmd = 'adb push '
    cmd = cmd + handlerPara.getValue('id_adb_push_file') + "  "
    cmd = cmd + handlerPara.getValue('id_adb_push_folder')
    #subprocess.call([cmd], shell=True)
    shellRun(handlerPara.getValue('id_setting_adb_path'),cmd)
    windowHandler.showWindow(True)

builder.setCtrlHandler('id_adb_push_button', onAdbPushBtn)


def onAdbPushFolderBtn(windowHandler, handlerPara):
    devicePath = handlerPara.getValue('id_setting_adb_path')
    if devicePath == '':
        devicePath = '/'
    DeviceFile.initFileManger(devicePath)
    returnOk, valueList = windowHandler.showForm(DeviceFile.deviceFile, True)
    if returnOk:
         windowHandler.setValue('id_setting_adb_path', valueList['return'])


builder.setCtrlHandler('id_adb_push_folder_btn', onAdbPushFolderBtn)

valueList = FormUI.loadCachedValue(os.path.expanduser('~') + "/.adbgui.cfg")
if 'id_setting_adb_path' in valueList.keys():
    builder.setCtrlAttribute('id_setting_adb_path','value', valueList['id_setting_adb_path'])
builder.updateValue(valueList)
# Show FormUI
formUI = FormUI(builder)
formUI.show()
