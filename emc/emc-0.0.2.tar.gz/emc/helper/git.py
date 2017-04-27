'''
Git utilities
@author Csaba Sulyok
'''

import os
from subprocess import CalledProcessError, check_output
from sys import stderr



def verifyGitOnPath():
    try:
        check_output(['git', '--version'])
        return True
    except CalledProcessError:
        stderr.write('WARNING: Git not on path. Cannot check integrity. Behavior unpredictable.\n')
        return False
    


def gitRevision():
    if verifyGitOnPath():
        try:
            ret = check_output(['git', 'rev-parse', '--short', 'HEAD'])
            return ret.strip()
        except CalledProcessError:
            stderr.write('WARNING: Current folder is not in a git repo: %s\n' %(os.getcwd()))
            return None
    else:
        return None


def verifyGitRevision(targetRev):
    currentRev = gitRevision()
    if currentRev != None and targetRev != currentRev:
        stderr.write('WARNING: The used file was created with a different git revision (%s) than the current (%s). Behavior unpredictable.\n'
                      %(targetRev, currentRev))
        