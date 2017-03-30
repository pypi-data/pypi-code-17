import os
import re
import logging
import shutil
import datetime
import time
import subprocess
from subprocess import CalledProcessError

from mimetypes import MimeTypes

class Utils(object):
    """
    Utility classes
    """

    mime = None

    @staticmethod
    def get_folder_size(folder):
        """
        Get directory path full size

        :param folder: directory path
        :type folder: str
        """
        if not os.path.exists(folder):
            return -1
        folder_size = 0
        for (path, dirs, files) in os.walk(folder):
            for ffile in files:
                filename = os.path.join(path, ffile)
                folder_size += os.path.getsize(filename)
        return folder_size

    @staticmethod
    def detect_format(filename):
        """
        try to detect file format by extension
        """
        if Utils.mime is None:
            Utils.mime = MimeTypes()
            mimesfile = os.path.join(os.path.dirname(__file__), 'mimes-bio.txt')
            Utils.mime.read(mimesfile, True)
        return Utils.mime.guess_type(filename, True)

    @staticmethod
    def get_more_recent_file(files):
        """
        Return the date of the most recent file in list.

        Each file is a dict like with (at least) parameters: year, month, day
        """
        release = None
        for rfile in files:
            if release is None:
                release = {'year': rfile['year'], 'month': rfile['month'], 'day': rfile['day']}
            else:
                rel_date = datetime.date(int(release['year']), int(release['month']), int(release['day']))
                file_date = datetime.date(int(rfile['year']), int(rfile['month']), int(rfile['day']))
                if file_date > rel_date:
                    release['year'] = rfile['year']
                    release['month'] = rfile['month']
                    release['day'] = rfile['day']
        return release

    @staticmethod
    def month_to_num(date):
        return{
              'Jan': 1,
              'Feb': 2,
              'Mar': 3,
              'Apr': 4,
              'May': 5,
              'Jun': 6,
              'Jul': 7,
              'Aug': 8,
              'Sep': 9,
              'Oct': 10,
              'Nov': 11,
              'Dec': 12,
              '01': 1,
              '02': 2,
              '03': 3,
              '04': 4,
              '05': 5,
              '06': 6,
              '07': 7,
              '08': 8,
              '09': 9,
              '10': 10,
              '11': 11,
              '12': 12
             }[date]

    @staticmethod
    def copy_files(files_to_copy, to_dir, move=False, lock=None):
        """
        Copy or move files to to_dir, keeping directory structure.

        Copy keeps the original file stats.
        Files should have attributes name and root:
        - root: root directory
        - name: relative path of file in root directory

        /root/file/file1 will be copied in to_dir/file/file1

        :param files_to_copy: list of files to copy
        :type files_to_copy: list
        :param to_dir: destination directory
        :type to_dir: str
        :param move: move instead of copy
        :type move: bool
        :param lock: thread lock object for multi-threads
        :type lock: Lock
        """
        logger = logging.getLogger('biomaj')
        nb_files = len(files_to_copy)
        cur_files = 1
        for file_to_copy in files_to_copy:
            logger.debug(str(cur_files) + '/' + str(nb_files) + ' copy file ' + file_to_copy['name'])
            cur_files += 1
            from_file = file_to_copy['root'] + '/' + file_to_copy['name']
            to_file = to_dir + '/' + file_to_copy['name']
            if lock is not None:
                lock.acquire()
                try:
                    if not os.path.exists(os.path.dirname(to_file)):
                        os.makedirs(os.path.dirname(to_file))
                except Exception as e:
                    logger.error(e)
                finally:
                    lock.release()

            else:
                if not os.path.exists(os.path.dirname(to_file)):
                    try:
                        os.makedirs(os.path.dirname(to_file))
                    except Exception as e:
                        logger.error(e)
            if move:
                shutil.move(from_file, to_file)
            else:
                start_time = datetime.datetime.now()
                start_time = time.mktime(start_time.timetuple())
                shutil.copyfile(from_file, to_file)
                end_time = datetime.datetime.now()
                end_time = time.mktime(end_time.timetuple())
                file_to_copy['download_time'] = end_time - start_time
                shutil.copystat(from_file, to_file)

    @staticmethod
    def copy_files_with_regexp(from_dir, to_dir, regexps, move=False, lock=None):
        """
        Copy or move files from from_dir to to_dir matching regexps.
        Copy keeps the original file stats.

        :param from_dir: origin directory
        :type from_dir: str
        :param to_dir: destination directory
        :type to_dir: str
        :param regexps: list of regular expressions that files in from_dir should match to be copied
        :type regexps: list
        :param move: move instead of copy
        :type move: bool
        :param lock: thread lock object for multi-threads
        :type lock: Lock
        :return: list of copied files with their size
        """
        logger = logging.getLogger('biomaj')
        files_to_copy = []
        for root, dirs, files in os.walk(from_dir, topdown=True):
            for name in files:
                for reg in regexps:
                    file_relative_path = os.path.join(root, name).replace(from_dir, '')
                    if file_relative_path.startswith('/'):
                        file_relative_path = file_relative_path.replace('/', '', 1)
                    if reg == "**/*":
                        files_to_copy.append({'name': file_relative_path})
                        continue
                    if re.match(reg, file_relative_path):
                        files_to_copy.append({'name': file_relative_path})
                        continue

        for file_to_copy in files_to_copy:
            from_file = from_dir + '/' + file_to_copy['name']
            to_file = to_dir + '/' + file_to_copy['name']

            if lock is not None:
                lock.acquire()
                try:
                    if not os.path.exists(os.path.dirname(to_file)):
                        os.makedirs(os.path.dirname(to_file))
                except Exception as e:
                    logger.error(e)
                finally:
                    lock.release()
            else:
                if not os.path.exists(os.path.dirname(to_file)):
                    os.makedirs(os.path.dirname(to_file))
            if move:
                shutil.move(from_file, to_file)
            else:
                shutil.copyfile(from_file, to_file)
                shutil.copystat(from_file, to_file)
            file_to_copy['size'] = os.path.getsize(to_file)
            f_stat = datetime.datetime.fromtimestamp(os.path.getmtime(to_file))
            file_to_copy['year'] = str(f_stat.year)
            file_to_copy['month'] = str(f_stat.month)
            file_to_copy['day'] = str(f_stat.day)
            (file_format, encoding) = Utils.detect_format(to_file)
            file_to_copy['format'] = file_format
        return files_to_copy

    @staticmethod
    def uncompress(archivefile, remove=True):
        """
        Test if file is an archive, and uncompress it
        Remove archive file if specified

        :param file: full path to file to check and uncompress
        :type file: str
        :param remove: remove archive if present
        :type remove: bool
        :return: True if ok, False if an error occured
        """
        is_archive = False
        logger = logging.getLogger('biomaj')
        try:
            if archivefile.endswith('.tar.gz'):
                subprocess.check_call("tar xfz " + archivefile + " --overwrite -C " + os.path.dirname(archivefile), shell=True)
                is_archive = True
            elif archivefile.endswith('.tar'):
                subprocess.check_call("tar xf " + archivefile + " --overwrite -C " + os.path.dirname(archivefile), shell=True)
                is_archive = True
            elif archivefile.endswith('.bz2'):
                subprocess.check_call("tar xjf " + archivefile + " --overwrite -C " + os.path.dirname(archivefile), shell=True)
                is_archive = True
            elif archivefile.endswith('.gz'):
                subprocess.check_call("gunzip -f " + archivefile, shell=True)
                is_archive = True
            elif archivefile.endswith('.zip'):
                subprocess.check_call("unzip -o " + archivefile + " -d " + os.path.dirname(archivefile), shell=True)
                is_archive = True
        except CalledProcessError as uncompresserror:
            logger.error("Uncompress error of %s: %s" % (archivefile, str(uncompresserror)))
            return False

        if is_archive:
            logger.debug('Uncompress:uncompress:' + archivefile)

        if is_archive and remove and os.path.exists(archivefile):
            os.remove(archivefile)

        return True
