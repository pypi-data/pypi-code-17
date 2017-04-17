# -*- coding: utf-8 -*-

'''
python protobuf beauty tools
'''

import argparse
import os

def InitCmdline():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', default='', type=str, required=True, help='protobuf file path')
    parser.add_argument('-i', '--in-place', action='store_true', default=False, help='make changes to files in place')
    parser.add_argument('-r', '--recursive', action='store_true', default=False, help='run recursively over directories')
    return parser.parse_args()


def MakeBeauty(filename, inplace):
    import decoder
    package_descriptor = decoder.Decode(filename)

    import format_encoder
    encode_string = format_encoder.FormatEncoder(package_descriptor).encode()
    if inplace:
        open(filename, 'w').write(encode_string)
    else:
        print encode_string

def Main():
    arg = InitCmdline()
    filepath = arg.file
    if not os.path.isfile(filepath) and not os.path.isdir(filepath):
        print 'Input filenames did not match any proto files'
        return
    if os.path.isfile(filepath):
        MakeBeauty(filepath, arg.in_place)
        return
    if not arg.recursive:
        print "directory specified without '--recursive' flag:", arg.file
        return
    for root, dirs, files in os.walk(arg.file):
        for filename in files:
            if filename.endswith('.proto') and not filename.startswith('.'):
                MakeBeauty(os.path.join(root, filename), arg.in_place)
    return


if __name__ == '__main__':
    Main()
