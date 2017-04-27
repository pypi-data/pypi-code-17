import serial
import serial.threaded


class StructuredPacket(serial.threaded.Protocol):
    """
    Read binary packets. Packets are expected to be fixed length have a header
    to mark its beginning.
    """

    HEADER = b'\x01\x02\x03\x04\x05'

    def __init__(self, data_size):
        """Initialize with packet size excluding header"""
        try:
            self.data_size = int(data_size)
        except ValueError as exc:
            raise ValueError("Exepected arg 'size' to be int: " + str(exc))
        self.packet = bytearray()
        self.in_data = False
        self.header_pos = 0
        self.transport = None

    def connection_made(self, transport):
        """Store transport"""
        self.transport = transport

    def conneciton_lost(self, exc):
        """Forget transport"""
        self.transport = None
        del self.packet[:]
        super(StructuredPacket, self).connection_lost(exc)

    def data_received(self, data):
        """Find data after HEADER, call handle_packet"""
        for byte in serial.iterbytes(data):
            if self.in_data and (len(self.packet) < self.data_size):
                self.packet.extend(byte)
                if len(self.packet) == self.data_size:
                    self.in_data = False
                    # make read-only copy
                    self.handle_packet(bytes(self.packet))
                    del self.packet[:]
            # Since there is no 'byte' object, indexing a bytes or bytearray
            # object yields an int. Instead, we need to compare a bytes object
            # of size 1 with a bytes object of size 1
            elif byte == self.HEADER[self.header_pos:self.header_pos+1]:
                self.header_pos += 1
                if self.header_pos == len(self.HEADER):
                    self.header_pos = 0
                    self.in_data = True
            else:
                self.header_pos = 0

    def handle_packet(self, packet):
        """Process packets - to be overridden by subclassing"""
        raise serial.threaded.NotImplementedError(
                'please implement functionality in handle_packet')
