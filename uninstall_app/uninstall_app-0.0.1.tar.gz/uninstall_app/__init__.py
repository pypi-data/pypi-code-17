#!/usr/bin/env python
# encoding=utf-8
import os;

# 删除所有你指定包名的 APP
def clear1( ):
    print 'start delete all your app in your simulator '
    os.popen('adb wait-for-device');
    corename = raw_input("input your app package corename:")
    oriPackages = os.popen('adb shell pm list packages {name}'.format(name=corename));
    # list all PackageName
    for oriPackage in oriPackages:
        deletePackage = oriPackage.split(':')[1]
        os.popen('adb uninstall ' + deletePackage );
        print deletePackage + "is deleted"

def clear2( ):
    print 'start uninstall...'
    os.popen('adb wait-for-device');
    packages = os.popen('adb shell pm list packages -3');
    for package in packages.readlines():
        packageName = package.split(':')[-1].splitlines()[0];
        os.popen('adb uninstall ' + packageName );
        print packageName,'uninstall successed';
    print 'uninstall all successed...'
        
 
# 清除 LogCat 缓存   
def clear3( ):
    print 'start clear logcat buffer in your Phone or Simulator'
    os.popen('adb wait-for-device');
    os.popen('adb logcat -c');
    print 'logcat is cleared success'     