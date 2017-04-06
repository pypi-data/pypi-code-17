#    This file is part of PYTHorrent.
#
#    PYTHorrent is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PYTHorrent is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PYTHorrent.  If not, see <http://www.gnu.org/licenses/>.

def splice(s, n):
    """Split apart a string at a particular length"""
    return [ s[i:i+n] for i in range(0, len(s), n) ]

class BitTorrentException(Exception):
    pass

from .torrent import Torrent, TorrentClient
from .peer import Peer, BitTorrentPeerException
from .peer_stores import store_from_url, TrackerException, \
    HTTPTracker, UDPTracker
from .pieces import PieceLocal, PieceRemote

