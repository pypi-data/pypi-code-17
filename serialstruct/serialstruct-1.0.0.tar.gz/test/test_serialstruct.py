import os
import serial
import struct
import sys
import time
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import serialstruct

# on which port should the tests be performed:
PORT = 'loop://'

class Test_serialstruct(unittest.TestCase):
    """Test seriastruct related functionality"""

    def test_structured_packet(self):
        """simple test of structured packet class"""

        class TestStructuredPacket(serialstruct.StructuredPacket):

            DATA_SIZE = 8

            def __init__(self):
                super(TestStructuredPacket, self).__init__(self.DATA_SIZE)
                self.received_packets = []

            def handle_packet(self, packet):
                self.received_packets.append(packet)

            def send_packet(self, packet):
                self.transport.write(self.HEADER)
                self.transport.write(packet)

        ser = serial.serial_for_url(PORT, baudrate=115200, timeout=1)
        with serial.threaded.ReaderThread(ser, TestStructuredPacket) as protocol:
            protocol.send_packet(struct.pack("2I", *[1, 2]))
            protocol.send_packet(struct.pack("2I", *[3, 4]))
            time.sleep(1)
            self.assertEqual(protocol.received_packets,
                    [b'\x01\x00\x00\x00\x02\x00\x00\x00',
                        b'\x03\x00\x00\x00\x04\x00\x00\x00'])

if __name__ == '__main__':
    unittest.main()
