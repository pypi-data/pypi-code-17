# -*- coding: utf-8 -*-

from cffi import FFI
import os.path

LIBRECRYPTO_PATH = "cppsrc"
RECRYPTO_H = os.path.join(LIBRECRYPTO_PATH, "recrypto.h")


def readlines(path):
    with open(path) as f:
        return f.readlines()


ffibuilder = FFI()
ffibuilder.set_source("recrypto._recrypto", '#include "recrypto.h"',
                      libraries=["recrypto", "stdc++"],
                      library_dirs=[LIBRECRYPTO_PATH],
                      include_dirs=[LIBRECRYPTO_PATH])

# skip CPP directives and extern "C"
defs = "\n".join(l for l in readlines(RECRYPTO_H)
                 if not (l.startswith("#")
                         or l.startswith("extern")
                         or l.startswith("}")))
ffibuilder.cdef(defs)
ffibuilder.cdef("""
    void free(void *);
    int strlen(const char *);
""")

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
