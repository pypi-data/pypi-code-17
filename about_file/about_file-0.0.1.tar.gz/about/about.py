#!/usr/bin/env python3

import sys
import os
from homer import Config

def main():
    db = Config(app="about")

    if len(sys.argv) == 3:
        filename = sys.argv[1]
        comment  = sys.argv[2]
        if os.path.exists(filename) and comment != "":
            filename = os.path.abspath(filename)
            db[filename] = comment
        elif os.path.exists(filename) and comment == "":
            filename = os.path.abspath(filename)
            del db[filename]
        else:
            print("ERROR: File {} not exists!")
            sys.exit(1)
    else:
        dirname = os.getenv("PWD")
        dir_info = db.get(dirname, "Information about the {} directory".format(dirname))
        print("")
        print("# {}".format(dir_info))
        for i in db.search("{}/".format(dirname)):
            file = i[0]
            content = db[file]
            file = file.replace(dirname + "/", "")
            print(" * {} : {}".format(file, content))
        print("")
        print("--")
        print("Autogen by about - https://github.com/manoelhc/about")
