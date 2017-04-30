#Academic Torrents Unit Tests

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

""" Academic Torrents Unit Tests
Features:
- TestGet Class tests simple at_get() function.
- TestClient Class tests whole Client class plus npyscreen console display.
- TestConsole Class tests urwid console interface.
"""

import unittest
import os
import sys
import six
import academictorrents as at
import console


class TestGet(unittest.TestCase):
    """ This class tests the get function call.

    This is the preferred function to use for downloading a single torrent
    without too much boilerplate code from Client Class.
    """

    def test_download_at_get(self):
        """Try downloading a torrent from Academic Torrents
        and check if it successfully finishes downloading
        until a complete message shows as final output
        """

        filename = at.get('2269d7d1c77375aea732eea0905e370d4741575f.torrent')
        six.print_('\n', 'Check out the downloaded file in ' + os.getcwd(), '\n')
        self.assertEqual(filename, six.text_type('Race-Results.zip'))
        self.assertTrue(os.path.isfile('Race-Results.zip'))


class TestClient(unittest.TestCase):
    """ This class tests various downloading options that are only available in
    the Client Class.
    """

    def test_download_magnet(self):
        """Try downloading a magnet link from Academic Torrents
        and check if it successfully finishes downloading
        until a complete message shows as final output
        """

        # testing with wrong port 80000 which defaults to a valid ports range
        client = at.Client(port=80000)
        magnet_link = ('magnet:?xt=urn:btih:323a0048d87ca79b68f12a6350a57776b6a3'
                       'b7fb&tr=http%3A%2F%2Facademictorrents.com%2Fannounce.php'
                       '&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80%2Fannounce&tr='
                       'udp%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce')
        handles = client.add_torrent([magnet_link])
        filename = client.getmodes(handles)
        # filename is not available in the case of magnet
        # link before downloading is complete
        self.assertEqual(filename[0], six.text_type('-'))
        # Download must be completed first; otherwise, getpriorities
        # will return 0
        self.assertEqual(client.getpriorities(handles[0]), 0)
        client.query_handle_sp(handles[0])
        filename = client.getmodes(handles)
        six.print_('\n', 'Check out the downloaded file in ' + os.getcwd(), '\n')
        self.assertEqual(filename[0], six.text_type('mnist.pkl.gz'))
        self.assertTrue(os.path.isfile('mnist.pkl.gz'))

    def test_download_http(self):
        """Try downloading a torrent from a URL and check if it
        successfully finishes downloading until a complete message
        shows as final output
        """

        # testing with wrong port -50 which defaults to a valid ports range
        client = at.Client(port=-50)
        http_url = ('http://academictorrents.com/download/4cdade8fa3c6d451441fda'
                    '7ae19bb53537b6ee21.torrent')
        handles = client.add_torrent([http_url])
        filename = client.getmodes(handles)
        # filename is not available in the case of http url before downloading
        # is complete.
        self.assertEqual(filename[0], six.text_type('-'))
        # Download must be completed first; otherwise, getpriorities will
        # return 0
        self.assertEqual(client.getpriorities(handles[0]), 0)
        client.query_handle_sp(handles[0])
        filename = client.getmodes(handles)
        six.print_('\n', 'Check out the downloaded file in ' +
                   os.getcwd(), '\n')
        self.assertEqual(filename[0],
                         six.text_type('devinberg.com_471592PB.pdf'))
        self.assertTrue(os.path.isfile('devinberg.com_471592PB.pdf'))

    def test_set_priorities(self):
        """ Try downloading from a torrent file and check if the
        setpriorities and getpriorities() methods set and return
        correct lists of priorities. Also check if the train-labels
        file was correctly downloaded (1 means download and 0 means
        do not download)."""

        client = at.Client()
        torrent_file = '42714f859770f1a9d8b27985f9f16ea17e8ba2f6.torrent'
        handles = client.add_torrent([torrent_file])
        client.setpriorities(handles[0], [0, 1, 0])
        expected_after_set = [0, 1, 0]
        self.assertListEqual(client.getpriorities(handles[0]),
                             expected_after_set)
        client.query_handle_sp(handles[0])
        six.print_('\n', 'Check out the downloaded file in ' + os.getcwd(), '\n')
        self.assertTrue(os.path.isfile(os.path.join(os.getcwd(),
                                                    'files',
                                                    'train-labels.tif')))
        self.assertEquals(os.path.getsize(os.path.join(os.getcwd(), 'files',
                                                       'train-labels.tif')),
                          7869573, msg='download size is incomplete')

    def test_prioritize_file(self):
        """ Try downloading from a torrent file and check if the
        prioritize_file and getpriorities() methods set and return
        correct lists of priorities. Also check if the train-labels
        file was correctly downloaded (1 means download and 0 means
        do not download)."""

        client = at.Client()
        torrent_file = '1d16994c70b7fff8bfe917f83c397b1193daee7f.torrent'
        handles = client.add_torrent([torrent_file])
        client.prioritize_file(handles[0], 0, 0)
        client.prioritize_file(handles[0], 1, 0)
        expected_after_set = [0, 0, 1]
        self.assertListEqual(client.getpriorities(handles[0]),
                             expected_after_set)
        client.query_handle_sp(handles[0])
        six.print_('\n', 'Check out the downloaded file in ' +
                   os.getcwd(), '\n')
        self.assertTrue(os.path.isfile(os.path.join(os.getcwd(),
                                                    'coil-20',
                                                    'coil-20.ps.zip')))
        self.assertEquals(os.path.getsize(os.path.join(os.getcwd(), 'coil-20',
                                                       'coil-20.ps.zip')),
                          442932, msg='download size is incomplete')

    @unittest.skipUnless(sys.platform.startswith('linux'), 'requires Linux')
    def test_process_handles(self):
        """ This is a npyscreen and curses libraries test, so it is
        only available for POSIX systems. The goal is to check if the
        user can visualize actual displayss for establishing downloading
        priorities by using npyscreen library and for downloading
        multiple files by using curses library respectively"""

        client = at.Client()
        torrent_list = ['3efc53f35d49669b89039f2b4ec9de11ec1d73fd.torrent',
                        'ce990b28668abf16480b8b906640a6cd7e3b8b21.torrent']
        handles = client.add_torrent(torrent_list)
        client.run_set_priorities(handles)
        client.process_handles(handles)
        six.print_('\n', 'Check out the downloaded files in ' + os.getcwd(), '\n')

    def test_path_info_and_versioning(self):
        """ This is only a look and check test. The goal here is to make
        sure the environment variables for academictorrents such as
        LD_LIBRARY_PATH and PKG_CONFIG_PATH were correctly set"""

        at.release_info()


class TestConsole(unittest.TestCase):
    """ This class tests urwid menus and browser window."""

    @unittest.skipUnless(sys.platform.startswith('linux'), 'requires Linux')
    def test_at_navigation(self):
        """ Testing of Presentation Cover and Navigation Menu of
        Academic Torrents"""

        console.Presentation().main()
        selected_option = console.NavigationMenu().main()
        pool_of_options = ('from .torrent', 'from URL', 'from infohash',
                           'Appearance', 'Lock Screen')
        self.assertIn(selected_option, pool_of_options,
                      msg='selected option is not in tuple')

    @unittest.skipUnless(sys.platform.startswith('linux'), 'requires Linux')
    def test_at_browser(self):
        """ Testing of Directory Browser of Academic Torrents"""

        torrent_files = console.DirectoryBrowser().main()
        six.print_('These are the selected files:')
        six.print_(torrent_files)


if __name__ == '__main__': # pragma: no cover
    unittest.main()
