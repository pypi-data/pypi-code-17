raise TecplotNotImplementedError
'''
# place-holder for remote access to 360 from PyTecplot
from ..exception import TecplotError


class TecUtilRemote(object):
    def __init__(self, socket):
        self.socket = socket

    def _send_recv(self, cmd, *args):
        msg = cmd
        for a in args:
            msg += '|' + a
        self.socket.send(msg.encode())
        result = self.socket.recv(4096).decode()
        if result.startswith('ERROR|'):
            raise TecplotError(result[6:])
        else:
            return result

    def NewLayout(self):
        return self._send_recv('NewLayout') == 'true'

    def MacroExecuteCommand(self, command):
        result = self._send_recv('MacroExecuteCommand', command)
        return result == 'true'
'''
