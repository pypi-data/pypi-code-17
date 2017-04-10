#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(__file__, '..', '..')))
import horetu
import horetu.types as T
import bguo.parse as p
from email.message import Message
from email.policy import SMTPUTF8

def merge(voipms_file: T.InputFile, mh_file: T.InputFile,
          dout: T.OutputDirectory='.', *, dry=False):
    '''
    Create a new directory with data merged from VOIP.ms and MH.

    :param voipms_file: CSV export from voip.ms
    :param mh_file: MH ~/.aliases file
    :param dout: Output directory, or the current directory by default
    :param bool dry: Write no files, but print what files would have been written.
    '''
    data = dict(p.mh(mh_file))
    voipms_data = dict(p.voipms(voipms_file))

    for identifier in data:
        if identifier in voipms_data:
            data[identifier].update(voipms_data[identifier])
        m = Message(SMTPUTF8)
        for header, value in data[identifier].items():
            m[header] = value

        filename = os.path.join(dout, identifier)
        if dry:
            action = 'Overwrite' if os.path.exists(filename) else 'Create'
            sys.stdout.write('%s %s:\n%s\n' % (action, filename, text))
        else:
            with open(filename, 'w') as fp:
                fp.write(str(m).strip() + '\n')

horetu.cli(merge)
