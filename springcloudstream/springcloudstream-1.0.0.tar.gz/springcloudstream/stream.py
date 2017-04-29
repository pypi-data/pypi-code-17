"""
Copyright 2017 the original author or authors.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
__author__ = 'David Turanski'
import sys
'''
Python 2 or 3 agnostic input function
'''
import sys

PY3K = sys.version_info >= (3, 0)

if PY3K:
    binary_input = sys.stdin.buffer
    receive_input = input
else:
    # Python 2 on Windows opens sys.stdin in text mode, and
    # binary data that read from it becomes corrupted on \r\n
    #if sys.platform == "win32":
    #    # set sys.stdin to binary mode
    #    import os, msvcrt
    #    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    binary_input = sys.stdin
    receive_input = raw_input

class Encoders:
    CRLF, LF, BINARY = range(3)

'''
Wraps a function and handles streaming I/O for request/reply communications to use the function as
a Spring XD processor.
NOTE: This implementation only works with LF, or CRLF encoding since reading single chars from stdin is not
standard nor portable.
'''
class Processor:

    def __init__(self, encoder = Encoders.CRLF):
        self.encoder = encoder

    '''
    Write data to stdout
    '''
    def send(self, data):
        sys.stdout.write(self.encode(data))
        sys.stdout.flush()

    '''
    encode data
    '''
    def encode(self,data):
        if self.encoder == Encoders.CRLF:
            data = data + '\r\n'
        elif self.encoder == Encoders.LF:
            data = data + '\n'
        elif self.encoder == Encoders.BINARY:
            data = data + '\x1a'
        return data
    '''
    decode data
    '''
    def decode(self,data):
        if self.encoder == Encoders.CRLF:
            data = data.rstrip('\n')
            data = data.rstrip('\r')
        elif self.encoder == Encoders.LF:
            data = data.rstrip('\n')
        elif self.encoder == Encoders.BINARY:
            data = data.rstrip('\x1a')
        return data

    def read_input(self):
        if self.encoder == Encoders.BINARY:
            input = self.binary_input()
        else:
            input = receive_input()

        if input:
            return self.decode(input)

    '''
    Run the I/O loop with a user-defined function
    '''
    def start(self, func):
        while True:
            try:
               data = self.read_input()
               if data:
                    self.send(func(data))
            except EOFError:
                break
            except KeyboardInterrupt:
                break

    def binary_input(self):
        buf=[]
        while True:
            buf.append(binary_input.read(1))
            if buf[-1] == '\x1a':
                break

        return ''.join(buf)


class Sink(Processor):
    '''
    Run the I/O loop with a user-defined function
    '''
    def start(self, func):
        pass
        while True:
            try:
                data = self.read_input()
                if data:
                    func(data)
            except EOFError:
                break
            except EOFError:
                break
            except KeyboardInterrupt:
                break
