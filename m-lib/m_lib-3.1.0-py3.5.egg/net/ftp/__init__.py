"""Broytman FTP Library for Python"""


__all__ = [
   "ftpparse", "ftpscan", "TelnetFTP"
]


from ftplib import FTP
from telnetlib import IAC


class TelnetFTP(FTP):
    def putline(self, line):
        line = line.replace(IAC, IAC+IAC)
        FTP.putline(self, line)
