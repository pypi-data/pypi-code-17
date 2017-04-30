'''
Insteon PLM TCP Python Library

https://github.com/heathbar/insteontcp


Published under the MIT license - See LICENSE file for more details.
'''

 # pylint: disable=missing-docstring
import threading
import time
import queue
import socket

import binascii

INSTEONTCP_CMD_TYPE_STANDARD = b'\x02\x62'
INSTEONTCP_CMD_TYPE_ALL_LINK = b'\x02\x61'

INSTEONTCP_CMD_INFO = 16 # 0x10
INSTEONTCP_CMD_TURN_ON = 17 # 0x11
INSTEONTCP_CMD_TURN_OFF = 19 # 0x13

INSTEONTCP_FLAG_STD_MSG = 15 # 0x0F
INSTEONTCP_FLAG_EXTENDED_MESSAGE = 16

INSTEONTCP_LEVEL_MAX = 255 # 0xFF
INSTEONTCP_LEVEL_ZERO = 0 # 0x00

INSTEONTCP_EVENT_LIGHT_SWITCH = 0
INSTEONTCP_EVENT_GROUP_SWITCH = 1
INSTEONTCP_EVENT_CLEANUP = 2

class InsteonTCP():
    
    def __init__(self, host, port=9761, event_callback=print, data_callback=print):
        self.__event_callback = event_callback
        self.__data_callback = data_callback

        self._queue = queue.Queue(maxsize=255)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((host, port))

        self._listener = threading.Thread(target=self.__message_listener)
        self._listener.daemon = True
        self._listener.start()

        self._sender = threading.Thread(target=self.__command_sender)
        self._sender.daemon = True
        self._sender.start()

    def info(self, id, callback):
        self.__standard_command(id, INSTEONTCP_CMD_INFO)
                
    def turn_on(self, id):
        self.__standard_command(id, INSTEONTCP_CMD_TURN_ON, INSTEONTCP_LEVEL_MAX)
        
    def turn_off(self, id):
        self.__standard_command(id, INSTEONTCP_CMD_TURN_OFF, INSTEONTCP_LEVEL_MAX)

    def activate_scene(self, group_number):
        self.__send_command(INSTEONTCP_CMD_TYPE_ALL_LINK + bytes.fromhex(group_number) + INSTEONTCP_CMD_TURN_ON + INSTEONTCP_LEVEL_ZERO)

    def __standard_command(self, id, cmd1, cmd2=INSTEONTCP_LEVEL_ZERO):
        self.__send_command(INSTEONTCP_CMD_TYPE_STANDARD + bytes.fromhex(id) + INSTEONTCP_FLAG_STD_MSG.to_bytes(1, byteorder='big') + cmd1.to_bytes(1, byteorder='big') + cmd2.to_bytes(1, byteorder='big'))

    def __send_command(self, cmd):
        self._queue.put(cmd)

    # processes the first event from data and returns the remainder (if any) of data
    def __process_next_event(self, data):
        message_type = data[1]
        
        if (message_type == 0x50):
            from_addr = binascii.hexlify(data[2:5]).decode("utf-8").upper()
            to_addr = binascii.hexlify(data[5:8]).decode("utf-8").upper()
            flags = data[8]
            cmd1 = data[9]
            cmd2 = data[10]

            self.__event_callback({'type': INSTEONTCP_EVENT_LIGHT_SWITCH, 'address': from_addr, 'cmd1': cmd1, 'cmd2': cmd2})
            self.__data_callback(data[0:11])
            return data[11:]
        elif (message_type == 0x58):
            self.__event_callback({'type': INSTEONTCP_EVENT_CLEANUP, 'status': data[2]})
            self.__data_callback(data[0:3])
            return data[3:]
        elif (message_type == 0x61):
            self.__event_callback({'type': INSTEONTCP_EVENT_GROUP_SWITCH, 'group': data[2], 'cmd': data[3]})
            self.__data_callback(data[0:6])
            return data[6:]  
        elif (message_type == 0x62):
            from_addr = binascii.hexlify(data[2:5]).decode("utf-8").upper()
            flags = data[5]
            cmd1 = data[6]
            cmd2 = data[7]

            if (flags & INSTEONTCP_FLAG_EXTENDED_MESSAGE):
                self.__data_callback(data[0:9])
                return data[23:]
            else:
                self.__data_callback(data[0:9])
                return data[9:]
        else:
            self.__data_callback(data)
            return []

    def __command_sender(self):
        """ Command sender. """

        while True:
            try:
                # this statement is blocking
                cmd = self._queue.get()
                self._sock.sendall(cmd)

                # Don't overload the hub or it skips commands
                time.sleep(0.1)            
            except:
                pass
    
    def __message_listener(self):
        """ message listener. """

        while True:
            try:
              # TODO: deal with the possibility that we didn't read an entire message
              data = self._sock.recv(64)

              while (len(data) > 0):
                  data = self.__process_next_event(data)  

            except:
                pass
