#Academic Torrents API

#Copyright (C) [2017] Ronald D. Barrios

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

"""
Academic Torrents Application Programming Interface
Features:
- Initialize a libtorrent session by instantiating an object of the Client Class.
- Add torrents to the libtorrent session.
- Query the torrent handler for downloading information of a single torrent.
- Process the torrent handler for downloading multiple torrents/
- Straightforward get function for simple direct download of a single torrent
  file with no information about subfiles.
- Set priorities for downloading in case of multiple files within a single
  torrent.
"""

from __future__ import absolute_import
import os
import warnings
import time
import sys
import six
from prior import PriorityApp, get_so

try:
    import curses
except ImportError:
    if os.name == 'nt':
        pass

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import libtorrent as lt


class Client(object):
    """ Class that initializes a libtorrent session.

    Attributes:
        ses: An object that represents the libtorrent session
        defaults: A dictionary that keeps default values for the session
    """

    def __init__(self, port=6881, max_download_rate=0, max_upload_rate=0,
                 save_path='.', proxy_host=''):
        """ Contructor that initializes the libtorrent session.

        Sets the ports range whereby downloaded data will flow. It does
        the conversion of the max upload and download rate from KB/s
        to B/s and inserts these in the dictionary of default values.
        After that, those default values are added to the session. Same
        applies to proxy connection and save_path.

        Args:
            port: an int in the range of 0 to 65525 to make a range up to 65535.
            max_download_rate: an int that assigns the maximum rate of
                downloading in KB/s. 0 means infinite.
            max_upload_rate: an int that assigns the maximum rate of
                uploading in KB/s. 0 means infinite.
            save_path: a string that specifies the destination location in the
            file system of the downloaded files.
            proxy_host: a string with information about the http proxy and its
            port to use separated by a colon.
        """

        self.ses = lt.session()
        self.defaults = {'port': 6881}

        if port < 0 or port > 65525:
            self.ses.listen_on(self.defaults['port'], self.defaults['port'] + 10)
        else:
            self.ses.listen_on(port, port+10)
            self.defaults['port'] = port

        max_upload_rate *= 1000
        max_download_rate *= 1000

        if max_upload_rate <= 0:
            max_upload_rate = -1
        if max_download_rate <= 0:
            max_download_rate = -1

        if proxy_host != '':
            ps = lt.proxy_settings()
            ps.type = lt.proxy_type.http
            ps.hostname = proxy_host.split(':')[0]
            ps.port = int(proxy_host.split(':')[1])
            self.ses.set_proxy(ps)

        self.defaults['max_download_rate'] = max_download_rate
        self.defaults['max_upload_rate'] = max_upload_rate
        self.defaults['save_path'] = save_path
        self.defaults['proxy_host'] = proxy_host

        self.ses.set_download_rate_limit(int(max_download_rate))
        self.ses.set_upload_rate_limit(int(max_upload_rate))
        self.ses.set_settings(lt.session_settings())
        self.ses.set_alert_mask(0xfffffff)

    def add_torrent(self, torrent_files):
        """ Adds torrent files to the libtorrent session.

        Receives a list that contains various paths of torrents files and creates
        a dictionary to store the downloading configuration. It resumes the
        downloading process in case of a previous download job that did not
        finish or that actually finished by updating the resume_data in the
        atp configuration dictionary. Creates a torrent handler h for querying
        information that is then appended to a handles list.

        Args:
            torrent_files: a list of strings containing the path to torrent files
                inside the local file system or as an http link in a website or
                as a magnet link.

        Returns:
            a list of torrent handlers objects suitable for querying progress
            information about the torrent while downloading or after it while
            seeding.
        """

        handles = []
        for tf in torrent_files:
            atp = {}
            atp['save_path'] = self.defaults['save_path']
            atp['storage_mode'] = lt.storage_mode_t.storage_mode_sparse
            atp['paused'] = False
            atp['auto_managed'] = True
            atp['duplicate_is_error'] = True

            if (tf.startswith('magnet:') or tf.startswith('http://') or
                    tf.startswith('https://')):
                atp['url'] = tf
            else:
                info = lt.torrent_info(tf)

                try:
                    resume_path = os.path.join(self.defaults['save_path'],
                                               info.name() + '.fastresume')
                    atp['resume_data'] = open(resume_path, 'rb').read()
                except:
                    pass

                atp['ti'] = info

            h = self.ses.add_torrent(atp)
            h.set_max_connections(60)
            h.set_max_uploads(-1)
            handles.append(h)
        return handles

    def query_handle_sp(self, h):
        """ Queries a single torrent handler object.

        Prints in terminal an updated row with download information: progress,
        download_rate, upload_rate, number of peers, number of seeds, number of
        distributed copies and a state. The state can take any value of the
        following: queued, checking, downloading metadata, downloading, finished,
        seeding, allocating and checking fastresume. In case there are alerts to
        pop from libtorrent to be displayed, they are also printed. After data
        is retrieved, application sleeps for 1 s and repeats until downloading
        is finished.

        Args:
            h: a libtorrent torrent handler object.
        """

        while not h.is_finished():
            s = h.status()

            state_str = ['queued', 'checking', 'downloading metadata',
                         'downloading', 'finished', 'seeding', 'allocating',
                         'checking fastresume']
            six.print_('\r%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: '
                       '%d seeds: %d distributed copies: %d) %s' %
                       (s.progress * 100, s.download_rate / 1000,
                        s.upload_rate / 1000, s.num_peers, s.num_seeds,
                        s.distributed_copies, state_str[s.state].ljust(20)),
                       end=' ')

            alerts = self.ses.pop_alerts()
            for a in alerts:
                if a.category() & lt.alert.category_t.error_notification:
                    six.print_(a)

            sys.stdout.flush()
            time.sleep(1)

        six.print_('\n', h.name(), 'complete')

    def process_handles(self, handles):
        """ Queries a list with multiple libtorrent torrent handlers.

        By using the curses library, this method prints multiline information
        about each torrent handler (one line per handler object). Data retrieved
        from the query is the same as in the case of the query_handle_sp method.
        This method sleeps for one second as well and repeats the process.

        Args:
            handles: a list of libtorrent torrent handler objects.
        """

        state_str = ['queued', 'checking', 'downloading metadata',
                     'downloading', 'finished', 'seeding',
                     'allocating', 'checking fastresume']
        stdscr = curses.initscr()
        while any(not hand.is_finished() for hand in handles):
            stdscr.erase()
            for h in handles:
                s = h.status()
                stdscr.addstr("{name} {progress}{padding}{percent}% "
                              "complete(down: {down} kB/s up: {up} kB/s peers: "
                              "{peers} seeds: {seeds} copies: "
                              "{distributed_copies}) {state}\n".format(
                                  name=h.name(),
                                  progress="#" * int(s.progress*10),
                                  padding=" " * (10 - int(s.progress*10)),
                                  percent=round(s.progress*100, 2),
                                  down=s.download_rate / 1000,
                                  up=s.upload_rate / 1000,
                                  peers=s.num_peers,
                                  seeds=s.num_seeds,
                                  distributed_copies=round(s.distributed_copies),
                                  state=state_str[s.state]
                                  ))
                alerts = self.ses.pop_alerts()
                for a in alerts:
                    if a.category() & lt.alert.category_t.error_notification:
                        if isinstance(a, str):
                            stdscr.addstr(a)
                        else:
                            pass
                time.sleep(1)
            stdscr.refresh()
        curses.endwin()

    def getmodes(self, handles):
        """ Gets a list with the filenames or top level root directories.

        By receiving a list of torrent handlers, the method queries the name for
        each element of the list. If the target to download is a single file,
        the filename will be retrieved. If the target is a directory containing
        multiple files, then the directory name is retrieved. Each name is
        appended to a list which is returned finalizing the method.

        Ags:
            handles: a list of libtorrent torrent handler objects.

        Returns:
            A list with the target names to download
        """

        names = []
        for h in handles:
            if h.has_metadata():
                names.append(h.name())
            else:
                names.append('-')
        return names

    def getpriorities(self, h):
        """ Returns a list with the priorities of all files within the target.

        There are 8 different priority levels:
        0. piece is not downloaded at all
        1. normal priority. Download order is dependent on availability.
        2. higher than normal priority. Pieces are preferred over pieces with
           the same availability, but not over pieces with lower availability.
        3. pieces are as likely to be picked as partial pieces.
        4. pieces are preferred over partial pieces, but not over pieces with
           lower availability.
        5. currently the same as 4.
        6. piece is as likely to be picked as any piece with availability 1.
        7. maximum priority, availability is disregarded, the piece is preferred
           over any other piece with lower priority.

        Args:
            h: a libtorrent torrent handler object.

        Returns:
            A list with the priorities of all files within a single torrent.
        """

        if h.has_metadata():
            return h.file_priorities()
        return 0

    def setpriorities(self, h, priorityList):
        """ Sets the downloading priority of all files.

        Args:
            h: a libtorrent torrent handler object.
            priorityList: a list with int elements in the range 0-7. See full
            specification in the getpriorities method.
        """

        if h.has_metadata():
            h.prioritize_files(priorityList)

    def prioritize_file(self, h, fileIndex, priorityIndex):
        """ Sets the priority index for just one of the files.

        Args:
            h: a libtorrent torrent handler object.
            fileIndex: the index position of the file which priority is desired
            to change.
            priorityIndex: an int in the range 0-7.
        """

        if h.has_metadata():
            h.file_priority(fileIndex, priorityIndex)

    def run_set_priorities(self, handles):
        """ Runs npyscreen application to set the priorities of various torrent
        handlers.

        Args:
            handles: a list of libtorrent torrent handler objects.
        """

        if any(hand.get_torrent_info().num_files() > 1 for hand in handles):
            pApp = PriorityApp()
            pApp.set_handler(handles)
            pApp.run()

            for h, pl in get_so().items():
                if h.has_metadata():
                    h.prioritize_files(pl)


def get(tf):
    """ Downloads a single torrent file by a simple get() client method.

    No need for the API user to write bolierplate code for Client() object
    instantiation, torrent adding and name retrieving.

    Args:
        tf: a string that represents the path of the .torrent file.
    """

    client = Client()
    handles = client.add_torrent([tf])
    filenames = client.getmodes(handles)
    client.query_handle_sp(handles[0])
    return filenames[0]


def version():
    """ Returns App Version Number."""

    return 'Academic Torrents Version 1.10'


def release_info():
    """ Prints environment variable information and application versioning."""

    six.print_('LD_LIBRARY PATH set to: ', os.environ['LD_LIBRARY_PATH'])
    six.print_('PKG_CONFIG_PATH set to: ', os.environ['PKG_CONFIG_PATH'])
    six.print_('Libtorrent Version Installed is: ' + lt.version)
    six.print_(version())


if __name__ == "__main__": # pragma: no cover
    release_info()
