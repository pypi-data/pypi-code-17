from time import strftime
from datetime import datetime


def dump(data):
    """
    Dump the memory data, e.g.:
    
    00 cc 30 31 30 30 72 30 05 80 20 c0 92 00 31 36         ..0100r0.. ...16
    38 39 39 30 30 31 31 32 33 34 35 36 37 38 39 30         8990011234567890
    30 30 30 30 30 30 30 30 30 30 30 30 30 32 30 30         0000000000000200
    30 30 31 34 39 34 35 30 34 34 39 34 38 30 30 32         0014945044948002
    33 31 31 37 30 35 31 31 31 32 30 38 31 34 39 30         3117051112081490
    30 31 30 30 30 30 33 32 38 39 39 30 30 31 31 32         0100003289900112
    33 34 35 36 37 38 39 30 44 31 38 30 39 32 30 31         34567890D1809201
    31 38 37 32 33 30 30 30 31 30 30 30 31 33 33 37         1872300010001337
    39 39 39 39 39 39 39 39 39 39 39 39 30 30 31 36         9999999999990016
    34 33 2b 68 7a ef c3 4b 1a 89 30 34 39 82 02 00         43+hz..K..049...
    00 9a 03 17 05 11 95 05 00 00 04 08 80 9f 10 02         ................
    00 00 9f 26 08 ed 2c d0 d2 98 94 fb aa 9f 36 02         ...&..,.......6.
    00 01 9f 37 04 8f a4 f2 bd 9f 1a 02 06 43               ...7.........C
    """

    i = 1

    if( isinstance(data, bytes) == False ):
        raise TypeError("Expected bytes for data")

    dump = '\t'
    dump_ascii = ''
    padding = '        '
    
    for c in data:
        try: # python 3
            dump += '{:02x} '.format(c) 
                
        except: # python 2.x
            dump += '{:02x} '.format(ord(c))
            
        if chr(c) >= ' ' and chr(c) < '~':
            dump_ascii += chr(c)
        else:
            dump_ascii += '.'

        if(i % 16 == 0):
            dump = dump + padding + dump_ascii + '\n\t'
            dump_ascii = ''
        i+=1

    if dump_ascii:
        for i in range(16 - len(dump_ascii)):
            padding += '   '
        dump = dump + padding + dump_ascii + '\n\t'

    return dump


def trace(title, data):
    """
    Trace the binary data - add user-defined title, timstamp and dumped data, e.g.:

    12:08:16.762628 >> User-defined-title:
    00 cc 30 31 30 30 72 30 05 80 20 c0 92 00 31 36         ..0100r0.. ...16
    38 39 39 30 30 31 31 32 33 34 35 36 37 38 39 30         8990011234567890
    30 30 30 30 30 30 30 30 30 30 30 30 30 32 30 30         0000000000000200
    30 30 31 34 39 34 35 30 34 34 39 34 38 30 30 32         0014945044948002
    33 31 31 37 30 35 31 31 31 32 30 38 31 34 39 30         3117051112081490
    30 31 30 30 30 30 33 32 38 39 39 30 30 31 31 32         0100003289900112
    33 34 35 36 37 38 39 30 44 31 38 30 39 32 30 31         34567890D1809201
    31 38 37 32 33 30 30 30 31 30 30 30 31 33 33 37         1872300010001337
    39 39 39 39 39 39 39 39 39 39 39 39 30 30 31 36         9999999999990016
    34 33 2b 68 7a ef c3 4b 1a 89 30 34 39 82 02 00         43+hz..K..049...
    00 9a 03 17 05 11 95 05 00 00 04 08 80 9f 10 02         ................
    00 00 9f 26 08 ed 2c d0 d2 98 94 fb aa 9f 36 02         ...&..,.......6.
    00 01 9f 37 04 8f a4 f2 bd 9f 1a 02 06 43               ...7.........C


    """
    print('{} {}\n{}'.format(get_timestamp(), title, dump(data)))


def get_timestamp(t=None):
    """
    Get current timestamp
    """
    return datetime.now().strftime("%H:%M:%S.%f")
