import logging
import socket
import threading
import time

import ldap.mock

__log__ = logging.getLogger(__name__)


class Thread(threading.Thread):

    def __init__(self, conn, addr, server):
        self.conn = conn
        self.addr = addr
        self._client = None
        self._server = server
        threading.Thread.__init__(self)

    def run(self):
        __log__.info("Connected, thread started.")
        while True:
            try:
                messages = ldap.mock.receive(self.conn)
                if not messages:
                    __log__.info("Nothing more was received.")
                    break

                for msg in messages:
                    __log__.debug("IN: %s", msg.prettyPrint())

                for response in ldap.mock.respond(messages=messages):
                    __log__.debug("OUT: %s", response.prettyPrint())

                    self.conn.sendall(ldap.mock.encode(response))

            except Exception as e:
                # import time
                # time.sleep(0.5)
                # raise
                __log__.error("Connection aborted: %r", e)
                break
        __log__.info("Thread closed.")


class Server(threading.Thread):

    def __init__(self, host, port, daemon=False):
        self._host = host
        self._threads = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        threading.Thread.__init__(self)
        if daemon:
            self.daemon = daemon

    def run(self):
        self.sock.listen(5)
        while True:
            try:
                conn, (ip, port) = self.sock.accept()
            except ConnectionAbortedError:
                __log__.debug('Connection aborted')
                break
            except Exception as e:
                __log__.error('Server error: %s', e)
                break
            else:
                th = Thread(conn, (ip, port), server=self)
                self._threads.append(th)
                th.daemon = True
                th.start()

    def stop(self):
        for th in self._threads:
            __log__.info("Closing %s", th.addr)
            try:
                th.conn.shutdown(socket.SHUT_RDWR)
                th.conn.close()
            except Exception as e:
                __log__.error("Could not close connection: %s", e)
        self.sock.close()


def serve(host='localhost', port=3389):
    server = Server(host=host, port=port, daemon=True)

    try:
        __log__.info("Server start.")
        server.start()
        input("Enter to quit...\n")

    except KeyboardInterrupt:
        __log__.info("Received KeyboardInterrupt")

    except SystemExit:
        __log__.info("Caught SystemExit, closing down")

    finally:
        server.stop()
        __log__.info("Server stop.")
        time.sleep(1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    serve()
