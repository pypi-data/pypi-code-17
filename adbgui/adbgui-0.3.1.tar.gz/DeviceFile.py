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

def getAdbLs(path):
    choise = ''
    if path != '/':
        choise = '..'
    fileList = commands.getstatusoutput("adb shell ls -F " + path)[1]
    fileList = fileList.strip()
    fileList = fileList.split('\r\n')
    for file in fileList:
        if file.find('Permission denied') < 0:
            if choise != '':
                choise = choise + ";"
            choise = choise + file
    return choise
#Load layout xml file
deviceFile = Builder()
deviceFile.loadLayout(os.path.split(os.path.realpath(__file__))[0] + os.path.sep + 'devicefile.xml')


def getCurrentPath(handlerPara):
    path = handlerPara.getValue('id_current_dir')
    select = handlerPara.getValue('id_file_manager')
    bFolder = True
    if select == '..':
        if path != '/':
            path = path[0:-1]
            path = path[:path.rfind('/') + 1]
    else:
        type = select[0:select.find(' ')]
        select = select[select.find(' ') + 1:]
        if 'd' in type:
            path = path + select + "/"
        else:
            bFolder = False
            path = path + select
    return bFolder,path

def onUpdateFileManger(windowHandler, handlerPara):
    if handlerPara.getEventType() == 'evt_listbox_dclick':
        bFolder,path = getCurrentPath(handlerPara)
        if not bFolder:
            return
        initFileManger(path)
        windowHandler.update(deviceFile,False)
deviceFile.setCtrlHandler('id_file_manager', onUpdateFileManger)

def ondeviceFileOK(windowHandler, handlerPara):
    bFolder,deviceFileReturn = getCurrentPath(handlerPara)
    handlerPara.valueList['return'] = deviceFileReturn
    windowHandler.closeWindow(True)
deviceFile.setCtrlHandler('id_deviceFile_ok', ondeviceFileOK)

def initFileManger(path):
    deviceFile.setCtrlAttribute('id_file_manager', 'choices', getAdbLs(path))
    deviceFile.setCtrlAttribute('id_current_dir', 'value', path)
initFileManger('/')