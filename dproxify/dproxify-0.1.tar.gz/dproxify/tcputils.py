# tcp utility functions
# Written by nature through Francesco Palumbo aka phranz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import socket
import struct
import select


class SocketMessageReadException(Exception):
    Exception
    pass


class SocketMessageWriteException(Exception):
    pass


def msgread(sock, decode=False):
    '''
    Reads a message from a connected tcp socket.
    The max size of the message is 2^32 bit.

    Keyword arguments:

    decode -- if True, returns UTF-8 encoded message. Defaults to False.
    '''

    def readsock(s, n):
        d     = bytes()
        count = 0

        while count < n:
            rd, wr, e = select.select((s,), (), ())

            if rd:
                d += s.recv(n - count)

            if not d:
                raise SocketMessageReadException('recv returned 0')

            count += len(d)

        return d

    msglen = struct.unpack('!L', readsock(sock, 4))[0]

    res = readsock(sock, msglen)

    if decode:
        res = res.decode()

    return res


def msgwrite(sock, msg, encode=False):
    '''
    Writes a message into a connected tcp socket.
    The max size of message is 2^32 bit.

    Keyword arguments:

    encode -- if True, UTF-8 encode the message. Defaults to False.
    '''

    def writesock(s, m):
        total = 0
        sent  = 0
        mlen  = len(m)

        while total < mlen:
            rd, wr, e = select.select((), (s,), ())

            if wr:
                sent = s.send(m[total:])

            if not sent:
                raise SocketMessageWriteException('send returned 0')

            total += sent

        else:
            return total

    msg    = msg.encode() if encode else msg
    msglen = len(msg)
    msglen = struct.pack('!L', msglen)

    writesock(sock, msglen) and writesock(sock, msg)


def make_UDS_socket_client(sockpath, autoconnect=True):
    '''
    Returns an AFUnix client socket.

    Arguments:

    sockpath -- the socket file path.

    autoconnect -- if True, calls connect on the socket
                   before returning it. Defaults to True.
    '''

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    if autoconnect:
        sock.connect(sockpath)

    return sock


def make_UDS_socket_server(sockpath, autolisten=True):
    '''
    Returns an AFUnix server socket.

    Arguments:

    sockpath -- the socket file path.

    autolisten -- if True, calls listen(1) on the socket
                  before returning it. Defaults to True.
    '''

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(sockpath)

    if autolisten:
        sock.listen(1)

    return sock
