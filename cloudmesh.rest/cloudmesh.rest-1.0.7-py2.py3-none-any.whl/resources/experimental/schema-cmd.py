"""
The admin command for the REST services
"""
from __future__ import print_function

from pprint import pprint

from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command

from cloudmesh.rest.elements import Elements
from cloudmesh.rest.schema import YmlToSpec, SpecToTex
from cloudmesh.rest.schema import ConvertSpec
import glob

import os.path


class SchemaCommand(PluginCommand):
    """
    The admin command to manage the REST service
    """

    @command
    def do_schema(self, args, arguments):
        """
        ::

          Usage:
            schema yml2spec  FILENAME [OUTFILE]
            schema spec2tex DIRIN DIROUT
            schema create DIRIN DIROUT
            schema cat [json|yml] DIRECTORY FILENAME  
            schema convert INFILE [OUTFILE]
                
          Arguments:
              FILENAME   a filename
              DIRECTORY  the derectory where the schma 
                         objects are defined

          Options:
              -h     help

          Description:
             schema eve [json|yml] DIRECTORY FILENAME
                concatenates all files with ending yml 
                or json in the directory and combines 
                them. Using evegenie on the combined 
                file a eve settings file is generated 
                and written into FILENAME
                
             schema cat [json|yml] DIRECTORY FILENAME
                Concatinates all files with the given 
                ending (either json, or yml) into the
                file called FILENAME
            
             schema create DIRIN DIROUT
                takes simpl yml documentations and creates 
                the enhanced spec in th OUTDIR
             
             schema spec2tex DIRIN DIROUT
                takes all specs and creates the output for 
                the tex document for NIST
                
        """
        #pprint(arguments)
        kind = "yml"
        if arguments.json:
            kind = "json"
        if arguments.cat:
            directory = arguments.DIRECTORY
            filename = arguments.FILENAME
            elements = Elements(directory, filename, kind)

        elif arguments.yml2spec:
            filename = arguments.FILENAME
            outfile = arguments.OUTFILE or filename
            elements = YmlToSpec(filename, outfile)


        elif arguments.create:
            dirin = arguments.DIRIN
            dirout = arguments.DIROUT
            files = glob.glob(os.path.join(dirin, "*.yml"))

            for infile in files:
                print('Processing', infile)
                outfile = infile.replace(dirin, dirout)
                elements = YmlToSpec(infile, outfile)


        elif arguments.spec2tex:
            dirin = arguments.DIRIN
            dirout = arguments.DIROUT
            files = glob.glob(os.path.join(dirin, "*.yml"))

            for infile in files:
                print('Processing', infile)
                elements = SpecToTex(infile, dirout)

        elif arguments.convert:

            filename = arguments.INFILE
            outfile = arguments.OUTFILE
            if arguments.OUTFILE is None:

                if ".json" in filename:
                    outfile = filename.replace(".json", ".yml")
                elif ".yml" in filename:
                    outfile = filename.replace(".yml", ".json")

            ConvertSpec(filename, outfile)