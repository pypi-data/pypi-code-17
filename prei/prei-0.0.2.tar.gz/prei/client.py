import os
import sys
import gevent
import paramiko

# 1 kb
RECV_BYTES = 1048576
SEND_BYTES = 1048576
# sleep for 100 ms if not ready for write
WRITE_SLEEP = 0.1


class Command:

    def __repr__(self):
        return 'Command({!r}, closed={!r})'.format(
            self.command, self.closed,
        )

    def __init__(self, channel, command, input=None):
        self._channel = channel
        self._input = input
        self._gevent = None
        self.command = command
        self.closed = False
        self.stdout, self.stderr, self.status = None, None, None

    def start(self):
        self._gevent = gevent.spawn(self.run)
        self._gevent.start()

    def join(self):
        if self._gevent is None:
            raise ValueError('greenlet never started for command {!r}'.format(
                self.command))
        self._gevent.join()

    def run(self):
        self._channel.exec_command(self.command)
        if self._input is not None:
            self._send_loop()
        self.stdout, self.stderr = self._recv_loop()
        self.status = self._channel.recv_exit_status()
        self.closed = True

    def _recv_loop(self):
        stdout = b''
        stderr = b''
        while True:
            if self._channel.closed:
                break
            elif self._channel.recv_ready():
                new_bytes = self._channel.recv(RECV_BYTES)
                while new_bytes:
                    stdout += new_bytes
                    new_bytes = self._channel.recv(RECV_BYTES)
            elif self._channel.recv_stderr_ready():
                new_bytes = self._channel.recv(RECV_BYTES)
                while new_bytes:
                    stdout += new_bytes
                    new_bytes = self._channel.recv(RECV_BYTES)
        return stdout, stderr

    def _send_loop(self):
        _input = self._input
        if isinstance(_input, str):
            _input = _input.encode('utf8')
        lines = _input.splitlines(True)
        for line in lines:
            while not self._channel.send_ready():
                gevent.sleep(WRITE_SLEEP)
            self._channel.send(line)

    @property
    def out(self):
        if self.stdout is None:
            return None
        return self.stdout.decode('utf8')

    @property
    def err(self):
        if self.stderr is None:
            return None
        return self.stderr.decode('utf8')


def _default_checker(val):
    return bool(val)


class Client:

    def __repr__(self):
        return 'Client({!r})'.format(self.hostname)

    def __init__(self):
        self.hostname = None
        self.config = None
        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._client.load_system_host_keys()
        self.load_config()
        self.connected = False

    def load_config(self):
        self.config = paramiko.SSHConfig()
        path = os.path.expanduser('~/.ssh/config')
        with open(path) as f:
            self.config.parse(f)

    def connect(self, hostname, keyfile=None, username=None, **kwargs):
        self.hostname = hostname
        conf = self.config.lookup(hostname)
        hostname = conf['hostname']
        if username:
            kwargs['username'] = username
        elif conf.get('user'):
            kwargs['username'] = conf['user']
        if keyfile:
            kwargs['key_filename'] = keyfile
        elif 'identityfile' in conf and conf['identityfile']:
            kwargs['key_filename'] = conf['identityfile']
        self._client.connect(hostname, **kwargs)
        self.connected = True

    def _new_channel(self):
        return self._client.get_transport().open_session()

    def spawn(self, command, input=None):
        '''
        Returns a Command with a triggered greenlet
        '''
        if not self.connected:
            raise ValueError('need to connect to a host first')
        chan = self._new_channel()
        cmd = Command(chan, command, input=input)
        cmd.start()
        return cmd

    def disconnect(self):
        if not self.connected:
            raise ValueError('not connected')
        self._client.close()

    def call(self, command, input=None):
        '''
        Execute a command, and return the Command object
        '''
        cmd = self.spawn(command, input=input)
        cmd.join()
        return cmd

    def status(self, command, input=None):
        cmd = self.call(command, input=input)
        return cmd.status

    def run(self, command, input=None):
        '''
        Execute a command and return the stdout
        '''
        cmd = self.call(command, input=input)
        print(cmd.out)
        print(cmd.err, file=sys.stderr)
        return cmd.out
