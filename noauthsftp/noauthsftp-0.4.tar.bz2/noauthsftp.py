#!/usr/bin/env python3
"""NoAuthSFTP: Anon SFTP server for quick and dirty file transfer
"""

__author__ = "Da_Blitz <code@pocketnix.org>"
__version__ = "0.4"
__email__ = "code@pockentix.org"
__license__ = "ISC"
__url__ = "http://blitz.works/noauthsftp"

from argparse import ArgumentParser, ArgumentTypeError, OPTIONAL

import asyncssh
import asyncio
import logging
import sys
import os


EXIT_OK = 0
EXIT_BAD = 1


formatter = logging.Formatter("%(name)-15s %(levelname)-8s %(asctime)10s %(process)s: %(message)s")
log = logging.getLogger('noauthsftp')


class NoAuthSSHServer(asyncssh.SSHServer):
    def connection_made(self, conn):
        self._conn = conn
        peer = conn.get_extra_info('peername')[:2]
        self._peer_addr = peer

        log.info("New connection from: %s:%d", *format_ipv6(peer))
        
    def connection_lost(self, exc):
        peer = self._peer_addr

        if exc:
            log.exception('Error during connection (%s:%d)', *peer, exc_info=exc)
            
        log.info("Remote host closed connection: %s:%d", *format_ipv6(peer))
    
    ################
    # Auth Methods #
    ################
    def begin_auth(self, username):
        log.info("User is attempting to connect as user %s", username)
        return False # user does not require auth to connect

    def public_key_auth_supported(self):
        return False
    
    def password_auth_supported(self):
        return False
    
    def kbdint_auth_supported(self):
        return False
        
    ##############
    # Subsystems #
    ##############
    # sftp is a subssytem inside a session, dont override this
    # and we can reuse the default implementation
#    def session_requested(self):
#        return False
    
    def connection_requested(self, *args):
        return False
    
    def unix_connection_requested(self, *args):
        return False
        
    def server_requested(self, *args):
        return False

    def unix_server_requested(self, *args):
        return False


def handle_session(stdin, stdout, stderr):
    stdout.write('This is an anonymous SSH server, all actions are logged')
    stdout.channel.exit(0)


def format_ipv6(addr):
    """Corectly format ipv6 addresses
    
    IPv6 with port numbers should hav square brakcets around them to make the port number stand out
    """
    ADDR = 0
    PORT = 1

    addr, port = addr

    if ":" in addr:
        return ("[{}]".format(addr), port)
    else:
        return (addr, port)


def is_dir(path):
    if not os.path.isdir(path):
        raise ArgumentTypeError("Provided path is not a directory: {}".format(path))
    
    return path


def has_access_to_file(path):
    if not os.path.isfile(path):
        raise ArgumentTypeError("Provided path is not a file: {}".format(path))

    if not os.access(path, os.R_OK):
        raise ArgumentTypeError("Cant read provided file: {}".format(path))
    
    return path
    

def main(argv=sys.argv[1:]):
    args = ArgumentParser()

    args.add_argument('-v', '--verbosity', action='count',
        help="Increase the verbosity of the logging output")
    args.add_argument('-k', '--key', action="append", default=[], type=has_access_to_file,
        help="SSH Server key to present to clients to identify itself")
    args.add_argument('-p', '--port', default=8022,
        help="The port to listen on (Default: %(default)d)")
    args.add_argument('address', default="localhost", nargs=OPTIONAL,
        help="The IP address to listen on (Default: localhost)")
    args.add_argument('path', default=".", type=is_dir,
        help="The directory to serve files from")

    options = args.parse_args(argv)
    
    level = {
             1: logging.CRITICAL,
             2: logging.ERROR,
             3: logging.WARNING,
             4: logging.INFO,
             5: logging.DEBUG,
            }.get(options.verbosity, logging.DEBUG)
    
    debug = True if level <= logging.DEBUG else False
    
    if options.verbosity:
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(formatter)
        log.addHandler(handler)
        log.setLevel(level)
    log.info("Logging initialized")
    

    class ChrootSFTPServer(asyncssh.SFTPServer):
        def __init__(self, conn):
            super().__init__(conn, chroot=options.path)

    # rmdir mkdir symlink link remove rename posix_rename
    # open close read write
    
    async def start_server():
        await asyncssh.create_server(NoAuthSSHServer, options.address, options.port,
                                     server_host_keys=options.key,
                                     session_factory=handle_session,
                                     sftp_factory=ChrootSFTPServer)

    for key in options.key:
        log.info("Using server key: %s", key)
    log.info("Restricting sftp connections to %s directory", options.path)
    log.info("Starting up server on %s:%d", *format_ipv6((options.address, options.port),))

    loop = asyncio.get_event_loop()
    
    try:
        loop.run_until_complete(start_server())
    except (OSError, asyncssh.Error):
        log.exception("Error starting server")
        sys.exit(EXIT_BAD)
    except ValueError as err:
        log.error("Multiple keys of the same type specified: %s", err)
        sys.exit(EXIT_BAD)



    try:
        loop.run_forever()
    except KeyboardInterrupt:
        log.info("User requested exit")
    
    
if __name__ == "__main__":
    main()
