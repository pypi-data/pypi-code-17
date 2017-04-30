import os
import time
import shutil
import hashlib
import datetime

try:
    import pyudev
    PYUDEV = True
except:
    PYUDEV = False


class FileTransfer(object):

    def hash_text(self, text):
        self.hasher = hashlib.md5()
        self.hasher.update(text)
        return self.hasher.hexdigest()

    def print_dictionary(self):
        for key, value in self.file_dictionary.items():
            print "Hash Name: " + key + " File Name: " + value


    def create_dictionary(self):
        for dirName, subdirList, fileList in os.walk(self.target_directory):
            for fname in fileList:
                with open(os.path.join(dirName, fname), 'r') as myfile:
                    hash_name = self.hash_text(myfile.read())
                    self.file_dictionary[fname + hash_name] = fname

        self.print_dictionary()


    def copy_files(self):
        target = os.path.join(self.target_directory, datetime.datetime.now().strftime("%m-%d-%y %H-%M-%S"))
        if os.path.isdir(self.source_directory):
            shutil.copytree(self.source_directory, target)
        for dirName, subdirList, fileList in os.walk(target):
            for fname in fileList:
                with open(os.path.join(dirName, fname), 'r') as myfile:
                    hash_name = self.hash_text(myfile.read())
                    if (fname + hash_name) in self.file_dictionary.keys():
                        os.remove(os.path.join(dirName, fname))


    def main(self):
        assert PYUDEV, "Need PYUDEV to run this!"
        self.source = "test"
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by('block')
        for device in iter(monitor.poll, None):
            if 'ID_FS_TYPE' in device and device.action == 'add':
                print('{0} partition {1}'.format(device.action,device.get('ID_FS_LABEL')))
                time.sleep(5)
                for l in file('/proc/mounts'):
                    if device.device_node in l:
                        print l
                        x = l.split(' ')[1].replace('\\040',' ')
                        self.source_directory = x + "/" + self.source
                        self.target_directory = os.path.expanduser("~")+"/"+"Documents"
                        if self.source in os.listdir(x):
                            self.file_dictionary = {}
                            self.create_dictionary()
                            self.copy_files()
        
        
                
def run_filetransfer():
    FileTransfer().main()


if __name__ == '__main__':
    FileTransfer().main()
