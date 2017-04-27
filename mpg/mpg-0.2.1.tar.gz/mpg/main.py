# Copyright  2016  Kevin Murray <spam@kdmurray.id.au>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import absolute_import, division, print_function
from . import MarkovGenerator
from .util import seq2fa
from pymer import TransitionKmerCounter

from docopt import docopt
from sys import stdout, stderr


def mpg_main():
    cli = '''
    USAGE:
        mpg [options] <reference> ...

    OPTIONS:
        -l LENGTH       Length of sequence to simulate [default: 0].
        -k ORDER        Markovian Order [default: 1].
        -s SEED         Random seed for generation. (uses /dev/urandom if unset)
        -d DUMPFILE     Dump transition count data to DUMPFILE.
        -r              Reference file is a pre-computed transition count dump
                        file (see -d).

    '''
    opts = docopt(cli)
    k = int(opts['-k'])
    l = int(opts['-l'])

    # + 1 as k is markovian order, TC takes kmer len
    t = TransitionKmerCounter(k + 1)
    if opts['-r']:
        filename = opts['<reference>'][0]
        print('Loading reference dump from "{}"'.format(filename),
              file=stderr)
        t.load(filename)
    else:
        print('Inferring transition matrix from reference sequences',
              file=stderr)
        for fn in opts['<reference>']:
            t.consume_file(fn)
            print('Consumed', fn, file=stderr)

    if opts['-d']:
        filename = opts['-d']
        print('Saving reference dump to "{}"'.format(filename), file=stderr)
        t.save(filename)

    m = MarkovGenerator(t, seed=opts['-s'])
    print('Initialised Markov Generator', file=stderr)
    if l > 0:
        print("Generating sequence of", l, "bases", file=stderr)
        print(seq2fa('genseq', m.generate_sequence(l)))
