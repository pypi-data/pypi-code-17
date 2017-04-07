#!/usr/bin/env python3
"""
 @file
 operating system functions
"""
from __future__ import print_function
import subprocess
import os
from . import main


def is_tool(name):
    """
    Test if a Program is Installed

    Will raise an error if the programm is not found.
    Kwargs:
        name: The name of the program to be tested for.
    Returns:
        True if the Program is installed.
    """
    try:
        devnull = open(os.devnull)
        subprocess.Popen([name, "-h"], stdout=devnull,
                         stderr=devnull).communicate()
        devnull.close()
    except OSError:
        print("please install " + name)
        if name == "pandoc" and os.name != "posix":
            print("you may try\n" + 'install.packages("installr"); ' +
                  'library("installr"); install.pandoc()\n' + "in GNU R")
        raise
    return True


def pandoc(file_name, compile_latex=False, formats="tex"):
    """
    Run Pandoc on a File

        file_name: The file on which to run pandoc.
        formats: The pandoc output formats to be used.
        compile_latex: Compile the LaTeX file?
    Returns:
        0 if parsing was successful, 1 otherwise.
    """
    status = 1
    if is_tool("pandoc"):
        for form in formats.split(","):
            subprocess.call(["pandoc", "-sN", file_name, "-o",
                             main.modify_path(file_name=file_name,
                                              extension=form)])
            if compile_latex & (form == "tex"):
                tex_file_name = main.modify_path(file_name=file_name,
                                                 extension="tex")
                if os.name == "posix":
                    if is_tool("texi2pdf"):
                        subprocess.call(["texi2pdf", "--batch", "--clean",
                                         tex_file_name])
                else:
                    print("you are not running posix, see how to compile\n" +
                          tex_file_name +
                          "\nconsulting your operating system's " +
                          "documentation.")
    status = 0
    return status
