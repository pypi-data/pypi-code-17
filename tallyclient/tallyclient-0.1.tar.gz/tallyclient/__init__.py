import socket


class TallyClient(object):
    """
    TallyClient is a tcp client responsible for send data packets to go-tally
    """

    # BUFFER_SI

    def __init__(self, host, port=8173):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (host, port)
        self.sock.connect(self.server_address)

    def count(self, label, value=1):
        assert isinstance(value, int)

        counter_message = "c:%s:%d\n" % (label, value)
        self.sock.send(counter_message)

    def gauge(self, label, value):
        assert isinstance(value, int)

        gauge_message = "g:%s:%d\n" % (label, value)
        self.sock.sendall(gauge_message)
