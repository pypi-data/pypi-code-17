import pyudev
import ctypes
import os
import time

def copy_files(dirname):
    return ""


def main():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('block')
    for device in iter(monitor.poll, None):
        if 'ID_FS_TYPE' in device and device.action == 'add':
            print('{0} partition {1}'.format(device.action,device.get('ID_FS_LABEL')))
            time.sleep(5)
            for l in file('/proc/mounts'):
                if device.device_node in l:
                    x = l.split(' ')[1]
                    if dirname in os.listdir(x):
                        copy_files(x+"/"+dirname)
            

if __name__ == '__main__':
    main()
