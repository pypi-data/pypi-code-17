import datetime
import hashlib
import shutil
import time
import sys
import os


class FileTransfer:
    """
    Interface for moving local files from
    one directory to another without duplicates
    """

    default_source_directory = os.path.abspath("test_source")
    default_target_directory = os.path.abspath("test_dest")

    # file hash set
    existing_hash_set = {}

    # pyudev variables
    try:
        import pyudev
        pyudev_available = True
        monitor = pyudev.Monitor.from_netlink(pyudev.Context())
        monitor.filter_by('block')
    except:
        pyudev_available = False

    def __init__(self, source_directory=default_source_directory,
                 target_directory=default_target_directory):
        """
        Initialize the transfer class, determining where
        to upload the files to
        """
        self.source_directory = source_directory
        self.target_directory = target_directory
        assert os.path.exists(self.source_directory), ("Cannot find source: %s" % source_directory)
        assert os.path.exists(self.target_directory), ("Cannot find target: %s" % target_directory)
        self.build_existing_file_set()

    def hash_text(self, text):
        """
        Takes in text and hashes it
        """
        hasher = hashlib.md5()
        hasher.update(text)
        return hasher.hexdigest()

    def build_existing_file_set(self):
        """
        Builds a set of hashes for the files that
        we have already seen
        """
        # initialize an empty set of hashes
        file_hash_set = set()

        # walk through the file tree
        for file_dir, _, file_list in os.walk(self.target_directory):

            # add each value to our set
            for fname in file_list:
                file_hash = self.hash_text(open(os.path.join(file_dir, fname)).read())
                file_hash_set.add(file_hash)

        # update the set of existing hashes
        self.existing_hash_set = file_hash_set

    def file_destination_from_name(self, fname):
        """
        Takes in a file name and determines where it should be
        sent
        """
        relative_path = fname.replace(self.source_directory, "").strip("/")
        date_prefix = datetime.datetime.now().strftime("%b %d %y/")
        return os.path.join(self.target_directory, date_prefix, relative_path)

    def upload_file(self, fname, contents):
        """
        Uploads a file named fname into
        the new directory
        """
        destination = self.file_destination_from_name(fname)
        os.makedirs(os.path.dirname(destination))
        with open(destination, "wb+") as f:
            f.write(contents)

    def copy_new_files(self):
        """
        Iterates through the files in the source directory
        and uploads new ones
        """
        for file_dir, _, file_list in os.walk(self.source_directory):

            # check to see if we need to add each file in the source dir
            for fname in file_list:

                # get the details of a file
                file_path = os.path.abspath(os.path.join(file_dir, fname))
                file_text = open(file_path).read()
                file_hash = self.hash_text(file_text)

                # if it is new upload the file
                if file_hash not in self.existing_hash_set:
                    self.upload_file(file_path, file_text)

                # mark that we have handled this file
                self.existing_hash_set.add(file_hash)

    def poll(self):
        """
        Polls a usb port and waits for it to be added
        """
        assert self.pyudev_available, "Pyudev unavailable!"
        for device in iter(monitor.poll, None):
            if 'ID_FS_TYPE' in device and device.action == 'add':
                time.sleep(5)
                for l in file('/proc/mounts'):
                    if device.device_node in l:
                        self.copy_new_files()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        ft = FileTransfer(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        ft = FileTransfer(sys.argv[1])
    else:
        ft = FileTransfer()
    # ft.poll()