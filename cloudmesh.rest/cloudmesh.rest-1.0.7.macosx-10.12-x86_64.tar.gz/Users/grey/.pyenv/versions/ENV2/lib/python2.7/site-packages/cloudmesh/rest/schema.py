from __future__ import print_function

from ruamel import yaml
import os
from os.path import splitext, exists
import glob
from cloudmesh.common.Shell import Shell
import json
from cloudmesh.common.util import writefile
from cloudmesh.common.Shell import Shell

class ConvertSpec(object):

    def __init__(self, infile, outfile, indent=2):


        if ".py" in outfile:

            print("... converting", infile, "->", outfile)

            r = Shell.execute("evegenie", [infile])
            print (r)

        elif ".yml" in infile and ".json" in outfile:
            element = yaml.safe_load(open(infile))
            print("... writing to", outfile)
            writefile(outfile, json.dumps(element, indent=indent))
        else:
            print("conversion not yet supported")


